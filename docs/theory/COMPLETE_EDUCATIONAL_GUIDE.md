# Complete Educational Guide: Compiler Construction Concepts

## Table of Contents
1. [Introduction to Compilers](#introduction)
2. [Lexical Analysis (Tokenization)](#lexical-analysis)
3. [Regular Expressions](#regular-expressions)
4. [Syntactic Analysis (Parsing)](#syntactic-analysis)
5. [Context-Free Grammars (CFG)](#context-free-grammars)
6. [LL(1) Parsing](#ll1-parsing)
7. [SLR(1) Parsing](#slr1-parsing)
8. [FIRST and FOLLOW Sets](#first-and-follow-sets)
9. [Left Recursion Removal](#left-recursion-removal)
10. [Left Factoring](#left-factoring)
11. [How Our Project Works](#how-our-project-works)

---

## 1. Introduction to Compilers {#introduction}

### What is a Compiler?
A **compiler** is a program that translates source code written in one language (high-level) into another language (usually machine code or bytecode).

### Compiler Phases
```
Source Code → Lexical Analysis → Syntax Analysis → Semantic Analysis → Code Generation → Target Code
```

### Our Project Focus
We're building a **mini-compiler** that analyzes informal urban communication from Yaoundé. Instead of generating machine code, we:
- **Tokenize** expressions (break into words/tokens)
- **Parse** expressions (check if they follow grammar rules)
- **Analyze** patterns (detect languages, count tokens)

---

## 2. Lexical Analysis (Tokenization) {#lexical-analysis}

### What is Lexical Analysis?
**Lexical Analysis** (also called **tokenization** or **scanning**) is the first phase of compilation. It reads the source code character by character and groups them into **tokens**.

### Analogy
Think of reading a sentence:
- **Characters**: "b", "r", "o", "s", " ", "d", "r", "o", "p"...
- **Tokens**: "bros", "drop", "me", "for", "Total"

### What is a Token?
A **token** is the smallest meaningful unit in a language. Examples:
- **Keywords**: "if", "while", "for"
- **Identifiers**: variable names, function names
- **Operators**: "+", "-", "="
- **Literals**: numbers, strings

### In Our Project
We tokenize Yaoundé expressions:
```
Input: "bros drop me for Total"
Tokens:
  - SLANG_RESPONSE: "bros"
  - VERB_MOVEMENT: "drop"
  - PRONOUN: "me"
  - PREPOSITION: "for"
  - NOUN_PLACE: "Total"
```

### How Tokenization Works
1. **Read input** character by character
2. **Match patterns** using regular expressions
3. **Group characters** into tokens
4. **Return token list**

---

## 3. Regular Expressions {#regular-expressions}

### What is a Regular Expression?
A **regular expression** (regex) is a pattern that describes a set of strings. It's like a template for matching text.

### Basic Regex Symbols
- `.` - matches any character
- `*` - matches zero or more of the preceding
- `+` - matches one or more of the preceding
- `?` - matches zero or one of the preceding
- `|` - OR (matches either pattern)
- `[]` - character class (matches any character inside)
- `^` - start of string
- `$` - end of string
- `\b` - word boundary

### Examples
```regex
\d+           # One or more digits (numbers)
[a-z]+        # One or more lowercase letters
\b(bros|masa) # Word boundary + "bros" OR "masa"
```

### In Our Project
We use regex to identify token types:

```python
# Pattern for slang responses
r'\b(bros|masa|mass|chief|sango)\b'

# Pattern for verbs
r'\b(drop|send|give|go|come)\b'

# Pattern for places
r'\b(Total|campus|ICT|carrefour)\b'
```

### How It Works
1. **Define patterns** for each token type
2. **Try each pattern** in order
3. **Match longest** possible token
4. **Return token** with type and value

---

## 4. Syntactic Analysis (Parsing) {#syntactic-analysis}

### What is Syntactic Analysis?
**Syntactic Analysis** (also called **parsing**) checks if tokens form a valid sentence according to grammar rules.

### Analogy
- **Lexical Analysis**: Breaking "The cat sat" into words
- **Syntactic Analysis**: Checking if it's a valid sentence (Subject-Verb structure)

### What Does a Parser Do?
1. **Reads tokens** from lexical analyzer
2. **Checks grammar rules** to see if tokens match
3. **Builds parse tree** showing structure
4. **Reports errors** if syntax is invalid

### Example
```
Tokens: [SLANG_RESPONSE, VERB_MOVEMENT, PRONOUN, PREPOSITION, NOUN_PLACE]
Grammar Rule: Request → VERB_MOVEMENT LocationPhrase
              LocationPhrase → PREPOSITION NOUN_PLACE

Result: ✓ ACCEPTED (matches Request rule)
```

---

## 5. Context-Free Grammars (CFG) {#context-free-grammars}

### What is a Grammar?
A **grammar** is a set of rules that define valid sentence structures in a language.

### Grammar Notation
- **Non-terminals**: Abstract concepts (written in CAPS or with angle brackets)
  - Example: `Statement`, `Request`, `Greeting`
- **Terminals**: Actual tokens/words (written in lowercase or quotes)
  - Example: `bros`, `drop`, `me`
- **Production Rules**: How to expand non-terminals
  - Example: `Request → VERB_MOVEMENT LocationPhrase`

### Grammar Components
```
Grammar = (N, T, P, S)
- N: Non-terminals (variables)
- T: Terminals (tokens)
- P: Production rules
- S: Start symbol
```

### Our Grammar Example
```
S → Statement
Statement → Greeting | Request | Question | Complaint | Negotiation
Request → VERB_MOVEMENT LocationPhrase
LocationPhrase → PREPOSITION NOUN_PLACE
```

### Reading Grammar Rules
- `→` means "can be replaced by"
- `|` means "OR" (alternative)
- Order matters (try first rule, then second, etc.)

---

## 6. LL(1) Parsing {#ll1-parsing}

### What is LL(1)?
**LL(1)** stands for:
- **L**: Left-to-right scan of input
- **L**: Leftmost derivation (expand leftmost non-terminal first)
- **(1)**: One token lookahead (peek at next token)

### How LL(1) Works
1. **Read tokens** left to right
2. **Look at next token** (lookahead)
3. **Choose production rule** based on lookahead
4. **Expand non-terminal** using chosen rule
5. **Repeat** until all tokens matched

### LL(1) Parsing Table
A table that tells which rule to use based on:
- Current non-terminal
- Next token (lookahead)

```
Table[NonTerminal][Token] = Production Rule
```

### Example
```
Table[Request][VERB_MOVEMENT] = Request → VERB_MOVEMENT LocationPhrase
Table[Request][VERB_GIVE] = Request → VERB_GIVE PRONOUN TransportRequest
```

### Advantages
- ✅ Simple to implement
- ✅ Fast (O(n) time)
- ✅ Easy to understand

### Disadvantages
- ❌ Requires grammar to be LL(1) compatible
- ❌ Can't handle left recursion directly
- ❌ Limited lookahead

---

## 7. SLR(1) Parsing {#slr1-parsing}

### What is SLR(1)?
**SLR(1)** stands for:
- **S**: Simple
- **L**: Left-to-right scan
- **R**: Rightmost derivation (in reverse)
- **(1)**: One token lookahead

### How SLR(1) Works
1. **Build states** from grammar rules
2. **Create automaton** (state machine)
3. **Shift** tokens onto stack
4. **Reduce** when rule matches
5. **Accept** when start symbol reached

### SLR(1) vs LL(1)
| Feature | LL(1) | SLR(1) |
|---------|-------|--------|
| Direction | Top-down | Bottom-up |
| Derivation | Leftmost | Rightmost (reverse) |
| Stack | Non-terminals | States |
| Complexity | Simpler | More complex |
| Power | Less powerful | More powerful |

### When to Use SLR(1)?
- Grammar has left recursion
- LL(1) can't handle the grammar
- Need more parsing power

### In Our Project
We use **recursive descent** (similar to LL(1)) because:
- Grammar is relatively simple
- Easier to implement
- More flexible for informal language

---

## 8. FIRST and FOLLOW Sets {#first-and-follow-sets}

### What are FIRST Sets?
**FIRST(X)** = Set of terminals that can appear at the start of strings derived from X.

### Example
```
FIRST(Request) = {VERB_GIVE, VERB_MOVEMENT}
```
This means a Request can start with either VERB_GIVE or VERB_MOVEMENT.

### How to Compute FIRST
1. If X is a terminal: `FIRST(X) = {X}`
2. If X → ε (empty): Add ε to FIRST(X)
3. If X → Y₁Y₂...Yₖ:
   - Add FIRST(Y₁) to FIRST(X)
   - If ε ∈ FIRST(Y₁), add FIRST(Y₂)
   - Continue until no ε found

### What are FOLLOW Sets?
**FOLLOW(X)** = Set of terminals that can appear immediately after X in some derivation.

### Example
```
FOLLOW(Greeting) = {$, QUESTION}
```
This means after a Greeting, we might see end of input ($) or a question mark.

### How to Compute FOLLOW
1. Add $ to FOLLOW(start symbol)
2. For rule A → αBβ:
   - Add FIRST(β) - {ε} to FOLLOW(B)
   - If ε ∈ FIRST(β), add FOLLOW(A) to FOLLOW(B)
3. Repeat until no changes

### Why We Need Them
- **LL(1) parsing table**: Uses FIRST sets to choose rules
- **Error detection**: Know what tokens are expected
- **Grammar validation**: Check if grammar is LL(1)

### In Our Project
```python
FIRST(Statement) = {SLANG_RESPONSE, VERB_GIVE, VERB_MOVEMENT, 
                   PIDGIN_PHRASE, FRENCH_PHRASE, NOUN_TECH, ...}

FOLLOW(Statement) = {$, QUESTION}
```

---

## 9. Left Recursion Removal {#left-recursion-removal}

### What is Left Recursion?
**Left recursion** occurs when a non-terminal appears at the start of its own production:

```
A → Aα | β
```

### Problem with Left Recursion
- **LL(1) parsers** can't handle left recursion
- Causes infinite loop: A tries to expand A, which tries to expand A...

### How to Remove Left Recursion

#### Original (Left Recursive):
```
A → Aα | β
```

#### After Removal:
```
A → βA'
A' → αA' | ε
```

### Example from Our Grammar
If we had:
```
Request → Request PREPOSITION NOUN_PLACE | VERB_MOVEMENT NOUN_PLACE
```

After removal:
```
Request → VERB_MOVEMENT NOUN_PLACE Request'
Request' → PREPOSITION NOUN_PLACE Request' | ε
```

### Why It Matters
- Makes grammar compatible with LL(1)
- Allows top-down parsing
- Prevents infinite loops

---

## 10. Left Factoring {#left-factoring}

### What is Left Factoring?
**Left factoring** removes ambiguity when multiple productions start with the same symbols.

### Problem
```
A → αβ | αγ
```
Parser can't decide which rule to use when seeing α.

### How to Factor
Extract common prefix:

```
A → αA'
A' → β | γ
```

### Example
#### Before:
```
Request → VERB_GIVE PRONOUN TransportRequest
Request → VERB_GIVE PRONOUN NUMBER NOUN_MONEY
```

#### After:
```
Request → VERB_GIVE PRONOUN RequestRest
RequestRest → TransportRequest | NUMBER NOUN_MONEY
```

### Why It Matters
- Removes ambiguity
- Makes grammar LL(1) compatible
- Allows deterministic parsing

---

## 11. How Our Project Works {#how-our-project-works}

### Step-by-Step Process

#### Step 1: Input
```
User enters: "bros drop me for Total"
```

#### Step 2: Lexical Analysis (Tokenization)
```python
lexer = YaoundeLexer()
tokens = lexer.tokenize("bros drop me for Total")

# Result:
# [
#   Token(SLANG_RESPONSE, "bros", 0),
#   Token(VERB_MOVEMENT, "drop", 5),
#   Token(PRONOUN, "me", 10),
#   Token(PREPOSITION, "for", 13),
#   Token(NOUN_PLACE, "Total", 17),
#   Token(EOF, "", -1)
# ]
```

**How it works:**
1. Read input character by character
2. Match against regex patterns
3. When pattern matches, create token
4. Continue until end of input

#### Step 3: Syntactic Analysis (Parsing)
```python
parser = YaoundeParser(grammar)
accepted, message, parse_tree = parser.parse(tokens)

# Parser checks:
# 1. Does it match Statement?
# 2. Statement → Request (try this)
# 3. Request → VERB_MOVEMENT LocationPhrase
# 4. Check: first token is VERB_MOVEMENT? ✓
# 5. LocationPhrase → PREPOSITION NOUN_PLACE
# 6. Check: next tokens are PREPOSITION NOUN_PLACE? ✓
# 7. Result: ✓ ACCEPTED
```

**How it works:**
1. Start with Statement (start symbol)
2. Try each production rule
3. Match tokens against rule
4. If match, continue; if not, try next rule
5. If all tokens matched, ACCEPT; else REJECT

#### Step 4: Language Detection
```python
languages = analyzer.detect_languages(tokens)
# Result: ["English", "Franc-Anglais"]
```

**How it works:**
1. Check each token's type
2. Look for language indicators:
   - French: "je", "est", "mal"
   - Pidgin: "dey", "na", "wan"
   - English: "drop", "me", "for"
   - Slang: "bros", "masa"
3. Collect all detected languages

#### Step 5: Output
```
✓ ACCEPTED - Valid Yaoundé expression
Languages: English, Franc-Anglais
Tokens: 5
Parse Tree: [shows derivation steps]
```

### Complete Flow Diagram
```
Input String
    ↓
[Lexical Analyzer]
    ↓
Token Stream
    ↓
[Syntax Analyzer]
    ↓
Parse Tree / Error
    ↓
[Language Detector]
    ↓
Final Result
```

### Real Example Walkthrough

**Input:** `"masa network dey bad today"`

1. **Tokenization:**
   ```
   SLANG_RESPONSE: "masa"
   NOUN_TECH: "network"
   VERB_BE: "dey"
   ADJ_QUALITY: "bad"
   TIME: "today"
   ```

2. **Parsing:**
   ```
   Statement → Complaint
   Complaint → ComplaintPhrase TIME
   ComplaintPhrase → NOUN_TECH VERB_BE ADJ_QUALITY
   
   Check:
   - "network" = NOUN_TECH ✓
   - "dey" = VERB_BE ✓
   - "bad" = ADJ_QUALITY ✓
   - "today" = TIME ✓
   
   Result: ✓ ACCEPTED
   ```

3. **Language Detection:**
   ```
   - "masa" → Franc-Anglais
   - "network" → English
   - "dey" → Pidgin
   - "bad" → English
   - "today" → English
   
   Languages: English, Pidgin, Franc-Anglais
   ```

---

## Summary

### Key Concepts
1. **Lexical Analysis**: Break text into tokens using regex
2. **Syntactic Analysis**: Check if tokens follow grammar rules
3. **Grammar**: Rules defining valid sentence structures
4. **LL(1)**: Top-down parsing with 1-token lookahead
5. **SLR(1)**: Bottom-up parsing using state machine
6. **FIRST/FOLLOW**: Sets used for parsing decisions
7. **Left Recursion Removal**: Transform grammar for LL(1)
8. **Left Factoring**: Remove ambiguity from grammar

### Our Project's Approach
- **Lexer**: Uses regex patterns to tokenize
- **Parser**: Recursive descent (LL(1)-like)
- **Grammar**: Context-free grammar for Yaoundé expressions
- **Flexibility**: Handles informal, code-mixed language

---

## Quick Reference

### Token Types in Our Project
- `SLANG_RESPONSE`: bros, masa, chief
- `VERB_MOVEMENT`: drop, go, come
- `NOUN_PLACE`: Total, campus, ICT
- `PREPOSITION`: for, to, at
- `PRONOUN`: me, you, we
- `NOUN_TECH`: network, phone, airtime
- `VERB_BE`: dey, is, est
- `ADJ_QUALITY`: bad, good, mal
- `TIME`: today, now, tomorrow
- And many more...

### Grammar Rules (Simplified)
```
Statement → Greeting | Request | Question | Complaint | Negotiation
Greeting → SLANG_RESPONSE [TimePhrase] [StatePhrase]
Request → VERB_MOVEMENT LocationPhrase | VERB_GIVE PRONOUN ...
Complaint → ComplaintPhrase [SLANG_EXCLAIM] [TIME]
Question → QuestionWord Statement QUESTION
```

---

**This guide explains all the concepts you need to understand and present your compiler construction project!**

