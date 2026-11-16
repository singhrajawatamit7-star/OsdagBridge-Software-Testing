# OSDAGBRIDGE DEFECT REPORT TEMPLATE

## Defect Summary
- **Bug ID:** `OB-BUG-XXX`
- **Date Reported:** YYYY-MM-DD
- **Reported By:** [Your Name / QA Intern]
- **Module Affected:** [Basic Inputs | Input Validation | Design Engine | Project Lifecycle | Report Generation | UI & CAD]
- **Severity:** [Critical | High | Medium | Low]
- **Priority:** [P1 (Urgent) | P2 (High) | P3 (Normal) | P4 (Low)]
- **Status:** [New | Open | Under Investigation | Fixed | Retested | Closed]

---

## Environment Details
- **OS:** Windows 11 64-bit / Linux Ubuntu 22.04
- **Python Version:** 3.11.x / 3.12.x / 3.13.x
- **OsdagBridge Build/Commit:** v1.0.0 (main branch)
- **Dependencies:** PySide6, NumPy, Pandas, Pytest

---

## Description
[Provide a clear and concise description of what the bug is.]

---

## Steps to Reproduce
1. Launch OsdagBridge desktop application (`python -m osdagbridge.desktop`).
2. Navigate to `[Menu / Form Name]`.
3. Input the following values: `[Field Name = Value]`.
4. Click `[Action Button / Run Design]`.
5. Observe the system response.

---

## Expected Result
[State what the application should have done according to the engineering requirements and IRC:24 / IS 800 specifications.]

---

## Actual Result
[State what the application actually did, including any error dialogues, unresponsive states, or unhandled tracebacks.]

---

## Evidence & Logs
- **Screenshot / Screen Recording:** `reports/screenshots/filename.svg`
- **Application Log Extract:**
```text
[PASTE RELEVANT TRACEBACK OR LOG EXTRACT HERE]
```

---

## Suggested Fix / Developer Notes
[Provide any insights from code inspection or structural engineering logic to assist the development team.]
