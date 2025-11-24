# Yaoundé Urban Communication Lexical & Syntactic Analyzer

A sophisticated compiler for multilingual Cameroonian street language that supports English, French, Pidgin, Fulfulde, Ewondo, and Franc-Anglais.

## 🌍 Overview

This project implements a complete lexical and syntactic analyzer for the rich multilingual expressions commonly used in Yaoundé, Cameroon's capital city. It captures the dynamic code-switching and linguistic creativity found in urban Cameroonian communication.

## 🎯 Supported Languages

- **English** - Base language
- **French** - Colonial language
- **Pidgin** - West African Pidgin English
- **Fulfulde** - Northern Cameroon language
- **Ewondo** - Central region language
- **Franc-Anglais** - French-English code mixing

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
```

## 🚀 Usage

```python
from main import YaoundeAnalyzer

analyzer = YaoundeAnalyzer()
result = analyzer.analyze("bros drop me for Total")
analyzer.print_analysis(result)
```

## 📝 Example Expressions

- `"bros drop me for Total"` - Transport request
- `"masa network dey bad today"` - Tech complaint
- `"give me 500 francs"` - Money request
- `"je wanda how far ?"` - Franc-Anglais question
- `"walahi light don comot direct"` - Fulfulde-Pidgin complaint

## 🎓 Academic Features

- **Token Frequency Analysis**: Statistical breakdown of expression components
- **Parse Tree Generation**: Visual syntax structure
- **Grammar Validation**: Real-time syntax checking
- **Multilingual Support**: Seamless code-switching recognition

## 🔧 Technical Implementation

- **Language**: Python 3.7+
- **Parsing Method**: LL(1) recursive descent
- **Pattern Matching**: Regular expressions
- **Data Structures**: Enums, dataclasses, sets
- **Analysis**: Frequency counting, tree generation

## 📈 Project Structure

```
compiler/
├── main.py              # Complete implementation
├── README.md            # This documentation
├── PROJECT_INDEX.md     # Detailed project index
├── API_REFERENCE.md     # API documentation
└── EXAMPLES.md          # Usage examples
```

## 🤝 Contributing

This project captures the linguistic diversity of Cameroon. Contributions for additional languages, expressions, or grammar rules are welcome.

## 📚 Research Applications

- Computational linguistics research
- African language technology
- Code-switching analysis
- Urban sociolinguistics
- Natural language processing for African languages

## 📄 License

Academic research project - Open source educational use.