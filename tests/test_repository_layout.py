"""
Test Module: test_repository_layout.py
Validates the QA project deliverables, test case repository, defect records,
and documentation integrity.
"""

import csv
from pathlib import Path


def test_test_cases_csv_exists_and_populated(project_root):
    """Verify test_cases.csv contains 50 comprehensive scenarios across 8 categories."""
    csv_file = project_root / "test_cases.csv"
    assert csv_file.exists(), "test_cases.csv missing in project root."

    with open(csv_file, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) >= 50, f"Expected 50 test cases, found {len(rows)}"

    expected_cols = {
        "Test_ID", "Category", "Title", "Description", "Preconditions",
        "Test_Steps", "Expected_Result", "Actual_Result",
        "Status", "Severity", "Execution_Type"
    }
    assert expected_cols.issubset(set(reader.fieldnames))


def test_test_results_csv_exists_and_complete(project_root):
    """Verify test_results.csv contains 50 test execution records with valid statuses."""
    csv_file = project_root / "test_results.csv"
    assert csv_file.exists(), "test_results.csv missing in project root."

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) >= 50, f"Expected 50 execution entries, found {len(rows)}"
    valid_statuses = {"PASS", "FAIL", "SKIPPED", "BLOCKED", "ERROR"}
    for row in rows:
        assert row["Status"] in valid_statuses, f"Invalid status: {row['Status']}"


def test_issues_csv_format_and_data(project_root):
    """Verify issues.csv contains documented defects with reproduction steps and evidence."""
    csv_file = project_root / "issues.csv"
    assert csv_file.exists(), "issues.csv missing in project root."

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) >= 5, f"Expected at least 5 documented issues, found {len(rows)}"
    for r in rows:
        assert r["Bug_ID"].startswith("OB-BUG-")
        assert r["Severity"] in ["Critical", "High", "Medium", "Low"]
        assert r["Priority"] in ["P1", "P2", "P3", "P4"]
        assert r["Status"] in ["Open", "Fixed", "Verified", "Under Investigation"]
        assert len(r["Steps_to_Reproduce"]) > 10


def test_documentation_files_exist(project_root):
    """Verify all 10 formal documentation deliverables exist."""
    doc_dir = project_root / "documentation"
    assert (doc_dir / "installation_guide.md").exists()
    assert (doc_dir / "test_strategy.md").exists()
    assert (doc_dir / "test_plan.md").exists()
    assert (doc_dir / "test_execution_report.md").exists()
    assert (doc_dir / "bug_report_guide.md").exists()
    assert (doc_dir / "internship_summary_report.md").exists()
    assert (doc_dir / "test_environment.md").exists()
    assert (doc_dir / "known_limitations.md").exists()
    assert (doc_dir / "test_data_description.md").exists()
    assert (doc_dir / "release_checklist.md").exists()


def test_github_actions_workflow_exists(project_root):
    """Verify GitHub Actions CI workflow file."""
    wf_file = project_root / ".github" / "workflows" / "qa.yml"
    assert wf_file.exists(), "GitHub Actions workflow .github/workflows/qa.yml missing."
    assert wf_file.stat().st_size > 50
