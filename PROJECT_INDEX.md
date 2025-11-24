# Project Index - Yaoundé Urban Communication Analyzer

## 📁 File Structure

```
compiler/
├── main.py                 # Main orchestrator (85 lines)
├── lexical_analyzer.py     # Yaoundé multilingual lexer (200 lines)
├── syntactic_analyzer.py   # Grammar and parser (190 lines)
├── Lexer code/            # Traffic light lexical analyzers
│   ├── lexical_analyzer.py      # DFA-based traffic light lexer (159 lines)
│   ├── lexical_analyzer2.py     # Compact traffic sequence validator (50 lines)
│   └── lexical_analyzer3.py     # Cameroonian traffic rules lexer (100 lines)
├── README.md              # Project documentation
├── PROJECT_INDEX.md       # This index file
├── API_REFERENCE.md       # API documentation
└── EXAMPLES.md            # Usage examples and test cases
```

## 🧩 Code Organization (main.py)

### Line Ranges by Component

### Yaoundé Analyzer Components (Separated Architecture)

| File | Lines | Description |
|------|-------|-------------|
| **main.py** | 85 | Main orchestrator importing components |
| **lexical_analyzer.py** | 200 | TokenType, Token, YaoundeLexer classes |
| **syntactic_analyzer.py** | 190 | YaoundeGrammar, YaoundeParser classes |

#### Component Breakdown:

**main.py (85 lines)**
- Imports & Setup (1-10)
- YaoundeAnalyzer class (11-50) 
- Demo & Test Cases (51-85)

**lexical_analyzer.py (200 lines)**
- Token Definitions (1-70): TokenType enum and Token dataclass
- Lexical Analyzer (71-170): YaoundeLexer with patterns
- Testing Module (171-200): Standalone lexer tests

**syntactic_analyzer.py (190 lines)**
- Grammar Engine (1-120): YaoundeGrammar with LL(1)
- Syntactic Parser (121-170): YaoundeParser implementation  
- Testing Module (171-190): Standalone parser tests

## 🚦 Lexer Code Components (309+ lines)

### Traffic Light System Analyzers

| File | Lines | Purpose | Domain |
|------|-------|---------|--------|
| **lexical_analyzer.py** | 159 | Full DFA implementation with validation | Academic/Complete |
| **lexical_analyzer2.py** | 50 | Compact minimized DFA | Efficient/Production |
| **lexical_analyzer3.py** | 100 | Cameroonian traffic rules | Localized/Practical |

#### lexical_analyzer.py Features
- **Token Class**: RED, GREEN, YELLOW, PEDESTRIAN, EOF
- **Lexer Class**: Full tokenization with error handling
- **Validator Class**: DFA state machine (A→B→C→D→E→F)
- **Interactive Mode**: Console input with validation feedback

#### lexical_analyzer2.py Features  
- **Minimized DFA**: 4 states (A', C, D', F-trap)
- **Compact Design**: Single function lexer
- **Extended Alphabet**: Includes LEFT_TURN token
- **Batch Processing**: File or stdin input

#### lexical_analyzer3.py Features
- **Cameroonian Context**: Carrefour Warda traffic rules
- **System Integration**: Command-line and file processing
- **Test Suite**: Built-in valid/invalid test cases
- **Cultural Adaptation**: Local traffic patterns

### 🚦 Traffic Light Token System

#### Core Tokens (5 types)
- **RED (R)**: Stop signal
- **GREEN (G)**: Go signal  
- **YELLOW (Y)**: Caution signal
- **PEDESTRIAN (P)**: Walk signal
- **LEFT_TURN (L)**: Turn signal (extended)

#### Valid Sequences (DFA Rules)
```
Basic Pattern: G → Y → R → P → (R|L)
Minimized States: A'(0) → C(1) → D'(2) [accept]
Trap State: F(3) for invalid transitions
```

#### Example Valid Sequences
- `"GYRPL"` - Complete cycle with left turn
- `"GYRR"` - Skip optional pedestrian
- `"GYRPLGYR"` - Multiple cycles

#### Example Invalid Sequences  
- `"GR"` - Missing yellow transition
- `"PG"` - Pedestrian before red (unsafe)

### 🔄 DFA Implementation Comparison

| Feature | analyzer.py | analyzer2.py | analyzer3.py |
|---------|-------------|--------------|---------------|
| **Architecture** | OOP Classes | Functional | Hybrid |
| **States** | 6 (A-F) | 4 (0-3) | 6 (0-5) |
| **Error Handling** | Exception-based | Return codes | Boolean + message |
| **Input Method** | Interactive | stdin/args | stdin/file/args |
| **Validation** | Step-by-step | Batch | Integrated |
| **Use Case** | Educational | Production | Localized |

### 🌍 Cultural Adaptation (lexical_analyzer3.py)

#### Carrefour Warda Rules
- **Local Context**: Yaoundé intersection patterns
- **Safety Focus**: Pedestrian-priority validation
- **Cultural Integration**: Cameroon-specific traffic behavior
- **System Requirements**: Command-line integration for traffic management

### 🔤 Token Categories (40+ Types)

#### Semantic Tokens
- **NOUN_PLACE** (8 patterns): quartier, carrefour, campus, ICT, université, rond-point, marché, Total
- **NOUN_PERSON** (10 patterns): moto-guy, bendskin-man, patron, boss, mbere, sauveteur, gars
- **NOUN_TRANSPORT** (8 patterns): taxi, bendskin, moto, clandos, car, bus, voiture
- **NOUN_MONEY** (11 patterns): fap, mbongo, kop, francs, CFA, sousous, money, argent
- **NOUN_FOOD** (12 patterns): tchop, ndolé, eru, koki, fufu, water-fufu, achu, banga
- **NOUN_TECH** (13 patterns): call, airtime, crédit, WiFi, réseau, MTN, Orange, Camtel

#### Action Tokens
- **VERB_MOVEMENT** (15 patterns): go, comot, waka, aller, venir, come, reach, arrive
- **VERB_GIVE** (8 patterns): give, send, dash, donner, envoyer, pay, dié
- **VERB_BE** (9 patterns): be, dey, être, sef, stay, tann, trouve
- **VERB_GENERAL** (16 patterns): do, see, hear, tok, parler, dire, mek, make

#### Cultural Phrases
- **PIDGIN_PHRASE** (13 patterns): na so, no be, i don, you don, weti, wetin, how far
- **FRENCH_PHRASE** (18 patterns): c'est comment, ça va, tu vois, on dit, je dis
- **EWONDO_PHRASE** (8 patterns): a ye moan, mbokesso, a sala, ndolo, yaa
- **FULFULDE_PHRASE** (6 patterns): allah yai, wallahi, walahi, inshallah, mashallah

#### Expression Tokens
- **SLANG_EXCLAIM** (15 patterns): ehn, eh, hmmm, garrr, ekiee, oyee, weh, chei
- **SLANG_EMPHASIS** (13 patterns): direct, serious, sérieux, correct, zéro-zéro
- **SLANG_RESPONSE** (10 patterns): masa, mass, bros, brother, chief, sango, paddy

### 🎯 Grammar Rules (Context-Free)

```
S → Statement
Statement → Greeting | Request | Question | Complaint | Negotiation

Production Rules:
├── Greeting → SLANG_RESPONSE [TimePhrase] [StatePhrase]
├── Request → VERB_GIVE PRONOUN TransportRequest
│           | VERB_MOVEMENT LocationPhrase  
├── Question → QuestionWord Statement QUESTION
├── Complaint → ComplaintPhrase SLANG_EXCLAIM
└── Negotiation → PricePhrase MoneyAmount

Supporting Rules:
├── TransportRequest → PREPOSITION NOUN_PLACE
├── LocationPhrase → PREPOSITION NOUN_PLACE
├── TimePhrase → TIME
├── StatePhrase → VERB_BE ADJ_QUALITY
├── QuestionWord → PIDGIN_PHRASE | FRENCH_PHRASE
├── ComplaintPhrase → NOUN_TECH VERB_BE ADJ_QUALITY | NOUN_MONEY ADJ_QUANTITY
├── PricePhrase → NUMBER NOUN_MONEY
└── MoneyAmount → NUMBER NOUN_MONEY
```

### 🔧 Key Classes & Methods

#### YaoundeLexer
- `__init__()`: Initialize with 40+ regex patterns
- `tokenize(text)`: Convert text to Token list
- `analyze_frequency(tokens)`: Generate frequency statistics

#### YaoundeGrammar
- `__init__()`: Set up grammar rules and compute sets
- `compute_first()`: Calculate FIRST sets for LL(1)
- `compute_follow()`: Calculate FOLLOW sets
- `build_ll1_table()`: Generate parsing table

#### YaoundeParser
- `__init__(grammar)`: Initialize with grammar
- `parse(tokens)`: Main parsing entry point
- `parse_statement()`: Parse top-level statements
- `parse_greeting()`, `parse_request()`, etc.: Specific parsers
- `consume(expected_type)`: Token consumption with validation

#### YaoundeAnalyzer
- `__init__()`: Orchestrate lexer, grammar, and parser
- `analyze(text)`: Complete end-to-end analysis
- `print_analysis(result)`: Pretty-print formatted results

### 📊 Analysis Output Structure

```python
{
    'original': str,           # Input text
    'tokens': List[Token],     # Tokenized representation
    'frequency': Dict[str, int], # Token frequency counts
    'parse_result': str,       # Acceptance/rejection message
    'parse_tree': List[str],   # Step-by-step parsing trace
    'accepted': bool          # Grammar validation result
}
```

### 🧪 Test Cases (10 Built-in Examples)

1. **Transport Request**: `"bros drop me for Total"`
2. **Tech Complaint**: `"masa network dey bad today"`
3. **Money Request**: `"give me 500 francs"`
4. **Franc-Anglais Question**: `"je wanda how far ?"`
5. **Campus Navigation**: `"moto-guy go for ICT campus"`
6. **Money Exclamation**: `"ehn mbongo plenty garrr"`
7. **WiFi Complaint**: `"WiFi no dey work hmmm"`
8. **Location Request**: `"bendskin-man send me for carrefour"`
9. **Power Outage**: `"walahi light don comot direct"`
10. **Food Praise**: `"tchop dey correct today bros"`

### 🎓 Academic Features

- **Formal Grammar Theory**: LL(1) parsing implementation
- **Computational Linguistics**: Multilingual tokenization
- **Sociolinguistic Modeling**: Urban code-switching patterns
- **NLP Research**: African language processing

### 🔍 Pattern Recognition Details

#### Regex Patterns (Examples)
```python
# Numbers (priority matching)
r'\d+k|\d+\.\d+|\d+'

# Places with word boundaries
r'\b(quartier|carrefour|campus|ICT|université?|rond[- ]?point)\b'

# Compound words with hyphens
r'\b(moto[- ]?guy|bendskin[- ]?man|water[- ]?fufu)\b'

# French contractions
r'\b(c\'?est comment|ça va|je dis|aujourd\'?hui)\b'
```

#### Token Matching Algorithm
1. Skip whitespace
2. Try each pattern in priority order
3. Match against current position
4. Create token with type, value, position
5. Advance position to end of match
6. Handle unrecognized tokens as UNKNOWN
7. Append EOF token

### 🌐 Multilingual Support Matrix

| Language | Tokens | Phrases | Grammar Integration |
|----------|--------|---------|-------------------|
| **English** | ✓ Core | ✓ Base | ✓ Primary structure |
| **French** | ✓ Full | ✓ Contractions | ✓ Code-switching |
| **Pidgin** | ✓ Extensive | ✓ Expressions | ✓ Natural flow |
| **Fulfulde** | ✓ Islamic | ✓ Exclamations | ✓ Cultural context |
| **Ewondo** | ✓ Regional | ✓ Greetings | ✓ Local integration |
| **Franc-Anglais** | ✓ Mixed | ✓ Hybrid | ✓ Seamless blend |

### 🔄 Processing Flow

```
Input Text → Lexical Analysis → Token Stream → Syntactic Analysis → Parse Result
     ↓              ↓              ↓              ↓                  ↓
  Raw String → Pattern Matching → Token List → Grammar Rules → Accept/Reject
```

### 📈 Performance Characteristics

- **Tokenization**: O(n×m) where n=text length, m=pattern count
- **Parsing**: O(n) for LL(1) grammar
- **Memory**: Linear in input size
- **Extensibility**: Easy pattern addition without core changes

### 🎯 Use Cases

1. **Academic Research**: Computational linguistics studies
2. **Language Technology**: African NLP development  
3. **Cultural Documentation**: Urban language preservation
4. **Educational Tools**: Multilingual learning systems
5. **Social Media**: Content understanding in African contexts