# Testing the Flask Web Interface

## Quick Start

1. **Start the Flask server:**
   ```bash
   cd Compiler
   python app.py
   ```

2. **Open your browser:**
   Navigate to: `http://localhost:5000`

## Test Cases for Language Detection

### Test 1: Full Analysis
1. Enter: `bros drop me for Total`
2. Click "Full Analysis"
3. **Expected:**
   - Languages Detected: English, Franc-Anglais
   - Status: ✓ ACCEPTED
   - Tokens displayed with syntax highlighting

### Test 2: Tokenize Only
1. Enter: `ICT est mal scia gars`
2. Click "Tokenize"
3. **Expected:**
   - Languages Detected: French, Franc-Anglais
   - All tokens listed
   - Statistics shown

### Test 3: Parse Only
1. Enter: `masa network dey bad today`
2. Click "Parse"
3. **Expected:**
   - Languages Detected: English, Pidgin, Franc-Anglais
   - Parse result shown
   - Parse tree displayed

### Test 4: Multilingual Expression
1. Enter: `walahi light don comot direct`
2. Click "Full Analysis"
3. **Expected:**
   - Languages Detected: Fulfulde, Pidgin, English
   - Status: ✓ ACCEPTED

### Test 5: French + English
1. Enter: `give me 500 francs`
2. Click "Full Analysis"
3. **Expected:**
   - Languages Detected: English, French
   - Status: ✓ ACCEPTED

## Verification Checklist

- [ ] Languages section appears below input area
- [ ] Language tags display correctly (e.g., "English", "French", "Pidgin")
- [ ] Languages detected in Full Analysis mode
- [ ] Languages detected in Tokenize Only mode
- [ ] Languages detected in Parse Only mode
- [ ] Language count shown in Statistics tab
- [ ] Languages included in PDF export
- [ ] Languages shown in comparison mode

## API Endpoint Testing

You can also test the API directly using curl or Postman:

### Full Analysis
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"expression": "bros drop me for Total"}'
```

### Tokenize Only
```bash
curl -X POST http://localhost:5000/api/tokenize \
  -H "Content-Type: application/json" \
  -d '{"expression": "ICT est mal scia gars"}'
```

### Parse Only
```bash
curl -X POST http://localhost:5000/api/parse \
  -H "Content-Type: application/json" \
  -d '{"expression": "masa network dey bad today"}'
```

## Expected Response Format

All endpoints should return `languages_detected` in the JSON response:

```json
{
  "original": "bros drop me for Total",
  "accepted": true,
  "languages_detected": ["English", "Franc-Anglais"],
  "tokens": [...],
  "token_count": 5,
  ...
}
```

## Troubleshooting

- **Server not starting:** Check if port 5000 is available
- **Languages not showing:** Check browser console for JavaScript errors
- **API errors:** Check Flask terminal output for error messages

