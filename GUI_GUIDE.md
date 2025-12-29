# Graphical User Interface Guide

## 🖥️ GUI Interface Overview

The Yaoundé Analyzer now includes a modern, user-friendly graphical interface perfect for presentations and demonstrations.

## 🚀 Launching the GUI

### Method 1: Direct Launch
```bash
python gui_interface.py
```

### Method 2: Through Main Menu
```bash
python main.py
# Then select option 2 for GUI
```

### Method 3: Command Flag
```bash
python main.py --gui
```

## 🎨 Interface Features

### Main Window Layout

The GUI is divided into two main panels:

#### Left Panel - Input & Controls
1. **Expression Input Area**
   - Large text area for entering Yaoundé expressions
   - Supports multi-line input
   - Real-time editing

2. **Action Buttons**
   - **🔍 Full Analysis**: Performs complete lexical + syntactic analysis
   - **🔤 Tokenize**: Only performs lexical analysis
   - **🌳 Parse**: Only performs syntactic analysis
   - **🗑️ Clear All**: Clears input and all results

3. **Example Expressions**
   - Pre-loaded list of example expressions
   - Double-click to load into input
   - Automatically analyzes when loaded

#### Right Panel - Results (Tabbed Interface)

1. **🔤 Tokens Tab**
   - Displays all tokens from lexical analysis
   - Shows token types and values
   - Includes frequency analysis
   - Formatted for easy reading

2. **🌳 Parse Result Tab**
   - Shows acceptance/rejection status
   - Color-coded: Green for accepted, Red for rejected
   - Displays parse tree steps
   - Shows detailed parsing information

3. **📚 Grammar Info Tab**
   - Complete grammar rules
   - FIRST and FOLLOW sets
   - LL(1) parsing table sample
   - Reference information

4. **📊 Statistics Tab**
   - Token type distribution
   - Most frequent tokens
   - Analysis statistics
   - Summary information

## 💡 Usage Tips

### For Presentations

1. **Start with Examples**
   - Double-click examples to load them
   - Shows immediate results
   - Demonstrates different expression types

2. **Show Full Analysis**
   - Use "Full Analysis" button
   - Switch between tabs to show different aspects
   - Highlight tokenization, parsing, and statistics

3. **Try Custom Expressions**
   - Enter your own Yaoundé expressions
   - Show real-time analysis
   - Demonstrate the analyzer's capabilities

### For Testing

1. **Tokenize Only**
   - Use "Tokenize" button
   - Focus on lexical analysis
   - Check token recognition

2. **Parse Only**
   - Use "Parse" button
   - Focus on syntactic analysis
   - Check grammar validation

3. **Compare Results**
   - Try accepted vs rejected expressions
   - Show grammar limitations
   - Demonstrate error handling

## 🎯 Example Workflow

### Demonstration Flow

1. **Launch GUI**
   ```bash
   python gui_interface.py
   ```

2. **Load Example**
   - Double-click "bros drop me for Total"
   - Automatically performs full analysis

3. **Show Tokens**
   - Click "🔤 Tokens" tab
   - Explain token types
   - Show frequency analysis

4. **Show Parse Result**
   - Click "🌳 Parse Result" tab
   - Explain acceptance status
   - Show parse steps

5. **Show Statistics**
   - Click "📊 Statistics" tab
   - Discuss token distribution
   - Highlight multilingual aspects

6. **Try Custom Expression**
   - Type new expression
   - Click "Full Analysis"
   - Show real-time results

## 🎨 Color Coding

- **Green**: Accepted expressions
- **Red**: Rejected expressions
- **Blue**: Action buttons
- **Gray**: Secondary buttons
- **Dark Header**: Professional appearance

## ⌨️ Keyboard Shortcuts

- **Enter**: Submit expression (in some contexts)
- **Double-click**: Load example from list
- **Tab**: Navigate between elements

## 📸 Screenshot Tips

For your report and presentation:

1. **Main Interface**: Show the full GUI layout
2. **Tokenization**: Screenshot of Tokens tab with example
3. **Parsing**: Screenshot of Parse Result tab (accepted)
4. **Statistics**: Screenshot of Statistics tab
5. **Grammar Info**: Screenshot of Grammar Info tab

## 🔧 Technical Details

- **Framework**: tkinter (built into Python)
- **No Dependencies**: Works with standard Python installation
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Responsive**: Adapts to window resizing

## 🐛 Troubleshooting

### GUI Won't Launch
- Ensure Python 3.6+ is installed
- Check that tkinter is available: `python -m tkinter`
- Try command-line interface as fallback

### Import Errors
- Ensure all files are in the same directory
- Check that `lexical_analyzer.py` and `syntactic_analyzer.py` exist

### Display Issues
- Try resizing the window
- Check screen resolution settings
- Restart the application

## 🎓 Academic Use

The GUI is perfect for:
- **Presentations**: Visual demonstration
- **Demos**: Interactive showcase
- **Teaching**: Clear visualization of concepts
- **Reports**: Screenshot inclusion
- **Evaluation**: Easy to use and understand

---

**Enjoy using the Yaoundé Analyzer GUI!** 🇨🇲

