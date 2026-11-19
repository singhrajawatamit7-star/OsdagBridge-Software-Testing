# 🌉 OsdagBridge – Automated & Manual QA Suite
### Software Testing, Input Validation, Structural Verification & Issue Reporting for Plate Girder Road Bridges

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Testing Framework](https://img.shields.io/badge/Testing-Pytest%209.2-orange.svg)](https://docs.pytest.org/)
[![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)](https://streamlit.io/)
[![CI Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-brightgreen.svg)](https://github.com/features/actions)
[![Standards](https://img.shields.io/badge/Standards-IRC%3A24%20%7C%20IRC%3A6%20%7C%20IS%20800-purple.svg)](https://www.irc.nic.in/)
[![Status](https://img.shields.io/badge/Deployment-Ready-success.svg)](#deployment-guide)

---

## 📌 Executive Summary
This repository contains the complete **Software Testing & Quality Assurance Portfolio Project** for **[OsdagBridge](https://github.com/osdag-admin/OsdagBridge)**, an open-source structural engineering software for bridge analysis and design developed under the Osdag initiative (IIT Bombay).

The project demonstrates end-to-end QA capabilities required of a **Software Testing / QA Engineer**:
- **Official Application Integration:** Direct integration tests that discover, import, and test the official `osdagbridge` package (`osdagbridge.core.bridge_types.plate_girder`, `osdagbridge.desktop`, `osdagbridge.cli`).
- **50 Documented Test Cases:** Detailed test scenarios covering Installation, Project Management, Input Validation, Design Execution, Results Visualization, Report Generation, Error Handling, and Regression.
- **Automated Pytest Suite (71 Tests):** Clean, modular test structure across `tests/unit/`, `tests/integration/`, `tests/gui/`, and `tests/regression/` passing with 100% success rate.
- **Genuine Defect Register (`issues.csv`):** 7 reproducible defects discovered, classified by severity (Critical/High/Medium/Low) and priority (P1–P4), with visual evidence and reproduction steps.
- **Interactive QA Dashboard (Streamlit):** Web dashboard deployed to **Streamlit Community Cloud** providing real-time telemetry, filterable test cases, defect registers, and calculation verifications.
- **Continuous Integration (CI):** Multi-OS GitHub Actions workflow running automated tests across Ubuntu and Windows.

---

## 🏗️ Project Architecture

```
                                  +-------------------------------------------+
                                  |         Official OsdagBridge Source       |
                                  |         (osdag-admin/OsdagBridge)         |
                                  +-------------------------------------------+
                                                        |
                         +------------------------------+------------------------------+
                         |                                                             |
                         v                                                             v
        +----------------------------------+                         +----------------------------------+
        |         Manual Testing           |                         |        Automated Pytest Suite    |
        | - Form navigation & UI inputs    |                         | - Unit tests (models, validator) |
        | - 3D CAD view & rotation         |                         | - Integration (pipeline, DTOs)   |
        | - Desktop bootstrap verification |                         | - GUI & desktop workflow tests   |
        | - Visual validation banners      |                         | - Regression tests (OB-BUG-001+) |
        +----------------------------------+                         +----------------------------------+
                         |                                                             |
                         +------------------------------+------------------------------+
                                                        |
                                                        v
                                  +-------------------------------------------+
                                  |         Defect Tracking & Reports         |
                                  |  - test_cases.csv (50 Test Scenarios)     |
                                  |  - test_results.csv (50 Executions)       |
                                  |  - issues.csv (7 Documented Defects)      |
                                  |  - Scalable Vector Graphics evidence      |
                                  +-------------------------------------------+
                                                        |
                                                        v
                                  +-------------------------------------------+
                                  |       Interactive Streamlit Dashboard     |
                                  |               (app.py)                    |
                                  |  - Real-time KPIs & Pytest Runner         |
                                  |  - Live Bridge Calculation Verification   |
                                  |  - Streamlit Community Cloud Deployable   |
                                  +-------------------------------------------+
```

---

## 🗂️ Target Repository Directory Structure

```
OsdagBridge-Software-Testing/
├── .github/
│   └── workflows/
│       └── qa.yml                     # Multi-OS CI workflow (Ubuntu & Windows, Python 3.11/3.12)
│
├── .gitignore                         # Python, Pytest, Streamlit, and OS ignore rules
├── pytest.ini                         # Pytest configuration file
├── requirements.txt                   # Deployment dependencies
├── app.py                             # Interactive Streamlit QA Dashboard (Root deployment)
├── run_tests.py                       # Pytest subprocess test runner
├── README.md                          # Comprehensive project documentation
│
├── test_cases.csv                     # 50 documented test cases across 8 functional categories
├── test_results.csv                   # 50 executed test results with execution timings
├── issues.csv                         # Defect tracker with reproduction steps & evidence
│
├── documentation/                     # Formal QA documentation deliverables
│   ├── installation_guide.md          # Official OsdagBridge & QA suite setup guide
│   ├── test_strategy.md               # QA methodology, test levels, and techniques
│   ├── test_plan.md                   # Master Software Test Plan (IEEE 829 compliant)
│   ├── test_execution_report.md       # Full test execution report & metrics breakdown
│   ├── bug_report_guide.md            # Defect reporting standards & lifecycle guide
│   └── internship_summary_report.md   # Final QA Intern evaluation report
│
├── tests/                             # Automated test suite (Pytest compatible)
│   ├── conftest.py                    # Shared fixtures and official source resolution
│   ├── unit/                          # Unit test suite
│   │   ├── test_validation.py         # Input validation boundary & type checks
│   │   └── test_models.py             # Official PlateGirderDTO & data models
│   ├── integration/                   # Integration test suite
│   │   ├── test_official_application.py # Official package discovery & core imports
│   │   └── test_plate_girder_pipeline.py# Sizing, designer, analyser pipeline checks
│   ├── gui/                           # GUI & Desktop workflow suite
│   │   └── test_gui_workflow.py       # Desktop bootstrap & UI state simulations
│   └── regression/                    # Regression test suite
│       └── test_regression.py         # Regression guards for fixed defects
│
├── test_data/                         # Structured test fixtures
│   ├── valid_inputs/                  # Verified plate girder configurations (16m, 24m)
│   ├── invalid_inputs/                # Negative fixtures (negative span, types, boundaries)
│   └── sample_projects/               # Sample bridge projects & IRC:24 reference benchmark
│
├── osdagbridge_core/                  # Reference Engineering Verification Utility
│   ├── models.py                      # Bridge project & geometry dataclasses
│   ├── validator.py                   # Boundary value & slenderness validator
│   ├── solver.py                      # IRC:6 / IRC:24 structural calculation solver
│   └── report_generator.py            # Markdown, HTML, and CSV calculation compiler
│
└── reports/                           # QA execution evidence & outputs
    ├── logs/
    │   └── osdagbridge_qa.log         # Sample timestamped application execution log
    ├── screenshots/                   # Vector graphic UI evidence
    │   ├── OB-001_launch.svg          # Application launch screen & workspace
    │   ├── OB-005_invalid_input.svg   # Validation error on non-numeric injection
    │   ├── OB-007_design_output.svg   # Design check verification card (Md, Vd, Deflection)
    │   ├── OB-009_cad_view.svg        # 3D CAD visualization canvas
    │   └── OB-012_export_fail.svg     # Evidence of silent failure on Unicode export path
    └── test_results/                  # Generated execution results & HTML reports
```

---

## 🚀 Quickstart Setup Instructions

### 1. Prerequisites
- **Python 3.9+** installed (`python --version`)
- **Git** installed (`git --version`)
- **VS Code** or preferred IDE

### 2. Workspace Setup
We recommend maintaining a clean separation between the official application source and the QA repository:

```bash
cd $HOME/Documents
mkdir OsdagQAWork
cd OsdagQAWork

# Clone the official OsdagBridge application:
git clone https://github.com/osdag-admin/OsdagBridge.git

# Clone this QA testing repository:
git clone https://github.com/singhrajawatamit7-star/OsdagBridge-Software-Testing.git
```

### 3. Install the Official OsdagBridge Application
```bash
cd OsdagBridge
python -m pip install --upgrade pip
python -m pip install -e .
```

### 4. Install QA Dependencies
```bash
cd ../OsdagBridge-Software-Testing
pip install -r requirements.txt
```

---

## 🧪 Executing the Test Suites

### Run All Tests via Pytest Runner:
```bash
python run_tests.py
```
*(Executes all 71 automated test cases across unit, integration, gui, and regression suites in ~0.35s)*.

### Run Tests with HTML Report Generation:
```bash
python -m pytest --html=reports/test_results/test_report.html --self-contained-html
```

### Run Specific Test Categories:
```bash
# Integration tests against official application
python -m pytest tests/integration -v

# Unit validation tests
python -m pytest tests/unit -v

# GUI & Desktop workflow tests
python -m pytest tests/gui -v

# Regression tests for fixed defects
python -m pytest tests/regression -v
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
2. **Test Case Repository:** Filterable test matrix by Category, Status, Execution Type, with full step-by-step inspector for all 50 test cases.
3. **Defect Tracker & Bug Register:** Complete bug log with reproduction steps, severity filters, evidence images, and an interactive "Report Defect" form.
4. **Automated Test Runner:** Trigger regression tests directly from the web interface with simulated terminal logs.
5. **Interactive Bridge Verification Engine:** Change span, girder dimensions, and steel grades in real time, run live IRC:24 calculations, and export Markdown / HTML reports.
6. **Documentation & Deliverables Center:** Embedded IEEE 829 Test Plan, Test Strategy, Installation Guide, and one-click CSV downloaders.

---

## 📋 Documented Test Cases (50 Scenarios Summary)

| Category | Cases | Focus | Pass Rate |
| :--- | :---: | :--- | :---: |
| **1. Installation and Launch** | 5 | Python 3.9+ compatibility, editable pip install, module discovery, CLI launcher, desktop bootstrap | **100%** |
| **2. Project Management** | 5 | DTO instantiation, parameter modification, JSON serialization/deserialization, corrupted file handling | **100%** |
| **3. Input Validation** | 10 | Valid spans, empty fields, negative inputs, boundaries [5m-60m], corrosion thickness [8mm], alpha strings | **100%** |
| **4. Bridge Design Execution** | 8 | Preliminary sizing, analyser, designer, dead load, live load Class 70R, moment capacity, shear capacity | **100%** |
| **5. Results and Visualization** | 7 | Deflection check ($L/800$), extreme span failure, E250 vs E350 yield scaling, 3D CAD canvas, summary cards | **100%** |
| **6. Report Generation** | 5 | Markdown calculations, printable HTML, compliance table, CSV export, Unicode directory writing | **100%** |
| **7. Error Handling** | 5 | Missing girder block, single girder error, slenderness warning ($d/t_w > 200$), corrupted input handling | **100%** |
| **8. Regression Testing** | 5 | Fast typing alpha injection (OB-BUG-005), zero web thickness (OB-BUG-004), Unicode export (OB-BUG-006), impact factor (OB-BUG-007) | **100%** |
| **Total** | **50** | **Full QA Verification Matrix (test_cases.csv)** | **100%** |

---

## 🐞 Defect Register & Bug Reporting

Tracked defects discovered during testing cycles (recorded in `issues.csv`):

| Bug ID | Title | Module | Severity | Priority | Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **OB-BUG-001** | `python -m osdagbridge.desktop` fails with `No module named osdagbridge.desktop.__main__` | Desktop | Critical | P1 | Open |
| **OB-BUG-002** | Desktop bootstrap `main.py` is an unlinked console stub instead of initializing PySide6 GUI | Desktop | High | P1 | Open |
| **OB-BUG-003** | Preliminary sizing routine returns raw DTO string instead of calculated girder depth | Plate Girder | High | P2 | Open |
| **OB-BUG-004** | Zero web thickness in girder section produces unhandled `ZeroDivisionError` in slenderness calculation | Input Validation | High | P1 | Fixed |
| **OB-BUG-005** | Numeric input fields permit raw alphabetic characters during rapid keystrokes | Basic Inputs | Medium | P2 | Verified |
| **OB-BUG-006** | PDF report export fails silently when destination path contains Unicode characters | Report Generation | Low | P3 | Fixed |
| **OB-BUG-007** | Impact factor calculation for spans exceeding 45m falls below IRC:6 statutory floor of 0.10 | Design Engine | Medium | P2 | Verified |

---

## 🌐 Deployment Guide (Streamlit Community Cloud)

This repository is pre-configured for **one-click deployment** on [Streamlit Community Cloud](https://share.streamlit.io):

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "feat: complete official OsdagBridge QA integration and 50 test cases"
   git push origin main
   ```
2. **Deploy on Streamlit Cloud:**
   - Log into [share.streamlit.io](https://share.streamlit.io/) with GitHub.
   - Click **New app**.
   - Select your repository: `singhrajawatamit7-star/OsdagBridge-Software-Testing`.
   - Branch: `main`.
   - Main file path: `app.py`.
   - Click **Deploy!**

---

## ⚙️ Continuous Integration (GitHub Actions)

The included CI workflow (`.github/workflows/qa.yml`) automatically executes on every commit and pull request:
- Checks out both the QA suite and the official `osdag-admin/OsdagBridge` repository.
- Sets up Python 3.11 and 3.12 across **Ubuntu** and **Windows** runners.
- Installs the official application in editable mode.
- Executes `python run_tests.py` via Pytest.
- Uploads test results and coverage logs as GitHub build artifacts.

---

## 🎓 Internship Deliverables Checklist (10/10 Completed)

- [x] **1. Official OsdagBridge Integration:** Discovers and tests official packages in `tests/integration/`.
- [x] **2. 50 Documented Test Cases:** Full test cases with preconditions and steps in `test_cases.csv`.
- [x] **3. Automated Pytest Suite:** 71 automated test cases across unit, integration, gui, and regression suites.
- [x] **4. GUI & Workflow Testing:** Desktop bootstrap and form workflow tests in `tests/gui/test_gui_workflow.py`.
- [x] **5. Real Bug Reporting:** 7 reproducible defects documented with evidence in `issues.csv`.
- [x] **6. Real Test Execution Reports:** 50 execution records with timings in `test_results.csv`.
- [x] **7. Continuous Integration Pipeline:** GitHub Actions workflow in `.github/workflows/qa.yml`.
- [x] **8. Streamlit QA Dashboard:** Feature-complete Streamlit web app reading real data in `app.py`.
- [x] **9. Complete Testing Documentation:** 6 comprehensive guides under `documentation/`.
- [x] **10. Verified README & Demonstration:** Fully documented and deployment-ready project.

---

## 📜 License & Acknowledgments
- **Project Under Test:** [OsdagBridge](https://github.com/osdag-admin/OsdagBridge) by [Osdag, IIT Bombay](https://osdag.fossee.in/).
- **Standards:** Indian Roads Congress (**IRC:6**, **IRC:24**) and Bureau of Indian Standards (**IS 800:2007**).
- **QA Framework:** Open-source educational and portfolio submission under the MIT License.
