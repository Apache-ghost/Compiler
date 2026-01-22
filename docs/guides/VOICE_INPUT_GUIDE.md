# Voice Input Feature Guide

## Overview

The web interface includes a voice input feature that allows you to speak expressions instead of typing them. This is great for demonstrations!

## How to Use

1. **Click the microphone button** (🎤) in the input area
2. **Allow microphone permission** when prompted by your browser
3. **Speak clearly** your Yaoundé expression
4. **Wait for capture** - the system will automatically analyze

## Best Practices for Voice Input

### ✅ Works Best With:
- **Clear English phrases**: "bros drop me for Total"
- **Simple French**: "give me 500 francs"
- **Short expressions**: Keep it under 10 words
- **Clear pronunciation**: Speak slowly and clearly

### ⚠️ May Have Issues With:
- **Pidgin words**: "dey", "wan", "fit" may not be recognized accurately
- **Code-mixed expressions**: Mixing languages can confuse recognition
- **Local pronunciations**: Accents may affect accuracy
- **Long expressions**: Keep it concise

### 💡 Tips for Better Results:

1. **Speak clearly and slowly**
   - Pronounce each word distinctly
   - Pause slightly between words

2. **Use common phrases**
   - "bros drop me for Total" ✓
   - "give me 500 francs" ✓
   - "network is bad today" ✓

3. **Check the result**
   - Review what was captured
   - Edit if needed before analyzing

4. **Environment matters**
   - Use in quiet environment
   - Speak close to microphone
   - Reduce background noise

## Browser Compatibility

### ✅ Supported Browsers:
- **Google Chrome** (Best support)
- **Microsoft Edge** (Chromium-based)
- **Safari** (iOS/macOS)

### ❌ Not Supported:
- Firefox (doesn't support Web Speech API)
- Older browsers

## Troubleshooting

### "No speech detected"
- **Solution**: Speak louder, closer to microphone
- Check microphone is working
- Ensure microphone permission is granted

### "Microphone permission denied"
- **Solution**: 
  1. Click the lock icon in browser address bar
  2. Allow microphone access
  3. Refresh the page

### "Voice recognition error"
- **Solution**: 
  - Check internet connection (recognition uses online service)
  - Try typing instead
  - Use a different browser

### Poor Accuracy
- **Solution**:
  - Speak more clearly
  - Use simpler expressions
  - Type complex multilingual expressions manually

## For Demonstrations

### Recommended Approach:

1. **Start with voice input** (2-3 examples)
   - Use simple expressions
   - Show the feature works
   - Demonstrate real-time capture

2. **Switch to typing** for complex examples
   - Show multilingual expressions
   - Demonstrate Pidgin/French mixing
   - Show edge cases

3. **Explain the limitation**
   - Voice works best for simple expressions
   - Complex code-mixed expressions work better typed
   - This is normal for multilingual speech recognition

### Demo Script:

```
1. "Let me show you the voice input feature"
   → Click microphone
   → Say: "bros drop me for Total"
   → Show it captures and analyzes

2. "It works great for simple expressions"
   → Say: "give me 500 francs"
   → Show results

3. "For complex multilingual expressions, typing is more accurate"
   → Type: "masa network dey bad today"
   → Explain why (Pidgin words, code-mixing)
```

## Technical Details

### How It Works:
- Uses **Web Speech API** (browser's built-in speech recognition)
- Sends audio to online service (Google/Apple)
- Returns text transcript
- Automatically analyzes the captured text

### Language Settings:
- Currently set to `en-US` (US English)
- Works best with English words
- Can recognize some French words
- May struggle with Pidgin/local words

### Limitations:
- Requires internet connection
- Accuracy depends on pronunciation
- May not recognize all Yaoundé-specific words
- Code-mixing can reduce accuracy

## Alternative: Console Demo

For presentations where voice input might not work perfectly, use the console demo:

```bash
python demo_console.py
```

This provides:
- ✅ Reliable demonstration
- ✅ Clear step-by-step output
- ✅ No microphone needed
- ✅ Professional appearance

## Summary

**Voice input is great for:**
- Simple demonstrations
- Showing interactive features
- Engaging the audience

**Typing is better for:**
- Complex multilingual expressions
- Accurate demonstrations
- Professional presentations

**Best practice:** Use both! Start with voice to show the feature, then use typing for complex examples.

