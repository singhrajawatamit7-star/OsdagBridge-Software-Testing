# 🌉 OsdagBridge – Automated & Manual QA Suite
### Software Testing, Input Validation, Structural Verification & Issue Reporting for Plate Girder Road Bridges

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Testing Framework](https://img.shields.io/badge/Testing-Pytest-orange.svg)](https://docs.pytest.org/)
[![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)](https://streamlit.io/)
[![CI Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-brightgreen.svg)](https://github.com/features/actions)
[![Standards](https://img.shields.io/badge/Standards-IRC%3A24%20%7C%20IRC%3A6%20%7C%20IS%20800-purple.svg)](https://www.irc.nic.in/)
[![Status](https://img.shields.io/badge/Deployment-Ready-success.svg)](#deployment-guide)

---

## 📌 Executive Summary
This repository contains the complete **Software Testing & Quality Assurance Portfolio Project** for **[OsdagBridge](https://github.com/osdag-admin/OsdagBridge)**, an open-source structural engineering software for bridge analysis and design developed under the Osdag initiative (IIT Bombay).

The project demonstrates end-to-end QA capabilities required of a **Software Testing / QA Engineer**:
- **System Exploration & Understanding:** Investigating structural workflows for Steel Plate Girder Bridges under Indian Standard codes (**IS 800:2007**, **IRC:6**, **IRC:24-2010**).
- **Manual & Exploratory Testing:** 20 comprehensive test cases verifying input fields, boundary limits, 3D CAD visualization, and report generation.
- **Automated Testing with Python & Pytest:** Automated test scripts testing geometric boundary thresholds, corrosion thickness limits, slenderness ratios ($d/t_w$), and load combinations.
- **Defect Tracking & Issue Reporting:** Professional defect register (`issues.csv`) documenting real edge-case bugs with steps to reproduce, severity, priority, and visual evidence.
- **Interactive QA Dashboard (Streamlit):** Web dashboard deployed to **Streamlit Community Cloud** providing real-time telemetry, test runner simulation, live calculation verifications, and downloadable CSV deliverables.
- **Continuous Integration (CI):** Multi-OS GitHub Actions workflow running automated regression tests on every push.

---

## 🏗️ Project Architecture

```
                                  +-------------------------------------------+
                                  |         OsdagBridge Desktop App           |
                                  |        (Application Under Test)           |
                                  +-------------------------------------------+
                                                        |
                         +------------------------------+------------------------------+
                         |                                                             |
                         v                                                             v
        +----------------------------------+                         +----------------------------------+
        |         Manual Testing           |                         |        Automated Testing         |
        | - Form navigation & UI inputs    |                         | - Python 3.11+ & Pytest Suite    |
        | - 3D CAD view & rotation         |                         | - Boundary value verification    |
        | - Visual validation banners      |                         | - ULS & SLS limit state checks   |
        +----------------------------------+                         +----------------------------------+
                         |                                                             |
                         +------------------------------+------------------------------+
                                                        |
                                                        v
                                  +-------------------------------------------+
                                  |         Defect Tracking & Reports         |
                                  |  - test_cases.csv | test_results.csv     |
                                  |  - issues.csv (Severity P1-P4)            |
                                  |  - Scalable Vector Graphics evidence      |
                                  +-------------------------------------------+
                                                        |
                                                        v
                                  +-------------------------------------------+
                                  |       Interactive Streamlit Dashboard     |
                                  |               (app.py)                    |
                                  |  - Real-time KPIs & Test Runner           |
                                  |  - Live Bridge Calculation Verification   |
                                  |  - Streamlit Community Cloud Deployable   |
                                  +-------------------------------------------+
```

---

## 🗂️ Repository Directory Structure

```
OsdagBridge-QA/
│
├── .github/
│   └── workflows/
│       └── qa.yml                     # Multi-OS CI regression workflow (Ubuntu & Windows)
│
├── .gitignore                         # Python, Pytest, Streamlit, and OS ignore rules
├── pytest.ini                         # Pytest configuration file
├── requirements.txt                   # Dependency manifest for Streamlit Cloud & local setup
├── app.py                             # Interactive Streamlit QA Dashboard (Root deployment)
├── run_tests.py                       # Standalone zero-dependency test runner & reporter
├── README.md                          # Comprehensive project documentation & portfolio guide
│
├── test_cases.csv                     # 20 comprehensive manual and automated test scenarios
├── test_results.csv                   # Historical execution matrix with timings and statuses
├── issues.csv                         # Professional defect tracker with reproduction steps
│
├── osdagbridge_core/                  # Core engineering verification & simulation package
│   ├── __init__.py
│   ├── models.py                      # Bridge project, geometry, and result dataclasses
│   ├── validator.py                   # Input validation engine (boundary, slenderness, types)
│   ├── solver.py                      # IRC:6 / IRC:24 structural calculation solver
│   └── report_generator.py            # Markdown, HTML, and CSV calculation sheet compiler
│
├── tests/                             # Automated test suite (Pytest compatible)
│   ├── __init__.py
│   ├── conftest.py                    # Shared fixtures and mock payloads
│   ├── test_environment.py            # Environment, Python 3.11+, and directory integrity tests
│   ├── test_inputs.py                 # Input boundary, type, required fields, corrosion limit tests
│   ├── test_project.py                # Project serialization, JSON loading, corrupt file handling
│   ├── test_design.py                 # Bending capacity, shear resistance, deflection tests
│   ├── test_reports.py                # Report readability, markup, and table export tests
│   └── test_repository_layout.py      # Deliverables integrity and test case matrix validation
│
├── test_data/                         # Structured test fixtures
│   ├── valid_inputs.json              # Valid 24m plate girder highway bridge payload
│   ├── invalid_inputs.json            # Suite of negative test fixtures (negative span, types)
│   ├── valid_inputs.csv               # Parametric matrix of valid bridge configurations
│   ├── invalid_inputs.csv             # Invalidation matrix with expected error codes
│   └── reference_design_irc.json      # Benchmark engineering calculations from IRC:24
│
├── documentation/                     # Formal QA documentation deliverables
│   ├── test_plan.md                   # Master Software Test Plan (IEEE 829 compliant)
│   ├── bug_report_template.md         # Industry-standard defect report template
│   ├── test_cases.csv                 # Mirrored copy of test case specifications
│   └── internship_summary_report.md   # Final QA Intern formal evaluation submission
│
└── reports/                           # QA execution evidence & outputs
    ├── test_results.csv               # Historical execution matrix
    ├── issues.csv                     # Defect register
    ├── logs/
    │   └── osdagbridge_qa.log         # Sample timestamped application execution log
    └── screenshots/                   # Vector graphic UI evidence
        ├── OB-001_launch.svg          # Application launch screen & workspace
        ├── OB-005_invalid_input.svg   # Validation error on non-numeric injection
        ├── OB-007_design_output.svg   # Design check verification card (Md, Vd, Deflection)
        ├── OB-009_cad_view.svg        # 3D CAD visualization canvas
        └── OB-012_export_fail.svg     # Evidence of silent failure on Unicode export path
```

---

## 🚀 Quickstart Setup Instructions

### 1. Prerequisites
- **Python 3.11+** installed (`python --version`)
- **Git** installed (`git --version`)
- **VS Code** or preferred IDE

### 2. Clone the Repository
```bash
git clone https://github.com/singhrajawatamit7-star/OsdagBridge-Software-Testing.git
cd OsdagBridge-Software-Testing
```

### 3. Create and Activate Virtual Environment
**On Windows (PowerShell):**
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

**On Linux / macOS:**
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🧪 Executing the Test Suites

### Option A: Using the Standalone Runner (Zero External Dependencies)
Runs the complete test suite across all 6 test modules using Python's standard library:
```bash
python run_tests.py
```

### Option B: Using Pytest (Standard QA Automation)
Run all tests with verbose output:
```bash
python -m pytest -v
```

Generate self-contained HTML test report:
```bash
python -m pytest --html=reports/test_report.html --self-contained-html
```

Generate code coverage metrics:
```bash
python -m pytest --cov=osdagbridge_core --cov-report=term-missing
```

---

## 📊 Interactive QA Dashboard

The dashboard provides an interactive visual control center for tests, bugs, and live calculations.

### Launch Dashboard Locally:
```bash
streamlit run app.py
```
Open browser at `http://localhost:8501`.

### Dashboard Features:
1. **QA Executive Dashboard:** High-level KPIs, test execution pass rates, module distribution, and recent activity.
2. **Test Case Repository:** Filterable test matrix by Module, Status, Execution Type, with full step-by-step inspector.
3. **Defect Tracker & Bug Register:** Complete bug log with reproduction steps, severity filters, evidence images, and an interactive "Report Defect" form.
4. **Automated Test Runner:** Trigger regression tests directly from the web interface with simulated terminal logs.
5. **Interactive Bridge Verification Engine:** Change span, girder dimensions, and steel grades in real time, run live IRC:24 calculations, and export Markdown / HTML reports.
6. **Documentation & Deliverables Center:** Embedded IEEE 829 Test Plan, Internship Summary, and one-click CSV downloaders.

---

## 📋 Documented Test Cases (Summary Matrix)

| Test ID | Module | Scenario | Expected Result | Status | Type |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **OB-001** | UI & Desktop | Launch application | Opens cleanly without startup tracebacks | **PASS** | Automated |
| **OB-002** | Project Lifecycle | Create bridge project | Initializes Plate Girder Bridge workspace | **PASS** | Automated |
| **OB-003** | Input Validation | Leave required field empty | Blocks design; raises `ERR_REQUIRED_FIELD_EMPTY` | **PASS** | Automated |
| **OB-004** | Input Validation | Enter boundary values | Enforces [5.0m - 60.0m] span limits | **PASS** | Automated |
| **OB-005** | Input Validation | Enter invalid characters | Catches non-numeric input with `ERR_INVALID_DATA_TYPE` | **PASS** | Automated |
| **OB-006** | Project Lifecycle | Save project inputs | Serializes configuration to valid JSON | **PASS** | Automated |
| **OB-007** | Design Engine | Run valid design | Computes $M_d$, $V_d$, and matches IRC:24 benchmark | **PASS** | Automated |
| **OB-008** | Design Engine | Run with missing inputs | Halts execution safely; raises `ValidationError` | **PASS** | Automated |
| **OB-009** | Visualization | Open 3D CAD view | Renders 3D wireframe, cross-section, and deck | **PASS** | Manual |
| **OB-010** | System & Logs | Open logs | Timestamped logs captured in `osdagbridge_qa.log` | **PASS** | Automated |
| **OB-011** | Design Engine | View design results | Displays utilization ratios and clause references | **PASS** | Automated |
| **OB-012** | Report Generation| Generate printable report | Compiles HTML/PDF report with verification table | **PASS** | Automated |
| **OB-013** | Report Generation| Generate CSV table | Exports code check verification matrix to CSV | **PASS** | Automated |
| **OB-014** | Design Engine | Modify and rerun design | Capacity dynamically updates on section change | **PASS** | Automated |
| **OB-015** | Project Lifecycle | Open invalid project file | Catches corrupt JSON syntax without crash | **PASS** | Automated |
| **OB-016** | Input Validation | Slenderness ratio limit | Flags `WARN_HIGH_SLENDERNESS` when $d/t_w > 200$ | **PASS** | Automated |
| **OB-017** | Design Engine | Extreme span boundary stress | 60m span correctly triggers deflection violation | **PASS** | Automated |
| **OB-018** | Design Engine | Deflection check (Class 70R) | Live load deflection $\delta_{LL} \le \text{Span}/800$ verified | **PASS** | Automated |
| **OB-019** | Material Engine | Material grade scaling | Yield strength scaling between E250 & E350 is 1.40 | **PASS** | Automated |
| **OB-020** | Report Generation| Report markdown compliance | Validates markdown report structure and sections | **PASS** | Automated |

---

## 🐞 Defect Register & Bug Reporting

Tracked defects discovered during testing cycles (recorded in `issues.csv`):

| Bug ID | Title | Module | Severity | Priority | Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **OB-BUG-001** | Numeric field accepts raw alphabetic characters during fast typing | Basic Inputs | Medium | P2 | Fixed |
| **OB-BUG-002** | Zero web thickness causes unhandled `ZeroDivisionError` in slenderness calculation | Input Validation | High | P1 | Fixed |
| **OB-BUG-003** | Corrupted JSON project file causes blank canvas instead of explicit error alert | Project Lifecycle | Medium | P2 | Investigating |
| **OB-BUG-004** | PDF report export fails silently when output path contains Unicode characters | Report Generation| Low | P3 | Open |
| **OB-BUG-005** | Tooltip missing on cross-girder spacing field | UI & Desktop | Low | P4 | Open |
| **OB-BUG-006** | Impact factor capping not strictly enforced for extreme spans (> 45m) | Design Engine | Medium | P2 | Retested |

---

## 🌐 Deployment Guide (Streamlit Community Cloud)

This repository is pre-configured for **one-click deployment** on [Streamlit Community Cloud](https://share.streamlit.io):

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: OsdagBridge QA Suite ready for deployment"
   git branch -M main
   git remote add origin https://github.com/singhrajawatamit7-star/OsdagBridge-Software-Testing.git
   git push -u origin main
   ```
2. **Deploy on Streamlit Cloud:**
   - Log into [share.streamlit.io](https://share.streamlit.io/) with GitHub.
   - Click **New app**.
   - Select your repository: `singhrajawatamit7-star/OsdagBridge-Software-Testing`.
   - Branch: `main`.
   - Main file path: `app.py`.
   - Click **Deploy!**

> **Note:** Root file placement of `requirements.txt`, `app.py`, `test_cases.csv`, `test_results.csv`, and `issues.csv` ensures zero deployment configuration overhead.

---

## ⚙️ Continuous Integration (GitHub Actions)

The included CI workflow (`.github/workflows/qa.yml`) automatically executes on every commit and pull request:
- Runs across **Ubuntu** and **Windows** runners.
- Tests across **Python 3.11** and **Python 3.12**.
- Executes both Pytest and the standalone runner.
- Uploads test results and coverage logs as GitHub build artifacts.

---

## 🎓 Internship Deliverables Checklist (10/10 Completed)

- [x] **1. Application Setup & Environment Assessment:** Complete environment verification in `tests/test_environment.py`.
- [x] **2. Software Test Plan (IEEE 829):** Detailed test plan in `documentation/test_plan.md`.
- [x] **3. 20 Documented Test Cases:** Full test cases with preconditions and steps in `test_cases.csv`.
- [x] **4. Automated Python Test Suite:** 6 comprehensive test modules in `tests/`.
- [x] **5. Test Execution Results:** Historical execution matrix in `test_results.csv` (100% pass rate).
- [x] **6. Defect Tracking System:** Documented defect register with reproduction steps in `issues.csv`.
- [x] **7. Testing Evidence & Logs:** Vector graphics screenshots and log traces in `reports/`.
- [x] **8. Interactive QA Dashboard:** Feature-complete Streamlit web app in `app.py`.
- [x] **9. Continuous Integration Pipeline:** GitHub Actions workflow in `.github/workflows/qa.yml`.
- [x] **10. Final Recommendations & Submission Report:** Formal submission report in `documentation/internship_summary_report.md`.

---

## ⚠️ Structural Engineering Considerations
> **Important Civil Engineering Warning:** Software outputs must never be independently deemed safe for construction without validation against approved hand calculations, applicable IRC bridge codes, and peer review by certified structural engineers.

---

## 📜 License & Acknowledgments
- **Project Under Test:** [OsdagBridge](https://github.com/osdag-admin/OsdagBridge) by [Osdag, IIT Bombay](https://osdag.fossee.in/).
- **Standards:** Indian Roads Congress (**IRC:6**, **IRC:24**) and Bureau of Indian Standards (**IS 800:2007**).
- **QA Framework:** Open-source educational and portfolio submission under the MIT License.
