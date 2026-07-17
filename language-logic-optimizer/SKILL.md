---
name: 语言逻辑优化器
description: >
  A thought-organizing skill that takes messy, disorganized text and restructures it into clear,
  logical communication. This skill should be used when the user sends text prefixed with "优化" or
  explicitly asks to organize, restructure, clarify, or clean up messy writing. Supports both Chinese
  and English. Covers scenarios including voice-to-text transcripts, rough drafts, work emails/messages,
  and brainstorming notes. Auto-detects the appropriate tone based on context. Does NOT add AI-flavor
  words or fabricate meaning not present in the original text.
---

# 语言逻辑优化器

## Purpose

Transform disorganized, scattered text into logically structured, clear communication while preserving the author's original intent, tone, and personality. This is a thought organizer, not a writing polisher.

## Trigger Conditions

Activate when:
- User sends text prefixed with "优化" or "optimize"
- User explicitly asks to organize, restructure, clarify, clean up, or fix messy text
- User provides scattered thoughts, brainstorming output, or voice-to-text that needs structuring

## Core Principles

1. **Conservative editing** — Never add meaning the user did not express. Prefer less editing over more.
2. **No AI flavor** — Do not use AI-typical vocabulary (赋能, 抓手, 深耕, leverage, synergize, etc.). No forced parallelism, no unnecessary rhetorical flourishes.
3. **Preserve voice** — Retain the user's natural speaking style and personality. Smooth out logic, not personality.
4. **Structure first** — Prioritize logical organization over surface-level word choice.

## Processing Pipeline

Execute the following steps in order:

### Step 1: Scan and Classify

Identify:
- **Language**: Chinese, English, or mixed
- **Length**: Short (<200 chars), medium (200-1000), long (>1000)
- **Scenario**: Match against the style guide below
- **Goal**: What is the user trying to accomplish with this text?

### Step 2: Extract Information Points

Break the raw text into discrete information units:
- Key arguments / claims
- Supporting evidence / reasons
- Requests / calls to action
- Background context
- Emotional tone or urgency signals

### Step 3: Remove Noise

- Delete redundancy (same point expressed multiple times)
- Remove contradictions (flag to user if contradictory points seem intentional)
- Strip filler words, hedging, and circular phrasing
- Note: Do NOT remove hedging if it conveys genuine uncertainty the user wants preserved

### Step 4: Restructure Logic

Choose the most appropriate structure based on the identified goal:

| Goal type | Best structure |
|-----------|---------------|
| Persuade / argue | Claim → Evidence → Conclusion |
| Inform / explain | Context → Key points → Implication |
| Request / instruct | What I need → Why → When / How |
| Brainstorm / explore | Group by theme, then prioritize |
| Compare / decide | Criteria → Options → Analysis |
| Respond / reply | Acknowledge → Address each point → Close |

Within the chosen structure, apply:
- **Ordering**: Most important first, or chronological, or causal — whichever fits
- **Grouping**: Related points belong together
- **Hierarchy**: Main points vs. sub-points clearly differentiated

### Step 5: Add Transitions

Insert minimal, natural connectors between sections and sentences:
- Cause-effect: 因此, 所以, since, because
- Sequence: 首先, 然后, first, then
- Contrast: 但是, 然而, but, however
- Addition: 另外, 此外, additionally
- Do NOT over-connect — trust the reader

### Step 6: Style Adaptation

Apply the appropriate tone based on the detected scenario:

| Scenario | Style |
|----------|-------|
| WeChat message / voice transcript | Casual, concise, keep warmth |
| Work email / report | Formal, professional, conclusion first |
| Review comments / tech discussion | Rigorous, structured, argument + evidence clear |
| Brainstorm / draft notes | Faithful cleanup, preserve sharpness of original ideas |
| Unclear / ambiguous | Default: clean, structured, neutral-pro |

### Step 7: Output

Deliver the restructured text directly. Follow these output rules:

- **Default**: Provide one polished version
- **Long or complex input (>500 chars)**: Offer two versions:
  - **精简版 (Concise)**: Core message only, cut to essentials
  - **完整版 (Complete)**: Full restructuring with all original points preserved
- **Do NOT explain changes** unless the user asks (e.g., "改了什么？" or "why did you change X?")
- **If meaning is ambiguous**: Flag the ambiguity briefly after the output, e.g., "⚠️ 有一处含义不确定：[X]，请确认你想表达的是……"

## Format Guidelines

For Chinese text:
- Use proper punctuation (，。、！？：；) — no English punctuation mixed in unless quoting
- Paragraph breaks for each logical unit
- Bullet points or numbered lists for parallel items (3+ items)

For English text:
- Standard English punctuation and grammar
- Paragraph breaks for each logical unit
- Bullet points or numbered lists for parallel items (3+ items)

For mixed text:
- Match punctuation to the dominant language of each segment
- Keep technical terms in their original language

## Anti-Patterns (Never Do These)

- ❌ Add conclusions or recommendations the user didn't make
- ❌ Use AI-flavor words: 赋能, 抓手, 深耕, 颗粒度, 底层逻辑, 顶层设计, leverage, synergize, impactful, delve into, navigate, in today's landscape
- ❌ Force a three-part structure ("首先…其次…最后…") when two or four parts are more natural
- ❌ Add unnecessary em dashes or dramatic pauses
- ❌ Start with "好的，帮你优化一下" or similar filler — just deliver the result
- ❌ Expand a short message into a long one — if the user wrote 3 lines, the output should be roughly 3 lines, just clearer
