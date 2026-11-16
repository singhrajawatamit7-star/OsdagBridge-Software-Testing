"""
Test Module: test_repository_layout.py
Validates the QA project deliverable structure, test case matrices,
bug tracking records, and CI workflow configurations.
"""

import csv
from pathlib import Path


def test_test_cases_csv_exists_and_populated(project_root):
    """Verify test_cases.csv contains at least 15 comprehensive scenarios with required columns."""
    csv_file = project_root / "test_cases.csv"
    assert csv_file.exists(), "test_cases.csv missing in project root."

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) >= 15, f"Expected at least 15 test cases, found {len(rows)}"

    expected_cols = {
        "Test_ID", "Module", "Title", "Description", "Preconditions",
        "Test_Steps", "Test_Data", "Expected_Result", "Actual_Result",
        "Status", "Severity", "Execution_Type", "Automated_Script"
    }
    assert expected_cols.issubset(set(reader.fieldnames))

    # Verify OB-001 through OB-015 are present
    test_ids = {r["Test_ID"] for r in rows}
    for i in range(1, 16):
        expected_id = f"OB-{i:03d}"
        assert expected_id in test_ids, f"Required test case {expected_id} missing in test_cases.csv"


def test_test_results_csv_exists_and_complete(project_root):
    """Verify test_results.csv contains execution logs for all test cases."""
    csv_file = project_root / "test_results.csv"
    assert csv_file.exists(), "test_results.csv missing in project root."

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) >= 15, f"Expected at least 15 execution entries, found {len(rows)}"
    for row in rows:
        assert row["Status"] in ["PASS", "FAIL", "BLOCKED"]
        assert float(row["Execution_Time_sec"]) >= 0.0


def test_issues_csv_format_and_data(project_root):
    """Verify issues.csv contains documented defects with reproduction steps."""
    csv_file = project_root / "issues.csv"
    assert csv_file.exists(), "issues.csv missing in project root."

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) >= 3, "Expected at least 3 documented issues."
    for r in rows:
        assert r["Bug_ID"].startswith("OB-BUG-")
        assert r["Severity"] in ["Critical", "High", "Medium", "Low"]
        assert r["Priority"] in ["P1", "P2", "P3", "P4"]
        assert len(r["Steps_to_Reproduce"]) > 10


def test_documentation_files_exist(project_root):
    """Verify documentation directory deliverables."""
    doc_dir = project_root / "documentation"
    assert (doc_dir / "test_plan.md").exists()
    assert (doc_dir / "bug_report_template.md").exists()
    assert (doc_dir / "internship_summary_report.md").exists()
    assert (doc_dir / "test_cases.csv").exists()


def test_github_actions_workflow_exists(project_root):
    """Verify GitHub Actions CI workflow file."""
    wf_file = project_root / ".github" / "workflows" / "qa.yml"
    assert wf_file.exists(), "GitHub Actions workflow .github/workflows/qa.yml missing."
    assert wf_file.stat().st_size > 50
