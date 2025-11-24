# Interactive Usage Guide

## 🎮 Interactive Components

All three main files now support interactive mode instead of running automatically:

### 1. Lexical Analyzer (`lexical_analyzer.py`)
```bash
python lexical_analyzer.py
```
**Interactive Features:**
- Prompts for Yaoundé expressions
- Real-time tokenization 
- Frequency analysis
- Type 'quit' to exit
- Type expressions like "bros drop me for Total"

**Demo Mode:**
```bash
python lexical_analyzer.py --demo
```

### 2. Syntactic Analyzer (`syntactic_analyzer.py`)
```bash  
python syntactic_analyzer.py
```
**Interactive Features:**
- Prompts for expressions to parse
- Shows tokenization + parsing results
- Type 'grammar' to see grammar rules
- Type 'quit' to exit
- Displays parse steps and acceptance/rejection

**Demo Mode:**
```bash
python syntactic_analyzer.py --demo
```

### 3. Main Analyzer (`main.py`) 
```bash
python main.py
```
**Interactive Menu:**
```
🇨🇲 YAOUNDÉ MULTILINGUAL EXPRESSION ANALYZER
Supporting: English • French • Pidgin • Fulfulde • Ewondo • Franc-Anglais

🚀 What would you like to do?
  1. Analyze expressions (full analysis)
  2. Tokenize only (lexical analysis) 
  3. Parse only (syntactic analysis)
  4. Show grammar information
  5. Run demo with examples
  6. Exit

🎯 Select option (1-6):
```

**Demo Mode:**
```bash
python main.py --demo
```

## 💡 Sample Interactive Session

### Lexical Analyzer Example:
```
🔤 YAOUNDÉ INTERACTIVE LEXICAL ANALYZER
🇨🇲 Enter Yaoundé expression: bros drop me for Total

📝 Analyzing: 'bros drop me for Total'

🔤 Tokens:
  Token(SLANG_RESPONSE, 'bros')
  Token(VERB_MOVEMENT, 'drop') 
  Token(PRONOUN, 'me')
  Token(PREPOSITION, 'for')
  Token(NOUN_PLACE, 'total')

📊 Token Frequency:
  1x NOUN_PLACE: total
  1x PREPOSITION: for
  1x PRONOUN: me
  1x SLANG_RESPONSE: bros
  1x VERB_MOVEMENT: drop
```

### Main Menu Example:
```
🎯 Select option (1-6): 1

🔍 FULL ANALYSIS MODE
🇨🇲 Expression: give me 500 francs

================================================================================
YAOUNDÉ URBAN COMMUNICATION ANALYSIS
================================================================================

📝 Original: give me 500 francs
✗ REJECTED - Incomplete parse

🔤 TOKENS:
  Token(VERB_GIVE, 'give')
  Token(PRONOUN, 'me')
  Token(NUMBER, '500')
  Token(NOUN_MONEY, 'francs')
```

## 🔧 Key Changes Made

1. **No Automatic Execution**: Files won't run test cases automatically
2. **User Input Prompts**: Each tool asks for input interactively  
3. **Menu System**: Main.py provides organized menu options
4. **Graceful Exit**: Type 'quit', 'exit', or Ctrl+C to stop
5. **Demo Options**: Use `--demo` flag for automated examples
6. **Error Handling**: Better user experience with error messages

## 🎯 Benefits

- **Educational**: Users learn by entering their own expressions
- **Exploratory**: Easy to test different linguistic patterns
- **User-Friendly**: Clear prompts and feedback
- **Flexible**: Choose specific analysis modes
- **Safe**: No risk of running unwanted code automatically