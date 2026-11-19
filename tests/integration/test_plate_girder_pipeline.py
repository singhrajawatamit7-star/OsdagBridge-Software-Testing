"""
Integration Tests: Official OsdagBridge Plate Girder Pipeline
Verifies the official plate girder pipeline and documents upstream integration blockers.
"""

import pytest


@pytest.mark.integration
def test_official_core_import_blocked_by_missing_models(official_source, monkeypatch):
    """
    INT-PG-01: Verifies that importing official 'osdagbridge.core' fails due to missing upstream models.py.
    Upstream Defect: src/osdagbridge/core/__init__.py contains 'from .models import *',
    but models.py does not exist in the official repository checkout.
    """
    monkeypatch.syspath_prepend(str(official_source))
    with pytest.raises(ModuleNotFoundError) as exc_info:
        import osdagbridge.core  # noqa: F401
    assert "osdagbridge.core.models" in str(exc_info.value)


@pytest.mark.integration
def test_official_plate_girder_pipeline_blocked_by_missing_models(official_source, monkeypatch):
    """
    INT-PG-02: Verifies that importing plate_girder modules fails due to parent package import failure.
    Until upstream resolves models.py, downstream plate_girder functions cannot be imported directly.
    """
    monkeypatch.syspath_prepend(str(official_source))
    with pytest.raises(ModuleNotFoundError) as exc_info:
        from osdagbridge.core.bridge_types.plate_girder import dto  # noqa: F401
    assert "osdagbridge.core.models" in str(exc_info.value)


@pytest.mark.integration
def test_official_plate_girder_files_exist_on_disk(official_source):
    """
    INT-PG-03: Verifies that the plate_girder files exist physically in the official source tree.
    """
    pg_dir = official_source / "osdagbridge" / "core" / "bridge_types" / "plate_girder"
    assert (pg_dir / "dto.py").is_file()
    assert (pg_dir / "initial_sizing.py").is_file()
    assert (pg_dir / "designer.py").is_file()
    assert (pg_dir / "analyser.py").is_file()
    assert (pg_dir / "report_generator.py").is_file()
    assert (pg_dir / "cad_generator.py").is_file()
