# -*- coding: utf-8 -*-
"""
Yaoundé Urban Communication Analyzer - GUI Interface
Modern graphical user interface for the analyzer
Perfect for presentations and demonstrations
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Dict, List
from lexical_analyzer import YaoundeLexer, Token, TokenType
from syntactic_analyzer import YaoundeGrammar, YaoundeParser
from main import YaoundeAnalyzer

class YaoundeAnalyzerGUI:
    """Graphical User Interface for Yaoundé Analyzer"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🇨🇲 Yaoundé Urban Communication Analyzer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize analyzer components
        self.analyzer = YaoundeAnalyzer()
        
        # Color scheme
        self.colors = {
            'bg': '#f0f0f0',
            'header': '#2c3e50',
            'accent': '#3498db',
            'success': '#27ae60',
            'error': '#e74c3c',
            'warning': '#f39c12',
            'text_bg': '#ffffff',
            'input_bg': '#ecf0f1'
        }
        
        self.setup_ui()
        self.load_examples()
    
    def setup_ui(self):
        """Set up the user interface"""
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['header'], height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🇨🇲 Yaoundé Multilingual Expression Analyzer",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg=self.colors['header']
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            header_frame,
            text="English • French • Pidgin • Fulfulde • Ewondo • Franc-Anglais",
            font=('Arial', 10),
            fg='#bdc3c7',
            bg=self.colors['header']
        )
        subtitle_label.pack()
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Input and controls
        left_panel = tk.Frame(main_container, bg=self.colors['bg'], width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        left_panel.pack_propagate(False)
        
        # Input section
        input_frame = tk.LabelFrame(
            left_panel,
            text="📝 Enter Yaoundé Expression",
            font=('Arial', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['header']
        )
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            height=8,
            font=('Arial', 11),
            bg=self.colors['input_bg'],
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.input_text.bind('<KeyRelease>', self.on_input_change)
        
        # Buttons frame
        buttons_frame = tk.Frame(left_panel, bg=self.colors['bg'])
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Analysis buttons
        btn_analyze = tk.Button(
            buttons_frame,
            text="🔍 Full Analysis",
            command=self.full_analysis,
            font=('Arial', 10, 'bold'),
            bg=self.colors['accent'],
            fg='white',
            relief=tk.RAISED,
            cursor='hand2',
            padx=10,
            pady=5
        )
        btn_analyze.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        btn_tokenize = tk.Button(
            buttons_frame,
            text="🔤 Tokenize",
            command=self.tokenize_only,
            font=('Arial', 10),
            bg='#95a5a6',
            fg='white',
            relief=tk.RAISED,
            cursor='hand2',
            padx=10,
            pady=5
        )
        btn_tokenize.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        btn_parse = tk.Button(
            buttons_frame,
            text="🌳 Parse",
            command=self.parse_only,
            font=('Arial', 10),
            bg='#95a5a6',
            fg='white',
            relief=tk.RAISED,
            cursor='hand2',
            padx=10,
            pady=5
        )
        btn_parse.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        # Clear button
        btn_clear = tk.Button(
            left_panel,
            text="🗑️ Clear All",
            command=self.clear_all,
            font=('Arial', 9),
            bg='#e74c3c',
            fg='white',
            relief=tk.RAISED,
            cursor='hand2',
            pady=5
        )
        btn_clear.pack(fill=tk.X, pady=(0, 10))
        
        # Examples section
        examples_frame = tk.LabelFrame(
            left_panel,
            text="💡 Example Expressions",
            font=('Arial', 10, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['header']
        )
        examples_frame.pack(fill=tk.BOTH, expand=True)
        
        self.examples_listbox = tk.Listbox(
            examples_frame,
            font=('Arial', 9),
            bg=self.colors['text_bg'],
            selectbackground=self.colors['accent'],
            relief=tk.SOLID,
            borderwidth=1
        )
        self.examples_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.examples_listbox.bind('<Double-Button-1>', self.load_example)
        
        # Right panel - Results
        right_panel = tk.Frame(main_container, bg=self.colors['bg'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Results notebook (tabs)
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tokens tab
        tokens_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tokens_frame, text="🔤 Tokens")
        
        tokens_label = tk.Label(
            tokens_frame,
            text="Tokenized Output",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['header']
        )
        tokens_label.pack(pady=5)
        
        self.tokens_text = scrolledtext.ScrolledText(
            tokens_frame,
            font=('Courier', 10),
            bg=self.colors['text_bg'],
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.tokens_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Parse Result tab
        parse_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(parse_frame, text="🌳 Parse Result")
        
        self.parse_status_label = tk.Label(
            parse_frame,
            text="No expression parsed yet",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg'],
            fg='#7f8c8d'
        )
        self.parse_status_label.pack(pady=10)
        
        self.parse_text = scrolledtext.ScrolledText(
            parse_frame,
            font=('Courier', 9),
            bg=self.colors['text_bg'],
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.parse_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Grammar Info tab
        grammar_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(grammar_frame, text="📚 Grammar Info")
        
        self.grammar_text = scrolledtext.ScrolledText(
            grammar_frame,
            font=('Courier', 9),
            bg=self.colors['text_bg'],
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.grammar_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.load_grammar_info()
        
        # Statistics tab
        stats_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(stats_frame, text="📊 Statistics")
        
        self.stats_text = scrolledtext.ScrolledText(
            stats_frame,
            font=('Arial', 10),
            bg=self.colors['text_bg'],
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def load_examples(self):
        """Load example expressions"""
        examples = [
            "bros drop me for Total",
            "give me 500 francs",
            "masa network dey bad today",
            "je wanda how far ?",
            "walahi light don comot direct",
            "Je go campus now, you dey come?",
            "Bros, na taxi or clando?",
            "Je wan buy fufu, where e dey?",
            "Bros, you sabi the road for Total?",
            "Je wan call my friend, phone no dey"
        ]
        
        for example in examples:
            self.examples_listbox.insert(tk.END, example)
    
    def load_example(self, event):
        """Load selected example into input"""
        selection = self.examples_listbox.curselection()
        if selection:
            example = self.examples_listbox.get(selection[0])
            self.input_text.delete('1.0', tk.END)
            self.input_text.insert('1.0', example)
            self.full_analysis()
    
    def get_input_text(self) -> str:
        """Get text from input field"""
        return self.input_text.get('1.0', tk.END).strip()
    
    def on_input_change(self, event):
        """Called when input changes (for real-time updates if needed)"""
        pass
    
    def full_analysis(self):
        """Perform full lexical and syntactic analysis"""
        expression = self.get_input_text()
        if not expression:
            messagebox.showwarning("Empty Input", "Please enter an expression to analyze.")
            return
        
        try:
            result = self.analyzer.analyze(expression)
            self.display_tokens(result['tokens'])
            self.display_parse_result(result)
            self.display_statistics(result)
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
    
    def tokenize_only(self):
        """Perform only lexical analysis"""
        expression = self.get_input_text()
        if not expression:
            messagebox.showwarning("Empty Input", "Please enter an expression to tokenize.")
            return
        
        try:
            tokens = self.analyzer.lexer.tokenize(expression)
            self.display_tokens(tokens)
            self.notebook.select(0)  # Switch to tokens tab
        except Exception as e:
            messagebox.showerror("Error", f"Tokenization failed: {str(e)}")
    
    def parse_only(self):
        """Perform only syntactic analysis"""
        expression = self.get_input_text()
        if not expression:
            messagebox.showwarning("Empty Input", "Please enter an expression to parse.")
            return
        
        try:
            tokens = self.analyzer.lexer.tokenize(expression)
            accepted, message, parse_tree = self.analyzer.parser.parse(tokens)
            
            result = {
                'original': expression,
                'accepted': accepted,
                'parse_result': message,
                'parse_tree': parse_tree
            }
            self.display_parse_result(result)
            self.notebook.select(1)  # Switch to parse tab
        except Exception as e:
            messagebox.showerror("Error", f"Parsing failed: {str(e)}")
    
    def display_tokens(self, tokens: List[Token]):
        """Display tokens in the tokens tab"""
        self.tokens_text.delete('1.0', tk.END)
        
        if not tokens:
            self.tokens_text.insert('1.0', "No tokens found.")
            return
        
        output = []
        output.append("=" * 70)
        output.append("TOKENIZED OUTPUT")
        output.append("=" * 70)
        output.append(f"\nOriginal Expression: {self.get_input_text()}")
        output.append(f"\nTotal Tokens: {len([t for t in tokens if t.type != TokenType.EOF])}")
        output.append("\n" + "-" * 70)
        output.append("\nTokens:\n")
        
        for i, token in enumerate(tokens, 1):
            if token.type != TokenType.EOF:
                output.append(f"{i:3}. {token.type.name:25} → '{token.value}'")
        
        # Frequency analysis
        frequency = self.analyzer.lexer.analyze_frequency(tokens)
        if frequency:
            output.append("\n" + "-" * 70)
            output.append("\nToken Frequency:\n")
            for token_info, count in sorted(frequency.items()):
                output.append(f"  {count:2}x {token_info}")
        
        self.tokens_text.insert('1.0', '\n'.join(output))
    
    def display_parse_result(self, result: Dict):
        """Display parse result in the parse tab"""
        self.parse_text.delete('1.0', tk.END)
        
        expression = result.get('original', self.get_input_text())
        accepted = result.get('accepted', False)
        message = result.get('parse_result', '')
        parse_tree = result.get('parse_tree', [])
        
        # Update status label with color
        if accepted:
            self.parse_status_label.config(
                text="✓ ACCEPTED - Valid Yaoundé Expression",
                fg=self.colors['success']
            )
        else:
            self.parse_status_label.config(
                text="✗ REJECTED - Expression doesn't match patterns",
                fg=self.colors['error']
            )
        
        output = []
        output.append("=" * 70)
        output.append("SYNTACTIC ANALYSIS RESULT")
        output.append("=" * 70)
        output.append(f"\nExpression: {expression}")
        output.append(f"\nResult: {message}")
        output.append("\n" + "-" * 70)
        
        if parse_tree:
            output.append("\nParse Steps (showing first 20):\n")
            for i, step in enumerate(parse_tree[:20], 1):
                output.append(f"{i:3}. {step}")
            if len(parse_tree) > 20:
                output.append(f"\n... and {len(parse_tree) - 20} more steps")
        else:
            output.append("\nNo parse tree generated.")
        
        self.parse_text.insert('1.0', '\n'.join(output))
    
    def display_statistics(self, result: Dict):
        """Display statistics"""
        self.stats_text.delete('1.0', tk.END)
        
        tokens = result.get('tokens', [])
        frequency = result.get('frequency', {})
        accepted = result.get('accepted', False)
        
        output = []
        output.append("=" * 70)
        output.append("ANALYSIS STATISTICS")
        output.append("=" * 70)
        
        output.append(f"\nExpression: {result.get('original', 'N/A')}")
        output.append(f"\nStatus: {'✓ ACCEPTED' if accepted else '✗ REJECTED'}")
        output.append(f"\nTotal Tokens: {len([t for t in tokens if t.type != TokenType.EOF])}")
        
        # Token type distribution
        token_types = {}
        for token in tokens:
            if token.type != TokenType.EOF:
                token_types[token.type.name] = token_types.get(token.type.name, 0) + 1
        
        if token_types:
            output.append("\n" + "-" * 70)
            output.append("\nToken Type Distribution:\n")
            for token_type, count in sorted(token_types.items(), key=lambda x: x[1], reverse=True):
                output.append(f"  {token_type:30} : {count:3}")
        
        # Most frequent tokens
        if frequency:
            output.append("\n" + "-" * 70)
            output.append("\nMost Frequent Tokens:\n")
            sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
            for token_info, count in sorted_freq[:10]:
                output.append(f"  {count:2}x {token_info}")
        
        self.stats_text.insert('1.0', '\n'.join(output))
    
    def load_grammar_info(self):
        """Load grammar information"""
        grammar = self.analyzer.grammar
        
        output = []
        output.append("=" * 70)
        output.append("GRAMMAR INFORMATION")
        output.append("=" * 70)
        
        output.append("\n📚 Production Rules:\n")
        for non_terminal, productions in sorted(grammar.rules.items()):
            output.append(f"\n{non_terminal} →")
            for i, production in enumerate(productions):
                arrow = "|" if i > 0 else " "
                output.append(f"  {arrow} {' '.join(production)}")
        
        output.append("\n\n" + "=" * 70)
        output.append("FIRST Sets (Sample):\n")
        key_sets = ['Statement', 'Greeting', 'Request', 'Question', 'Complaint']
        for non_terminal in key_sets:
            if non_terminal in grammar.first_sets:
                first_set = grammar.first_sets[non_terminal]
                first_list = sorted(list(first_set))[:10]
                output.append(f"FIRST({non_terminal}) = {{{', '.join(first_list)}" + 
                            (f", ... ({len(first_set)} total)" if len(first_set) > 10 else "") + "}")
        
        output.append("\n\n" + "=" * 70)
        output.append("FOLLOW Sets (Sample):\n")
        for non_terminal in key_sets[:3]:
            if non_terminal in grammar.follow_sets:
                follow_set = grammar.follow_sets[non_terminal]
                follow_list = sorted(list(follow_set))
                output.append(f"FOLLOW({non_terminal}) = {{{', '.join(follow_list)}}}")
        
        output.append("\n\n" + "=" * 70)
        output.append(f"Parsing Table: {len(grammar.parsing_table)} entries")
        output.append("\n" + grammar.display_parsing_table(limit=15))
        
        self.grammar_text.insert('1.0', '\n'.join(output))
    
    def clear_all(self):
        """Clear all input and output"""
        self.input_text.delete('1.0', tk.END)
        self.tokens_text.delete('1.0', tk.END)
        self.parse_text.delete('1.0', tk.END)
        self.stats_text.delete('1.0', tk.END)
        self.parse_status_label.config(
            text="No expression parsed yet",
            fg='#7f8c8d'
        )

def main():
    """Launch the GUI application"""
    root = tk.Tk()
    app = YaoundeAnalyzerGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()

