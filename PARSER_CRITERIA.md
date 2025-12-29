# Parser Acceptance Criteria

## 📋 Overview

The Yaoundé Analyzer uses a **flexible recursive descent parser** that accepts expressions based on recognizable patterns in Yaoundé urban communication.

## ✅ Acceptance Criteria

An expression is **ACCEPTED** if it matches one or more of these patterns:

### 1. **Greetings** ✓
- **Pattern**: `SLANG_RESPONSE` (optional additional content)
- **Examples**:
  - `bros` ✓
  - `masa` ✓
  - `chief` ✓

### 2. **Transport Requests** ✓
- **Pattern**: `VERB_MOVEMENT` + optional `PRONOUN` + `PREPOSITION` + `NOUN_PLACE`
- **Examples**:
  - `bros drop me for Total` ✓
  - `drop me for Total` ✓
  - `go for campus` ✓
  - `je go campus now` ✓

### 3. **Money Requests** ✓
- **Pattern**: `VERB_GIVE` + optional `PRONOUN` + `NUMBER` + `NOUN_MONEY`
- **Examples**:
  - `give me 500 francs` ✓
  - `give me 2k` ✓
  - `send me urgent 2k` ✓

### 4. **Complaints** ✓
- **Pattern**: Optional `SLANG_EMPHASIS` + `NOUN` (tech/money/transport) + optional `VERB_BE` + optional `ADJ` + optional `TIME` + optional `SLANG_EXCLAIM`
- **Examples**:
  - `network dey bad` ✓
  - `masa network dey bad today` ✓
  - `light don comot direct` ✓
  - `walahi light don comot direct` ✓

### 5. **Questions** ✓
- **Pattern**: `PIDGIN_PHRASE` or `FRENCH_PHRASE` + content + optional `QUESTION`
- **Examples**:
  - `je wanda how far ?` ✓
  - `wetin you dey do ?` ✓
  - `how far` ✓

### 6. **Negotiations** ✓
- **Pattern**: `NUMBER` + `NOUN_MONEY`
- **Examples**:
  - `500 francs` ✓
  - `2k` ✓

## 🔄 Flexible Parsing Rules

The parser is designed to be **flexible** to handle the informal nature of Yaoundé communication:

1. **Optional Elements**: Many components are optional
   - Pronouns can be omitted
   - Time phrases are optional
   - Exclamations are optional

2. **Prefix Handling**: 
   - Expressions starting with `SLANG_RESPONSE` (like "bros", "masa") are accepted even if followed by other patterns
   - Example: `bros drop me for Total` is parsed as: greeting prefix + request

3. **Partial Matches**:
   - If an expression partially matches a pattern, it may still be accepted
   - The parser looks for recognizable structures rather than strict grammar compliance

4. **Token Recognition**:
   - Expressions with mostly recognized tokens are more likely to be accepted
   - Unknown tokens don't immediately cause rejection

## ❌ Rejection Criteria

An expression is **REJECTED** if:

1. **No Recognizable Pattern**: 
   - Contains only unrecognized tokens
   - Example: `xyzabc unknownword123` ✗

2. **Empty Input**: 
   - No tokens generated
   - Example: `   ` (only whitespace) ✗

3. **Invalid Token Sequence**:
   - Tokens don't form any recognizable pattern
   - Example: `? ! , .` (only punctuation) ✗

## 🎯 Examples of Accepted vs Rejected

### ✅ ACCEPTED Expressions

```
bros drop me for Total
  → Greeting prefix + Transport request
  → ACCEPTED ✓

give me 500 francs
  → Money request
  → ACCEPTED ✓

masa network dey bad today
  → Greeting prefix + Complaint
  → ACCEPTED ✓

je wanda how far ?
  → Question
  → ACCEPTED ✓

walahi light don comot direct
  → Complaint with emphasis
  → ACCEPTED ✓
```

### ❌ REJECTED Expressions

```
xyzabc123
  → Only unknown tokens
  → REJECTED ✗

? ! .
  → Only punctuation, no content
  → REJECTED ✗
```

## 📊 Acceptance Statistics

Based on the collected data:
- **Most expressions are ACCEPTED** because they follow common Yaoundé patterns
- **Rejection is rare** and usually indicates:
  - Unrecognized vocabulary
  - Invalid token sequences
  - Empty or malformed input

## 🔧 Parser Behavior

### How It Works

1. **Tokenization First**: 
   - Expression is tokenized by the lexical analyzer
   - Each word/phrase is assigned a token type

2. **Pattern Matching**:
   - Parser tries to match token sequence to known patterns
   - Uses recursive descent with flexible matching

3. **Acceptance Decision**:
   - If tokens match a pattern → ACCEPTED ✓
   - If tokens partially match → ACCEPTED ✓ (with note)
   - If no pattern matches → REJECTED ✗

### Parse Tree Generation

- Accepted expressions generate a parse tree showing:
  - Which patterns were matched
  - Token consumption order
  - Parse steps

## 💡 Tips for Understanding Results

1. **Check Tokenization First**:
   - Look at the Tokens tab to see how the expression was tokenized
   - If tokens look correct, parsing should work

2. **Review Parse Steps**:
   - The Parse Result tab shows step-by-step parsing
   - This explains why an expression was accepted/rejected

3. **Grammar Info**:
   - Check the Grammar Info tab to see supported patterns
   - This helps understand what the parser expects

## 🎓 Academic Note

The parser uses a **flexible recursive descent** approach rather than strict LL(1) table-driven parsing. This is appropriate for:

- **Informal language**: Yaoundé expressions are naturally flexible
- **Code-switching**: Multiple languages mixed together
- **Real-world data**: Collected expressions may not follow strict grammar

The grammar rules define the **ideal structure**, but the parser accepts **variations** that are common in actual usage.

---

**For best results**: Use expressions from the collected data or follow the example patterns shown in the GUI.

