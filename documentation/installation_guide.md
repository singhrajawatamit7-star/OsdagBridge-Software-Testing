# OsdagBridge Installation & Setup Guide

This guide provides step-by-step instructions for installing the official **OsdagBridge** application, setting up the Python development environment, and configuring the **OsdagBridge QA Testing Suite**.

---

## 1. System Requirements
- **Operating System:** Windows 10/11 (64-bit), Ubuntu Linux 20.04+, or macOS 12+
- **Python Version:** Python 3.9, 3.10, 3.11, 3.12, or 3.13 (Python 3.11+ recommended)
- **Version Control:** Git 2.30+
- **Terminal:** PowerShell on Windows, or Bash on Linux/macOS

---

## 2. Directory Layout
We recommend maintaining a clean separation between the application under test and the QA test suite:

```text
OsdagQAWork/
├── OsdagBridge/                      # Official application source
│   ├── src/osdagbridge/
│   ├── tests/
│   └── pyproject.toml
│
└── OsdagBridge-Software-Testing/     # QA test suite and dashboard
    ├── tests/
    ├── app.py
    └── requirements.txt
```

---

## 3. Installing the Official OsdagBridge Application

### Step 3.1: Clone the Official Repository
```bash
cd $HOME/Documents
mkdir OsdagQAWork
cd OsdagQAWork
git clone https://github.com/osdag-admin/OsdagBridge.git
cd OsdagBridge
```

### Step 3.2: Create and Activate Virtual Environment
**On Windows (PowerShell):**
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

**On Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

### Step 3.3: Install OsdagBridge in Editable Mode
```bash
python -m pip install -e .
```
This builds and installs `osdagbridge` version 0.1.0 with its core dependencies (`numpy`, `scipy`, `pydantic`, `pyyaml`, `matplotlib`).

### Step 3.4: Verify Installation
Verify that the package can be imported:
```powershell
python -c "import osdagbridge; print(osdagbridge.__file__)"
```

Execute the official unit and integration tests:
```powershell
python -m pytest tests -v
```

---

## 4. Setting up the QA Testing Suite

### Step 4.1: Clone the QA Repository
```bash
cd $HOME/Documents/OsdagQAWork
git clone https://github.com/singhrajawatamit7-star/OsdagBridge-Software-Testing.git
cd OsdagBridge-Software-Testing
```

### Step 4.2: Install QA Dependencies
```bash
pip install -r requirements.txt
```

### Step 4.3: Set Environment Variable (Optional)
To specify an explicit path to the official OsdagBridge checkout:
```powershell
$env:OSDAGBRIDGE_ROOT = "$HOME\Documents\OsdagQAWork\OsdagBridge"
```
*(If unset, the test suite automatically looks in the standard sibling location `$HOME/Documents/OsdagQAWork/OsdagBridge`)*.

### Step 4.4: Execute QA Automated Tests
```powershell
python run_tests.py
```

### Step 4.5: Launch the Streamlit QA Dashboard
```powershell
streamlit run app.py
```
Open your browser at `http://localhost:8501`.
