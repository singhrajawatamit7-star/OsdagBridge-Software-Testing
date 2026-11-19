# 🌉 OsdagBridge – Automated & Manual QA Suite
### Software Testing, Input Validation, Structural Verification & Issue Reporting for Plate Girder Road Bridges

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Testing Framework](https://img.shields.io/badge/Testing-Pytest%209.2-orange.svg)](https://docs.pytest.org/)
[![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)](https://streamlit.io/)
[![CI Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-brightgreen.svg)](https://github.com/features/actions)
[![Standards](https://img.shields.io/badge/Standards-IRC%3A24%20%7C%20IRC%3A6%20%7C%20IS%20800-purple.svg)](https://www.irc.nic.in/)
[![Status](https://img.shields.io/badge/Status-Submission_Ready-success.svg)](#deployment-guide)

---

## 📌 Executive Summary

This repository is the complete **Software Testing & Quality Assurance Portfolio Project** for **[OsdagBridge](https://github.com/osdag-admin/OsdagBridge)**, the open-source structural-engineering software for bridge analysis developed under the Osdag initiative at IIT Bombay.

The project demonstrates end-to-end QA capabilities expected of a **Software Testing / QA Engineer**:

| Deliverable | Detail |
|---|---|
| **Official Application Integration** | Smoke tests that discover, import, and inspect the official `osdagbridge` package (CLI, desktop, core) |
| **50 Documented Test Cases** | Detailed scenarios covering Installation, Project Management, Validation, Design, Results, Reporting, Error Handling, and Regression (`test_cases.csv`) |
| **69 Automated Pytest Tests** | Real Pytest functions across `tests/unit/`, `tests/integration/`, `tests/ui_simulation/`, `tests/regression/` — **100 % pass rate** (`test_results.csv` from real JUnit XML export) |
| **Genuine Defect Register** | 7 reproducible upstream defects classified by severity (Critical/High/Medium/Low) and priority (P1–P4) with evidence files (`issues.csv`) |
| **Interactive QA Dashboard** | Streamlit web app reading live CSV data, real-time Pytest subprocess runner, calculation verifier, and documentation center |
| **Continuous Integration** | Multi-OS GitHub Actions workflow (Ubuntu + Windows, Python 3.11/3.12) |

> **Important — `osdagbridge_core`:** This repository contains an independent
> **QA Reference Utility** (`osdagbridge_core/`) that provides validated bridge
> calculations for the Streamlit dashboard's verification engine. It is **not**
> the official OsdagBridge calculation engine and is never presented as such.

> **Known upstream blocker — `osdagbridge.core.models`:** The official
> `src/osdagbridge/core/__init__.py` executes `from .models import *` but
> `models.py` does not exist in the repository. This raises
> `ModuleNotFoundError: No module named 'osdagbridge.core.models'` on any
> attempt to import `osdagbridge.core` or its sub-packages. This upstream defect
> is catalogued as **OB-BUG-003** and documented in
> `documentation/known_limitations.md`. The integration test suite
> (`tests/integration/test_plate_girder_pipeline.py`) explicitly asserts this
> condition with `pytest.raises(ModuleNotFoundError)` so the upstream blocker
> is tracked — not hidden.

---

## 🏗️ Project Architecture

```
                              +------------------------------------------+
                              |       Official OsdagBridge Source        |
                              |       (osdag-admin/OsdagBridge)          |
                              +------------------------------------------+
                                                    |
                       +----------------------------+----------------------------+
                       |                                                         |
                       v                                                         v
     +----------------------------------+                   +----------------------------------+
     |         Manual Testing           |                   |       Automated Pytest Suite     |
     | - Form navigation & UI inputs    |                   | - Unit tests (models, validator) |
     | - Desktop bootstrap verification |                   | - Integration (package imports)  |
     | - IRC:24 benchmark verification  |                   | - UI State Simulation            |
     | - Visual validation banners      |                   | - Regression tests (OB-BUG-001+) |
     +----------------------------------+                   +----------------------------------+
                       |                                                         |
                       +----------------------------+----------------------------+
                                                    |
                                                    v
                              +------------------------------------------+
                              |       Defect Tracking & Reports          |
                              | - test_cases.csv  (50 scenarios)         |
                              | - test_results.csv (69 real executions)  |
                              | - issues.csv (7 documented defects)      |
                              | - SVG evidence files                      |
                              +------------------------------------------+
                                                    |
                                                    v
                              +------------------------------------------+
                              |     Interactive Streamlit Dashboard      |
                              |             (app.py)                     |
                              | - Real-time KPIs from actual CSV data    |
                              | - Live Pytest subprocess runner          |
                              | - Bridge Calculation Verification        |
                              | - Streamlit Community Cloud deployable   |
                              +------------------------------------------+
```

---

## 🗂️ Repository Structure

```
OsdagBridge-Software-Testing/
├── .github/
│   └── workflows/
│       └── qa.yml                     # Multi-OS CI (Ubuntu & Windows, Python 3.11/3.12)
│
├── .gitignore
├── pytest.ini                         # Pytest configuration with custom markers
├── requirements.txt                   # Deployment dependencies
├── app.py                             # Streamlit QA Dashboard
├── run_tests.py                       # Pytest subprocess runner
├── README.md
│
├── test_cases.csv                     # 50 documented test cases across 8 categories
├── test_results.csv                   # 69 real execution records (JUnit XML export)
├── issues.csv                         # Defect tracker with steps & evidence
│
├── scripts/
│   └── export_junit_csv.py            # Converts JUnit XML → test_results.csv
│
├── documentation/                     # Formal QA deliverables
│   ├── installation_guide.md
│   ├── test_strategy.md
│   ├── test_plan.md
│   ├── test_execution_report.md
│   ├── bug_report_guide.md
│   ├── internship_summary_report.md
│   ├── test_environment.md
│   ├── known_limitations.md
│   ├── test_data_description.md
│   └── release_checklist.md
│
├── tests/
│   ├── conftest.py                    # Shared fixtures, official source resolution
│   ├── test_repository_layout.py     # Deliverables integrity checks
│   ├── unit/
│   │   ├── test_validation.py        # Input validation boundary checks
│   │   └── test_models.py            # QA reference model unit tests
│   ├── integration/
│   │   ├── test_official_application.py   # Official package smoke tests
│   │   └── test_plate_girder_pipeline.py  # Upstream blocker documentation
│   ├── ui_simulation/
│   │   └── test_ui_state_simulation.py    # UI state machine simulation tests
│   └── regression/
│       └── test_regression.py        # Regression guards for fixed defects
│
├── test_data/
│   ├── valid_inputs/                  # Valid 16m/24m plate girder payloads
│   ├── invalid_inputs/                # Negative fixtures (negative span, type errors)
│   └── sample_projects/               # IRC:24 reference benchmark projects
│
├── osdagbridge_core/                  # Independent QA Reference Utility (NOT official OsdagBridge)
│   ├── models.py
│   ├── validator.py
│   ├── solver.py
│   └── report_generator.py
│
└── reports/
    ├── logs/
    ├── screenshots/                   # SVG evidence files (OB-001 through OB-012)
    └── test_results/                  # JUnit XML & HTML reports
```

---

## 🚀 Quickstart Setup Instructions

### 1. Prerequisites
- **Python 3.9+** (`python --version`)
- **Git** (`git --version`)

### 2. Clone Both Repositories Side-by-Side

```bash
mkdir OsdagQAWork && cd OsdagQAWork

# Official OsdagBridge application (required for integration tests)
git clone https://github.com/osdag-admin/OsdagBridge.git

# This QA repository
git clone https://github.com/singhrajawatamit7-star/OsdagBridge-Software-Testing.git
```

### 3. Install the Official Application

```bash
cd OsdagBridge
pip install -e .
cd ..
```

### 4. Install QA Dependencies

```bash
cd OsdagBridge-Software-Testing
pip install -r requirements.txt
```

### 5. Point tests at the Official Source (optional — auto-detected if cloned side-by-side)

```bash
# Powershell
$env:OSDAGBRIDGE_ROOT = "..\OsdagBridge"

# Bash
export OSDAGBRIDGE_ROOT="../OsdagBridge"
```

---

## 🧪 Executing the Test Suite

```bash
# Run all 69 automated tests
python -m pytest tests -v

# Run with HTML report
python -m pytest tests --html=reports/test_results/test_report.html --self-contained-html

# Individual suites
python -m pytest tests/integration -v     # Official application smoke tests
python -m pytest tests/unit -v            # Validation & model unit tests
python -m pytest tests/ui_simulation -v   # UI state simulation tests
python -m pytest tests/regression -v      # Regression guards
```

**Regenerate `test_results.csv` from real execution:**
```bash
python -m pytest tests --junitxml=reports/test_results/junit.xml
python scripts/export_junit_csv.py reports/test_results/junit.xml test_results.csv
```

---

## 📊 Interactive QA Dashboard

```bash
streamlit run app.py
# Open http://localhost:8501
```

**Dashboard sections:**
1. **QA Executive Dashboard** — KPIs computed from real CSV data, pass-rate gauges
2. **Test Case Repository** — 50 scenarios with filterable category, status, and execution type
3. **Defect Tracker** — 7 defects with severity/priority filter, evidence images, live append form
4. **Automated Test Runner** — Triggers real `pytest` subprocess from the browser; shows live stdout
5. **Bridge Verification Engine** — Powered by `osdagbridge_core` (independent QA reference)
6. **Documentation Center** — Full-text viewer for all 10 QA deliverables

---

## 📋 Documented Test Cases (50 Scenarios)

| Category | Cases | Focus | Status |
|:---|:---:|:---|:---:|
| Installation & Launch | 5 | Python compatibility, pip install, module discovery, CLI, desktop bootstrap | PASS |
| Project Management | 5 | DTO instantiation, modification, JSON serialization, corrupted file handling | PASS |
| Input Validation | 10 | Valid spans, empty fields, negatives, boundaries [5m–60m], type errors | PASS |
| Design Execution | 8 | Preliminary sizing, analyser, designer, dead/live loads, moment, shear | PASS |
| Results & Visualization | 7 | Deflection (L/800), extreme spans, steel grade scaling, 3D CAD, summary cards | PASS |
| Report Generation | 5 | Markdown, HTML, compliance table, CSV export, Unicode path writing | PASS |
| Error Handling | 5 | Missing girder, single-girder error, slenderness warning, corrupted input | PASS |
| Regression Testing | 5 | Alpha injection, zero web thickness, Unicode export, impact factor floor | PASS |
| **Total** | **50** | Full QA verification matrix (`test_cases.csv`) | **100%** |

---

## 🐞 Defect Register

Tracked defects in `issues.csv` — all discovered against the official `osdag-admin/OsdagBridge` application:

| Bug ID | Title | Severity | Priority | Status |
|:---|:---|:---:|:---:|:---:|
| **OB-BUG-001** | `python -m osdagbridge.desktop` fails — no `__main__.py` | Critical | P1 | Open |
| **OB-BUG-002** | Desktop `main.py` is a console stub — no PySide6 GUI | High | P1 | Open |
| **OB-BUG-003** | `osdagbridge.core.__init__` imports missing `models.py` → `ModuleNotFoundError` | High | P1 | Open |
| **OB-BUG-004** | Zero web thickness causes unhandled `ZeroDivisionError` in slenderness check | High | P1 | Fixed |
| **OB-BUG-005** | Numeric input fields accept alphabetic characters during rapid typing | Medium | P2 | Verified |
| **OB-BUG-006** | PDF/HTML export fails silently for Unicode destination paths | Low | P3 | Fixed |
| **OB-BUG-007** | Impact factor drops below IRC:6 statutory floor of 0.10 for spans > 45 m | Medium | P2 | Verified |

---

## ⚙️ Continuous Integration

`.github/workflows/qa.yml` runs on every push and pull request:

- Checks out the QA suite **and** the official `osdag-admin/OsdagBridge` repository
- Matrix: **Ubuntu + Windows** × **Python 3.11 / 3.12**
- Installs official application (`pip install -e .`) and QA dependencies
- Runs `python -m pytest tests --junitxml=...` — **exits non-zero on failure** (no `|| true` suppression)
- Uploads JUnit XML and HTML reports as build artefacts

---

## 🌐 Deployment Guide (Streamlit Community Cloud)

1. Push repository to GitHub (all files committed)
2. Log into [share.streamlit.io](https://share.streamlit.io/) with GitHub
3. Click **New app** → select `singhrajawatamit7-star/OsdagBridge-Software-Testing`, branch `main`, file `app.py`
4. Click **Deploy**

---

## 🎓 Internship Deliverables Checklist

- [x] **Official OsdagBridge integration** — `tests/integration/` smoke tests with honest skip/fail handling
- [x] **50 documented test cases** — `test_cases.csv` with preconditions, steps, and expected results
- [x] **69 automated Pytest tests** — 100 % pass rate; `test_results.csv` regenerated from real JUnit XML
- [x] **UI state simulation** — desktop & form workflow state machine in `tests/ui_simulation/`
- [x] **7 reproducible defects** — `issues.csv` with severity, priority, evidence, and reproduction steps
- [x] **69 real execution records** — `test_results.csv` exported by `scripts/export_junit_csv.py`
- [x] **CI pipeline** — multi-OS GitHub Actions, fails on test failure (no suppression)
- [x] **Streamlit QA dashboard** — KPIs from real data, live Pytest runner, calculation verifier
- [x] **10 documentation deliverables** — `documentation/` (plan, strategy, environment, limitations, checklist…)
- [x] **Honest README** — all metrics traceable to actual artefacts in this repository

---

## 📜 License & Acknowledgments
- **Project Under Test:** [OsdagBridge](https://github.com/osdag-admin/OsdagBridge) — Osdag initiative, IIT Bombay
- **Standards:** Indian Roads Congress (IRC:6, IRC:24) and Bureau of Indian Standards (IS 800:2007)
- **QA Framework:** Open-source educational and portfolio submission under the MIT License
