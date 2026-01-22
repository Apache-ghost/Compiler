# 🇨🇲 Yaoundé Multilingual Expression Analyzer

A sophisticated compiler construction project for analyzing informal urban communication in Yaoundé, Cameroon. This project implements a complete lexical and syntactic analyzer that handles code-switching between English, French, Pidgin, Fulfulde, Ewondo, and Franc-Anglais.

## 🌍 Overview

This project is a mini-compiler that performs:
- **Lexical Analysis (Tokenization)**: Breaking expressions into tokens using regular expressions
- **Syntactic Analysis (Parsing)**: Validating expressions against a Context-Free Grammar (CFG)
- **Language Detection**: Identifying which languages are present in code-mixed expressions
- **Statistical Analysis**: Token frequency and pattern analysis

## ✨ Features

- ✅ **Multilingual Support**: Handles 6 languages/codes (English, French, Pidgin, Fulfulde, Ewondo, Franc-Anglais)
- ✅ **40+ Token Types**: Comprehensive token recognition for urban communication
- ✅ **Context-Free Grammar**: Formal grammar rules for Yaoundé expressions
- ✅ **LL(1) Parsing**: Recursive descent parser with FIRST/FOLLOW sets
- ✅ **Multiple Interfaces**: Console, Web (Flask), and GUI (Tkinter) options
- ✅ **Voice Input**: Web interface with voice recognition (browser-based)
- ✅ **Language Detection**: Automatic detection of languages in expressions
- ✅ **Real-World Data**: Tested with 50+ collected expressions from Yaoundé
- ✅ **Comprehensive Testing**: Unit tests, edge cases, and integration tests

## 🎯 Supported Languages

- **English** - Base language
- **French** - Colonial language
- **Pidgin** - West African Pidgin English
- **Fulfulde** - Northern Cameroon language
- **Ewondo** - Central region language
- **Franc-Anglais** - French-English code mixing

## 📂 Project Structure

```
Compiler/
├── main.py                      # Main analyzer class and CLI interface
├── lexical_analyzer.py          # Tokenizer (Lexer) with regex patterns
├── syntactic_analyzer.py        # Grammar definition and Parser
├── app.py                       # Flask web application
├── gui_interface.py             # Tkinter GUI interface
├── demo_console.py              # Enhanced console demo for presentations
├── test_analyzer.py             # Comprehensive unit tests
├── test_collected_data_comprehensive.py  # Test all collected expressions
├── analyze_collected_data.py    # Analyze expressions by grammar rules
├── generate_edge_case_report.py # Edge case testing and reporting
├── collected_data.txt           # Real-world collected expressions
├── docs/                        # All documentation (organized)
│   ├── guides/                  # User guides
│   ├── theory/                  # Educational content
│   ├── reports/                 # Analysis reports
│   └── checklists/              # Project checklists
├── static/                      # Web interface assets
│   ├── css/
│   ├── js/
│   └── img/
└── templates/                   # Flask templates
```

## 🚀 Quick Start

### Console Terminal Demo (Recommended for Presentations)

```bash
cd Compiler
python demo_console.py
```

This runs a complete step-by-step demo showing:
- Lexical Analysis (Tokenization)
- Language Detection
- Syntactic Analysis (Parsing)
- Statistics

**Other console options:**
```bash
python demo_console.py interactive  # Interactive mode
python demo_console.py quick        # Quick results
python main.py                     # Original menu interface
```

### Web Interface (Flask)

```bash
cd Compiler
python app.py
```

Then open your browser to: `http://localhost:5000`

**Features:**
- Real-time analysis
- Voice input support
- Interactive tokenization
- Parse tree visualization
- Language detection
- Statistics and charts
- Export to PDF/TXT

### GUI Interface (Tkinter)

```bash
cd Compiler
python gui_interface.py
```

**Features:**
- Interactive expression input
- Real-time tokenization display
- Parse result visualization
- Statistics and frequency analysis
- Grammar information
- Example expressions

## 📊 Example Expressions

### Simple Requests
- `"bros drop me for Total"` - Transport request
- `"give me 500 francs"` - Money request

### Complaints
- `"masa network dey bad today"` - Tech complaint (English + Pidgin + Franc-Anglais)
- `"ICT est mal scia gars"` - French-style complaint
- `"walahi light don comot direct"` - Fulfulde + Pidgin complaint

### Questions
- `"je wanda how far ?"` - Franc-Anglais question
- `"Bros, you sabi the road for Total?"` - Pidgin question

### Negotiations
- `"give me 500 francs"` - Money negotiation
- `"Massa, give me 200 francs change"` - Slang + negotiation

## 🏗️ Architecture

### Components

1. **Lexical Analyzer (`YaoundeLexer`)**
   - Tokenizes multilingual urban expressions
   - Recognizes 40+ token types using regular expressions
   - Handles code-switching seamlessly
   - Token frequency analysis

2. **Grammar Engine (`YaoundeGrammar`)**
   - Context-Free Grammar for street expressions
   - LL(1) parsing table generation
   - FIRST/FOLLOW set computation
   - Grammar rule definitions

3. **Syntactic Parser (`YaoundeParser`)**
   - Recursive descent parser (LL(1)-like)
   - Real-time syntax validation
   - Parse tree generation
   - Flexible parsing for informal language

4. **Complete Analyzer (`YaoundeAnalyzer`)**
   - End-to-end text analysis
   - Language detection
   - Frequency analysis
   - Pretty-printed results

## 📚 Documentation

All documentation is organized in the `docs/` directory:

- **`docs/guides/`** - User guides and how-to documentation
  - Console demo guide
  - Web interface testing
  - Voice input guide
  - Quick start guides

- **`docs/theory/`** - Educational content
  - Complete educational guide (LL(1), SLR(1), regex, tokenization, etc.)
  - Project explanation guide
  - Grammar transformations

- **`docs/reports/`** - Analysis reports
  - Expression acceptance analysis
  - Grammar analysis
  - Features summary
  - Completion summary

- **`docs/checklists/`** - Project management
  - Final submission checklist

See `docs/README.md` for complete documentation index.

## 🔬 Grammar Structure

```
S → Statement
Statement → Greeting | Request | Question | Complaint | Negotiation

Greeting → SLANG_RESPONSE [TimePhrase] [StatePhrase]
Request → VERB_GIVE PRONOUN TransportRequest
        | VERB_MOVEMENT LocationPhrase
        | VERB_MOVEMENT PRONOUN LocationPhrase
Complaint → ComplaintPhrase [SLANG_EXCLAIM] [TIME]
Question → QuestionWord Statement QUESTION
Negotiation → PricePhrase | VERB_GIVE PRONOUN NUMBER NOUN_MONEY
```

See `docs/theory/grammar_transformations.md` for detailed grammar documentation.

## 📊 Token Categories

### Semantic Categories
- **Places**: quartier, carrefour, campus, ICT, Total
- **People**: moto-guy, bendskin-man, patron, mbere
- **Transport**: taxi, bendskin, moto, clandos
- **Money**: fap, mbongo, kop, francs, CFA
- **Food**: tchop, ndolé, eru, koki, fufu
- **Technology**: call, airtime, WiFi, network, MTN

### Linguistic Elements
- **Pidgin Phrases**: na so, no be, i don, wetin, dey, wan, fit
- **French Phrases**: c'est comment, ça va, tu vois, je, est, mal
- **Ewondo Phrases**: a ye moan, mbokesso, ndolo
- **Fulfulde Phrases**: allah yai, wallahi, inshallah
- **Slang & Exclamations**: ehn, garrr, ekiee, weh, bros, masa

## 🧪 Testing

### Run All Tests
```bash
python test_analyzer.py
```

### Test Collected Data
```bash
python test_collected_data_comprehensive.py
```

### Analyze Grammar Rules
```bash
python analyze_collected_data.py
```

### Generate Edge Case Report
```bash
python generate_edge_case_report.py
```

## 🔧 Technical Implementation

- **Language**: Python 3.7+
- **Parsing Method**: LL(1) recursive descent (flexible for informal language)
- **Pattern Matching**: Regular expressions (regex)
- **Data Structures**: Enums, dataclasses, sets, dictionaries
- **Analysis**: Frequency counting, tree generation, language detection
- **Web Framework**: Flask
- **GUI Framework**: Tkinter
- **Voice Recognition**: Web Speech API (browser-based)

## 📝 Usage Examples

### Python API

```python
from main import YaoundeAnalyzer

analyzer = YaoundeAnalyzer()
result = analyzer.analyze("bros drop me for Total")

print(f"Accepted: {result['accepted']}")
print(f"Languages: {result['languages_detected']}")
print(f"Tokens: {len(result['tokens'])}")
analyzer.print_analysis(result)
```

### Command Line

```bash
# Interactive menu
python main.py

# Console demo
python demo_console.py

# Web interface
python app.py
```

## 🎓 Academic Features

- **Token Frequency Analysis**: Statistical breakdown of expression components
- **Parse Tree Generation**: Visual syntax structure
- **Grammar Validation**: Real-time syntax checking
- **Multilingual Support**: Seamless code-switching recognition
- **FIRST/FOLLOW Sets**: LL(1) parsing table computation
- **Grammar Transformations**: Left recursion removal, left factoring
- **Edge Case Testing**: Comprehensive boundary condition testing

## 📈 Project Requirements Coverage

✅ **Data Collection**: 50+ real-world expressions collected and categorized  
✅ **Lexical Analysis**: Custom lexical specification with regular expressions  
✅ **Syntactic Analysis**: Context-Free Grammar with LL(1) parsing  
✅ **Grammar Transformations**: Left recursion removal, left factoring documented  
✅ **FIRST/FOLLOW Sets**: Computed and used in parsing  
✅ **Implementation**: LL(1)-like recursive descent parser  
✅ **Testing**: Grammar tested with collected sentences  
✅ **Acceptance/Rejection**: Shows which sentences are accepted/rejected  
✅ **Interfaces**: Console, Web, and GUI interfaces  
✅ **Documentation**: Comprehensive documentation (25+ pages of content)  

## 🤝 Contributing

This project captures the linguistic diversity of Cameroon. Contributions for additional languages, expressions, or grammar rules are welcome.

## 📚 Research Applications

- Computational linguistics research
- African language technology
- Code-switching analysis
- Urban sociolinguistics
- Natural language processing for African languages
- Compiler construction education

## 📄 License

Academic research project - Open source educational use.

## 🔗 Quick Links

- **Documentation**: `docs/README.md`
- **Educational Guide**: `docs/theory/COMPLETE_EDUCATIONAL_GUIDE.md`
- **Project Explanation**: `docs/theory/PROJECT_EXPLANATION_GUIDE.md`
- **Console Demo Guide**: `docs/guides/CONSOLE_DEMO_GUIDE.md`
- **Web Interface Guide**: `docs/guides/TEST_WEB_INTERFACE.md`

---

**ICT University - Compiler Construction Project**  
**Yaoundé Multilingual Expression Analyzer** 🇨🇲
