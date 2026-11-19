# Software Quality Assurance & Test Strategy
## Project: OsdagBridge – Automated & Manual Testing Suite

---

### 1.0 Purpose & Strategy Overview
The testing strategy establishes a structured, multi-tier testing framework for **OsdagBridge**, ensuring compliance with Indian Standard codes (**IS 800:2007**) and Indian Roads Congress bridge design rules (**IRC:6**, **IRC:24**).

The strategy balances:
1. **Verification of the Official Application Source:** Ensuring proper package structure, imports, DTO handling, preliminary sizing, and solver pipeline integration.
2. **Structural Limit State Engineering Checks:** Validating bending capacity ($M_d$), shear resistance ($V_d$), and live load deflection ($\delta_{LL} \le L/800$).
3. **Robust Input Validation & Boundary Analysis:** Preventing improper inputs (negative values, extreme spans, corrosion limit violations) from crashing the system.
4. **Defect Lifecycle Management:** Systematically documenting reproducible defects and verifying regression fixes.

---

### 2.0 Test Levels & Categories

```
┌────────────────────────────────────────────────────────┐
│               GUI & Desktop Workflow Tests             │
│  - Application launch, bootstrap, and UI state flows   │
├────────────────────────────────────────────────────────┤
│           Integration & Pipeline Tests                 │
│  - Official DTO -> Sizing -> Analyser -> Designer flow │
├────────────────────────────────────────────────────────┤
│              Unit & Model Validation Tests             │
│  - Boundary value analysis, type safety, dataclasses   │
├────────────────────────────────────────────────────────┤
│                 Regression Tests                       │
│  - ZeroDivisionError, Unicode filepaths, impact factor │
└────────────────────────────────────────────────────────┘
```

#### 2.1 Unit Testing (`tests/unit/`)
- **Scope:** Individual functions, dataclass models, and validation routines.
- **Key Modules:** `test_validation.py`, `test_models.py`.
- **Target:** 100% path coverage for boundary limits and error handlers.

#### 2.2 Integration Testing (`tests/integration/`)
- **Scope:** Interaction between official application submodules.
- **Key Modules:** `test_official_application.py`, `test_plate_girder_pipeline.py`.
- **Target:** Verify that official `PlateGirderDTO`, `preliminary_sizing()`, `designer.design()`, and `analyser.analyse()` interoperate without failures.

#### 2.3 GUI & Workflow Testing (`tests/gui/`)
- **Scope:** Desktop bootstrap entry points, CLI command discovery, and user workflow simulations.
- **Key Modules:** `test_gui_workflow.py`.
- **Target:** Ensure GUI start functions and user input forms execute predictably.

#### 2.4 Regression Testing (`tests/regression/`)
- **Scope:** Guarding against previously fixed defects.
- **Key Modules:** `test_regression.py`.
- **Target:** Verify that zero-division bugs, input injection errors, and Unicode file export failures remain permanently mitigated.

---

### 3.0 Test Design Techniques

1. **Equivalence Partitioning (EP):**
   - Partitioning bridge spans into:
     - Invalid Lower ($< 5.0\text{ m}$)
     - Valid Plate Girder Range ($5.0\text{ m} \le L \le 60.0\text{ m}$)
     - Invalid Upper ($> 60.0\text{ m}$)
2. **Boundary Value Analysis (BVA):**
   - Minimum web thickness: $7.9\text{ mm}$ (Fail), $8.0\text{ mm}$ (Pass), $8.1\text{ mm}$ (Pass).
   - Maximum web slenderness: $d/t_w = 200.0$ threshold for stiffener requirement.
3. **Error Guessing & Negative Testing:**
   - Empty required strings, non-numeric alphanumeric inputs, corrupted JSON files, non-ASCII directory paths.

---

### 4.0 Entry & Exit Criteria

| Milestone | Entry Criteria | Exit Criteria |
| :--- | :--- | :--- |
| **Unit Testing** | Models and validator routines implemented | 100% unit tests passing with zero assertions failing |
| **Integration Testing**| Official application installed in editable mode | All official submodules discovered and pipeline chains execute |
| **System QA** | Test suite fully configured and fixtures loaded | 50 test cases executed; all critical/high severity defects resolved |
| **Deployment** | Dashboard validated against real CSV datasets | Streamlit Cloud deployment green; CI workflow passing on GitHub Actions |
