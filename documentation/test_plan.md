# MASTER SOFTWARE TEST PLAN (IEEE 829 COMPLIANT)
## Project: OsdagBridge – Automated & Manual QA Suite
**Document Reference:** OB-QA-STP-001  
**Version:** 1.0.0  
**Author:** QA Engineering Intern  
**Date:** November 2026  
**Status:** Approved / Deployment Ready  

---

### 1.0 Introduction & Objectives
OsdagBridge is an open-source Python-based bridge analysis and design software package developed under the Osdag initiative (IIT Bombay). The software specializes in Plate Girder Bridge systems, implementing structural design procedures compliant with Indian Standards (IS 800:2007) and Indian Roads Congress bridge specifications (IRC:6, IRC:24).

The primary objective of this Software Testing and Quality Assurance project is to:
1. Validate system stability, input validation resilience, and mathematical calculation accuracy.
2. Establish a comprehensive test suite combining Manual Testing and Pytest-based Automated Testing.
3. Detect, isolate, and professionally document software defects with clear reproduction steps and severity ratings.
4. Provide a continuous verification pipeline and interactive Streamlit QA Dashboard ready for deployment.

---

### 2.0 Scope of Testing

#### 2.1 In-Scope
- **Input Validation & Boundary Testing:** Verification of numeric boundaries (span length, carriageway width, web depth, thickness, girder spacing) and edge cases (negative values, zero division, non-numeric strings).
- **Structural Design Engine:** Verification of dead load distribution, IRC Class 70R & Class A live load bending moments, section modulus ($Z_e, Z_p$), moment capacity ($M_d$), shear capacity ($V_d$), and live load deflection limits ($\delta \le L/800$).
- **Project Lifecycle:** Creation, serialization to JSON, file integrity, corrupted file handling, and recalculation on modification.
- **Reporting & Export:** Generation of Markdown, HTML, and CSV calculation sheets containing clause references and pass/fail criteria.
- **User Interface & Visual Feedback:** Layout integrity, error alert banners, and 3D CAD visualization state.

#### 2.2 Out-of-Scope
- Non-plate-girder bridge types (e.g. cable-stayed, suspension, arch bridges not currently supported by OsdagBridge).
- Modification of core third-party C/C++ finite element solvers.
- Commercial stress testing of server infrastructure (OsdagBridge is a desktop and client-side design package).

---

### 3.0 Test Strategy & Methodology

The testing strategy follows a multi-tier V-Model and Agile QA methodology:

```
[ Requirements / IRC Specs ] <-------------> [ Acceptance / System QA Dashboard ]
       \                                                /
  [ Design / Geometry Models ] <------------> [ Integration / Workflow Tests ]
         \                                          /
    [ Modules / Solvers ] <--------------> [ Unit / Pytest Automated Tests ]
```

1. **Equivalence Partitioning & Boundary Value Analysis (BVA):** Applied to span lengths ($5.0\text{m} \le L \le 60.0\text{m}$) and web thicknesses ($t_w \ge 8.0\text{mm}$).
2. **Negative & Error Guessing Testing:** Ingestion of malicious, blank, and corrupt payloads to verify that the application handles errors gracefully without crashing.
3. **Reference Calculation Cross-Validation:** Comparing automated test output against published worked examples in IRC:24-2010.
4. **Continuous Integration (CI):** Running tests on every commit via GitHub Actions across Python 3.11, 3.12, and 3.13.

---

### 4.0 Pass / Fail Criteria

| Level | Criteria |
| :--- | :--- |
| **Pass** | Feature functions exactly per specification; all checks pass; zero unhandled exceptions; output matches reference within 1.0% tolerance. |
| **Fail** | Calculation exceeds tolerance; invalid input accepted without error; crash or unhandled exception encountered. |
| **Blocked** | Precondition failed or prerequisite module crashed, preventing further testing. |

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
- **Python Version:** 3.11+
- **Test Framework:** Pytest >= 8.0, Pytest-cov, Pytest-html
- **Presentation Layer:** Streamlit >= 1.38, Pandas >= 2.0
- **CI/CD:** GitHub Actions Matrix Runner
