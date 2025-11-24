# Usage Examples - Yaoundé Urban Communication Analyzer

## 🚀 Quick Start

### Basic Analysis
```python
from main import YaoundeAnalyzer

# Initialize the analyzer
analyzer = YaoundeAnalyzer()

# Analyze a simple greeting
result = analyzer.analyze("bros how far")
print(f"Accepted: {result['accepted']}")
print(f"Message: {result['parse_result']}")

# Pretty print full analysis
analyzer.print_analysis(result)
```

### Output:
```
================================================================================
YAOUNDÉ URBAN COMMUNICATION ANALYSIS
================================================================================

📝 Original: bros how far

✓ ACCEPTED - Valid Yaoundé expression

🔤 TOKENS:
  Token(SLANG_RESPONSE, 'bros')
  Token(PIDGIN_PHRASE, 'how far')

📊 FREQUENCY:
  PIDGIN_PHRASE: how far: 1
  SLANG_RESPONSE: bros: 1

🌳 PARSE TRACE:
  Matched: Token(SLANG_RESPONSE, 'bros')
  Matched: Token(PIDGIN_PHRASE, 'how far')
```

---

## 🎯 Expression Categories

### 1. Transport Requests
```python
analyzer = YaoundeAnalyzer()

# Basic transport request
result = analyzer.analyze("bros drop me for Total")
# ✓ ACCEPTED - SLANG_RESPONSE + VERB_MOVEMENT + PRONOUN + PREPOSITION + NOUN_PLACE

# Alternative phrasing
result = analyzer.analyze("moto-guy go for ICT campus")
# ✓ ACCEPTED - NOUN_PERSON + VERB_MOVEMENT + PREPOSITION + NOUN_PLACE

# With location details
result = analyzer.analyze("bendskin-man send me for carrefour")
# ✓ ACCEPTED - NOUN_PERSON + VERB_GIVE + PRONOUN + PREPOSITION + NOUN_PLACE
```

### 2. Technology Complaints
```python
# Network issues
result = analyzer.analyze("masa network dey bad today")
# ✓ ACCEPTED - SLANG_RESPONSE + NOUN_TECH + VERB_BE + ADJ_QUALITY + TIME

# WiFi problems with emphasis
result = analyzer.analyze("WiFi no dey work hmmm")
# ✓ ACCEPTED - NOUN_TECH + PIDGIN_PHRASE + VERB_GENERAL + SLANG_EXCLAIM

# Power outage with cultural expression
result = analyzer.analyze("walahi light don comot direct")
# ✓ ACCEPTED - FULFULDE_PHRASE + NOUN_TECH + PIDGIN_PHRASE + VERB_MOVEMENT + SLANG_EMPHASIS
```

### 3. Money Requests & Negotiations
```python
# Simple money request
result = analyzer.analyze("give me 500 francs")
# ✓ ACCEPTED - VERB_GIVE + PRONOUN + NUMBER + NOUN_MONEY

# Excitement about money
result = analyzer.analyze("ehn mbongo plenty garrr")
# ✓ ACCEPTED - SLANG_EXCLAIM + NOUN_MONEY + ADJ_QUANTITY + SLANG_EXCLAIM

# Negotiation
result = analyzer.analyze("200 francs 150 kop")
# ✓ ACCEPTED - NUMBER + NOUN_MONEY + NUMBER + NOUN_MONEY
```

### 4. Food & Social
```python
# Food appreciation
result = analyzer.analyze("tchop dey correct today bros")
# ✓ ACCEPTED - NOUN_FOOD + VERB_BE + ADJ_QUALITY + TIME + SLANG_RESPONSE

# Restaurant suggestion
result = analyzer.analyze("make we go chop ndolé")
# ✓ ACCEPTED - VERB_GENERAL + PRONOUN + VERB_MOVEMENT + VERB_GENERAL + NOUN_FOOD
```

### 5. Questions & Inquiries
```python
# Franc-Anglais question
result = analyzer.analyze("je wanda how far ?")
# ✓ ACCEPTED - FRENCH_PHRASE + PIDGIN_PHRASE + QUESTION

# Status inquiry
result = analyzer.analyze("c'est comment today ?")
# ✓ ACCEPTED - FRENCH_PHRASE + TIME + QUESTION

# General question
result = analyzer.analyze("wetin you dey do ?")
# ✓ ACCEPTED - PIDGIN_PHRASE + PRONOUN + VERB_BE + VERB_GENERAL + QUESTION
```

---

## 🔤 Advanced Tokenization

### Custom Lexical Analysis
```python
from main import YaoundeLexer

# Initialize lexer only
lexer = YaoundeLexer()

# Complex multilingual expression
text = "wallahi masa this WiFi for ICT campus dey bad serious garrr"
tokens = lexer.tokenize(text)

# Print each token with details
for i, token in enumerate(tokens):
    if token.type != TokenType.EOF:
        print(f"{i+1:2d}. {token.type.name:15s} | '{token.value}' | pos:{token.position}")

# Output:
#  1. FULFULDE_PHRASE  | 'wallahi' | pos:0
#  2. SLANG_RESPONSE   | 'masa' | pos:8
#  3. DETERMINER       | 'this' | pos:13
#  4. NOUN_TECH        | 'wifi' | pos:18
#  5. PREPOSITION      | 'for' | pos:23
#  6. NOUN_PLACE       | 'ict' | pos:27
#  7. NOUN_PLACE       | 'campus' | pos:31
#  8. VERB_BE          | 'dey' | pos:38
#  9. ADJ_QUALITY      | 'bad' | pos:42
# 10. SLANG_EMPHASIS   | 'serious' | pos:46
# 11. SLANG_EXCLAIM    | 'garrr' | pos:54
```

### Frequency Analysis
```python
# Analyze token patterns
frequency = lexer.analyze_frequency(tokens)

# Sort by frequency
sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

print("Token Frequency Analysis:")
for token_info, count in sorted_freq[:5]:  # Top 5
    print(f"  {count}x {token_info}")
```

---

## 📝 Grammar Exploration

### Understanding Parse Trees
```python
from main import YaoundeParser, YaoundeGrammar

# Initialize grammar and parser
grammar = YaoundeGrammar()
parser = YaoundeParser(grammar)

# Parse with detailed trace
tokens = lexer.tokenize("bros give me taxi for university")
accepted, message, parse_tree = parser.parse(tokens)

print(f"Parse Result: {message}")
print("\nDetailed Parse Steps:")
for step in parse_tree:
    print(f"  {step}")
```

### Grammar Rule Analysis
```python
# Explore grammar structure
print("Available Statement Types:")
for rule in grammar.rules['Statement']:
    print(f"  Statement → {' '.join(rule)}")

print("\nRequest Patterns:")
for rule in grammar.rules['Request']:
    print(f"  Request → {' '.join(rule)}")

# Check FIRST sets
print(f"\nFIRST(Statement) = {grammar.first_sets['Statement']}")
print(f"FOLLOW(Statement) = {grammar.follow_sets['Statement']}")
```

---

## 🌍 Multilingual Examples

### Code-Switching Patterns
```python
expressions = [
    # English-Pidgin
    "I want go for market",
    
    # French-English  
    "je vais à la université for class",
    
    # Pidgin-French
    "na so ça va être",
    
    # Fulfulde-Pidgin-English
    "wallahi this moto-guy dey cheat people",
    
    # Ewondo-French
    "a ye moan frère comment ça va",
    
    # Multi-language mix
    "masa tu vois this network dey bad walahi"
]

for expr in expressions:
    result = analyzer.analyze(expr)
    status = "✓" if result['accepted'] else "✗"
    print(f"{status} {expr}")
    
    # Show language distribution
    tokens = result['tokens'][:-1]  # Remove EOF
    languages = {}
    for token in tokens:
        if 'PIDGIN' in token.type.name:
            languages['Pidgin'] = languages.get('Pidgin', 0) + 1
        elif 'FRENCH' in token.type.name:
            languages['French'] = languages.get('French', 0) + 1
        elif 'FULFULDE' in token.type.name:
            languages['Fulfulde'] = languages.get('Fulfulde', 0) + 1
        elif 'EWONDO' in token.type.name:
            languages['Ewondo'] = languages.get('Ewondo', 0) + 1
        else:
            languages['English/Base'] = languages.get('English/Base', 0) + 1
    
    print(f"  Languages: {dict(languages)}")
    print()
```

---

## 🛠️ Custom Extensions

### Adding New Expressions
```python
# Example: Adding new slang terms
from main import YaoundeLexer, TokenType

# Extend lexer patterns (in practice, modify the class)
custom_patterns = [
    (TokenType.SLANG_EXCLAIM, r'\b(eeeh|waaaah|cheiiii)\b'),
    (TokenType.NOUN_PLACE, r'\b(Pentagon|Biyem[- ]?Assi|Madagascar)\b'),
    (TokenType.SLANG_EMPHASIS, r'\b(na[- ]?fire|na[- ]?die)\b')
]

# Test new expressions
test_expressions = [
    "eeeh this Pentagon place na fire",
    "waaaah Biyem-Assi traffic na die",  
    "cheiiii Madagascar far too much"
]

# Note: To actually extend, you'd modify the YaoundeLexer.__init__ method
```

### Creating Domain-Specific Analyzers
```python
# Example: University-focused analyzer
class UniversityYaoundeAnalyzer(YaoundeAnalyzer):
    def __init__(self):
        super().__init__()
        # Add university-specific patterns
        university_patterns = [
            (TokenType.NOUN_PLACE, r'\b(amphitheatre|lab|library|admin)\b'),
            (TokenType.NOUN_PERSON, r'\b(lecturer|prof|student|pion)\b'),
            (TokenType.NOUN_TECH, r'\b(projector|exam|TD|CM|credit)\b')
        ]
        # In practice, extend lexer.patterns
        
    def analyze_academic_context(self, text):
        result = self.analyze(text)
        # Add academic-specific analysis
        academic_tokens = [t for t in result['tokens'] 
                          if 'academic' in t.value.lower()]
        result['academic_elements'] = len(academic_tokens)
        return result

# Usage
university_analyzer = UniversityYaoundeAnalyzer()
result = university_analyzer.analyze("prof no dey for amphitheatre today")
```

---

## 📊 Batch Processing

### Analyzing Multiple Expressions
```python
# Process a dataset of expressions
expressions_dataset = [
    "bros drop me for Total",
    "masa network dey bad", 
    "give me 500 francs",
    "je wanda how far ?",
    "WiFi no dey work",
    "walahi light don comot",
    "tchop dey correct today",
    "bendskin for carrefour"
]

results = []
for expr in expressions_dataset:
    result = analyzer.analyze(expr)
    results.append({
        'expression': expr,
        'accepted': result['accepted'],
        'token_count': len(result['tokens']) - 1,  # Exclude EOF
        'languages': len(set(t.type.name.split('_')[0] 
                           for t in result['tokens'][:-1] 
                           if '_' in t.type.name))
    })

# Summary statistics
accepted_count = sum(r['accepted'] for r in results)
avg_tokens = sum(r['token_count'] for r in results) / len(results)

print(f"Dataset Analysis:")
print(f"  Total expressions: {len(results)}")
print(f"  Accepted: {accepted_count}/{len(results)} ({accepted_count/len(results)*100:.1f}%)")
print(f"  Average tokens per expression: {avg_tokens:.1f}")
```

---

## 🎓 Educational Use Cases

### Computational Linguistics Demo
```python
def linguistic_analysis_demo():
    """Demonstrate computational linguistics concepts"""
    
    print("=== COMPUTATIONAL LINGUISTICS DEMO ===\n")
    
    # 1. Morphological Analysis
    print("1. MORPHOLOGICAL ANALYSIS:")
    compound_words = ["moto-guy", "bendskin-man", "water-fufu"]
    for word in compound_words:
        tokens = analyzer.lexer.tokenize(word)
        print(f"  '{word}' → {tokens[0].type.name}")
    
    # 2. Code-switching Detection  
    print("\n2. CODE-SWITCHING ANALYSIS:")
    mixed_expr = "walahi masa this network dey bad serious"
    result = analyzer.analyze(mixed_expr)
    
    print(f"  Expression: '{mixed_expr}'")
    print("  Language switches:")
    prev_lang = None
    for token in result['tokens'][:-1]:
        lang = token.type.name.split('_')[0]
        if prev_lang and lang != prev_lang:
            print(f"    {prev_lang} → {lang} at '{token.value}'")
        prev_lang = lang
    
    # 3. Syntactic Parsing
    print("\n3. SYNTACTIC STRUCTURE:")
    expr = "bros give me taxi for university"
    result = analyzer.analyze(expr)
    print(f"  Expression: '{expr}'")
    print(f"  Parse result: {result['parse_result']}")
    print("  Syntactic structure:")
    print("    [Greeting [SLANG_RESPONSE bros]]")
    print("    [Request [VERB_GIVE give] [PRONOUN me] [NOUN_TRANSPORT taxi]]")
    print("    [LocationPhrase [PREPOSITION for] [NOUN_PLACE university]]")

# Run the demo
linguistic_analysis_demo()
```

### Language Learning Application
```python
def language_learning_tool(target_language="PIDGIN"):
    """Help users learn specific language elements"""
    
    # Filter expressions by target language
    pidgin_expressions = [
        "how far bros",
        "wetin you dey do", 
        "na so e be",
        "i don reach",
        "no wahala"
    ]
    
    print(f"=== {target_language} LEARNING TOOL ===\n")
    
    for expr in pidgin_expressions:
        result = analyzer.analyze(expr)
        
        # Extract target language tokens
        target_tokens = [t for t in result['tokens'][:-1] 
                        if target_language in t.type.name]
        
        print(f"Expression: '{expr}'")
        print(f"  {target_language} elements:")
        for token in target_tokens:
            print(f"    '{token.value}' ({token.type.name})")
        print(f"  Grammar: {result['parse_result']}")
        print()

# Usage
language_learning_tool("PIDGIN")
```

---

## 🔍 Debugging & Validation

### Token Pattern Testing
```python
def test_token_patterns():
    """Test regex patterns for edge cases"""
    
    test_cases = [
        # Numbers
        ("500", TokenType.NUMBER),
        ("2k", TokenType.NUMBER), 
        ("1.5k", TokenType.NUMBER),
        
        # Compound words
        ("moto-guy", TokenType.NOUN_PERSON),
        ("water fufu", TokenType.NOUN_FOOD),  # Should match "water"
        
        # Contractions
        ("c'est", TokenType.FRENCH_PHRASE),
        ("aujourd'hui", TokenType.TIME),
        
        # Case sensitivity
        ("BROS", TokenType.SLANG_RESPONSE),
        ("WiFi", TokenType.NOUN_TECH)
    ]
    
    lexer = YaoundeLexer()
    
    for text, expected_type in test_cases:
        tokens = lexer.tokenize(text)
        actual_type = tokens[0].type if tokens else None
        
        status = "✓" if actual_type == expected_type else "✗"
        print(f"{status} '{text}' → {actual_type.name if actual_type else 'None'}")

test_token_patterns()
```

### Grammar Validation
```python
def validate_grammar_coverage():
    """Check grammar rule coverage"""
    
    # Test each statement type
    test_expressions = {
        'Greeting': ["bros", "masa how far", "chief ça va"],
        'Request': ["give me taxi", "go for Total", "drop me campus"],
        'Question': ["wetin ?", "c'est comment ?", "how far ?"], 
        'Complaint': ["network bad", "mbongo small"],
        'Negotiation': ["500 francs 300 kop"]
    }
    
    for category, expressions in test_expressions.items():
        print(f"\n{category} expressions:")
        for expr in expressions:
            result = analyzer.analyze(expr)
            status = "✓" if result['accepted'] else "✗"
            print(f"  {status} '{expr}'")

validate_grammar_coverage()
```

This comprehensive example set demonstrates the full capabilities of the Yaoundé Urban Communication Analyzer, from basic usage to advanced linguistic analysis and educational applications.