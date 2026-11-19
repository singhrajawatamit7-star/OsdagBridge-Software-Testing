"""Smoke tests for the official OsdagBridge installation."""
import importlib.util
from io import StringIO
from pathlib import Path
import sys
import pytest


@pytest.mark.smoke
@pytest.mark.integration
def test_official_repository_exists(official_root):
    assert official_root.is_dir()


@pytest.mark.smoke
@pytest.mark.integration
def test_official_source_directory_exists(official_source):
    assert (official_source / "osdagbridge").is_dir()


@pytest.mark.smoke
@pytest.mark.integration
def test_package_resolves_from_official_source(
    official_source,
    monkeypatch,
):
    monkeypatch.syspath_prepend(str(official_source))
    spec = importlib.util.find_spec("osdagbridge")
    assert spec is not None
    assert spec.submodule_search_locations is not None
    package_dir = (
        Path(next(iter(spec.submodule_search_locations))).resolve()
    )
    expected_dir = (official_source / "osdagbridge").resolve()
    assert package_dir == expected_dir


@pytest.mark.smoke
@pytest.mark.integration
def test_official_core_package_exists(official_source, monkeypatch):
    monkeypatch.syspath_prepend(str(official_source))
    core_dir = official_source / "osdagbridge" / "core"
    assert core_dir.is_dir()
    assert (core_dir / "__init__.py").is_file()


@pytest.mark.smoke
@pytest.mark.integration
def test_official_desktop_main_start(official_source, monkeypatch):
    """Verifies official desktop entry point executes its console stub."""
    monkeypatch.syspath_prepend(str(official_source))
    from osdagbridge.desktop.main import start

    old_stdout = sys.stdout
    sys.stdout = buffer = StringIO()
    try:
        start()
    finally:
        sys.stdout = old_stdout

    output = buffer.getvalue()
    assert "Starting desktop UI" in output


@pytest.mark.smoke
@pytest.mark.integration
def test_official_cli_entry_points(official_source, monkeypatch):
    """Verifies official CLI commands module is discoverable and imports."""
    monkeypatch.syspath_prepend(str(official_source))
    import osdagbridge.cli.commands as cli_commands
    assert cli_commands is not None
