# Final QA checklist

## Pass 1 — Logic and identity
- [ ] Identity resolved from current-task evidence only.
- [ ] Candidate product codes/identifiers are supported.
- [ ] Exact-device, product-family and device-class results remain separate.
- [ ] No class-level count is described as model-specific.
- [ ] Date windows are exact and consistent.
- [ ] No unsupported causality, incidence or comparative-safety claim.

## Pass 2 — Data and source integrity
- [ ] Every material number is traceable to source/query/date.
- [ ] Unique reports, events and problem-code mentions are not conflated.
- [ ] Raw/excluded/duplicate/included counts reconcile.
- [ ] Recall/FSCA duplicates are handled.
- [ ] Current database/module status verified, including the FDA AEMS/MAUDE transition resolver where applicable.
- [ ] Every source is assigned an authority tier (A-D).
- [ ] `zero_hit` is used only after a completed official-source query; inaccessible sources are marked `access_limited`.
- [ ] Standards thresholds are clause-verified or omitted/marked unverified.
- [ ] Zero-hit wording does not imply no adverse events exist.

## Pass 3 — Client-data contamination and input-document consistency
- [ ] No prior client/company/product/model names.
- [ ] No prior product codes/submission numbers/comparator names.
- [ ] No hard-coded prior MDR/recall counts.
- [ ] No prior project IDs/dates as fixed content.
- [ ] No local absolute file paths/usernames.
- [ ] No unrelated emails/phones/person names.
- [ ] No device-specific conclusions/thresholds copied into reusable templates.

- [ ] Supplied source documents were scanned for unrelated device/model names, device-type mismatch, population mismatch and copied template residue.
- [ ] Any source-document inconsistency is reported separately from adverse-event evidence.
- [ ] Full Audit Surveillance produced both DOCX and XLSX artifacts.
