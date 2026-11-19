# Test Environment Specification

## 1. Overview
This document specifies the software, hardware, environment variables, and runtime configurations utilized for manual, automated, and continuous integration testing of the **OsdagBridge** application and its accompanying QA verification suite.

---

## 2. Operating System & Platform Support

| Environment | Operating System | Kernel / Build | Architecture | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Local Primary** | Windows 11 Pro | Version 23H2 / 24H2 | x86_64 (64-bit) | Developer workstation, GUI manual testing, Streamlit dashboard execution |
| **Local Secondary** | Ubuntu Linux (WSL2) | Linux 6.6.x | x86_64 (64-bit) | Linux parity validation & headless CLI testing |
| **CI Runner 1** | Ubuntu 22.04 LTS (`ubuntu-latest`) | Linux 6.5.x | x86_64 (64-bit) | Automated Pytest regressions, code linting, packaging |
| **CI Runner 2** | Windows Server 2022 (`windows-latest`) | NT 10.0 | x86_64 (64-bit) | Automated Pytest cross-platform execution, path separator tests |

---

## 3. Python Runtime & Toolchain

- **Primary Python Version:** `Python 3.13.7` (64-bit, MSC v.1944 on Windows)
- **CI Matrix Python Versions:** `Python 3.11.x`, `Python 3.12.x`
- **Testing Framework:** `pytest >= 8.0.0, <= 9.2.0`
- **Pytest Plugins:**
  - `pytest-cov` (v7.1.0) — Code coverage analysis
  - `pytest-html` (v4.2.0) — Standalone HTML test execution report generation
  - `pytest-metadata` (v3.1.1) — Environment and runtime telemetry capture

---

## 4. Software Dependencies

### Official Application Under Test (`osdag-admin/OsdagBridge`)
- Repository: `https://github.com/osdag-admin/OsdagBridge`
- Installation Method: `pip install -e .` (editable development mode)
- Core Dependencies:
  - `numpy >= 1.24.0` — Numerical linear algebra and matrix evaluations
  - `PySide6 >= 6.5.0` — Qt GUI framework (Desktop interface)
  - `python-docx >= 0.8.11` — Engineering calculation docx generator

### QA Suite & Interactive Dashboard (`OsdagBridge-Software-Testing`)
- Core Dependencies:
  - `streamlit >= 1.30.0` — Interactive web telemetry dashboard
  - `pandas >= 2.0.0` — Test data management, CSV parsing, defect registry
  - `pytest >= 8.0.0` — Automated test runner and assertion engine
  - `pytest-html >= 4.0.0` — HTML test reporting
  - `pytest-cov >= 5.0.0` — Code coverage reporting

---

## 5. Directory Layout & Path Resolution

To maintain clear separation between the software under test and the QA test suite, the following directory layout is standardized:

```
OsdagQAWork/
├── OsdagBridge/                            # Official OsdagBridge application source
│   ├── src/
│   │   └── osdagbridge/
│   │       ├── cli/                        # CLI entry points
│   │       ├── core/                       # Bridge types (plate_girder), analysis, design
│   │       └── desktop/                    # PySide6 desktop application bootstrap
│   ├── pyproject.toml
│   └── README.md
│
└── OsdagBridge-Software-Testing/           # QA Testing Repository
    ├── app.py                              # Streamlit QA dashboard
    ├── run_tests.py                        # Automated Pytest runner
    ├── test_cases.csv                      # 50 documented test cases
    ├── test_results.csv                    # 50 test execution records
    ├── issues.csv                          # 7 documented defects
    ├── tests/                              # 71 automated Pytest tests
    │   ├── conftest.py                     # Dynamic source path discovery fixture
    │   ├── unit/
    │   ├── integration/
    │   ├── gui/
    │   └── regression/
    └── documentation/
```

---

## 6. Environment Variables

The test configuration detects the official OsdagBridge checkout using the following prioritized resolution logic in `tests/conftest.py`:

1. `OSDAGBRIDGE_ROOT`: Absolute path to official OsdagBridge root (e.g. `/home/runner/work/.../OsdagBridge` or `C:\Users\sobhi\Documents\OsdagQAWork\OsdagBridge`).
2. `OSDAGBRIDGE_SRC`: Absolute path to official `src/` directory.
3. **Sibling Discovery:** Automatically checks `../OsdagBridge/src` relative to the QA repository root directory.
4. **Standard User Path:** Checks `$HOME/Documents/OsdagQAWork/OsdagBridge/src`.

---

## 7. Execution Profiles

### Profile A: Local Command-Line Pytest Runner
```bash
python run_tests.py
# Runs all 71 tests, reports summary in terminal, exit code 0 on success.
```

### Profile B: HTML Test Report Generation
```bash
python -m pytest --html=reports/test_results/test_report.html --self-contained-html
# Produces standalone, self-contained HTML report with CSS and test timings.
```

### Profile C: Interactive Streamlit QA Dashboard
```bash
streamlit run app.py
# Spawns local HTTP server on port 8501 with real-time test execution and bug persistence.
```

### Profile D: GitHub Actions Multi-OS CI
Triggered on every Git `push` or `pull_request` targeting `main`. Clones both repositories, provisions Python 3.11/3.12, executes `run_tests.py`, and archives artifacts.
