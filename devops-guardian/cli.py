import typer
from rich.console import Console

console= Console()
app = typer.Typer(help="DevOps Guardian CLI - DevOps Helper CLI")

@app.command()
def version():
    from . import __version__
    console.print(f"[bold green]DevOps Guardian[/] version: {__version__}")
    
@app.command()
def init(project_name: str = typer.Option("devops-guardian",help="Project name to initialize"),
         force: bool = typer.Option(False,"--force","-f", help="Overwrite existing config")):
    """Initialize a local project configuration."""
    import  os,json
    cfg={"project_name": project_name}
    cfg_path = ".dg_config.json"
    if os.path.exists(cfg_path) and not force:
        console.print(f"[yellow]Configuration {cfg_path} already exists. Use --force to overwrite.[/]")
        raise typer.Exit(code=1)
    with open(cfg_path,"w") as f:
        json.dump(cfg, f, indent=2)
    console.print(f"[green]Created Configuration file {cfg_path}[/]")

@app.command()
def k8s_create_deployment(name: str = typer.Argument(..., help="Deployment name"),
                        image: str = typer.Option("nginx:latest", help="Container image"),
                        replicas: int =typer.Option(1, help="Number of replicas")):
    """Create a simple Kubernetes Deployment manifest and print it."""
    import yaml

    manifest = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": name},
        "spec": {
            "replicas": replicas,
            "selector": {"matchLabels": {"app": name}},
            "template": {
                "metadata": {"labels": {"app": name}},
                "spec": {"containers": [{"name": name, "image": image}]},
            },
        },
    }
    import yaml, sys
    yaml.safe_dump(manifest, sys.stdout, sort_keys=False)
    console.print(f"[blue]Generated Kubernetes deployment manifest for {name}[/]")
    
@app.command()
def generate_ci(provider: str = typer.Option("github", "--provider", "-p", help="ci provider (github/jenkins)")):
    """Generate a basic CI template (preview)."""
    if provider.lower() == "github":
        console.print("name: CI\non: [push]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - name: Set up Python\n        uses: actions/setup-python@v4\n        with:\n          python-version: '3.10'\n")
    else:
        console.print("# Jenkinsfile (placeholder)\npipeline {\n  agent any\n  stages {\n    stage('Build') { steps { echo 'build' } }\n  }\n}\n")
    console.print(f"[green]Previewed CI config for {provider}[/]")

if __name__ == "__main__":
    app()