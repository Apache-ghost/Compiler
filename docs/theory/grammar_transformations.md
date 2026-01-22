# Grammar Transformations for LL(1) Parsing

## 📋 Overview

This document details the grammar transformations performed to convert the original Context-Free Grammar (CFG) for Yaoundé urban communication into an LL(1) grammar suitable for predictive parsing. The transformations include **Left Recursion Removal** and **Left Factoring**.

---

## 🔄 Part 1: Left Recursion Removal

### Problem: Left Recursive Grammar Rules

Left recursion occurs when a non-terminal appears as the first symbol in its own production. This creates infinite loops in top-down parsers and must be eliminated for LL(1) parsing.

### Example 1: Statement with Left Recursion

**Original Grammar (with left recursion):**
```
Statement → Statement CONJUNCTION Phrase
Statement → Greeting
Statement → Request
Statement → Question
Statement → Complaint
Statement → Negotiation
Phrase → Greeting | Request | Question | Complaint | Negotiation
```

**Problem:** The rule `Statement → Statement CONJUNCTION Phrase` is left-recursive. A parser trying to parse `Statement` would immediately try to parse `Statement` again, creating infinite recursion.

**Solution: Left Recursion Removal Algorithm**

We apply the standard transformation:
- For a rule `A → Aα | β`, we transform it to:
  - `A → βA'`
  - `A' → αA' | ε`

**Transformed Grammar:**
```
Statement → Greeting Statement'
Statement → Request Statement'
Statement → Question Statement'
Statement → Complaint Statement'
Statement → Negotiation Statement'

Statement' → CONJUNCTION Phrase Statement'
Statement' → ε

Phrase → Greeting | Request | Question | Complaint | Negotiation
```

**Explanation:**
- `Statement'` (Statement-prime) handles the recursive part
- The base cases (Greeting, Request, etc.) come first
- `Statement' → ε` allows the recursion to terminate
- This maintains the same language but removes left recursion

**Example Parse:**
```
Input: "bros and give me 500 francs"
Parse: Statement → Greeting Statement'
     → "bros" Statement'
     → "bros" CONJUNCTION Phrase Statement'
     → "bros" "and" Request Statement'
     → "bros" "and" "give me 500 francs" Statement'
     → "bros" "and" "give me 500 francs" ε
```

### Example 2: Request with Left Recursion

**Original Grammar (with left recursion):**
```
Request → Request CONJUNCTION TransportRequest
Request → VERB_GIVE PRONOUN TransportRequest
Request → VERB_GIVE PRONOUN NUMBER NOUN_MONEY
Request → VERB_MOVEMENT LocationPhrase
```

**Transformed Grammar:**
```
Request → VERB_GIVE PRONOUN TransportRequest Request'
Request → VERB_GIVE PRONOUN NUMBER NOUN_MONEY Request'
Request → VERB_MOVEMENT LocationPhrase Request'

Request' → CONJUNCTION TransportRequest Request'
Request' → ε
```

**Before/After Comparison:**

| Before (Left Recursive) | After (Right Recursive) |
|------------------------|------------------------|
| `Request → Request CONJUNCTION TransportRequest` | `Request → VERB_GIVE PRONOUN TransportRequest Request'` |
| `Request → VERB_GIVE PRONOUN TransportRequest` | `Request' → CONJUNCTION TransportRequest Request'` |
| | `Request' → ε` |

---

## 🔀 Part 2: Left Factoring

### Problem: Common Prefixes in Productions

Left factoring is needed when multiple productions of the same non-terminal start with the same symbols, making it impossible to decide which production to choose based on the first token.

### Example 1: Request with Common Prefix

**Original Grammar (needs left factoring):**
```
Request → VERB_GIVE PRONOUN TransportRequest
Request → VERB_GIVE PRONOUN NUMBER NOUN_MONEY
Request → VERB_MOVEMENT LocationPhrase
Request → VERB_MOVEMENT PRONOUN LocationPhrase
Request → VERB_MOVEMENT PREPOSITION NOUN_PLACE
```

**Problem:** 
- Multiple productions start with `VERB_GIVE PRONOUN`
- Multiple productions start with `VERB_MOVEMENT`
- The parser cannot decide which production to use after seeing `VERB_GIVE PRONOUN`

**Solution: Left Factoring Algorithm**

For rules with common prefixes:
1. Identify the common prefix
2. Factor it out into a new production
3. Create a new non-terminal for the remaining parts

**Step-by-Step Transformation:**

**Step 1: Factor out `VERB_GIVE PRONOUN`**
```
Request → VERB_GIVE PRONOUN RequestGiveRest
Request → VERB_MOVEMENT RequestMoveRest

RequestGiveRest → TransportRequest
RequestGiveRest → NUMBER NOUN_MONEY

RequestMoveRest → LocationPhrase
RequestMoveRest → PRONOUN LocationPhrase
RequestMoveRest → PREPOSITION NOUN_PLACE
```

**Step 2: Factor out `VERB_MOVEMENT` (already done)**
The `VERB_MOVEMENT` productions are already factored.

**Final Transformed Grammar:**
```
Request → VERB_GIVE PRONOUN RequestGiveRest
Request → VERB_MOVEMENT RequestMoveRest

RequestGiveRest → TransportRequest
RequestGiveRest → NUMBER NOUN_MONEY

RequestMoveRest → LocationPhrase
RequestMoveRest → PRONOUN LocationPhrase
RequestMoveRest → PREPOSITION NOUN_PLACE
```

**Before/After Comparison:**

| Before (Common Prefix) | After (Factored) |
|----------------------|------------------|
| `Request → VERB_GIVE PRONOUN TransportRequest` | `Request → VERB_GIVE PRONOUN RequestGiveRest` |
| `Request → VERB_GIVE PRONOUN NUMBER NOUN_MONEY` | `RequestGiveRest → TransportRequest` |
| | `RequestGiveRest → NUMBER NOUN_MONEY` |

### Example 2: Complaint with Common Prefix

**Original Grammar:**
```
Complaint → NOUN_TECH VERB_BE ADJ_QUALITY
Complaint → NOUN_TECH VERB_BE ADJ_QUALITY TIME
Complaint → NOUN_MONEY ADJ_QUANTITY
Complaint → NOUN_TRANSPORT VERB_BE ADJ_QUALITY
Complaint → SLANG_EMPHASIS NOUN_TECH VERB_BE ADJ_QUALITY
```

**Problem:** Multiple productions start with `NOUN_TECH VERB_BE ADJ_QUALITY`

**Transformed Grammar:**
```
Complaint → NOUN_TECH VERB_BE ADJ_QUALITY ComplaintTechRest
Complaint → NOUN_MONEY ADJ_QUANTITY
Complaint → NOUN_TRANSPORT VERB_BE ADJ_QUALITY
Complaint → SLANG_EMPHASIS NOUN_TECH VERB_BE ADJ_QUALITY

ComplaintTechRest → ε
ComplaintTechRest → TIME
```

**Explanation:**
- The common prefix `NOUN_TECH VERB_BE ADJ_QUALITY` is factored out
- `ComplaintTechRest` handles the optional `TIME` token
- This makes the grammar LL(1) compatible

---

## 📊 Summary of Transformations

### Transformations Applied

1. **Left Recursion Removal:**
   - `Statement → Statement CONJUNCTION Phrase` → `Statement → Phrase Statement'` with `Statement' → CONJUNCTION Phrase Statement' | ε`
   - `Request → Request CONJUNCTION TransportRequest` → Factored out

2. **Left Factoring:**
   - `Request` productions with `VERB_GIVE PRONOUN` prefix → `RequestGiveRest`
   - `Complaint` productions with `NOUN_TECH VERB_BE ADJ_QUALITY` prefix → `ComplaintTechRest`

### Grammar Properties After Transformation

✅ **No Left Recursion:** All productions are right-recursive or non-recursive  
✅ **No Common Prefixes:** All productions of the same non-terminal have distinct FIRST sets  
✅ **LL(1) Compatible:** The grammar can be parsed with a predictive parser using a single lookahead token

### Verification: FIRST Sets

After transformation, we verify that each non-terminal has disjoint FIRST sets for its productions:

```
FIRST(RequestGiveRest) = {PREPOSITION, NUMBER}
FIRST(RequestMoveRest) = {PREPOSITION, PRONOUN}
FIRST(ComplaintTechRest) = {TIME, ε}
```

These sets are disjoint, confirming the grammar is LL(1).

---

## 🎯 Impact on Parser Implementation

### Before Transformations:
- Parser would loop infinitely on left-recursive rules
- Parser would need backtracking for common prefixes
- Not suitable for LL(1) predictive parsing

### After Transformations:
- Parser can use predictive parsing (single lookahead)
- No backtracking needed
- Efficient O(n) parsing time
- Clear parse tree structure

---

## 📝 Notes

1. **Epsilon Productions:** The `ε` (epsilon) productions are necessary to handle optional elements and terminate recursion.

2. **Parse Tree Structure:** The transformed grammar produces slightly different parse trees, but they represent the same language.

3. **Associativity:** For operators like `CONJUNCTION`, the transformation changes associativity from left to right, but for our use case (natural language), this is acceptable.

4. **Practical Implementation:** In the actual parser implementation (`syntactic_analyzer.py`), we use a more flexible recursive descent approach that handles variations in real-world expressions, but the grammar rules follow these transformations.

---

## 🔗 References

- Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson Education.
- Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Pearson Education.

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Author:** Yaoundé Analyzer Project Team

