# Yaoundé Urban Communication Grammar Documentation

## 📚 Context-Free Grammar (CFG)

This document provides a complete description of the grammar used for parsing Yaoundé urban communication expressions.

## 🔄 Grammar Rules

### Start Symbol
```
S → Statement
```

### Main Production Rules

```
Statement → Greeting | Request | Question | Complaint | Negotiation
```

### Detailed Productions

#### Greeting
```
Greeting → SLANG_RESPONSE
         | SLANG_RESPONSE TimePhrase
         | SLANG_RESPONSE StatePhrase
         | SLANG_RESPONSE TimePhrase StatePhrase
```

**Examples:**
- `bros`
- `bros today`
- `bros dey good`
- `bros today dey good`

#### Request
```
Request → VERB_GIVE PRONOUN TransportRequest
        | VERB_GIVE PRONOUN NUMBER NOUN_MONEY
        | VERB_MOVEMENT LocationPhrase
        | VERB_MOVEMENT PRONOUN LocationPhrase
        | VERB_MOVEMENT PREPOSITION NOUN_PLACE
```

**Examples:**
- `give me for Total`
- `give me 500 francs`
- `drop me for Total`
- `go for campus`

#### Question
```
Question → QuestionWord Statement QUESTION
```

**Examples:**
- `je wanda how far ?`
- `wetin you dey do ?`

#### Complaint
```
Complaint → ComplaintPhrase
          | ComplaintPhrase SLANG_EXCLAIM
          | ComplaintPhrase TIME
          | ComplaintPhrase SLANG_EXCLAIM TIME
```

**Examples:**
- `network dey bad`
- `network dey bad today`
- `light don comot direct`

#### Negotiation
```
Negotiation → PricePhrase
             | VERB_GIVE PRONOUN NUMBER NOUN_MONEY
```

**Examples:**
- `500 francs`
- `give me 2k`

### Supporting Rules

```
TransportRequest → PREPOSITION NOUN_PLACE
LocationPhrase → PREPOSITION NOUN_PLACE
TimePhrase → TIME
StatePhrase → VERB_BE ADJ_QUALITY
QuestionWord → PIDGIN_PHRASE | FRENCH_PHRASE
ComplaintPhrase → NOUN_TECH VERB_BE ADJ_QUALITY
                | NOUN_TECH VERB_BE ADJ_QUALITY TIME
                | NOUN_MONEY ADJ_QUANTITY
                | NOUN_TRANSPORT VERB_BE ADJ_QUALITY
                | SLANG_EMPHASIS NOUN_TECH VERB_BE ADJ_QUALITY
PricePhrase → NUMBER NOUN_MONEY
MoneyAmount → NUMBER NOUN_MONEY
```

## 🔤 FIRST Sets

The FIRST set of a non-terminal is the set of terminals that can begin strings derived from that non-terminal.

### Key FIRST Sets

```
FIRST(S) = {SLANG_RESPONSE, VERB_GIVE, VERB_MOVEMENT, PIDGIN_PHRASE, FRENCH_PHRASE, 
            NOUN_TECH, NOUN_MONEY, NOUN_TRANSPORT, NUMBER, SLANG_EMPHASIS}

FIRST(Statement) = {SLANG_RESPONSE, VERB_GIVE, VERB_MOVEMENT, PIDGIN_PHRASE, 
                    FRENCH_PHRASE, NOUN_TECH, NOUN_MONEY, NOUN_TRANSPORT, 
                    NUMBER, SLANG_EMPHASIS}

FIRST(Greeting) = {SLANG_RESPONSE}

FIRST(Request) = {VERB_GIVE, VERB_MOVEMENT}

FIRST(Question) = {PIDGIN_PHRASE, FRENCH_PHRASE}

FIRST(Complaint) = {NOUN_TECH, NOUN_MONEY, NOUN_TRANSPORT, SLANG_EMPHASIS}

FIRST(Negotiation) = {NUMBER, VERB_GIVE}
```

## 🔍 FOLLOW Sets

The FOLLOW set of a non-terminal is the set of terminals that can appear immediately after that non-terminal in some sentential form.

### Key FOLLOW Sets

```
FOLLOW(S) = {$}

FOLLOW(Statement) = {QUESTION, $}

FOLLOW(Greeting) = {$, QUESTION}

FOLLOW(Request) = {$, QUESTION}

FOLLOW(Question) = {$, QUESTION}

FOLLOW(Complaint) = {$, QUESTION}

FOLLOW(Negotiation) = {$, QUESTION}
```

## 📊 LL(1) Parsing Table

The LL(1) parsing table M[A, a] specifies which production to use when non-terminal A is on the stack and terminal a is the current input.

### Sample Table Entries

```
M[S, SLANG_RESPONSE] = [Statement]
M[S, VERB_GIVE] = [Statement]
M[S, VERB_MOVEMENT] = [Statement]
M[S, PIDGIN_PHRASE] = [Statement]
M[S, FRENCH_PHRASE] = [Statement]
M[S, NOUN_TECH] = [Statement]
M[S, NUMBER] = [Statement]

M[Statement, SLANG_RESPONSE] = [Greeting]
M[Statement, VERB_GIVE] = [Request]
M[Statement, VERB_MOVEMENT] = [Request]
M[Statement, PIDGIN_PHRASE] = [Question]
M[Statement, FRENCH_PHRASE] = [Question]
M[Statement, NOUN_TECH] = [Complaint]
M[Statement, NUMBER] = [Negotiation]

M[Greeting, SLANG_RESPONSE] = [SLANG_RESPONSE, TimePhrase, StatePhrase]
M[Request, VERB_GIVE] = [VERB_GIVE, PRONOUN, NUMBER, NOUN_MONEY]
M[Request, VERB_MOVEMENT] = [VERB_MOVEMENT, LocationPhrase]
```

## ✅ Grammar Properties

### Left Recursion Removal
The grammar has been transformed to remove left recursion. All productions are in a form suitable for LL(1) parsing.

### Left Factoring
Common prefixes have been factored out where necessary to ensure the grammar is LL(1).

### LL(1) Property
The grammar is designed to be LL(1), meaning:
- For each non-terminal A and each terminal a, there is at most one production A → α such that a ∈ FIRST(α) or (ε ∈ FIRST(α) and a ∈ FOLLOW(A))
- The parsing table has no conflicts (each entry has at most one production)

## 🎯 Expression Categories

### 1. Transport & Commuting
- `bros drop me for Total`
- `je go campus now`
- `Bros, na taxi or clando?`

### 2. Internet Connectivity
- `masa network dey bad today`
- `Je wan call my friend, phone no dey`

### 3. Electricity Issues
- `walahi light don comot direct`
- `light dey comot for quartier`

### 4. Market Bargaining
- `give me 500 francs`
- `Je wan buy fufu, where e dey?`

### 5. Weather & Seasonal
- `rain don fall plenty today`
- `water dey plenty for road`

### 6. Security & Checkpoints
- `Bros, you fit show me ICT junction?`
- `Je wanda where checkpoint dey?`

### 7. University Life
- `Je go campus now, you dey come?`
- `Bros, na campus you dey go?`

## 📝 Notes

1. **Multilingual Support**: The grammar handles code-switching between English, French, Pidgin, and local languages seamlessly.

2. **Flexibility**: Optional elements (marked with `?` in BNF notation) are handled through multiple production rules.

3. **Error Handling**: The parser gracefully handles expressions that don't fully match the grammar, providing informative error messages.

4. **Extensibility**: New expression patterns can be added by extending the grammar rules and updating the FIRST/FOLLOW sets.

## 🔧 Implementation Details

- **Parser Type**: LL(1) table-driven parser
- **Table Construction**: Automatic from FIRST/FOLLOW sets
- **Error Recovery**: Basic error reporting with position information
- **Parse Tree**: Generated during parsing for visualization

## 📚 References

- Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson Education.
- Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Pearson Education.

