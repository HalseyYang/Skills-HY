# IMA Knowledge Base Reference

Use Tencent ima knowledge bases as a private reference source for medical device registration, regulatory strategy, document review, and evidence checks.

## Rule

For registration-related work, search ima knowledge bases before or alongside public sources when:

- The user asks about FDA, CE MDR, NMPA, clinical evaluation, registration pathways, standards, guidance, review reports, deficiency questions, or regulatory document drafting.
- The user asks for "引用", "依据", "知识库", "资料库", "内部资料", or asks whether existing knowledge covers an issue.
- The answer would benefit from accumulated local/industry materials rather than only public web search.

Use ima results as supporting references. For high-stakes regulatory conclusions, cross-check with official laws, guidance, standards, or primary literature where possible.

## Relevant Knowledge Bases

Prioritize these knowledge bases:

| Name | ID | Notes |
| --- | --- | --- |
| 医疗器械 | `eL8VTnWYqXBWxibVUUrgIZnuajXkF8bcFsEkVy79xXw=` | Large lifecycle medical-device knowledge base. |
| 医疗器械资料 | `KbDCOT4c1FDrYaG6d-eV1uInSMi6O2rJ2DuQf6GZ4Ew=` | Regulations, standards, registration process, review reports, guidance, FDA guidance. |
| 医疗器械国际认证汇总知识库 | `SQma_FtLh-Sh7gDyLWvIBcTZ0m_H7RdSkOTbC2vnrgo=` | International certification and registration references. |
| 医疗器械国内注册汇总知识库 | `_C0TjoatRKIX_5FVSjjhxwC01-ob-FepKwtdf6ctMfQ=` | China/NMPA registration references. |
| CE与FDA法规解读 | `sulzXmP_VIFmLOvFjr_wTZLdJPUEpfpzAKV4wdmHOU0=` | CE/FDA regulatory interpretation. |
| FDA认证汇总知识库 | `M_daNwQAaqov4X8CLnjCOguVG2lqiWLO1vbxpAW3K2c=` | FDA-focused reference library. |
| 全球产品认证合规 | `PkfULCuR2PYiqiUtT2KdJrjSDQu9NCHsEdpxBB2gD8g=` | Global product compliance and official policy sources. |
| 医疗器械公众号文章 | `VUJ-nc8nXeEQWHi9xrAIvk8VYmN8Lp39W1JCM777NQ4=` | WeChat/public article collection; use as secondary context, not primary authority. |

## Citation Discipline

When using ima search results:

- Cite the knowledge base name and source title.
- Include highlighted content or a short paraphrase of the relevant passage.
- If `media_id` is available, preserve it in notes or a source table.
- Distinguish ima knowledge-base support from official regulatory authority.
- Do not treat public-account articles as controlling law or guidance.

## Search Command

Use:

```bash
python3 /Users/hanyueyang/.codex/skills/meddev-regulatory-strategy/scripts/ima_kb_search.py "your query"
```

The script reads credentials from:

- `IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY`
- or `~/.config/ima/client_id` and `~/.config/ima/api_key`

The script searches the prioritized medical-device knowledge bases and prints titles, knowledge-base names, media IDs, and highlight snippets.
