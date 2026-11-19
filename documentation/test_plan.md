# MASTER SOFTWARE TEST PLAN (IEEE 829 COMPLIANT)
## Project: OsdagBridge – Automated & Manual QA Suite
**Document Reference:** OB-QA-STP-001  
**Version:** 2.0.0  
**Author:** QA Engineering Intern  
**Date:** November 2026  
**Status:** Approved / Deployment Ready  

---

### 1.0 Introduction & Objectives
OsdagBridge is an open-source Python-based bridge analysis and design software package developed under the Osdag initiative (IIT Bombay). The software specializes in Plate Girder Bridge systems, implementing structural design procedures compliant with Indian Standards (**IS 800:2007**) and Indian Roads Congress bridge specifications (**IRC:6**, **IRC:24**).

The primary objective of this Software Testing and Quality Assurance project is to:
1. Verify the official OsdagBridge application source (`osdag-admin/OsdagBridge`), its modules, DTO structures, and execution pipelines.
2. Establish a comprehensive suite of **50 documented test cases** combining Pytest automated testing and workflow verifications.
3. Detect, isolate, and professionally document software defects with clear reproduction steps, severity, and priority ratings in `issues.csv`.
4. Provide a continuous verification pipeline and interactive Streamlit QA Dashboard ready for deployment.

---

### 2.0 Scope of Testing

#### 2.1 In-Scope
- **Official Package Structure & Discovery:** Verification of `osdagbridge`, `osdagbridge.core`, and submodules (`bridge_types`, `bridge_components`, `loads`, `solvers`, `reports`, `cli`, `desktop`).
- **Input Validation & Boundary Testing:** Verification of numeric boundaries (span length, carriageway width, web depth, thickness, girder spacing) and edge cases (negative values, zero division, non-numeric strings).
- **Structural Design Engine:** Verification of dead load distribution, IRC Class 70R & Class A live load bending moments, section modulus ($Z_e, Z_p$), moment capacity ($M_d$), shear capacity ($V_d$), and live load deflection limits ($\delta_{LL} \le L/800$).
- **Project Lifecycle:** Creation, serialization to JSON, file integrity, corrupted file handling, and recalculation on modification.
- **Reporting & Export:** Generation of Markdown, HTML, and CSV calculation sheets containing clause references and pass/fail criteria.
- **GUI & Desktop Workflows:** Bootstrap launch points, CLI options, and UI error states.

#### 2.2 Out-of-Scope
- Non-plate-girder bridge types (e.g. cable-stayed, suspension, arch bridges not currently supported).
- Third-party C/C++ finite element binary solvers (OpenSees binaries).
- Stress testing of multi-tenant server infrastructure (desktop/client-side focus).

---

### 3.0 Test Case Target Breakdown (50 Cases)

| Category | Cases | Primary Focus |
| :--- | :---: | :--- |
| **1. Installation and Launch** | 5 | Python compatibility, editable pip install, module discovery, CLI launcher, desktop bootstrap |
| **2. Project Creation & Management** | 5 | DTO instantiation, parameter modification, JSON serialization/deserialization, corrupted file handling |
| **3. Input Validation** | 10 | Valid spans, empty fields, negative inputs, boundaries [5m-60m], corrosion thickness [8mm], alpha strings |
| **4. Bridge Design Execution** | 8 | Preliminary sizing, analyser, designer, dead load, live load Class 70R, moment capacity, shear capacity |
| **5. Results and Visualization** | 7 | Deflection check ($L/800$), extreme span failure, E250 vs E350 yield scaling, 3D CAD canvas, summary cards |
| **6. Report Generation** | 5 | Markdown calculations, printable HTML, compliance table, CSV export, Unicode directory writing |
| **7. Error Handling** | 5 | Missing girder block, single girder error, slenderness warning ($d/t_w > 200$), corrupted input handling |
| **8. Regression Testing** | 5 | Fast typing alpha injection (OB-BUG-005), zero web thickness (OB-BUG-004), Unicode export (OB-BUG-006), impact factor (OB-BUG-007) |
| **Total** | **50** | Full QA verification matrix |

---

### 4.0 Pass / Fail Criteria

| Level | Criteria |
| :--- | :--- |
| **Pass** | Feature functions exactly per specification; all checks pass; zero unhandled exceptions; output matches reference within 1.0% tolerance. |
| **Fail** | Calculation exceeds tolerance; invalid input accepted without error; crash or unhandled exception encountered. |
| **Blocked / Skipped** | Precondition failed or external dependency unavailable, preventing test execution. |

---

### 5.0 Defect Severity & Priority Classification

| Severity | Definition | Target Resolution |
| :--- | :--- | :--- |
| **Critical** | Application crash, unhandled traceback, data loss, or catastrophically incorrect structural calculation. | Within 24 hours |
| **High** | Core design feature fails or produces invalid results under standard valid inputs. | Within 3 days |
| **Medium** | Edge-case input accepted; cosmetic validation timing issue; minor formula deviation. | Next sprint |
| **Low** | Minor UI misalignment, missing tooltip, or documentation typo. | As scheduled |

---

### 6.0 Environmental Setup
- **Operating Systems:** Windows 11 / Windows 10 / Ubuntu Linux
- **Python Version:** 3.9+ (Python 3.11+ recommended)
- **Official Package:** `osdagbridge` 0.1.0 (cloned from `github.com/osdag-admin/OsdagBridge`)
- **Testing Framework:** Pytest >= 8.0, Pytest-cov, Pytest-html
- **Presentation Layer:** Streamlit >= 1.38, Pandas >= 2.0
- **CI/CD:** GitHub Actions Matrix Runner
