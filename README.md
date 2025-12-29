# Yaoundé Urban Communication Lexical & Syntactic Analyzer
# 🇨🇲 Yaounde Urban Communication Analyzer

A sophisticated compiler for multilingual Cameroonian street language that supports English, French, Pidgin, Fulfulde, Ewondo, and Franc-Anglais.
This project is a lexical and syntactic analyzer for the vibrant, multilingual street language spoken in Yaoundé, Cameroon. It's a compiler front-end designed to understand expressions that blend English, French, Cameroonian Pidgin, and local dialect words.

## 🌍 Overview
The tool can deconstruct sentences, identify parts of speech (like nouns, verbs, and slang), and validate the expression against a formal grammar for Yaoundé urban communication.

This project implements a complete lexical and syntactic analyzer for the rich multilingual expressions commonly used in Yaoundé, Cameroon's capital city. It captures the dynamic code-switching and linguistic creativity found in urban Cameroonian communication.
## ✨ Features

## 🎯 Supported Languages
- **Multilingual Tokenizer**: Recognizes a wide vocabulary from English, French, Pidgin, Ewondo, and Fulfulde.
- **Context-Aware Lexer**: Identifies specific urban concepts like transport (`bendskin`, `clando`), money (`mbongo`, `fap`), and places (`carrefour`, `quartier`).
- **Formal Grammar**: Defines the structure of common street expressions (greetings, requests, negotiations, etc.).
- **LL(1) Parser**: Validates token sequences against the formal grammar using a predictive parsing table.
- **Interactive Interface**: A user-friendly command-line menu to perform different types of analysis.
- **Comprehensive Demos**: Includes a rich set of example sentences to showcase the analyzer's capabilities.

- **English** - Base language
- **French** - Colonial language
- **Pidgin** - West African Pidgin English
- **Fulfulde** - Northern Cameroon language
- **Ewondo** - Central region language
- **Franc-Anglais** - French-English code mixing
## 📂 Project Structure

## 🏗️ Architecture

### Components

1. **Lexical Analyzer (`YaoundeLexer`)**
   - Tokenizes multilingual urban expressions
   - Recognizes 40+ token types
   - Handles code-switching seamlessly

2. **Grammar Engine (`YaoundeGrammar`)**
   - Context-Free Grammar for street expressions
   - LL(1) parsing table generation
   - FIRST/FOLLOW set computation

3. **Syntactic Parser (`YaoundeParser`)**
   - Recursive descent parser
   - Real-time syntax validation
   - Parse tree generation

4. **Complete Analyzer (`YaoundeAnalyzer`)**
   - End-to-end text analysis
   - Frequency analysis
   - Pretty-printed results

## 📊 Token Categories

### Semantic Categories
- **Places**: quartier, carrefour, campus, ICT, Total
- **People**: moto-guy, bendskin-man, patron, mbere
- **Transport**: taxi, bendskin, moto, clandos
- **Money**: fap, mbongo, kop, francs, CFA
- **Food**: tchop, ndolé, eru, koki, fufu
- **Technology**: call, airtime, WiFi, network, MTN

### Linguistic Elements
- **Pidgin Phrases**: na so, no be, i don, wetin
- **French Phrases**: c'est comment, ça va, tu vois
- **Ewondo Phrases**: a ye moan, mbokesso, ndolo
- **Fulfulde Phrases**: allah yai, wallahi, inshallah
- **Slang & Exclamations**: ehn, garrr, ekiee, weh

## 🔬 Grammar Structure

```
S → Statement
Statement → Greeting | Request | Question | Complaint | Negotiation
Greeting → SLANG_RESPONSE TimePhrase? StatePhrase?
Request → VERB_GIVE PRONOUN TransportRequest | VERB_MOVEMENT LocationPhrase
Question → QuestionWord Statement QUESTION
compiler/
├── main.py                 # Main entry point with interactive menu
├── lexical_analyzer.py     # Tokenizer (Lexer) for the language
├── syntactic_analyzer.py   # Grammar definition and Parser
├── test_analyzer.py        # Unit tests for the project
└── README.md               # This file
```

## 🚀 Usage

### Graphical User Interface (Recommended for Presentations)
```bash
python gui_interface.py
# or
python main.py --gui
```

The GUI provides:
- 📝 Interactive expression input
- 🔤 Real-time tokenization display
- 🌳 Parse result visualization
- 📊 Statistics and frequency analysis
- 📚 Grammar information
- 💡 Example expressions to try

### Command-Line Interface
- **`lexical_analyzer.py`**: Contains `YaoundeLexer`, which uses regular expressions to convert raw text into a stream of `Token`s.
- **`syntactic_analyzer.py`**: Contains `YaoundeGrammar` (which defines the language's structure) and `YaoundeParser` (which checks if the tokens form a valid sentence).
- **`main.py`**: The user-facing application. It orchestrates the lexer and parser and provides a menu for users to interact with the system.
- **`test_analyzer.py`**: Contains unit tests to ensure the reliability and correctness of the lexer and parser.

```python
from main import YaoundeAnalyzer
## 🚀 Getting Started

analyzer = YaoundeAnalyzer()
result = analyzer.analyze("bros drop me for Total")
analyzer.print_analysis(result)
```
### Prerequisites

- Python 3.6+

## 📝 Example Expressions
No external libraries are required to run the main application.

- "bros drop me for Total" - Transport request
- "masa network dey bad today" - Tech complaint
- "give me 500 francs" - Money request
- "je wanda how far ?" - Franc-Anglais question
- "walahi light don comot direct" - Fulfulde-Pidgin complaint
### Installation

### Franc-Anglais Test Block (Taxi, Student, Quartier)
1. Clone the repository or download the source code.
2. Navigate to the `compiler` directory.

The following 50 sentences are authentic Franc-Anglais expressions for analysis:
### Running the Analyzer

1. Bros, drop me for carrefour.
2. Je go campus now, you dey come?
3. Massa, give me 200 francs change.
4. You fit show me ICT junction?
5. Je wanda how far?
6. Bros, you sabi the road for Total?
7. I dey go marché, you fit carry me?
8. C’est comment, network dey bad today.
9. Bros, na so life dey for quartier.
10. Je wan chop ndolé, you get?
11. You fit wait small, I dey come.
12. Bros, na taxi or clando?
13. Je go school, drop me for gate.
14. You fit give me airtime?
15. Bros, na bendskin dey pass here?
16. Je wan buy fufu, where e dey?
17. Bros, you sabi patron for this place?
18. Je wan go campus, how much?
19. Bros, na moto or taxi?
20. Je wan call my friend, phone no dey.
21. Bros, you fit help me with kop?
22. Je wan go ICT, you dey go?
23. Bros, na bendskin-man dey for corner.
24. Je wan see my guy for marché.
25. Bros, na so e dey for Yaoundé.
26. Je wan drop for carrefour, how far?
27. Bros, na garri you dey chop?
28. Je wan go Total, you fit carry me?
29. Bros, na so e dey, no wahala.
30. Je wan buy airtime, you get?
31. Bros, na campus you dey go?
32. Je wan see my patron, you fit show me?
33. Bros, na so e dey, ehn!
34. Je wan go ICT, you fit drop me?
35. Bros, na taxi dey pass here?
36. Je wan buy eru, where e dey?
37. Bros, na so e dey for quartier.
38. Je wan go marché, you fit carry me?
39. Bros, na bendskin dey for road?
40. Je wan call my guy, phone dey bad.
41. Bros, na so e dey, garrr!
42. Je wan buy ndolé, you get?
43. Bros, na campus you dey go?
44. Je wan see my friend for Total.
45. Bros, na so e dey, weh!
46. Je wan go carrefour, you fit drop me?
47. Bros, na taxi or moto?
48. Je wan buy airtime, you fit help me?
49. Bros, na so e dey, ekiee!
50. Je wan go marché, you dey go?
To start the interactive menu, run `main.py`:

## 🎓 Academic Features
```bash
python main.py
```

- **Token Frequency Analysis**: Statistical breakdown of expression components
- **Parse Tree Generation**: Visual syntax structure
- **Grammar Validation**: Real-time syntax checking
- **Multilingual Support**: Seamless code-switching recognition
You will be presented with a menu of options:

## 🔧 Technical Implementation
1.  **Analyze expressions (full analysis)**: Performs both lexical and syntactic analysis and shows a detailed report.
2.  **Tokenize only (lexical analysis)**: Shows the tokens generated from an expression.
3.  **Parse only (syntactic analysis)**: Shows the result of the grammar validation.
4.  **Show grammar information**: Displays details about the grammar rules.
5.  **Run demo with examples**: Runs a series of predefined test cases.

- **Language**: Python 3.7+
- **Parsing Method**: LL(1) recursive descent
- **Pattern Matching**: Regular expressions
- **Data Structures**: Enums, dataclasses, sets
- **Analysis**: Frequency counting, tree generation
### Running the Demo

## 📈 Project Structure
To run the non-interactive demo directly from the command line:

```bash
python main.py --demo
```
compiler/
├── main.py              # Complete implementation
├── README.md            # This documentation
├── PROJECT_INDEX.md     # Detailed project index
├── API_REFERENCE.md     # API documentation
└── EXAMPLES.md          # Usage examples
```

## 🤝 Contributing
### Running Tests

This project captures the linguistic diversity of Cameroon. Contributions for additional languages, expressions, or grammar rules are welcome.
To ensure everything is working as expected, you can run the test suite:

## 📚 Research Applications
```bash
python test_analyzer.py
```

- Computational linguistics research
- African language technology
- Code-switching analysis
- Urban sociolinguistics
- Natural language processing for African languages

## 📄 License

Academic research project - Open source educational use.
This will execute all the unit tests for the lexer, parser, and grammar.