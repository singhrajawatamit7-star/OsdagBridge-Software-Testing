# Known Limitations & Upstream Defects

## 1. Executive Summary
During the comprehensive testing cycles of the official **OsdagBridge** application (`osdag-admin/OsdagBridge`), several architectural limitations, unhandled exceptions, and stubbed modules were discovered.

This document logs these known limitations, explaining their root cause, technical impact, QA workarounds, and remediation status.

---

## 2. Upstream Architecture Limitations & Defects

### 2.1 Missing `__main__.py` in Desktop Subpackage (OB-BUG-001)
- **Impact:** Critical (P1)
- **Symptom:** Running the officially documented launch command:
  ```bash
  python -m osdagbridge.desktop
  ```
  fails with `ImportError / ModuleNotFoundError: No module named osdagbridge.desktop.__main__`.
- **Root Cause:** The `desktop` directory contains `main.py`, but lacks a `__main__.py` entry point required for Python module execution via `-m`.
- **Workaround:** Launch via `python -c "from osdagbridge.desktop.main import start; start()"`.
- **Status:** Logged in `issues.csv` as **OB-BUG-001** (Open).

---

### 2.2 Unlinked Console Stub in Desktop Entry Point (OB-BUG-002)
- **Impact:** High (P1)
- **Symptom:** Calling `osdagbridge.desktop.main.start()` prints:
  ```
  Starting desktop UI (stub)
  ```
  to the terminal and exits without instantiating a PySide6 `QApplication` or displaying the main application window.
- **Root Cause:** The desktop UI implementation is in development upstream; the GUI launcher has not yet been linked to the PyQt/PySide6 window controllers.
- **QA Strategy:** GUI testing is divided into:
  1. Desktop bootstrap integration tests (`test_gui_workflow.py`).
  2. UI state machine verification testing simulated user interactions (project creation, validation checks, results rendering).
- **Status:** Logged in `issues.csv` as **OB-BUG-002** (Open).

---

### 2.3 Preliminary Sizing Routine Returns Raw DTO String (OB-BUG-003)
- **Impact:** High (P2)
- **Symptom:** Calling `preliminary_sizing(dto)` in `osdagbridge.core.bridge_types.plate_girder` returns:
  ```python
  {"depth_m": dto.name}
  ```
  instead of computing the girder depth as a function of span length (e.g. $L/10$ to $L/15$).
- **Root Cause:** Placeholder implementation in upstream source code.
- **QA Strategy:** The QA reference engine `osdagbridge_core` provides the verified formula ($D = \text{Span} / 12$) as an independent verification benchmark.
- **Status:** Logged in `issues.csv` as **OB-BUG-003** (Open).

---

### 2.4 Missing `models.py` in `osdagbridge.core` (Upstream Bug OB-BUG-008)
- **Impact:** High (P1)
- **Symptom:** `src/osdagbridge/core/__init__.py` contains `from .models import *`, but `models.py` does not exist in the official repository repository tree, causing an unhandled `ModuleNotFoundError` on package import.
- **QA Workaround:** In `tests/conftest.py`, a dynamic module shim injects `sys.modules["osdagbridge.core.models"] = types.ModuleType("osdagbridge.core.models")` before importing submodules.
- **Status:** Guarded by test fixtures and verified across all CI runners.

---

### 2.5 Zero Web Thickness Division by Zero (OB-BUG-004)
- **Impact:** High (P1)
- **Symptom:** Entering $t_w = 0.0\text{ mm}$ caused an unhandled `ZeroDivisionError` during web slenderness evaluation ($d / t_w$).
- **Remediation:** Input validator requires $t_w \ge 8.0\text{ mm}$ (corrosion allowance limit per IRC:24).
- **Status:** Verified and guarded in `tests/regression/test_regression.py`.

---

### 2.6 Numeric Field Alphabetic Character Injection (OB-BUG-005)
- **Impact:** Medium (P2)
- **Symptom:** Rapid form input allowed string characters in numeric span inputs, raising unhandled `ValueError` on conversion.
- **Remediation:** Strict regex type validator and numeric parsing guards.
- **Status:** Verified in `tests/regression/test_regression.py`.

---

### 2.7 Silent Failure on Unicode Destination Path (OB-BUG-006)
- **Impact:** Low (P3)
- **Symptom:** PDF and HTML report generation failed silently when destination folder names contained non-ASCII or Unicode characters.
- **Remediation:** Enforced UTF-8 encoding across file output writers.
- **Status:** Verified in `tests/regression/test_regression.py`.

---

### 2.8 Statutory Impact Factor Floor for Spans > 45m (OB-BUG-007)
- **Impact:** Medium (P2)
- **Symptom:** Impact factor formula $I = 4.5 / (6.0 + L)$ evaluated below the IRC:6 minimum statutory floor of $0.10$ for very long spans.
- **Remediation:** Impact factor calculation clamps output: $I = \max(0.10, 4.5 / (6.0 + L))$.
- **Status:** Verified in `tests/regression/test_regression.py`.

---

## 3. Scope Boundaries & Assumptions

1. **Bridge Type Scope:** Current QA focus is restricted to **Plate Girder Highway Bridges**. Truss bridges, cable-stayed bridges, and composite box girders are scheduled for subsequent test phases.
2. **Headless Execution:** Because desktop UI elements are in development upstream, automated CI execution operates in headless mode without requiring an active X11/Wayland display server.
3. **Reference Engine Role:** The custom package `osdagbridge_core` serves strictly as an independent QA reference validation tool and benchmark calculator for IRC:24 / IS 800 code checks, and is not a replacement for official OsdagBridge modules.
