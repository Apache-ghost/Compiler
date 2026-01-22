# Quick Start Guide - Yaoundé Analyzer

## 🚀 Running the Analyzer

### Option 1: GUI Interface (Recommended)
```bash
python gui_interface.py
```
- Modern graphical interface
- Real-time analysis
- Language detection display
- Perfect for presentations

### Option 2: Web Interface
```bash
python app.py
```
- Access via browser (usually http://localhost:5000)
- Full-featured web application
- Language detection with visual tags

### Option 3: Command Line
```bash
python main.py
```
- Interactive menu
- All analysis features
- Language detection included

## 🧪 Running Tests

### All Tests
```bash
python test_analyzer.py
```

### Edge Case Tests Only
```bash
python -m unittest test_analyzer.TestEdgeCases
```

### Multilingual Tests Only
```bash
python -m unittest test_analyzer.TestMultilingualSupport
```

### Comprehensive Collected Data Test
```bash
python test_collected_data_comprehensive.py
```

### Edge Case Report
```bash
python generate_edge_case_report.py
```

## 📊 Key Features

### 1. Multilingual Detection
Every analysis now shows detected languages:
- English
- French  
- Pidgin
- Ewondo
- Fulfulde
- Franc-Anglais

### 2. Edge Case Handling
The analyzer handles:
- Empty input
- Whitespace-only
- Unknown tokens (slang/typos)
- Mixed language orders
- Incomplete expressions

### 3. Comprehensive Testing
- 50+ collected expressions tested
- Edge cases validated
- Language detection verified
- Statistics generated

## 💡 Example Usage

```python
from main import YaoundeAnalyzer

analyzer = YaoundeAnalyzer()

# Analyze expression
result = analyzer.analyze("ICT est mal scia gars")

# Check results
print(f"Accepted: {result['accepted']}")
print(f"Languages: {result['languages_detected']}")
print(f"Tokens: {len(result['tokens'])}")
```

## 📝 For Your Report

### Generate Test Results
1. Run `python test_collected_data_comprehensive.py` - Get acceptance statistics
2. Run `python generate_edge_case_report.py` - Get edge case analysis
3. Run `python test_analyzer.py` - Get full test results

### Screenshots
1. Launch GUI: `python gui_interface.py`
2. Test "ICT est mal scia gars" - Shows language detection
3. Test edge cases - Shows robust handling
4. View statistics tab - Shows language distribution

---

**Everything is ready!** 🎉

