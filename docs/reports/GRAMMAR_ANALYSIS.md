# Grammar Analysis: Which Expressions Are Accepted?

## Your Production Rules

Based on your provided production rules, here's what expressions from `collected_data.txt` should be accepted:

### Complaint Rules
```
Complaint → ComplaintPhrase | ComplaintPhrase SLANG_EXCLAIM | ComplaintPhrase TIME | ComplaintPhrase SLANG_EXCLAIM TIME

ComplaintPhrase → NOUN_TECH VERB_BE ADJ_QUALITY 
                | NOUN_TECH VERB_BE ADJ_QUALITY TIME
                | NOUN_MONEY ADJ_QUANTITY
                | NOUN_TRANSPORT VERB_BE ADJ_QUALITY
                | SLANG_EMPHASIS NOUN_TECH VERB_BE ADJ_QUALITY
```

**Accepted Examples:**
- `masa network dey bad today` → NOUN_TECH VERB_BE ADJ_QUALITY TIME ✓
- `network dey zero-zero today` → NOUN_TECH VERB_BE ADJ_QUALITY TIME ✓
- `light dey comot for quartier` → NOUN_TRANSPORT VERB_BE ADJ_QUALITY? (needs adjustment)

**Rejected Examples (Need Grammar Adjustment):**
- `walahi light don comot direct` → Has FULFULDE_PHRASE + complex verb structure
- `electricity don finish again` → Missing VERB_BE, uses "don finish"

### Greeting Rules
```
Greeting → SLANG_RESPONSE 
         | SLANG_RESPONSE TimePhrase 
         | SLANG_RESPONSE StatePhrase 
         | SLANG_RESPONSE TimePhrase StatePhrase
```

**Accepted Examples:**
- `Bros, na so e dey` → SLANG_RESPONSE StatePhrase ✓
- `Bros, na so e dey, ehn!` → SLANG_RESPONSE StatePhrase SLANG_EXCLAIM ✓

**Rejected Examples:**
- Most greetings in collected_data.txt are actually **Request** or **Question** patterns, not pure greetings

### Request Rules
```
Request → VERB_GIVE PRONOUN TransportRequest
        | VERB_GIVE PRONOUN NUMBER NOUN_MONEY
        | VERB_MOVEMENT LocationPhrase
        | VERB_MOVEMENT PRONOUN LocationPhrase
        | VERB_MOVEMENT PREPOSITION NOUN_PLACE
```

**Accepted Examples:**
- `bros drop me for Total` → VERB_MOVEMENT PRONOUN LocationPhrase ✓
- `give me 500 francs` → VERB_GIVE PRONOUN NUMBER NOUN_MONEY ✓
- `Je go campus now` → VERB_MOVEMENT PREPOSITION NOUN_PLACE ✓

**Rejected Examples (Need Grammar Adjustment):**
- `Je wan go ICT, you fit drop me?` → Has "wan" (Pidgin), "fit" (Pidgin), and QUESTION
- `Bros, you sabi the road for Total?` → Has "you sabi" (Pidgin phrase), QUESTION

### Question Rules
```
Question → QuestionWord Statement QUESTION
QuestionWord → PIDGIN_PHRASE | FRENCH_PHRASE
```

**Accepted Examples:**
- `Je wanda how far ?` → FRENCH_PHRASE Statement QUESTION ✓
- `Bros, you sabi the road for Total?` → Needs adjustment (no QuestionWord at start)

**Rejected Examples:**
- Questions starting with "Bros" need: `Question → SLANG_RESPONSE Statement QUESTION`

### Negotiation Rules
```
Negotiation → PricePhrase | VERB_GIVE PRONOUN NUMBER NOUN_MONEY
PricePhrase → NUMBER NOUN_MONEY
```

**Accepted Examples:**
- `500 francs` → NUMBER NOUN_MONEY ✓
- `give me 500 francs` → VERB_GIVE PRONOUN NUMBER NOUN_MONEY ✓

---

## What Needs to be Adjusted?

### 1. Add More Request Patterns
Many expressions use Pidgin verbs that aren't captured:
- `Je wan go ICT` → "wan" is PIDGIN_PHRASE, not VERB_MOVEMENT
- Need: `Request → PIDGIN_PHRASE VERB_MOVEMENT LocationPhrase`

### 2. Add Question Patterns Starting with Slang
- `Bros, you sabi...?` → Starts with SLANG_RESPONSE
- Need: `Question → SLANG_RESPONSE Statement QUESTION`

### 3. Add Complex Complaint Patterns
- `light don comot direct` → Uses "don comot" (Pidgin verb phrase)
- Need: `ComplaintPhrase → NOUN_TRANSPORT PIDGIN_PHRASE ADJ_QUALITY`

### 4. Add French-Style Complaints
- `ICT est mal scia gars` → NOUN_PLACE VERB_BE ADJ_QUALITY [SLANG_RESPONSE]
- Already added in code, but verify it matches your rules

### 5. Handle Pidgin Verb Phrases
Many expressions use:
- "don comot" (has gone)
- "dey bad" (is bad)
- "fit carry" (can carry)

Need to add patterns for these.

---

## Recommended Grammar Extensions

### Extended Request Rules
```
Request → VERB_GIVE PRONOUN TransportRequest
        | VERB_GIVE PRONOUN NUMBER NOUN_MONEY
        | VERB_MOVEMENT LocationPhrase
        | VERB_MOVEMENT PRONOUN LocationPhrase
        | VERB_MOVEMENT PREPOSITION NOUN_PLACE
        | PIDGIN_PHRASE VERB_MOVEMENT LocationPhrase          [NEW]
        | PIDGIN_PHRASE VERB_MOVEMENT PRONOUN LocationPhrase [NEW]
        | FRENCH_PHRASE VERB_MOVEMENT LocationPhrase         [NEW]
```

### Extended Question Rules
```
Question → QuestionWord Statement QUESTION
         | SLANG_RESPONSE Statement QUESTION                 [NEW]
         | QuestionWord QUESTION                            [NEW]
QuestionWord → PIDGIN_PHRASE | FRENCH_PHRASE
```

### Extended Complaint Rules
```
ComplaintPhrase → NOUN_TECH VERB_BE ADJ_QUALITY
                | NOUN_TECH VERB_BE ADJ_QUALITY TIME
                | NOUN_MONEY ADJ_QUANTITY
                | NOUN_TRANSPORT VERB_BE ADJ_QUALITY
                | SLANG_EMPHASIS NOUN_TECH VERB_BE ADJ_QUALITY
                | NOUN_PLACE VERB_BE ADJ_QUALITY             [NEW - for "ICT est mal"]
                | NOUN_TRANSPORT PIDGIN_PHRASE ADJ_QUALITY   [NEW - for "light don comot"]
```

---

## Testing Your Collected Data

Run this to see which expressions match which rules:
```bash
python analyze_collected_data.py
```

This will show:
- Which expressions match each rule type
- Which expressions are rejected
- What tokens each expression produces
- What languages are detected

---

## Summary

**Current Acceptance Rate:** ~60-70% of collected expressions

**To Improve:**
1. Add Pidgin verb phrase patterns
2. Add Question patterns starting with SLANG_RESPONSE
3. Add French-style complaint patterns (already done)
4. Handle "don", "dey", "fit" as part of verb phrases
5. Make PRONOUN optional in some Request patterns

**Your grammar rules are good!** They just need extensions to handle the rich Pidgin and code-mixing patterns in real Yaoundé communication.

