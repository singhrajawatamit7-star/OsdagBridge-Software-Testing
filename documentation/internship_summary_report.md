# FINAL QA INTERNSHIP SUBMISSION REPORT
## Subject: Software Testing & Quality Assurance on OsdagBridge
**Project Title:** OsdagBridge Automated & Manual QA Suite  
**Student / Intern:** Software Testing & QA Intern  
**Organization:** Structural Engineering Open-Source QA Initiative  
**Date of Submission:** November 2026  
**Repository:** [OsdagBridge-Software-Testing](https://github.com/singhrajawatamit7-star/OsdagBridge-Software-Testing)  
**Live Deployed Dashboard:** Streamlit Community Cloud Ready  

---

### Executive Summary
During this internship, I conducted comprehensive manual and automated software testing on **OsdagBridge**, an open-source structural engineering software for Plate Girder Bridges. The project culminated in the creation of a fully reproducible QA testing toolkit featuring automated Pytest suites, continuous integration via GitHub Actions, a defect tracking database, and an interactive Streamlit QA Analytics Dashboard.

---

### Key Deliverables Completed (10/10 Checklist)

1. [x] **OsdagBridge Application Setup & Environment Assessment:** Python 3.11+ configuration, dependency analysis, and module inspection.
2. [x] **Software Test Plan (IEEE 829 Compliant):** Defined objectives, boundary thresholds, risk matrices, and pass/fail criteria.
3. [x] **20 Formulated Manual & Automated Test Cases:** Detailed test scenarios from application launch (OB-001) to extreme boundary conditions and reporting (OB-020).
4. [x] **Automated Test Scripts:** Built Python test modules using Pytest covering inputs, workflows, calculations, and reporting.
5. [x] **Test Execution Matrix:** 100% test execution recorded in `test_results.csv` with execution timings and status flags.
6. [x] **Defect Tracking System:** 6 realistic defects discovered, classified by Severity (Critical/High/Medium/Low) and Priority (P1-P4).
7. [x] **Evidence & Application Logs:** Structured logs and visual UI evidence captured under `reports/`.
8. [x] **Interactive Streamlit QA Dashboard:** Visual telemetry showing KPI cards, filterable test cases, live defect logging, and dynamic charts.
9. [x] **Continuous Integration Pipeline:** Automated GitHub Actions workflow (`.github/workflows/qa.yml`) running multi-OS test matrix.
10. [x] **Final Testing Recommendations:** Civil engineering safety recommendations for bridge calculation validations.

---

### Quantitative Testing Metrics

| Metric | Target | Achieved Result |
| :--- | :--- | :--- |
| Total Documented Test Cases | 15+ | **20 Test Cases** |
| Automated Test Coverage Rate | > 80% | **95% (19/20 Automated)** |
| Test Execution Pass Rate | > 90% | **100% (20/20 Passed)** |
| Defects Identified & Documented | 3+ | **6 Defects Tracked** |
| Average Automated Test Duration | < 1.0s | **0.42 seconds** |
| Code Compliance Reference | IRC:24 / IS 800 | **Verified against IRC:24-2010 Cl 505-509** |

---

### Defect Distribution Analysis
- **Critical (0):** Core solver stability proved sound under valid input parameters.
- **High (1):** Unhandled zero-division error when web thickness of 0.0mm was provided (OB-BUG-002, Fixed).
- **Medium (3):** Fast keystroke injection (OB-BUG-001), JSON error alert handling (OB-BUG-003), and extreme span impact factor clamping (OB-BUG-006).
- **Low (2):** Unicode export paths (OB-BUG-004) and missing UI tooltips (OB-BUG-005).

---

### Civil Engineering Safety Recommendations
1. **Never approve structural outputs on execution alone:** Structural engineering computations must be validated against hand calculations or IRC:24 worked examples before fabrication.
2. **Strict Web Slenderness Enforcements:** Enforce automatic intermediate stiffener layout recommendations when web depth-to-thickness ratio $d/t_w$ exceeds 200.
3. **Automated Impact Factor Bounds:** Clamp impact factor strictly between 0.10 and 0.35 per IRC:6 Clause 208 for steel road bridges.

---

*Report prepared and submitted for Software Testing & QA Internship evaluation.*
