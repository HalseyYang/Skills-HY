---
name: tplc-safety-report
description: >-
  Generate CE MDR-compliant Safety Data Report and/or Clinical Safety Parameters
  from FDA TPLC database. Supports any FDA product code with 5-year lookback.
  Now supports INTENDED USE text as primary input — auto-detects the correct
  product code via FDA classification/TPLC/510(k) search, then generates the report.
  Trigger: "TPLC报告", "FDA TPLC", "安全数据报告", "Safety Data Report",
  "Clinical Safety Parameters", "product code + safety", or when user provides
  an FDA product code and asks for post-market safety analysis, OR when user
  provides intended use/indication text and asks for FDA product code + TPLC report.
  (agent_created: true)
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
  - WebSearch
  - Skill
  - AskUserQuestion
---

# FDA TPLC Safety Data Report Generator

## Purpose

Generate CE MDR 2017/745-compliant post-market safety documentation from FDA TPLC (Total Product Life Cycle) database data, supporting CER (Clinical Evaluation Report) and PSUR (Periodic Safety Update Report) authoring.

## Trigger Conditions

- User provides **intended use / indication text** (e.g., "continuous non-invasive monitoring of regional cerebral oxygen saturation...") → **NEW: auto-detect product code**
- User provides an **FDA product code** (e.g., MHX, FGB, MUD) and requests safety data analysis
- User provides a TPLC URL
- User says "TPLC报告", "安全数据报告", "Safety Data Report", "Clinical Safety Parameters"

## Input Parameters

**Three input modes (in order of capability):**

1. **Intended Use Text (RECOMMENDED — primary upgrade)**  
   User provides a device description / intended use string → skill extracts key terms, searches FDA databases, identifies product code(s), presents ranked candidates, generates report after confirmation.

2. **Product Code**  
   User provides product code directly → skip to Phase 1.

3. **Both**  
   User provides intended use + product code → validate consistency, then proceed.

**Required parameters:**
- **Intended Use / Indication Text** OR **Product Code** (at least one)
- **Device Name** (if known; otherwise auto-detect)

**Optional parameters:**
- **Data range**: Default = last 5 years (current year − 5 to current year)
- **Output documents**: Ask (SDR only / CSP only / both)
- **Manufacturer of interest**: Specific manufacturer to highlight
- **Project reference**: Project ID or client name for file naming

## Workflow

### Phase 0: Intended Use → Product Code Auto-Detection

> **Triggered automatically when user provides intended use text without a product code.**

**Step 0.1 — Extract Key Terms**  
Parse the intended use text and identify:
- Measurement principle / technology (e.g., NIRS, pulse oximetry, photoelectric, fiber optic, spectrophotometry)
- Body site / target tissue (e.g., cerebral, brain, tissue, peripheral, ear, finger)
- Measurand (e.g., oxygen saturation, rSO₂, SpO₂, tHb, CO₂, blood oxygen)
- Intended clinical use (e.g., continuous monitoring, non-invasive, bedside, intraoperative)

**Step 0.2 — Parallel Search**  
Execute all three searches in parallel:

- **Search A — FDA Product Classification** (highest precision):  
  WebSearch: `{key term} site:accessdata.fda.gov "cfpcd/classification.cfm"`  
  e.g., "cerebral oximeter site:accessdata.fda.gov cfpcd/classification"

- **Search B — TPLC by Key Terms** (comprehensive):  
  WebSearch: `{key term} "FDA product code" "21 CFR"`  
  e.g., "tissue saturation oximeter "FDA product code" "21 CFR 870""

- **Search C — FDA 510(k) Substantial Equivalence** (predicate-based):  
  WebSearch: `{device description} 510(k) "substantially equivalent" "product code"`  
  e.g., "regional cerebral oximetry 510(k) substantially equivalent product code"

**Step 0.3 — Compile Candidates**  
Aggregate results. For each candidate product code found:
- Verify it exists via WebFetch of `https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfTPLC/tplc.cfm?id={CODE}`
- Extract regulation number, device class, panel
- Score match confidence: HIGH (regulation + measurand + body site all match) / MEDIUM / LOW

**Step 0.4 — Present & Confirm**  
Present ranked candidates to user:
```
Found N potential product code(s) for the device:
1. [CODE] — [Device Name] — 21 CFR [XXX.XXXX] — [Panel] — Confidence: [HIGH/MEDIUM/LOW]
   Rationale: [why this matches the intended use]
2. ...
3. [Directly proceed] — Use the top-ranked code and generate reports automatically
```
- If user confirms one → proceed to Phase 1 with that code
- If user selects "proceed automatically" → use top-ranked, add note in report
- If user rejects all → ask for manual product code input

**Example — MUD device mapping:**
| Intended Use Term | Maps to | FDA Element |
|---|---|---|
| "regional cerebral tissue oxygen saturation" | rSO₂ measurement | Measurand |
| "cerebral / brain tissue" | Tissue oximetry / NIRS | Body site |
| "non-invasive monitoring" | Oximeter classification | Technology |
| "peripheral tissue oxygen saturation" | Tissue saturation | Broader scope |
| Combined | **21 CFR 870.2700 / MUD** | HIGH match |

---

### Phase 1: Data Collection

1. **Construct TPLC URL**: `https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfTPLC/tplc.cfm?id={PRODUCT_CODE}&min_report_year={START_YEAR}`
   - Product code is confirmed from Phase 0
   - START_YEAR = current year − 5

2. **Fetch TPLC Page** using WebFetch with prompt:
   ```
   Extract ALL information: product code, device name, regulation number, panel,
   classification, all MDR report counts (total reports, total events),
   all recall records (firm name, date, classification, reason),
   all device problem categories with counts,
   all patient problem categories with counts,
   all premarket submission information,
   and any temporal/yearly breakdowns available.
   Get every detail on the page.
   ```

3. **Fetch Safety Statistics** (if separate URL available):
   ```
   Extract: top device problems with MDR counts, top patient problems with counts,
   event types, outcome distributions (death/injury/malfunction),
   and any trending data or additional safety statistics.
   ```

4. **Search for Recall Details** (supplement TPLC recall summary):
   WebSearch: `FDA recall {product code} {device name} {year}` × top 3 recall firms

> **Note on recall sub-pages**: TPLC recall/MDR sub-pages may return 404. If so, use the main TPLC page summary and supplement with WebSearch for each firm/date combination. Document this limitation in Section 8 (Data Gaps).

### Phase 2: Data Analysis

1. **Aggregate and categorize** all MDR data by:
   - Patient outcome severity (death, serious injury, minor injury, malfunction only)
   - Device problem categories (alarm, software, communication, power, skin, etc.)
   - Temporal trends (yearly MDR report counts and recall counts)
   - Manufacturer distribution

2. **Identify Safety Signals** (typically 5-8):
   - Group related device problem categories into logical safety domains
   - Rank by frequency and severity
   - Link each signal to specific TPLC subsection data

3. **Extract Clinical Safety Parameters**:
   - Each safety signal → 1-2 measurable endpoints
   - Acceptance criteria from applicable IEC/ISO standards (use CURRENT versions including amendments)
   - Literature citations must be verified (PMID/DOI required)

### Phase 3: Citation Verification

**CRITICAL**: Every reference must be verified before inclusion.

1. **Standards**: Verify current edition and amendment status via WebSearch
   - Format: `IEC 60601-1:2005+AMD2:2020` (always include latest AMD)
   - For IEC standards: `IEC 80601-2-XX:YYYY+AMD1:YYYY`
   - For ISO standards: `ISO XXXXX-1:YYYY`
   - NEVER cite an outdated edition

2. **Literature**: Verify via WebSearch with PMID/DOI
   - Format: `Author (Year). Title. Journal, Volume(Issue):Pages. PMID: XXXXXXXX. DOI: XXXXXX`
   - If PMID cannot be verified, DO NOT include the reference

3. **Numerical thresholds**: Distinguish between:
   - **Standard requirement**: Explicit numerical value in a standard clause → cite standard + clause number
   - **Industry benchmark**: Consensus value from literature → cite source + "industry benchmark" or "clinical consensus"
   - **Manufacturer internal**: Do NOT present as standard requirement

### Phase 4: Document Generation

Use the **docx** skill (call `Skill` with `command: "docx"`) to generate Word documents.

#### Document A: Safety Data Report

**Format specifications** (matching step_06 reference):
```
Font: Times New Roman (Latin) + SimSun (East Asian)
Section heading: 24pt Bold, color #000000, line spacing 240
Sub-section heading: 22pt Bold, color #000000, line spacing 240
Body text: 21pt, indent 400 twips, justified, line spacing 240
Table headers: #F0F0F0 fill, 21pt Bold
Table borders: Single, 4pt, color #000000
Table layout: autofit
Page: A4 (11906 x 16838 twips), margins 1440 twips all sides
```

**Chapter structure** (numbering starts from user's section number):
1. **Safety Data Overview** — 5 numbered paragraphs covering: data scope, product code description, time period, manufacturer coverage, recall summary
2. **Safety Database Search Results** — Summary table: Database | Region | Search Strategy | Records Retrieved | Status
3. **Adverse Event Classification** — Patient outcome table: Category | MDR Reports | MDR Events | Percentage | Severity
4. **Temporal Trend Analysis** — Yearly table: Year | MDR Reports | MDR Events | YoY Change | Recalls
5. **Device Problem Analysis** — Top 14+ problem categories table: Category | Count | Percentage | Severity | Examples
6. **Detailed Narrative Analysis** — Sub-sections:
   - 6.1 Fatal Adverse Events
   - 6.2 Injury Events
   - 6.3 Device Malfunctions (group by domain: alarm, software, communication, power, etc.)
   - 6.4 Comparative Safety Assessment (by manufacturer)
   - 6.5 Recall and Field Safety Corrective Action Analysis (recall table by firm)
7. **Safety Signal Assessment** — 5-8 numbered signals, each with: description, TPLC data reference, severity assessment
8. **Data Gaps and Limitations** — Table: Gap | Impact | Mitigation (6 rows)
9. **Conclusion** — 5-6 numbered conclusions
10. **Structured Data for Document Assembly** — Table: Database | Search Type | Date | Query | Items Found | Included

#### Document B: Clinical Safety Parameters (Table 5-4 format)

**Format specifications**:
```
Same base format as Safety Data Report
Table 5-4 headers: #F0F0F0 fill (same as SDR tables)
Columns: No. | Safety objective | TPLC safety signal (data source) | Measurable endpoints | Acceptance criterion
```

**Content rules**:
- **Safety endpoints include BOTH**:
  - (a) Direct safety failures: alarm failure, skin injury, device malfunction, communication failure
  - (b) **Measurement accuracy failures that can cause patient harm** — e.g., inaccurate rSO₂/SpO₂ readings that lead to missed hypoxic events or delayed intervention. When measurement inaccuracy is a top MDR complaint category, its accuracy validation IS a safety endpoint (linked to TPLC Signal: "Inaccurate readings" — largest MDR category). Acceptance criterion: ISO 80601-2-85:2021 Clause 201.12.1.101 (Ar₂ ≤ 10.0% for cerebral oximetry) and ISO 80601-2-61:2017 Clause 201.12.1.101 (Ar₂ ≤ 3.0% for pulse oximetry).
  - (c) Diagnostic specificity / therapeutic sensitivity — exclude (these are efficacy parameters, not safety)
- Each endpoint MUST trace back to a specific TPLC safety signal with section reference and exact MDR count
- Acceptance criteria from: (a) IEC/ISO standards with current edition, (b) verified literature with PMID, (c) clearly labeled industry benchmarks
- Reference standards table after main table
- Safety Endpoint Justification subsections (5.1.1, 5.1.2, etc.)

### Phase 5: Quality Checks

Before delivering:
1. [ ] All TPLC data numbers are internally consistent (total = sum of categories)
2. [ ] All standard citations include current edition + amendment number
3. [ ] All literature citations have verified PMID or DOI
4. [ ] No clinical benefit parameters mixed into safety parameters
5. [ ] Each safety endpoint traces to specific TPLC section + data point
6. [ ] Industry benchmarks are clearly labeled, NOT presented as standard requirements
7. [ ] Year-over-year calculations are mathematically correct
8. [ ] Report language is English (unless user specifies otherwise)

## Output

### File naming convention:
- `SDR-{PRODUCT_CODE}-{YYYY-MM-DD}_Safety_Data_Report.docx`
- `CSP-{PRODUCT_CODE}-{YYYY-MM-DD}_Clinical_Safety_Parameters.docx`

### Deliver:
- Generated .docx file(s) via `deliver_attachments`
- Summary of key findings and data highlights

## Known Limitations

- FDA TPLC data covers US market only; EU vigilance data (EUDAMED) should be supplemented separately
- MDR reports are reporter-submitted and do not establish causation
- No denominator/exposure data available for incidence rate calculation
- Partial current year data (note in report)
- Product code is aggregate — cannot isolate specific models without manufacturer filtering
- **TPLC sub-pages may return 404**: Recall detail and MDR detail sub-pages (`tplcRecall.cfm`, `tplcMDR.cfm`) frequently return 404 errors. Use the main TPLC page summary and supplement with WebSearch for recall details by firm/year. Document this in Section 8 (Data Gaps).
- **Auto-detection confidence**: Phase 0 product code identification is probabilistic. Low-confidence matches (< 2 independent sources) must be confirmed with the user before proceeding. Add a "confidence level" note in the report header.
- **Multi-function devices**: When a device spans multiple product codes (e.g., a patient monitor with ECG + SpO₂ + NIRS), generate one primary report for the main product code and note secondary codes. Full coverage of all codes may require multiple reports.

## Common Product Codes

| Code | Device | Regulation | Key Intended Use Terms |
|------|--------|------------|------------------------|
| **MUD** | Oximeter, Tissue Saturation | 21 CFR 870.2700 | cerebral oxygen saturation, rSO₂, NIRS, tissue saturation, near-infrared |
| **DQA** | Oximeter (Pulse) | 21 CFR 870.2710 | pulse oximetry, SpO₂, peripheral oxygen saturation |
| MHX | Patient Monitor with Arrhythmia Detection | 21 CFR 870.1025 | multiparameter monitor, ECG, arrhythmia |
| MSX | Monitor, Physiological, Patient (general) | 21 CFR 870.1025 | bedside monitor, vital signs |
| **FGB** | Ureteroscope, Flexible | 21 CFR 876.1500 | ureteroscopy, flexible ureteroscope, urinary tract |
| **FEX** | Endoscope, Flexible | 21 CFR 876.1500 | flexible endoscope, GI tract, bronchoscope |
| KIP | Laser, Surgical | 21 CFR 878.4810 | laser, surgical, ablation |
| DPF | Dilator, Ureteral | 21 CFR 876.1600 | ureteral dilation |
| PQU | Ureteral Dilator | 21 CFR 876.1600 | ureteral dilation |
| NLE | Introducer, Catheter | 21 CFR 870.1340 | catheter introducer, vascular access |
| DTR | Implant, Breast | 21 CFR 878.3500 | breast implant |
| HIG | Electrosurgical, Cutting & Coagulation | 21 CFR 878.4400 | electrosurgical, RF ablation |
| GEI | Electrosurgical Device (General & Plastic Surgery) | 21 CFR 878.4400 | electrosurgical, coagulation |

> **Coverage Note**: This table covers common codes. For any device not listed, use Phase 0 intended use search. Update this table as new codes are discovered.

## Intended Use → Product Code Mapping Knowledge

Use this as a quick-reference to skip Phase 0.2–0.3 for well-known device types:

| Intended Use Phrase Pattern | Likely Product Code | Confidence |
|---|---|---|
| "regional cerebral tissue oxygen saturation" / "cerebral oximetry" / "NIRS" | **MUD** | HIGH |
| "tissue oxygen saturation" (peripheral, somatic) | **MUD** | HIGH |
| "pulse oxygen saturation" / "SpO₂" alone | **DQA** | HIGH |
| "pulse oximeter" (standalone finger/ear probe) | **DQA** | HIGH |
| "flexible ureteroscope" / "single-use ureteroscope" | **FGB** | HIGH |
| "multiparameter patient monitor" / "bedside monitor" (with ECG) | **MHX** | HIGH |
| "patient monitor" (general, multiparameter, no arrhythmia) | **MSX** | MEDIUM |
| "laser surgical" / "laser ablation" | **KIP** | HIGH |
| "electrosurgical" / "RF ablation" / "bipolar" | **HIG** | HIGH |
| "catheter introducer" / "vascular introducer" | **NLE** | HIGH |
| Any combination above | Highest-match code (primary) + second code (if multi-function device) | MEDIUM |

**Multi-function device rule**: If the intended use covers multiple monitoring functions (e.g., rSO₂ + SpO₂ + ECG), identify the PRIMARY product code (highest clinical risk / primary intended function) as the main report target, and note the secondary code(s) in the SDR Section 1 overview. Both codes may need separate TPLC queries for completeness.

## Prompting the Agent

When user triggers this skill, follow this decision tree:

```
User Input?
├── Has intended use text (no product code)
│   → Execute Phase 0 (auto-detect), then Phase 1–5
│   → Present ranked candidates → ask for confirmation
│   → On confirmation → proceed
│   → On "proceed automatically" → use top match
│
├── Has product code only
│   → Confirm device name via WebSearch if needed
│   → Execute Phase 1–5 directly
│
├── Has both (intended use + product code)
│   → Validate consistency (does the code match the intended use?)
│   → If yes → Phase 1–5 directly
│   → If no → flag discrepancy, ask user to confirm correct code
│
└── Neither provided
    → Ask user: "Please provide the device intended use description or FDA product code"
```

**Phase execution summary:**
1. Phase 0: Intended Use → Product Code (NEW — skip if code already provided)
2. Phase 1: Fetch TPLC data (always)
3. Phase 2: Data analysis + safety signals (always)
4. Phase 3: Citation verification (always — verify standards online)
5. Phase 4: Document generation via docx skill (always)
6. Phase 5: Quality checks + deliver
