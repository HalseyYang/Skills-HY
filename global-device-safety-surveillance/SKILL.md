---
name: global-device-safety-surveillance
description: >-
  Autonomously investigate public post-market safety information for a medical device.
  Accepts a product name, model, manufacturer, intended use, IFU/product description, UDI,
  FDA product code, 510(k)/PMA/De Novo number, or a combination of these. Resolves device
  identity first, then searches official public adverse-event, recall, FSCA/FSN and safety-alert
  sources in the United States, European jurisdictions and selected other markets. Separates
  exact-device, product-family and device-class evidence; keeps an auditable search log;
  de-duplicates records; and produces a source-backed safety surveillance summary suitable
  for CER/PMS/PSUR/risk-management support. Never reuses project-specific data from prior runs.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
  - WebSearch
  - Skill
---

# Global Medical Device Safety Surveillance v2.1

## 1. Objective

Given a medical device or product description, independently identify the device and retrieve relevant public post-market safety information from official sources. The default deliverable is a final, decision-ready safety surveillance summary with a reproducible search trail. The workflow must work even when the user does not know the FDA product code, UDI, EMDN/GMDN code, or marketing authorization number.

This skill is for public regulatory intelligence and post-market safety evidence gathering. It does not replace the manufacturer's complaint database, PMS system, competent-authority correspondence, or non-public vigilance data.

## 2. Non-negotiable rules

1. **Identity before retrieval.** Do not search safety databases until a working Product Identity Object has been created.
2. **Official sources first.** Prefer regulator databases/APIs and regulator-hosted notices. Use general web search only for discovery or when an official source has no structured query interface.
3. **Keep evidence scopes separate.** Every record must be tagged `exact_device`, `product_family`, or `device_class`. Never merge these scopes into one unexplained total.
4. **Do not infer incidence from spontaneous reports.** MAUDE/TPLC/DAEN/MDI report counts do not provide an exposure denominator. Do not calculate adverse-event rates or compare safety rates between manufacturers/products unless a valid denominator is independently available.
5. **Do not equate problem-code counts with report counts.** A single report may contain multiple device/patient problem codes. Multi-label problem counts are descriptive distributions, not unique MDR totals.
6. **Do not infer causality from a report.** Use regulator caveats and neutral wording such as “reported in association with” or “the report describes.”
7. **Absence of public records is not evidence of absence.** State “no relevant public record identified within the searched sources and search window,” never “no adverse events.”
8. **No automatic benefit-risk conclusion.** Public surveillance evidence alone cannot establish that a device is safe, unsafe, or that benefit-risk is acceptable. Summarize signals and their evidentiary strength; leave final benefit-risk integration to the full evidence set.
9. **No fabricated standards thresholds.** If a numerical acceptance criterion is not verified in an accessible authoritative clause or source, label it `unverified` or omit it. Do not convert engineering preferences into IEC/ISO requirements.
10. **No project-memory contamination.** Never reuse device names, manufacturers, counts, predicates, equivalents, dates, conclusions, local paths, client names, or thresholds from a prior project unless supplied in the current task and required for the current output.
11. **Public-source boundary must be explicit.** For the EU, do not claim that EUDAMED provides a public EU-wide vigilance incident database when the Vigilance/PMS module is not publicly operational. Use Member State safety notices/FSCAs and clearly state the limitation.
12. **Every material number must be traceable.** Record source, query, date accessed, date range, raw count, de-duplication rule, and final included count.

## 2A. Source authority hierarchy

Assign every source an authority tier and use the tier in both interpretation and the audit log.

- **Tier A — regulator/competent authority:** FDA, European Commission/EUDAMED, national competent authorities, TGA, Health Canada, Swissmedic, MHRA and equivalent official regulator sources. These may directly support regulatory factual conclusions within their stated scope.
- **Tier B — official conformity/manufacturer source:** notified-body official certificate source and manufacturer official website. Use for product identity, certificate or product-family corroboration; do not let manufacturer claims override regulator records.
- **Tier C — trusted secondary database:** use for discovery or cross-checking. Material regulatory conclusions must be traced back to Tier A/B whenever possible.
- **Tier D — distributor, commercial aggregator, social platform, document mirror or uncited repost:** discovery only. Never use alone to establish clearance, approval, recall status, adverse-event absence or a regulatory conclusion.

If a Tier C/D result is the only available lead, label it as unverified secondary evidence and state what authoritative verification remains outstanding.

## 3. Inputs

Accept any of the following, individually or in combination:

- product/device name;
- manufacturer;
- brand/trade name;
- model/catalogue number;
- intended use / indication;
- device description / IFU / brochure;
- FDA product code / regulation number;
- 510(k), PMA, De Novo, HDE number;
- UDI-DI / GUDID identifier;
- Basic UDI-DI / EMDN / GMDN term;
- jurisdiction(s) and date range if the user specifies them.

Default date window: **the most recent 5 complete years plus current year-to-date**, reported explicitly as exact dates. Do not describe `current year - 5 through current year` as exactly five years without defining the window.

Default jurisdiction coverage:

- United States: dynamically resolve the current FDA public adverse-event infrastructure at runtime (AEMS when publicly queryable for the needed data; otherwise current MAUDE/openFDA and/or FDA MDR downloadable data as applicable), plus FDA Device Recall, TPLC cross-check, and FDA safety communications/recall notices. Never hard-code one adverse-event backend as permanently primary.
- European Union: EUDAMED for available device/actor identity where useful; Member State competent-authority FSN/FSCA/safety-notice sources. Do not present this as a complete EU incident dataset.
- Optional cross-check markets when useful: Australia TGA DAEN/DRAC, Health Canada Medical Device Incidents/Recalls, Switzerland Swissmedic FSCA; UK safety notices if relevant.

If the user asks for “global,” use all default and optional sources that are publicly accessible and relevant.

## 4. Phase A — Product identity resolution

### A1. Parse current-task information

Build `ProductIdentity` using `schemas/product_identity.schema.json`. Extract only information present in the current task or newly verified from public sources:

- generic device name;
- brand/trade name(s);
- manufacturer and aliases;
- model/catalogue numbers;
- intended use / indication;
- technology / mechanism;
- anatomical site and patient population;
- FDA product code(s), regulation number, class, review panel;
- 510(k)/PMA/De Novo/HDE numbers;
- UDI-DI / GUDID identifiers;
- EMDN/GMDN terms/codes if verified;
- EU identifiers if publicly available.

### A2. Resolve U.S. identity

Use official FDA/openFDA sources in this order when applicable:

1. Device Classification database / openFDA device classification.
2. 510(k), PMA, De Novo/HDE records as applicable.
3. GUDID/openFDA UDI for brand/model/DI cross-check.
4. Registration & Listing only as a supporting identity source; do not treat listing as FDA clearance/approval.

Generate multiple candidate product codes when the device is multi-function or ambiguous. Score each candidate on documented match dimensions:

- intended use match;
- technology match;
- anatomical/site match;
- device description match;
- cleared/approved comparator match;
- exact model/UDI linkage if available.

Use `high`, `medium`, or `low` confidence with a written rationale. Do not force a single code when evidence supports multiple codes.

### A3. Resolve EU/global identity

Use EUDAMED's currently available public modules only for functions that are actually available. Where EUDAMED does not expose the needed data, use manufacturer/public certificate/competent-authority sources and mark the identity element `not publicly verified`.

For Australia, Canada, Switzerland or other markets, map available product names, manufacturers, licence/ARTG/GMDN identifiers only when necessary for retrieval.

### A4. Automatic continuation rule

If one identity is high-confidence, proceed automatically. If identity remains ambiguous, do not fabricate. Run safety searches across the plausible candidates and keep results separated. Ask the user only when the ambiguity would materially change the answer and cannot be resolved from public sources.

## 5. Phase B — Search-plan generation

Create a query set before retrieval. At minimum include:

### Exact-device queries
- exact manufacturer + exact brand;
- exact manufacturer + model;
- exact brand + model;
- UDI-DI if available;
- 510(k)/PMA/De Novo number if linked to the device.

### Product-family queries
- manufacturer + family name;
- manufacturer aliases + family synonyms;
- previous/current brand names when documented.

### Device-class queries
- FDA product code;
- verified generic device name;
- EMDN/GMDN term where useful;
- technology + intended-use synonym combinations.

Store the query plan in the audit log before interpreting results.

### B1. Zero-hit protocol

A zero-hit conclusion is valid only when the relevant official source was successfully queried and at least two materially different identity strategies were executed. For exact-device searches, use as applicable:

1. manufacturer + exact model;
2. brand + exact model;
3. manufacturer alias + model/family;
4. UDI-DI;
5. linked 510(k)/PMA/De Novo number;
6. exact generic name + manufacturer.

Use `zero_hit` only after the source returned zero relevant records from a completed search. Use `access_limited` when the official database/interface/API could not be queried completely. Required wording for a valid exact-device zero hit:

> No relevant exact-device records were identified in the public sources and query combinations executed as of [date].

Never shorten this to “no adverse events” or “no recalls.”

## 6. Phase C — United States retrieval

### C1. FDA adverse-event source resolver — runtime decision required

Before querying U.S. adverse-event data, verify the current FDA public infrastructure and record the resolution decision. FDA is transitioning medical-device adverse-event data from MAUDE toward AEMS in 2026; therefore the skill must not permanently bind itself to MAUDE/openFDA.

Resolution order:

1. Check current FDA documentation for AEMS/MAUDE/MDR public-data status on the search date.
2. If AEMS exposes a public query path suitable for the required device-level search, use AEMS as the current primary event source.
3. Otherwise use the current MAUDE public query, openFDA Device Event endpoint, and/or FDA MDR downloadable data that can support the requested query.
4. If the desired primary event source cannot be queried, mark the search `access_limited`; do not silently substitute a web-index search and call it complete.
5. Record `source_system`, `system_status_verified_at`, query method, coverage period, update status, and any fallback used.

When openFDA Device Event is the resolved machine-readable route, the following fields are useful.

Important searchable identity fields include:

- `device.device_report_product_code`;
- `device.brand_name`;
- `device.generic_name`;
- `device.model_number`;
- `device.catalog_number`;
- `device.udi_di`;
- `device.manufacturer_d_name`;
- `date_received`;
- `event_type`;
- `mdr_report_key`;
- `report_number`;
- `event_key`;
- `product_problems`.

Use exact-device queries first, then product-family and device-class queries. Apply the explicit date range to every count/query where the endpoint supports it.

Retrieve or count, as applicable:

- unique reports;
- event-type distribution (`Death`, `Injury`, `Malfunction`, `Other`, etc. as returned by the source);
- temporal distribution by year;
- device problem terms;
- patient problem/outcome terms when available;
- manufacturer/model fields for relevance validation;
- narratives only for a targeted subset of high-severity or representative records, not for bulk unsupported causal inference.

### C2. FDA Device Recall — primary U.S. recall source

Use the openFDA Device Recall endpoint and/or FDA recall records. Search by combinations of:

- `product_code`;
- `k_numbers` / `pma_numbers`;
- `recalling_firm`;
- `product_description`;
- model/brand terms;
- date range.

Capture recall identifier, classification, status, initiation/posting dates, reason, root-cause description when present, affected product/model information, quantity/distribution when useful, and source URL.

### C3. FDA TPLC — cross-check and device-class overview

Use TPLC to validate procode-level premarket/postmarket context and to cross-check aggregate counts. Treat TPLC as **device-class/procode level**, not a brand/model database.

Do not require device-problem category totals to equal MDR-report totals. Record the TPLC disclaimer that reports can contain multiple problem codes and one or more events.

### C4. FDA safety communications / notices

Search official FDA pages for exact brand/model/manufacturer plus terms such as `safety communication`, `recall`, `letter`, `warning`, `correction`, and relevant device terminology. Do not substitute web-search hit counts for database record counts.

## 7. Phase D — European retrieval

### D1. EUDAMED boundary

Use EUDAMED for available public identity, UDI/device, actor, certificate or market-surveillance information as applicable. Before every run, verify the current EUDAMED module status from the European Commission.

If the Vigilance/PMS module is not publicly available, state explicitly:

> A complete EU-wide public incident-level vigilance dataset was not available through EUDAMED at the search date. EU public safety retrieval therefore relied on available competent-authority safety notices, FSCAs/FSNs and other public market-surveillance information.

Never translate “no EUDAMED vigilance search result” into “no EU adverse events.”

### D2. Member State competent-authority safety sources

Search official Member State sources using exact-device and product-family queries. Priority sources include, where accessible and relevant:

- Germany — BfArM medical-device safety information / FSNs;
- Spain — AEMPS medical-device safety notices and informative actions;
- France — ANSM medical-device safety/recall information;
- additional competent-authority sources where the product's market presence or results justify expansion.

For each notice capture:

- authority;
- publication date;
- manufacturer;
- affected brand/model/catalogue/lot if stated;
- FSCA/FSN or notice identifier;
- safety issue;
- clinical consequence/hazard as stated;
- corrective action;
- manufacturer reference number if available;
- source URL/document.

### D3. Cross-authority de-duplication

One manufacturer FSCA may be published by several national authorities. Collapse duplicate publications to one `unique_fsca` when manufacturer reference, affected product, issue and dates substantively match. Preserve all authority source URLs under the same record.

## 8. Phase E — Optional cross-check jurisdictions

Use these when the user asks for global coverage, when the device is marketed there, or when they materially strengthen the safety landscape.

### Australia
- TGA DAEN medical devices: public suspected adverse-event reports; search by trade name, sponsor/manufacturer, GMDN term or ARTG number where supported.
- TGA DRAC / regulator recall and product-correction sources.

### Canada
- Health Canada Medical Device Incidents database when accessible.
- Health Canada Recalls and Safety Alerts database/open data for medical-device recalls and safety alerts.

### Switzerland
- Swissmedic FSCA/FSN list; treat Switzerland separately from EU data.

### United Kingdom
- Use MHRA public safety alerts/field-safety information where relevant; treat UK data separately from EU data.

Apply each regulator's own data-limitations statement. Do not pool report counts across countries as if reporting systems were equivalent.

## 9. Phase F — Normalization and relevance classification

Normalize every included item to `schemas/safety_record.schema.json`.

Required relevance levels:

- **exact_device** — exact model, UDI, catalogue number, or sufficiently specific brand/model/manufacturer combination.
- **product_family** — same manufacturer and documented family/platform, but not an exact model match.
- **device_class** — generic device class/product-code/EMDN/GMDN evidence without model-level linkage.

If a record cannot be linked with reasonable confidence, mark `excluded` and log the exclusion reason. Do not silently include keyword-only false positives.

## 10. Phase G — De-duplication and counting

### U.S. adverse-event records

Maintain raw records and a deduplicated analytical view. Use available identifiers such as `mdr_report_key`, `report_number`, `event_key`, device sequence, and report-version/supplement information. Do not assume all rows returned by a broad query are unique clinical events.

Report at least:

- raw retrieved records;
- excluded non-relevant records;
- duplicate/supplemental records collapsed where justified;
- final unique analytical records.

### Problem-code counting

Device/patient problem terms are multi-label. Report them as “problem-code mentions” or “reports containing the problem term” according to the source/query method. Never label the sum of multi-label problem terms as unique MDR count.

### Recall/FSCA records

De-duplicate on stable regulator identifiers first. For cross-jurisdiction FSCAs, use manufacturer reference + affected product + issue + approximate date. Keep jurisdiction-specific publications as source instances linked to one unique global record.

## 11. Phase H — Analysis

Analyze only what the retrieved data support.

### Required analyses

1. identity and scope;
2. source coverage and search dates;
3. exact-device findings;
4. product-family findings;
5. device-class context;
6. adverse-event type distribution where valid;
7. device/patient problem term distribution with multi-label caveat;
8. recall/FSCA root causes and corrective actions;
9. time trend in **report counts**, clearly distinguished from incidence;
10. high-severity record review;
11. cross-source convergence/divergence;
12. data gaps and retrieval limitations.

### Safety-signal assessment

Use qualitative evidence dimensions rather than unsupported incidence estimates:

- severity;
- recurrence/repetition;
- recency;
- exact-device relevance;
- cross-source concordance;
- plausible device-related failure mode as described in source records;
- whether the issue led to recall/FSCA/corrective action.

Allowed signal labels:

- `established/publicly documented issue`;
- `recurrent reported issue`;
- `potential signal requiring further assessment`;
- `isolated report`;
- `insufficient public evidence`.

Each label must include the supporting records and limitations. Do not claim causality or comparative safety from report counts alone.

## 12. Clinical safety parameter boundary

This skill may identify **candidate safety domains/endpoints** from the post-market evidence. It must not automatically invent quantitative acceptance criteria.

For each candidate endpoint, optionally record:

- endpoint;
- rationale from surveillance data;
- candidate standard/guidance/literature source;
- `verification_status`: `verified_clause`, `source_verified_threshold_not_confirmed`, or `unverified`.

Only a `verified_clause` may be presented as an explicit normative numerical requirement, and the exact standard edition/amendment and clause must be verified.

## 12A. Input-document consistency check

When the user supplies an IFU, brochure, label, product description or technical document, run a separate consistency scan. This is not a substitute for a full regulatory document review; it is a contamination/template-residue check that looks for obvious unrelated content that could corrupt product identity or safety interpretation.

At minimum check for:

- unrelated product/model names;
- another device type (for example, ventilator text in a patient-monitor IFU);
- human/veterinary population mismatch;
- prior model numbers in EMC, labeling, accessories or software sections;
- inconsistent manufacturer/authorized-representative names;
- obsolete regulatory references that materially conflict with the current document;
- copied thresholds, warnings or intended-user requirements that belong to another product.

Report findings under `Input Document Consistency Findings` with page/line evidence. Do not silently edit or correct the customer's source document unless explicitly asked.

## 12B. Completion gate and deliverable modes

A **full surveillance run** cannot be marked final until all applicable completion-gate items are either completed or explicitly recorded as `access_limited`/`not_applicable` with rationale:

1. Product Identity resolved and confidence stated.
2. U.S. classification/identifier check completed when relevant.
3. Exact-device search completed across the agreed jurisdictions.
4. Product-family search completed where a family can be established.
5. Device-class context search completed.
6. U.S. adverse-event source resolver executed and its current system status documented.
7. U.S. recall/TPLC or equivalent class context completed where applicable.
8. EU identity/public-module status checked and national safety-notice/FSCA searches executed for agreed priority authorities.
9. Optional global jurisdictions executed when the user requests global coverage.
10. De-duplication and relevance classification completed.
11. Signal assessment completed.
12. Search audit trail complete.
13. Input-document consistency check completed when source documents were supplied.
14. Three QA passes completed.

Deliverable modes:

- **Quick Check:** concise chat answer; file optional unless requested.
- **Standard Surveillance:** formal DOCX report is mandatory.
- **Full Audit Surveillance:** formal DOCX report + XLSX audit workbook are mandatory.

If the user asks to “run the skill,” “global surveillance,” “formal surveillance,” or supplies a product for a full search without limiting the output, default to **Full Audit Surveillance**. The chat response should summarize the conclusion and link the final artifacts; it should not duplicate the full report.

File naming:

- `[Manufacturer]_[Device]_Global_Post-Market_Safety_Surveillance_Report_[YYYYMMDD].docx`
- `[Manufacturer]_[Device]_Safety_Surveillance_Audit_[YYYYMMDD].xlsx`

The final report must include the three QA pass results.

## 13. Output structure

Default final answer/report:

1. **Executive conclusion** — concise statement of what was found and the principal limitations; no unsupported benefit-risk verdict.
2. **Product identity resolution** — identifiers, candidate codes, confidence, and evidence.
3. **Search scope and date window** — exact dates and jurisdictions.
4. **Database/source coverage table** — source, jurisdiction, role, query, raw hits, included unique records, status/limitations.
5. **Exact-device findings**.
6. **Product-family findings**.
7. **Device-class context**.
8. **Adverse-event analysis** — unique report counts, event types, temporal pattern, problem-code mentions.
9. **Recall / FSCA / safety-notice analysis**.
10. **Safety-signal matrix** — issue, scope, severity evidence, recurrence, cross-source support, assessment, limitations.
11. **Data gaps and interpretation limits**.
12. **Search audit trail** — source URL, query, access date, date window, raw count, exclusions, de-duplication rule.
13. **References** — official sources first.

When the user requests CER/PMS/PSUR-ready language, produce formal narrative after the evidence table is complete. When the user asks only for a summary, preserve the same evidence boundaries in a shorter form.

## 14. Three-pass mandatory QA before finalization

Do not deliver or generate the final version until all three passes are complete.

### QA Pass 1 — Logic and identity

Check:

- product identity is supported and not inherited from prior projects;
- FDA product code/regulation and model/manufacturer links are consistent;
- multi-function devices are not forced into one code without justification;
- exact-device, family and class evidence remain separated;
- no device-class aggregate is presented as model-specific evidence;
- date windows are exact and internally consistent;
- no causal or comparative-safety inference is unsupported.

### QA Pass 2 — Data, counting and sources

Check:

- every material number has a source/query/date;
- unique-report counts are not confused with problem-code mentions or events;
- raw, excluded, duplicate and final counts reconcile;
- recall/FSCA duplicates are resolved;
- current regulator/database status was verified on the run date;
- citations point to authoritative sources;
- statements about standards/thresholds are clause-verified or explicitly unverified;
- “no records” statements include searched sources/date range and do not imply absence of events.

### QA Pass 3 — Client-data and contamination scan

Search the entire generated output and any reusable template/config created during the run for:

- client/company names not supplied in the current task;
- prior product names/models;
- prior FDA product codes or authorization numbers;
- prior comparator/equivalent/predicate names;
- hard-coded MDR/recall counts;
- project IDs/dates used as fixed template content;
- local absolute file paths/usernames;
- e-mail addresses/phone numbers/person names unrelated to the current task;
- conclusions or thresholds copied from another device type.

If any residue is found, remove it and repeat all three QA passes. Reusable skill files must contain zero customer-specific project information.

## 15. Source registry

Read `config/sources.yaml` before each run. Verify current public availability/status when it could have changed. The registry is a starting point, not proof that a database is currently operational.

## 16. Failure handling

- If an API is unavailable, use the regulator's official web interface or downloadable data where available and document the fallback.
- If a JavaScript-only public database cannot be reliably queried, document it as `access_limited` and use official regulator notices/search pages; do not pretend the database was fully searched.
- If a source returns zero results, run at least one alternate identity/synonym query before classifying it as zero-hit.
- If a result count is too large for record-level review, obtain aggregate counts first, then sample high-severity/most-recent/representative records using a documented rule.
- If public sources conflict, preserve both values, explain likely scope/date/query differences, and do not silently choose one.

## 17. Privacy and reusable-skill hygiene

The skill package itself must never contain customer project data. Current-task client information may be used transiently to perform the requested analysis and may appear in the user-requested report, but must not be written into reusable templates, examples, source registries, evaluation fixtures or default paths.

Use generic placeholders only in reusable files. Use relative output paths unless the user explicitly supplies a destination.
