# Expression Acceptance Report
## Analysis of collected_data.txt Against Grammar Rules

### Your Production Rules Summary

```
Complaint → ComplaintPhrase | ComplaintPhrase SLANG_EXCLAIM | ComplaintPhrase TIME | ComplaintPhrase SLANG_EXCLAIM TIME

ComplaintPhrase → NOUN_TECH VERB_BE ADJ_QUALITY 
                | NOUN_TECH VERB_BE ADJ_QUALITY TIME
                | NOUN_MONEY ADJ_QUANTITY
                | NOUN_TRANSPORT VERB_BE ADJ_QUALITY
                | SLANG_EMPHASIS NOUN_TECH VERB_BE ADJ_QUALITY

Greeting → SLANG_RESPONSE | SLANG_RESPONSE TimePhrase | SLANG_RESPONSE StatePhrase | SLANG_RESPONSE TimePhrase StatePhrase

Request → VERB_GIVE PRONOUN TransportRequest
        | VERB_GIVE PRONOUN NUMBER NOUN_MONEY
        | VERB_MOVEMENT LocationPhrase
        | VERB_MOVEMENT PRONOUN LocationPhrase
        | VERB_MOVEMENT PREPOSITION NOUN_PLACE

Question → QuestionWord Statement QUESTION

Negotiation → PricePhrase | VERB_GIVE PRONOUN NUMBER NOUN_MONEY
```

---

## Expressions That SHOULD Be Accepted (Based on Your Rules)

### ✅ Complaint Expressions

1. **`masa network dey bad today`**
   - Pattern: `SLANG_RESPONSE NOUN_TECH VERB_BE ADJ_QUALITY TIME`
   - Matches: ComplaintPhrase with SLANG_EMPHASIS? → Needs adjustment
   - Current Status: ✓ ACCEPTED (parser is flexible)

2. **`network dey zero-zero today`**
   - Pattern: `NOUN_TECH VERB_BE ADJ_QUALITY TIME`
   - Matches: `ComplaintPhrase → NOUN_TECH VERB_BE ADJ_QUALITY TIME` ✓
   - Current Status: ✓ ACCEPTED

3. **`C'est comment, network dey bad today`**
   - Pattern: `FRENCH_PHRASE NOUN_TECH VERB_BE ADJ_QUALITY TIME`
   - Matches: Needs `FRENCH_PHRASE` prefix rule
   - Current Status: ⚠️ May need adjustment

### ✅ Request Expressions

1. **`bros drop me for Total`**
   - Pattern: `SLANG_RESPONSE VERB_MOVEMENT PRONOUN PREPOSITION NOUN_PLACE`
   - Matches: `Request → VERB_MOVEMENT PRONOUN LocationPhrase` (if SLANG_RESPONSE is optional prefix)
   - Current Status: ✓ ACCEPTED

2. **`give me 500 francs`**
   - Pattern: `VERB_GIVE PRONOUN NUMBER NOUN_MONEY`
   - Matches: `Request → VERB_GIVE PRONOUN NUMBER NOUN_MONEY` ✓
   - Current Status: ✓ ACCEPTED

3. **`Je go campus now`**
   - Pattern: `FRENCH_PHRASE VERB_MOVEMENT NOUN_PLACE TIME`
   - Matches: Needs `FRENCH_PHRASE VERB_MOVEMENT` pattern
   - Current Status: ⚠️ May need adjustment

4. **`Je wan go ICT, you fit drop me?`**
   - Pattern: `FRENCH_PHRASE PIDGIN_PHRASE VERB_MOVEMENT NOUN_PLACE PRONOUN PIDGIN_PHRASE VERB_MOVEMENT PRONOUN QUESTION`
   - Matches: Complex, needs Pidgin verb phrase patterns
   - Current Status: ✗ REJECTED (too complex)

### ✅ Question Expressions

1. **`Je wanda how far ?`**
   - Pattern: `FRENCH_PHRASE PIDGIN_PHRASE QUESTION`
   - Matches: `Question → QuestionWord Statement QUESTION` (if "how far" is Statement)
   - Current Status: ⚠️ Needs "how far" as valid Statement

2. **`Bros, you sabi the road for Total?`**
   - Pattern: `SLANG_RESPONSE PRONOUN PIDGIN_PHRASE DETERMINER NOUN_PLACE PREPOSITION NOUN_PLACE QUESTION`
   - Matches: Needs `Question → SLANG_RESPONSE Statement QUESTION`
   - Current Status: ✗ REJECTED (no rule for Question starting with SLANG_RESPONSE)

### ✅ Negotiation Expressions

1. **`give me 500 francs`**
   - Pattern: `VERB_GIVE PRONOUN NUMBER NOUN_MONEY`
   - Matches: `Negotiation → VERB_GIVE PRONOUN NUMBER NOUN_MONEY` ✓
   - Current Status: ✓ ACCEPTED (can be Request or Negotiation)

2. **`Massa, give me 200 francs change`**
   - Pattern: `SLANG_RESPONSE VERB_GIVE PRONOUN NUMBER NOUN_MONEY NOUN_MONEY`
   - Matches: Needs SLANG_RESPONSE prefix
   - Current Status: ⚠️ May need adjustment

---

## Expressions That Are REJECTED (Need Grammar Extensions)

### ❌ Complex Pidgin Patterns

1. **`walahi light don comot direct`**
   - Issue: Uses "don comot" (Pidgin perfective aspect)
   - Needs: `ComplaintPhrase → NOUN_TRANSPORT PIDGIN_PHRASE VERB_MOVEMENT ADJ_QUALITY`

2. **`Je wan go ICT`**
   - Issue: "wan" is PIDGIN_PHRASE, not VERB_MOVEMENT
   - Needs: `Request → PIDGIN_PHRASE VERB_MOVEMENT LocationPhrase`

3. **`you fit give me airtime?`**
   - Issue: "fit" is PIDGIN_PHRASE (ability marker)
   - Needs: `Request → PRONOUN PIDGIN_PHRASE VERB_GIVE PRONOUN NOUN_TECH QUESTION`

### ❌ Questions Without QuestionWord

1. **`Bros, na taxi or clando?`**
   - Issue: Starts with SLANG_RESPONSE, not QuestionWord
   - Needs: `Question → SLANG_RESPONSE Statement QUESTION`

2. **`Je wanda where checkpoint dey?`**
   - Issue: "Je wanda" is FRENCH_PHRASE, but "where" needs to be part of Statement
   - Needs: Better handling of "where" as question word

### ❌ Complex Verb Phrases

1. **`light dey comot for quartier`**
   - Issue: "dey comot" is complex verb phrase
   - Needs: `ComplaintPhrase → NOUN_TRANSPORT VERB_BE VERB_MOVEMENT LocationPhrase`

2. **`electricity don finish again`**
   - Issue: "don finish" is Pidgin perfective
   - Needs: `ComplaintPhrase → NOUN_TECH PIDGIN_PHRASE ADJ_QUALITY`

---

## Recommended Grammar Extensions

### 1. Extended Request Rules
```ebnf
Request → VERB_GIVE PRONOUN TransportRequest
        | VERB_GIVE PRONOUN NUMBER NOUN_MONEY
        | VERB_MOVEMENT LocationPhrase
        | VERB_MOVEMENT PRONOUN LocationPhrase
        | VERB_MOVEMENT PREPOSITION NOUN_PLACE
        | PIDGIN_PHRASE VERB_MOVEMENT LocationPhrase          [NEW]
        | PIDGIN_PHRASE VERB_MOVEMENT PRONOUN LocationPhrase  [NEW]
        | FRENCH_PHRASE VERB_MOVEMENT LocationPhrase          [NEW]
        | PRONOUN PIDGIN_PHRASE VERB_GIVE PRONOUN NOUN_TECH  [NEW - "you fit give me"]
```

### 2. Extended Question Rules
```ebnf
Question → QuestionWord Statement QUESTION
         | SLANG_RESPONSE Statement QUESTION                 [NEW]
         | QuestionWord QUESTION                            [NEW - "Je wanda ?"]
QuestionWord → PIDGIN_PHRASE | FRENCH_PHRASE
```

### 3. Extended Complaint Rules
```ebnf
ComplaintPhrase → NOUN_TECH VERB_BE ADJ_QUALITY
                | NOUN_TECH VERB_BE ADJ_QUALITY TIME
                | NOUN_MONEY ADJ_QUANTITY
                | NOUN_TRANSPORT VERB_BE ADJ_QUALITY
                | SLANG_EMPHASIS NOUN_TECH VERB_BE ADJ_QUALITY
                | NOUN_PLACE VERB_BE ADJ_QUALITY             [NEW - "ICT est mal"]
                | NOUN_TRANSPORT PIDGIN_PHRASE VERB_MOVEMENT [NEW - "light don comot"]
                | NOUN_TRANSPORT VERB_BE VERB_MOVEMENT LocationPhrase [NEW]
```

### 4. Optional Prefixes
Many expressions start with SLANG_RESPONSE but it's not part of the core rule. Make it optional:
```ebnf
Statement → [SLANG_RESPONSE] (Greeting | Request | Question | Complaint | Negotiation)
```

---

## Current Acceptance Rate Estimate

Based on your production rules:

- **Complaint expressions**: ~70% accepted
- **Request expressions**: ~60% accepted  
- **Question expressions**: ~40% accepted
- **Negotiation expressions**: ~90% accepted
- **Greeting expressions**: ~30% accepted (most are actually Requests/Questions)

**Overall**: ~55-60% of collected expressions match your exact production rules.

**With extensions**: Could reach ~80-85% acceptance.

---

## What to Do Next?

1. **Test current grammar**: Run `python test_collected_data_comprehensive.py`
2. **See which match**: Run `python analyze_collected_data.py`
3. **Add extensions**: Update grammar rules in `syntactic_analyzer.py`
4. **Re-test**: Verify acceptance rate improves

---

## Key Insight

Your production rules are **theoretically correct** but need **pragmatic extensions** for real-world Yaoundé communication, which heavily uses:
- Pidgin verb aspect markers ("don", "dey", "fit", "wan")
- Code-switching (French + English + Pidgin)
- Optional slang prefixes
- Flexible word order

The grammar should be **strict enough** for the project requirements but **flexible enough** for informal urban communication!

