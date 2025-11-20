# tests/test_cli.py
from typer.testing import CliRunner
from devops_guardian.cli import app

runner = CliRunner()

def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "DevOps Guardian" in result.stdout
