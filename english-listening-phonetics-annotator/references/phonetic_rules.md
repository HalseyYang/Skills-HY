# Phonetic Rules Engine — English Connected Speech Annotation

## Complete reference for systematic annotation. Load this file before annotating.

---

## 1. STRESS (重读)

### Rule: Content words are stressed; function words are unstressed.

**Always stressed:**
- Nouns (Personnel, letter, tax, office, student, summer, records, name, surname, Finance)
- Main verbs (had, worked, wonder, look, spell, got, know, send)
- Adjectives (exact, monthly, first)
- Adverbs (actually, here, last, today)
- Numbers (183, 538, 457, thirty-eight, fifty-seven)
- Place names (School Road, Barnfield)
- Names (Tim, Jaye, Stephen)
- Negatives (not, never) — when emphasized
- Question words (How, What, Why)

**Never stressed (→ weak form instead):**
- Articles: a, an, the
- Prepositions: at, for, from, in, of, on, to, with
- Pronouns: he, him, his, I, you, your, they, them, we
- Auxiliary verbs: is, was, am, are, do, does, have, had, could, would, should
- Conjunctions: and, but, or, if, so
- Modal verbs: can, could, will, would, should, must

**Special stress rules:**
- Spelling out letters: each letter fully stressed (J-A-Y-E)
- Correcting/contrasting: the corrected word gets extra stress ("Customer **SERVICES**, **actually**")
- Numbers in addresses/amounts: all stressed ("**183** **School** **Road**")

---

## 2. WEAK FORMS (弱读)

### Complete weak form table

| Word | Strong form | Weak form | Notes |
|------|------------|-----------|-------|
| a | /eɪ/ | /ə/ | Always weak |
| an | /æn/ | /ən/ | /n/ after consonant |
| the (before C) | /ðiː/ | /ðə/ | Before consonant |
| **the (before V)** | /ðiː/ | **/ði/** | **Before vowel!** the information → /ðɪɪnfəˈmeɪʃən/ |
| of | /ɒv/ | /əv/ | Even /ə/ in fast speech |
| to | /tuː/ | /tə/ | Before consonant |
| at | /æt/ | /ət/ | |
| for | /fɔː/ | /fə/ | r-linking possible |
| from | /frɒm/ | /frəm/ | |
| in | /ɪn/ | /ɪn/ | Already short |
| on | /ɒn/ | /ən/ | |
| with | /wɪð/ | /wɪð/ | Less reduction |
| and | /ænd/ | /ən/ → /n/ | /d/ often drops |
| but | /bʌt/ | /bət/ | |
| or | /ɔː/ | /ə/ | |
| than | /ðæn/ | /ðən/ | |
| that | /ðæt/ | /ðət/ | As conjunction |
| is | /ɪz/ | /ɪz/ → /z/ | |
| are | /ɑː/ | /ə/ | |
| was | /wɒz/ | /wəz/ | |
| were | /wɜː/ | /wə/ | |
| am | /æm/ | /əm/ | |
| been | /biːn/ | /bɪn/ | |
| being | /ˈbiːɪŋ/ | /bɪŋ/ | |
| have | /hæv/ | /həv/ | |
| has | /hæz/ | /həz/ | |
| had | /hæd/ | /həd/ | |
| do | /duː/ | /də/ | |
| **does** | /dʌz/ | **/dəz/** | **schwa /ə/, NOT /ʌ/** |
| can | /kæn/ | /kən/ | |
| could | /kʊd/ | /kəd/ | |
| would | /wʊd/ | /wəd/ | |
| should | /ʃʊd/ | /ʃəd/ | |
| will | /wɪl/ | /əl/ → /l/ | |
| would | /wʊd/ | /wəd/ | |
| must | /mʌst/ | /məs(t)/ | |
| I | /aɪ/ | /aɪ/ → /ə/ | Very fast speech |
| you | /juː/ | /jə/ | |
| your | /jɔː/ | /jə/ | |
| he | /hiː/ | /hi/ → /i/ | h-dropping after consonants |
| him | /hɪm/ | /ɪm/ | h-dropping |
| his | /hɪz/ | /ɪz/ | h-dropping |
| her | /hɜː/ | /hə/ → /ə/ | h-dropping |
| them | /ðem/ | /ðəm/ | |
| us | /ʌs/ | /əs/ | |
| our | /aʊə/ | /ɑː/ | |
| my | /maɪ/ | /mɪ/ | Fast speech |
| some | /sʌm/ | /səm/ | |
| any | /ˈeni/ | /ni/ | |
| many | /ˈmeni/ | /mni/ | |
| such | /sʌtʃ/ | /sətʃ/ | |
| there | /ðeə/ | /ðə/ | |
| then | /ðen/ | /ðən/ | |
| not | /nɒt/ | /nɒt/ | Negative may stay strong |
| just | /dʒʌst/ | /dʒəs(t)/ | |

### Critical rules:
1. **"does" → /dəz/ (schwa), NEVER /dʌz/** — Most common error
2. **"the" before vowel → /ði/, before consonant → /ðə/** — Two weak forms
3. **"and" → /ən/ → /n/** — /d/ drops, vowel reduces to schwa
4. **"have/has/had" → /həv/ /həz/ /həd/** — Not /hæv/ etc.
5. **"could/would/should" → /kəd/ /wəd/ /ʃəd/** — Not /kʊd/ etc.

---

## 3. LIAISON (连读)

### Rule 3a: Consonant → Vowel (C→V liaison)

When a word ends in a consonant and the next word starts with a vowel, they connect.

Examples:
- had‿a → /hædə/
- tax‿office → /ˈtæksɒfɪs/
- look‿him → /ˈlʊkɪm/ (h-dropping first)
- what's‿the → /wɒtsðə/
- lives‿at → /lɪvzət/
- lots‿of → /lɒtsəv/
- an‿office → /ənɒfɪs/
- office‿assistant → /ˈɒfɪsəˈsɪstənt/
- send‿them → /sendðəm/
- the‿information → /ðɪɪnfəˈmeɪʃən/

### Rule 3b: Vowel → Vowel (V→V liaison with glide)

When a word ends in a vowel and the next starts with a vowel, insert a glide:
- After /iː/ /ɪ/ /eɪ/ /aɪ/ /ɔɪ/ → insert **/j/**
  - They‿also → /ðeɪjˈɔːlsəʊ/
  - he‿are → /hiˈjɑː/
  - seventy‿a → /ˈsevəntijə/
  - sorry,‿he → /ˈsɒriji/

- After /uː/ /ʊ/ /oʊ/ /aʊ/ → insert **/w/**
  - know‿about → /nəʊwəˈbaʊt/
  - know‿his → /nəʊwɪz/ (h-dropping first)
  - do‿it → /duːwɪt/

### Rule 3c: Multi-word liaison chains

- here‿we‿are → /hɪəwiˈɑː/ (three words)
- say‿he‿was → /seɪhiwəz/ (h may keep after vowel)
- He‿was‿an → /hiwəzən/ (three words)
- look‿him‿up‿in → /ˈlʊkɪmʌpɪn/ (four words, h-dropping)

---

## 4. LINKING /r/ (英式 r 连读)

### Rule: In British English, words ending in /ə/ or /ɔː/ insert /r/ before a vowel.

**Applicable endings:**
- Words spelled with final -er, -re, -a, -or, -ure, -ear (when pronounced /ə/ or /ɔː/)
- The /r/ is NOT pronounced when the word is isolated or before a consonant

**Examples:**
- summer‿I → /ˈsʌməraɪ/ (summer ends /ə/, insert /r/)
- wonder‿if → /ˈwʌndərɪf/
- for‿them → /fərðəm/ (also r-linking)
- there‿are → /ðərɑː/
- here‿we → /hɪəwi/ (here ends /ɪə/, linking /r/ possible but /w/ glide more common)
- your‿office → /jərɒfɪs/
- sure‿if → /ʃɔːrɪf/

**NOT linking /r/ (before consonant or pause):**
- summer was → /ˈsʌmə wəz/ (no /r/)
- wonder about → /ˈwʌndə əˈbaʊt/ (wait, this IS before vowel → /ˈwʌndərəbaʊt/)

### Distinguishing from American English:
- American: /r/ is always pronounced at word end → no special "linking" needed
- British: /r/ only appears before vowels → "linking /r/" is a distinct phenomenon

---

## 5. INCOMPLETE PLOSION /t̚/ (不完全爆破)

### Rule: /t/ (and /p/, /k/) before consonants are not fully released.

**This is NOT elision (省音).** The consonant is articulated (tongue/glottis position formed) but airflow is stopped before release. There is a brief silence then the next consonant.

### /t/ patterns:

| Phrase | IPA | Context |
|--------|-----|---------|
| got that | /ɡɒt̚ ðæt/ | /t/ before /ð/ |
| want to | /wɒn(t) tə/ | /t/ before /t/ — two /t/s overlap |
| last summer | /lɑːs(t) ˈsʌmə/ | /t/ between /s/ and /s/ |
| let me | /le(t) mi/ | /t/ before /m/ |
| exact job | /ɪɡˈzæk(t) ˈdʒɒb/ | /t/ before /dʒ/ |
| eight pounds | /eɪt̚ ˈpaʊndz/ | /t/ before /p/ |
| send them | /sen(d) ðəm/ | /d/ before /ð/ (same principle) |

### Key distinction:
- **Incomplete plosion /t̚/**: /t/ is formed but not released → brief silence → next sound
- **Elision Ø**: /t/ is completely skipped → no silence
- In exam recordings (BEC/IELTS): usually **incomplete plosion**, not full elision
- "want to" → /wɒn(t)tə/ — NOT American "wanna" /ˈwɒnə/

### /p/ and /k/ patterns (same principle):
- stop that → /stɒp̚ ðæt/
- look at → /lʊk̚ ət/

---

## 6. ASSIMILATION (同化)

### Rule 6a: h-dropping in pronouns

**After consonants → h drops:**
- does he → /dəzi/ (/z/ + /hɪ/ → /z/ + /ɪ/ → /zi/)
- spell his → /spelɪz/ (/l/ + /hɪz/ → /l/ + /ɪz/)
- look him → /lʊkɪm/ (/k/ + /hɪm/ → /k/ + /ɪm/)
- tell him → /telɪm/
- what's his → /wɒtsɪz/

**After vowels → h KEEPS:**
- say he → /seɪ hi/ (vowel + h → h retained, possible /j/ glide)
- sorry, he → /ˈsɒri hi/ (h retained after vowel)
- I think he → /aɪ ˈθɪŋk hi/ — wait, this is after consonant /k/ → h drops → /aɪ ˈθɪŋkɪ/
  - Correction: "I think he" — /k/ is consonant → h drops → /aɪˈθɪŋkɪ/

**Summary: h drops when preceded by a consonant; h may keep when preceded by a vowel or pause.**

### Rule 6b: /j/ and /w/ glide insertion (also listed under liaison)

- /iː/ /ɪ/ /eɪ/ /aɪ/ /ɔɪ/ + vowel → insert /j/
- /uː/ /ʊ/ /oʊ/ /aʊ/ + vowel → insert /w/

(See liaison section 3b for examples)

### Rule 6c: /ŋ/ → /ŋɡ/ before vowels

- anything else → /ˈeniθɪŋɡels/ (extra /ɡ/ appears)
- everything else → /ˈevriθɪŋɡels/
- nothing else → /ˈnʌθɪŋɡels/
- Bring it → /brɪŋɡɪt/

### Rule 6d: Yod coalescence

- /t/ + /j/ → /tʃ/: got you → /ɡɒtʃu/; not yet → /nɒtʃet/ (less common)
- /d/ + /j/ → /dʒ/: did you → /ˈdɪdʒu/; would you → /ˈwʊdʒu/
- /s/ + /j/ → /ʃ/: miss you → /ˈmɪʃu/
- /z/ + /j/ → /ʒ/: as you → /əʒu/

### Rule 6e: Consonant fusion

- /d/ + /j/ → /dʒ/: And you → /əndʒu/
- /t/ + /r/ → /tr/: tree (already a phoneme)

---

## ANNOTATION ORDER (process each sentence in this order)

1. **Identify speaker** (Woman/Man, or role: Personnel/Caller)
2. **Mark stress** on content words (red bold underline)
3. **Mark weak forms** on function words (yellow italic small)
4. **Mark liaison** C→V and V→V (blue dotted underline)
5. **Mark linking /r/** (orange background)
6. **Mark incomplete plosion /t̚/** (purple strikethrough)
7. **Mark assimilation** (green background)
8. **Write full IPA** for the line in an IPA box
9. **Write explanatory note** for each phenomenon found

## COMMON PITFALLS (errors made in practice)

1. ❌ "does" → /dʌz/ ✓ "does" → /dəz/ (schwa!)
2. ❌ "the information" → /ðə/ ✓ → /ði/ (before vowel!)
3. ❌ "got that" = elision (t dropped) ✓ = incomplete plosion /t̚/ (t suppressed)
4. ❌ "want to" = "wanna" ✓ = /wɒn(t)tə/ (formal British exam speech)
5. ❌ "anything else" = /ˈeniθɪŋels/ ✓ = /ˈeniθɪŋɡels/ (/ŋɡ/!)
6. ❌ "summer I" no liaison ✓ = /ˈsʌməraɪ/ (linking /r/!)
7. ❌ "does he" h kept ✓ = h drops after consonant → /dəzi/
8. ❌ "say he" h drops ✓ = h keeps after vowel → /seɪ hi/
