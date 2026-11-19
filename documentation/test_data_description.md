# Test Data & Fixture Catalog

## 1. Overview
The OsdagBridge QA test suite uses structured fixtures stored in JSON and CSV formats to validate input handling, mathematical solvers, boundary checks, and error responses.

Test data is divided into **valid design fixtures**, **boundary & invalid input fixtures**, and **reference benchmark projects**.

---

## 2. Directory Structure

```
test_data/
├── valid_inputs/
│   ├── 16m_single_lane.json           # Single-lane rural highway bridge
│   └── 24m_plate_girder.json          # Two-lane national highway bridge (Standard)
│
├── invalid_inputs/
│   ├── negative_span.json             # Negative span values (-24.0m)
│   ├── extreme_boundary.json          # Unrealistic span (95m) & below-corrosion web (4mm)
│   └── invalid_types.json             # Alphabetic characters in numeric fields & invalid grades
│
├── sample_projects/
│   ├── nh48_expressway_bridge.json    # Complete multi-girder expressway project
│   └── reference_design_irc.json      # Hand-calculated IRC:24-2010 reference benchmark
│
├── valid_inputs.csv                   # Tabular parameters for automated parameterized tests
├── valid_inputs.json                  # Multi-case valid configurations
├── invalid_inputs.csv                 # Tabular boundary edge-cases
├── invalid_inputs.json                # Complete negative test payloads
└── reference_design_irc.json          # IRC:24 design benchmark problem
```

---

## 3. Dataset Specifications

### 3.1 Valid Inputs (`test_data/valid_inputs/`)

#### A. Standard 24m Two-Lane Highway Bridge (`24m_plate_girder.json`)
- **Use Case:** Primary baseline test fixture for IRC:24 verification and preliminary sizing.
- **Span Length:** $24.0\text{ m}$
- **Carriageway Width:** $7.5\text{ m}$ (Two lanes of IRC Class 70R / Class A loading)
- **Girders:** 3 main I-girders spaced at $2.8\text{ m}$ centers
- **Cross Girders:** Spaced at $4.0\text{ m}$ centers
- **Deck Slab Thickness:** $220\text{ mm}$ (Grade M35 Concrete)
- **Girder Section:**
  - Web Depth: $1800\text{ mm}$
  - Web Thickness: $14\text{ mm}$
  - Flange Width: $500\text{ mm}$
  - Flange Thickness: $36\text{ mm}$
- **Steel Grade:** E250 (Yield stress $f_y = 250\text{ MPa}$, $\gamma_{m0} = 1.10$)
- **Expected Outcome:** Valid input check PASS; structural checks PASS with moment utilization $\approx 0.76$ and shear utilization $\approx 0.44$.

#### B. 16m Single-Lane Rural Road Bridge (`16m_single_lane.json`)
- **Use Case:** Compact bridge configuration for single-lane IRC Class A traffic.
- **Span Length:** $16.0\text{ m}$
- **Carriageway Width:** $4.25\text{ m}$
- **Girders:** 2 main I-girders spaced at $2.6\text{ m}$ centers
- **Deck Slab Thickness:** $200\text{ mm}$ (Grade M30 Concrete)
- **Girder Section:**
  - Web Depth: $1400\text{ mm}$
  - Web Thickness: $12\text{ mm}$
  - Flange Width: $400\text{ mm}$
  - Flange Thickness: $28\text{ mm}$
- **Expected Outcome:** Valid input check PASS; all IRC:24 checks PASS.

---

### 3.2 Negative & Boundary Test Data (`test_data/invalid_inputs/`)

#### A. Negative Span Test (`negative_span.json`)
- **Fault Injected:** `span_length: -24.0`
- **Target Test:** `tests/test_inputs.py::test_negative_span_rejected`, `tests/unit/test_validation.py::test_negative_span_rejected`
- **Expected Result:** Validator raises error code `VAL_SPAN_NEGATIVE` with user-friendly message.

#### B. Extreme Boundary Test (`extreme_boundary.json`)
- **Faults Injected:**
  - `span_length: 95.0` (Exceeds practical plate girder span threshold of $60.0\text{ m}$)
  - `web_thickness: 4.0` (Violates IRC:24 statutory corrosion allowance of $t_w \ge 8.0\text{ mm}$)
  - `number_of_main_girders: 1` (Violates redundancy requirement of $\ge 2$ main girders)
- **Target Test:** `tests/test_inputs.py::test_corrosion_web_thickness_minimum_limit`
- **Expected Result:** Rejection with error codes `VAL_WEB_CORROSION_MIN` and `VAL_MIN_GIRDERS`.

#### C. Invalid Types & Non-Numeric Characters (`invalid_types.json`)
- **Faults Injected:**
  - `span_length: "twenty-four meters"`
  - `steel_grade: "ALUMINUM_6061"`
- **Target Test:** `tests/test_inputs.py::test_non_numeric_characters_rejected`, `test_unsupported_steel_grade_rejected`
- **Expected Result:** Safe type rejection without unhandled runtime crash (`TypeError` / `ValueError`).

---

### 3.3 Reference Benchmark Projects (`test_data/sample_projects/`)

#### A. Reference Design Benchmark (`reference_design_irc.json`)
- **Source:** Indian Roads Congress Standard Design Handbook (IRC:24-2010 Example 4.1).
- **Benchmark Target Values:**
  - Self-weight dead load moment: $M_{DL} = 2,480.0\text{ kNm}$
  - Live load design moment (Class 70R Wheeled + Impact): $M_{LL} = 3,120.0\text{ kNm}$
  - Total Ultimate Factored Moment: $M_{ULS} = 1.35 M_{DL} + 1.5 M_{LL} = 8,028.0\text{ kNm}$
  - Elastic Section Modulus: $Z_{el} = 3.65 \times 10^7\text{ mm}^3$
  - Plastic Moment Capacity: $M_d = \beta_b Z_p f_y / \gamma_{m0} \ge 10,500\text{ kNm}$
- **Purpose:** Enables automated regression comparison verifying that the QA solver results match recognized civil engineering calculations within $\pm 2.0\%$ numerical tolerance.
