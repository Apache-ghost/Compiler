# API Reference - Yaoundé Urban Communication Analyzer

## 📚 Core Classes

### Token
```python
@dataclass
class Token:
    type: TokenType      # Token classification
    value: str          # Original text
    position: int       # Character position in input
```

**Example Usage:**
```python
token = Token(TokenType.SLANG_RESPONSE, "bros", 0)
print(token)  # Token(SLANG_RESPONSE, 'bros')
```

### TokenType (Enum)
Complete enumeration of all supported token types.

#### Noun Categories
- `NOUN_PLACE`: quartier, carrefour, campus, ICT, Total
- `NOUN_PERSON`: moto-guy, mbere, patron, boss
- `NOUN_TRANSPORT`: taxi, bendskin, moto, clandos
- `NOUN_MONEY`: fap, mbongo, kop, francs, CFA
- `NOUN_FOOD`: tchop, ndolé, eru, koki, fufu
- `NOUN_TECH`: call, airtime, WiFi, network, MTN

#### Verb Categories
- `VERB_MOVEMENT`: go, comot, waka, aller, come
- `VERB_GIVE`: give, send, dash, donner, pay
- `VERB_BE`: be, dey, être, stay, tann
- `VERB_GENERAL`: do, see, hear, tok, parler, make

#### Cultural Phrases
- `PIDGIN_PHRASE`: na so, no be, i don, wetin, how far
- `FRENCH_PHRASE`: c'est comment, ça va, tu vois, je dis
- `EWONDO_PHRASE`: a ye moan, mbokesso, ndolo
- `FULFULDE_PHRASE`: allah yai, wallahi, inshallah

#### Expression Types
- `SLANG_EXCLAIM`: ehn, hmmm, garrr, ekiee, weh
- `SLANG_EMPHASIS`: direct, serious, correct, trop
- `SLANG_RESPONSE`: masa, bros, chief, sango

#### Grammar Elements
- `PREPOSITION`: for, na, avec, à, from
- `CONJUNCTION`: and, avec, na, but, mais
- `DETERMINER`: the, di, le, la, un
- `PRONOUN`: me, i, you, we, tu, je
- `ADJ_QUALITY`: bon, nye, correct, bad
- `ADJ_QUANTITY`: plenty, small, trop, many
- `NUMBER`: 100, 500, 2k, 5k
- `TIME`: today, tomorrow, now, maintenant

---

## 🔤 YaoundeLexer Class

### Constructor
```python
def __init__(self):
    """Initialize lexer with predefined patterns"""
```

### Methods

#### tokenize()
```python
def tokenize(self, text: str) -> List[Token]:
    """
    Convert input text into a list of tokens.
    
    Args:
        text: Input string in any supported language
        
    Returns:
        List of Token objects with EOF token at end
        
    Example:
        lexer = YaoundeLexer()
        tokens = lexer.tokenize("bros drop me for Total")
        # Returns: [Token(SLANG_RESPONSE, 'bros'), 
        #          Token(VERB_MOVEMENT, 'drop'), ...]
    """
```

#### analyze_frequency()
```python
def analyze_frequency(self, tokens: List[Token]) -> Dict[str, int]:
    """
    Generate frequency analysis of tokens.
    
    Args:
        tokens: List of tokens from tokenize()
        
    Returns:
        Dictionary mapping "TYPE: value" to count
        
    Example:
        freq = lexer.analyze_frequency(tokens)
        # Returns: {"SLANG_RESPONSE: bros": 1,
        #          "VERB_MOVEMENT: drop": 1, ...}
    """
```

---

## 📝 YaoundeGrammar Class

### Constructor
```python
def __init__(self):
    """
    Initialize grammar with rules and compute parsing sets.
    Automatically builds FIRST sets, FOLLOW sets, and LL(1) table.
    """
```

### Properties
- `rules`: Dictionary of grammar production rules
- `first_sets`: FIRST sets for all non-terminals  
- `follow_sets`: FOLLOW sets for all non-terminals
- `parsing_table`: LL(1) parsing table

### Methods

#### compute_first()
```python
def compute_first(self) -> Dict[str, Set[str]]:
    """
    Compute FIRST sets for grammar using fixed-point algorithm.
    
    Returns:
        Dictionary mapping non-terminals to their FIRST sets
    """
```

#### compute_follow()
```python
def compute_follow(self) -> Dict[str, Set[str]]:
    """
    Compute FOLLOW sets for grammar.
    
    Returns:
        Dictionary mapping non-terminals to their FOLLOW sets
    """
```

#### build_ll1_table()
```python
def build_ll1_table(self) -> Dict[Tuple[str, str], List[str]]:
    """
    Build LL(1) parsing table from FIRST/FOLLOW sets.
    
    Returns:
        Dictionary mapping (non_terminal, terminal) to production
    """
```

---

## 🔍 YaoundeParser Class

### Constructor
```python
def __init__(self, grammar: YaoundeGrammar):
    """
    Initialize parser with grammar rules.
    
    Args:
        grammar: YaoundeGrammar instance
    """
```

### Main Methods

#### parse()
```python
def parse(self, tokens: List[Token]) -> Tuple[bool, str, List[str]]:
    """
    Parse token stream using recursive descent.
    
    Args:
        tokens: List of tokens from lexer
        
    Returns:
        Tuple of (accepted: bool, message: str, parse_tree: List[str])
        
    Example:
        parser = YaoundeParser(grammar)
        accepted, msg, tree = parser.parse(tokens)
        # Returns: (True, "✓ ACCEPTED - Valid expression", [...])
    """
```

### Helper Methods

#### current_token()
```python
def current_token(self) -> Token:
    """Get current token without consuming it"""
```

#### consume()
```python
def consume(self, expected_type: TokenType = None) -> Token:
    """
    Consume and return current token.
    
    Args:
        expected_type: Optional type validation
        
    Returns:
        Consumed token
        
    Raises:
        Exception: If expected_type doesn't match current token
    """
```

### Parse Methods
- `parse_statement()`: Parse top-level statements
- `parse_greeting()`: Parse greeting expressions  
- `parse_request()`: Parse request/command expressions
- `parse_question()`: Parse question expressions
- `parse_complaint()`: Parse complaint expressions
- `parse_negotiation()`: Parse negotiation expressions

---

## 🎯 YaoundeAnalyzer Class

### Constructor
```python
def __init__(self):
    """
    Initialize complete analyzer with lexer, grammar, and parser.
    """
```

### Main Methods

#### analyze()
```python
def analyze(self, text: str) -> Dict:
    """
    Perform complete lexical and syntactic analysis.
    
    Args:
        text: Input string in any supported language
        
    Returns:
        Dictionary with analysis results:
        {
            'original': str,           # Input text
            'tokens': List[Token],     # Tokenized form
            'frequency': Dict[str, int], # Token frequencies
            'parse_result': str,       # Accept/reject message
            'parse_tree': List[str],   # Parse steps
            'accepted': bool          # Grammar validation
        }
        
    Example:
        analyzer = YaoundeAnalyzer()
        result = analyzer.analyze("bros drop me for Total")
        print(result['accepted'])  # True
    """
```

#### print_analysis()
```python
def print_analysis(self, result: Dict):
    """
    Pretty print analysis results to console.
    
    Args:
        result: Dictionary from analyze() method
        
    Output:
        Formatted display including:
        - Original text and parse result
        - Token breakdown
        - Frequency statistics  
        - Parse tree trace (first 10 steps)
    """
```

---

## 📊 Data Structures

### Analysis Result Dictionary
```python
{
    'original': str,              # "bros drop me for Total"
    'tokens': [                   # List of Token objects
        Token(SLANG_RESPONSE, 'bros', 0),
        Token(VERB_MOVEMENT, 'drop', 5),
        # ...
    ],
    'frequency': {                # Token frequency counts
        'SLANG_RESPONSE: bros': 1,
        'VERB_MOVEMENT: drop': 1,
        # ...
    },
    'parse_result': str,          # "✓ ACCEPTED - Valid expression"
    'parse_tree': [               # Step-by-step parsing
        'Matched: Token(SLANG_RESPONSE, \'bros\')',
        'Matched: Token(VERB_MOVEMENT, \'drop\')',
        # ...
    ],
    'accepted': bool             # True/False
}
```

### Grammar Rules Structure
```python
{
    'S': [['Statement']],
    'Statement': [
        ['Greeting'],
        ['Request'], 
        ['Question'],
        ['Complaint'],
        ['Negotiation']
    ],
    'Greeting': [
        ['SLANG_RESPONSE'],
        ['SLANG_RESPONSE', 'TimePhrase'],
        # ...
    ]
    # ...
}
```

---

## 🚀 Quick Start Examples

### Basic Analysis
```python
from main import YaoundeAnalyzer

# Initialize analyzer
analyzer = YaoundeAnalyzer()

# Analyze expression
result = analyzer.analyze("masa give me 500 francs")

# Check if accepted
if result['accepted']:
    print("Valid Yaoundé expression!")
    
# Show tokens
for token in result['tokens']:
    print(f"{token.type.name}: {token.value}")
```

### Custom Lexing
```python
from main import YaoundeLexer

# Just tokenize without parsing
lexer = YaoundeLexer()
tokens = lexer.tokenize("walahi network don bad garrr")

# Analyze frequency
frequency = lexer.analyze_frequency(tokens)
print(frequency)
```

### Grammar Analysis
```python
from main import YaoundeGrammar

# Access grammar internals
grammar = YaoundeGrammar()

# Check FIRST sets
print("FIRST(Statement):", grammar.first_sets['Statement'])

# Check production rules  
print("Rules for Request:", grammar.rules['Request'])
```

---

## ⚠️ Error Handling

### Common Exceptions
- **Tokenization**: Unknown tokens create `TokenType.UNKNOWN`
- **Parsing**: Invalid syntax raises `Exception` with descriptive message
- **Grammar**: Missing rules handled gracefully with fallback parsing

### Error Messages
- `"✓ ACCEPTED - Valid Yaoundé expression"` - Successful parse
- `"✗ REJECTED - Incomplete parse"` - Tokens remain after parsing
- `"✗ REJECTED - {error message}"` - Specific parsing error

---

## 🔧 Extension Guidelines

### Adding New Tokens
1. Add new `TokenType` enum value
2. Add regex pattern to `YaoundeLexer.patterns`
3. Update grammar rules if needed
4. Add test cases

### Adding New Grammar Rules
1. Extend `YaoundeGrammar.rules` dictionary  
2. Add corresponding parse method to `YaoundeParser`
3. Update `parse_statement()` dispatch logic
4. Test with sample expressions

### Adding New Languages
1. Identify common expressions and patterns
2. Add token types for language-specific elements
3. Create regex patterns with proper word boundaries
4. Integrate into existing grammar structure