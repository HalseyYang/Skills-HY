---
name: literature-review
description: Plan, conduct, evaluate, and write rigorous literature reviews,
  scoping reviews, systematic review drafts, annotated bibliographies, evidence
  maps, and research syntheses. Use when the user asks for literature search
  strategy, paper screening, inclusion/exclusion criteria, PRISMA-style
  workflow, evidence tables, thematic synthesis, gap analysis, research
  background sections, related work sections, citation quality checks, or review
  of medical, scientific, technical, product, policy, or academic literature.
disable: true
---

# Literature Review

Use this skill to turn a broad research question into a traceable review process with explicit search logic, screened evidence, and defensible synthesis.

## Workflow

1. Define the review question.
   - Convert vague topics into a focused question using PICO, SPIDER, PCC, or a simpler topic-scope-outcome frame.
   - State population/domain, intervention or concept, comparator if any, outcomes, timeframe, geography, and document types.
   - If the user has not provided scope, make conservative assumptions and label them.

2. Plan the search.
   - Use `references/search-strategy.md` when designing queries, databases, source types, or grey literature searches.
   - Build query blocks from concepts, synonyms, acronyms, variant spellings, standards/regulations, and product or method names.
   - For current, medical, legal, regulatory, or safety-sensitive topics, browse and cite primary or authoritative sources.

3. Screen sources.
   - Use `references/screening-and-extraction.md` for inclusion/exclusion criteria and extraction fields.
   - Prefer peer-reviewed papers, guidelines, standards, systematic reviews, official regulatory sources, and primary datasets.
   - Exclude weak or irrelevant sources explicitly when they could otherwise bias the synthesis.

4. Extract evidence.
   - Capture citation, year, jurisdiction/context, study type, sample/data, method, outcomes, limitations, and relevance.
   - Preserve URLs, DOI/PMID/arXiv IDs, publication dates, and access dates when available.
   - Do not overstate claims from abstracts alone; flag when only an abstract or secondary summary was available.

5. Assess quality and bias.
   - Use `references/evidence-synthesis.md` for study-quality prompts and synthesis structure.
   - Match appraisal to source type: randomized study, observational study, qualitative study, guideline, standard, review, dataset, or technical report.
   - Separate evidence strength from volume of publications.

6. Synthesize and write.
   - Organize by themes, chronology, methods, mechanisms, jurisdictions, outcomes, or evidence strength.
   - Highlight consensus, disagreement, gaps, uncertainty, and practical implications.
   - Include a source table for substantial reviews unless the user asks for prose only.

## Output Patterns

For quick reviews, provide:

- Search scope and assumptions
- Key findings
- Evidence table
- Gaps and caveats
- Sources

For formal reviews, provide:

- Research question
- Methods and search strategy
- Inclusion/exclusion criteria
- Screening summary
- Evidence extraction table
- Thematic or quantitative synthesis
- Limitations
- References

For related-work sections, provide polished prose plus a short table showing how each cited work supports the narrative.

## Quality Rules

- Cite sources for factual claims about papers, guidance, standards, regulations, current evidence, or market/clinical state.
- Prefer primary sources over blogs and tertiary summaries.
- Distinguish "no evidence found" from "evidence of no effect."
- Do not invent citations, DOIs, study details, sample sizes, or findings.
- Mark low-confidence claims and explain what would verify them.
- When the topic is medical, regulatory, legal, or financial, keep recommendations informational and source-grounded.

## References

- `references/search-strategy.md`: Query construction, source selection, and search logging.
- `references/screening-and-extraction.md`: Criteria, extraction tables, and evidence matrix fields.
- `references/evidence-synthesis.md`: Quality appraisal, synthesis structures, and final review checklist.
