# Defect Reporting Standards & Bug Lifecycle Guide

This document defines the defect management protocol, severity and priority criteria, and reporting template for the **OsdagBridge Quality Assurance Project**.

---

### 1.0 Defect Lifecycle

```
   [ NEW ] ───> [ OPEN ] ───> [ UNDER INVESTIGATION ]
                   │                     │
                   v                     v
              [ REJECTED ]          [ FIXED ]
                                         │
                                         v
                                    [ VERIFIED ] ───> [ CLOSED ]
```

- **Open:** Defect logged with verified steps to reproduce and environment details.
- **Under Investigation:** Defect confirmed and being analyzed against application code.
- **Fixed:** Development team or QA test harness has applied a code correction.
- **Verified:** Defect retested via automated regression test suite (`tests/regression/test_regression.py`) with passing assertions.
- **Closed:** Defect resolved and closed in final release candidate.

---

### 2.0 Severity & Priority Matrix

#### Severity Classification
- **Critical (Blocker):** Application crashes, unhandled tracebacks, import failures, or severe calculation corruption that completely blocks testing.
  - *Example:* `OB-BUG-001`: `python -m osdagbridge.desktop` crashes with `No module named osdagbridge.desktop.__main__`.
- **High:** Major structural feature fails, invalid data accepted, or arithmetic error occurs under valid boundary conditions.
  - *Example:* `OB-BUG-004`: `web_thickness = 0.0` causes unhandled `ZeroDivisionError`.
- **Medium:** Minor functional failure, non-critical formula deviation, or validation notification delay.
  - *Example:* `OB-BUG-007`: Impact factor unclamped for spans $> 45\text{ m}$.
- **Low:** Cosmetic issues, missing documentation tooltips, or minor formatting inconsistencies.
  - *Example:* `OB-BUG-006`: Unicode directory path silently fails without alerting UI.

#### Priority Classification
- **P1 (Immediate):** Resolve within 24 hours or before build release.
- **P2 (High):** Resolve in current testing sprint.
- **P3 (Medium):** Resolve in upcoming maintenance iteration.
- **P4 (Low):** Nice-to-have cosmetic refinement.

---

### 3.0 Standard Defect Report Format

Every bug report in `issues.csv` must contain:

| Field | Description |
| :--- | :--- |
| **Bug_ID** | Unique identifier formatted as `OB-BUG-XXX` |
| **Bug_Title** | Concise summary of the defect symptom |
| **Application_Version**| Software version under test (`v0.1.0`) |
| **Operating_System** | OS platform, architecture, and Python runtime |
| **Steps_to_Reproduce** | Step-by-step numbered instructions |
| **Expected_Result** | Expected behavior according to IRC/IS specification |
| **Actual_Result** | Actual observed system response |
| **Severity** | Critical / High / Medium / Low |
| **Priority** | P1 / P2 / P3 / P4 |
| **Evidence_File** | Path to screenshot (`.svg`), log file, or test trace |
| **Status** | Open / Under Investigation / Fixed / Verified / Closed |
