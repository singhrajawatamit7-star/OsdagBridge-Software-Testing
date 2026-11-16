"""
Test Module: test_environment.py
Validates system requirements, Python version, project root structure,
required files, and logging infrastructure.
"""

import sys
from pathlib import Path


def test_python_version():
    """Verify that Python version meets or exceeds requirement (>= 3.11)."""
    assert sys.version_info >= (3, 11), f"Python 3.11+ is required. Found: {sys.version}"


def test_project_root_files_exist(project_root):
    """Verify essential project root files exist for deployment."""
    required_files = [
        "requirements.txt",
        "app.py",
        "README.md",
        "test_cases.csv",
        "test_results.csv",
        "issues.csv",
        "pytest.ini"
    ]
    for filename in required_files:
        filepath = project_root / filename
        assert filepath.exists(), f"Missing required file: {filename}"
        assert filepath.stat().st_size > 0, f"File {filename} is unexpectedly empty."


def test_test_data_files_exist(project_root):
    """Verify test data fixtures are in place."""
    data_dir = project_root / "test_data"
    assert data_dir.is_dir(), "test_data directory is missing."
    assert (data_dir / "valid_inputs.json").exists()
    assert (data_dir / "invalid_inputs.json").exists()
    assert (data_dir / "valid_inputs.csv").exists()
    assert (data_dir / "invalid_inputs.csv").exists()
    assert (data_dir / "reference_design_irc.json").exists()


def test_reports_directories_and_evidence_exist(project_root):
    """Verify reports, screenshots, and logs directories exist."""
    reports_dir = project_root / "reports"
    assert reports_dir.is_dir(), "reports directory is missing."
    assert (reports_dir / "logs").is_dir(), "reports/logs directory is missing."
    assert (reports_dir / "screenshots").is_dir(), "reports/screenshots directory is missing."
    assert (reports_dir / "logs" / "osdagbridge_qa.log").exists(), "QA execution log file missing."


def test_core_package_layout(project_root):
    """Verify osdagbridge_core modules are present."""
    core_dir = project_root / "osdagbridge_core"
    assert (core_dir / "__init__.py").exists()
    assert (core_dir / "models.py").exists()
    assert (core_dir / "validator.py").exists()
    assert (core_dir / "solver.py").exists()
    assert (core_dir / "report_generator.py").exists()
