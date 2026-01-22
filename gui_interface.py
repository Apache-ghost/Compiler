# -*- coding: utf-8 -*-
"""
Yaoundé Urban Communication Analyzer - Enhanced GUI Interface
Modern, beautiful graphical user interface with real-time analysis
Perfect for presentations and demonstrations
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from typing import Dict, List, Optional
from lexical_analyzer import YaoundeLexer, Token, TokenType
from syntactic_analyzer import YaoundeGrammar, YaoundeParser
from main import YaoundeAnalyzer
import re

class YaoundeAnalyzerGUI:
    """Graphical User Interface for Yaoundé Analyzer"""
    
    def __init__(self, root):
        self.root = root
        
        # Enhanced color scheme with modern design
        self.colors = {
            'bg': '#f5f7fa',
            'header': '#1a252f',
            'header_gradient': '#2c3e50',
            'accent': '#3498db',
            'accent_hover': '#2980b9',
            'success': '#27ae60',
            'success_light': '#2ecc71',
            'error': '#e74c3c',
            'error_light': '#c0392b',
            'warning': '#f39c12',
            'text_bg': '#ffffff',
            'input_bg': '#ffffff',
            'border': '#dfe6e9',
            'text_primary': '#2c3e50',
            'text_secondary': '#7f8c8d',
            'shadow': '#bdc3c7'
        }
        
        # Token type colors for syntax highlighting
        self.token_colors = {
            'NOUN': '#8e44ad',      # Purple
            'VERB': '#e67e22',      # Orange
            'ADJ': '#16a085',       # Teal
            'SLANG': '#c0392b',     # Red
            'PHRASE': '#2980b9',    # Blue
            'PREPOSITION': '#27ae60', # Green
            'PRONOUN': '#f39c12',   # Yellow
            'NUMBER': '#e74c3c',    # Red
            'TIME': '#3498db',      # Blue
            'UNKNOWN': '#95a5a6'    # Gray
        }
        
        # Configure root window
        self.root.title("🇨🇲 Yaoundé Urban Communication Analyzer")
        self.root.geometry("1400x900")
        self.root.configure(bg=self.colors['bg'])
        self.root.minsize(1000, 700)
        
        # Initialize analyzer components
        self.analyzer = YaoundeAnalyzer()
        
        # Real-time analysis
        self.analysis_timer = None
        self.last_analysis = None
        
        self.setup_ui()
        self.load_examples()
        self.setup_styles()
    
    def setup_styles(self):
        """Configure ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure notebook style
        style.configure('TNotebook', background=self.colors['bg'], borderwidth=0)
        style.configure('TNotebook.Tab', 
                       padding=[20, 10], 
                       background=self.colors['text_bg'],
                       foreground=self.colors['text_primary'])
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['accent'])],
                 foreground=[('selected', 'white')])
    
    def setup_ui(self):
        """Set up the enhanced user interface"""
        
        # Enhanced Header with gradient effect
        header_frame = tk.Frame(self.root, bg=self.colors['header'], height=100)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Header content container
        header_content = tk.Frame(header_frame, bg=self.colors['header'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        title_label = tk.Label(
            header_content,
            text="🇨🇲 Yaoundé Multilingual Expression Analyzer",
            font=('Segoe UI', 20, 'bold'),
            fg='white',
            bg=self.colors['header']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_content,
            text="English • French • Pidgin • Fulfulde • Ewondo • Franc-Anglais",
            font=('Segoe UI', 11),
            fg='#ecf0f1',
            bg=self.colors['header']
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Status bar in header
        self.header_status = tk.Label(
            header_content,
            text="Ready to analyze",
            font=('Segoe UI', 9),
            fg='#bdc3c7',
            bg=self.colors['header']
        )
        self.header_status.pack(pady=(8, 0))
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Input and controls
        left_panel = tk.Frame(main_container, bg=self.colors['bg'], width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        left_panel.pack_propagate(False)
        
        # Enhanced Input section
        input_frame = tk.LabelFrame(
            left_panel,
            text="📝 Enter Yaoundé Expression",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            bd=2
        )
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Input container with better styling
        input_container = tk.Frame(input_frame, bg=self.colors['bg'])
        input_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        self.input_text = scrolledtext.ScrolledText(
            input_container,
            height=8,
            font=('Segoe UI', 11),
            bg=self.colors['input_bg'],
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=2,
            highlightthickness=1,
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['accent'],
            padx=10,
            pady=10,
            insertbackground=self.colors['accent']
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        self.input_text.bind('<KeyRelease>', self.on_input_change)
        self.input_text.bind('<FocusIn>', lambda e: self.input_text.config(highlightbackground=self.colors['accent']))
        self.input_text.bind('<FocusOut>', lambda e: self.input_text.config(highlightbackground=self.colors['border']))
        
        # Character count label
        self.char_count_label = tk.Label(
            input_container,
            text="0 characters",
            font=('Segoe UI', 8),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg'],
            anchor='e'
        )
        self.char_count_label.pack(fill=tk.X, pady=(5, 0))
        
        # Buttons frame
        buttons_frame = tk.Frame(left_panel, bg=self.colors['bg'])
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Enhanced Analysis buttons with hover effects
        btn_style = {
            'font': ('Segoe UI', 10, 'bold'),
            'relief': tk.FLAT,
            'cursor': 'hand2',
            'padx': 15,
            'pady': 8,
            'bd': 0,
            'activebackground': None,
            'activeforeground': None
        }
        
        btn_analyze = tk.Button(
            buttons_frame,
            text="🔍 Full Analysis",
            command=self.full_analysis,
            bg=self.colors['accent'],
            fg='white',
            **btn_style
        )
        btn_analyze.pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
        btn_analyze.bind('<Enter>', lambda e: btn_analyze.config(bg=self.colors['accent_hover']))
        btn_analyze.bind('<Leave>', lambda e: btn_analyze.config(bg=self.colors['accent']))
        
        btn_tokenize = tk.Button(
            buttons_frame,
            text="🔤 Tokenize",
            command=self.tokenize_only,
            bg='#7f8c8d',
            fg='white',
            **btn_style
        )
        btn_tokenize.pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
        btn_tokenize.bind('<Enter>', lambda e: btn_tokenize.config(bg='#95a5a6'))
        btn_tokenize.bind('<Leave>', lambda e: btn_tokenize.config(bg='#7f8c8d'))
        
        btn_parse = tk.Button(
            buttons_frame,
            text="🌳 Parse",
            command=self.parse_only,
            bg='#7f8c8d',
            fg='white',
            **btn_style
        )
        btn_parse.pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
        btn_parse.bind('<Enter>', lambda e: btn_parse.config(bg='#95a5a6'))
        btn_parse.bind('<Leave>', lambda e: btn_parse.config(bg='#7f8c8d'))
        
        # Secondary buttons frame
        secondary_buttons = tk.Frame(left_panel, bg=self.colors['bg'])
        secondary_buttons.pack(fill=tk.X, pady=(0, 10))
        
        btn_clear = tk.Button(
            secondary_buttons,
            text="🗑️ Clear",
            command=self.clear_all,
            font=('Segoe UI', 9),
            bg=self.colors['error'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            padx=10,
            pady=6,
            bd=0
        )
        btn_clear.pack(side=tk.LEFT, padx=(0, 3), fill=tk.X, expand=True)
        btn_clear.bind('<Enter>', lambda e: btn_clear.config(bg=self.colors['error_light']))
        btn_clear.bind('<Leave>', lambda e: btn_clear.config(bg=self.colors['error']))
        
        btn_export = tk.Button(
            secondary_buttons,
            text="💾 Export",
            command=self.export_results,
            font=('Segoe UI', 9),
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            padx=10,
            pady=6,
            bd=0
        )
        btn_export.pack(side=tk.LEFT, padx=(3, 0), fill=tk.X, expand=True)
        btn_export.bind('<Enter>', lambda e: btn_export.config(bg=self.colors['success_light']))
        btn_export.bind('<Leave>', lambda e: btn_export.config(bg=self.colors['success']))
        
        # Enhanced Examples section
        examples_frame = tk.LabelFrame(
            left_panel,
            text="💡 Example Expressions (Double-click to load)",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            bd=2
        )
        examples_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollable examples with better styling
        examples_container = tk.Frame(examples_frame, bg=self.colors['bg'])
        examples_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        scrollbar_examples = tk.Scrollbar(examples_container)
        scrollbar_examples.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.examples_listbox = tk.Listbox(
            examples_container,
            font=('Segoe UI', 9),
            bg=self.colors['text_bg'],
            selectbackground=self.colors['accent'],
            selectforeground='white',
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=0,
            yscrollcommand=scrollbar_examples.set,
            activestyle='none'
        )
        self.examples_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar_examples.config(command=self.examples_listbox.yview)
        self.examples_listbox.bind('<Double-Button-1>', self.load_example)
        self.examples_listbox.bind('<Button-1>', lambda e: self.examples_listbox.selection_clear(0, tk.END))
        
        # Right panel - Results
        right_panel = tk.Frame(main_container, bg=self.colors['bg'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Results notebook (tabs)
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tokens tab
        tokens_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tokens_frame, text="🔤 Tokens")
        
        tokens_header = tk.Frame(tokens_frame, bg=self.colors['bg'])
        tokens_header.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        tokens_label = tk.Label(
            tokens_header,
            text="Tokenized Output",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text_primary']
        )
        tokens_label.pack(side=tk.LEFT)
        
        self.tokens_text = scrolledtext.ScrolledText(
            tokens_frame,
            font=('Consolas', 10),
            bg=self.colors['text_bg'],
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=0,
            padx=15,
            pady=15
        )
        self.tokens_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Parse Result tab
        parse_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(parse_frame, text="🌳 Parse Result")
        
        parse_header = tk.Frame(parse_frame, bg=self.colors['bg'])
        parse_header.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        self.parse_status_label = tk.Label(
            parse_header,
            text="No expression parsed yet",
            font=('Segoe UI', 13, 'bold'),
            bg=self.colors['bg'],
            fg='#7f8c8d'
        )
        self.parse_status_label.pack()
        
        self.parse_text = scrolledtext.ScrolledText(
            parse_frame,
            font=('Consolas', 9),
            bg=self.colors['text_bg'],
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=0,
            padx=15,
            pady=15
        )
        self.parse_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Grammar Info tab
        grammar_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(grammar_frame, text="📚 Grammar Info")
        
        self.grammar_text = scrolledtext.ScrolledText(
            grammar_frame,
            font=('Consolas', 9),
            bg=self.colors['text_bg'],
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=0,
            padx=15,
            pady=15
        )
        self.grammar_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.load_grammar_info()
        
        # Statistics tab
        stats_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(stats_frame, text="📊 Statistics")
        
        self.stats_text = scrolledtext.ScrolledText(
            stats_frame,
            font=('Consolas', 10),
            bg=self.colors['text_bg'],
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=0,
            padx=15,
            pady=15
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
        """Called when input changes - update character count and trigger real-time analysis"""
        # Update character count
        text = self.get_input_text()
        char_count = len(text)
        self.char_count_label.config(text=f"{char_count} characters")
        
        # Real-time analysis with debouncing (analyze after 1 second of no typing)
        if self.analysis_timer:
            self.root.after_cancel(self.analysis_timer)
        
        if text.strip():
            self.analysis_timer = self.root.after(1000, self.real_time_analysis)
            self.header_status.config(text="Typing...", fg=self.colors['warning'])
        else:
            self.header_status.config(text="Ready to analyze", fg='#bdc3c7')
    
    def real_time_analysis(self):
        """Perform real-time analysis as user types"""
        expression = self.get_input_text()
        if not expression.strip():
            return
        
        try:
            self.header_status.config(text="Analyzing...", fg=self.colors['accent'])
            result = self.analyzer.analyze(expression)
            self.last_analysis = result
            
            # Update status
            if result['accepted']:
                self.header_status.config(text="✓ Valid expression", fg=self.colors['success'])
            else:
                self.header_status.config(text="✗ Invalid expression", fg=self.colors['error'])
            
            # Auto-update display if user hasn't changed input
            current_text = self.get_input_text()
            if current_text == expression:
                self.display_tokens(result['tokens'])
                self.display_parse_result(result)
                self.display_statistics(result)
        except Exception as e:
            self.header_status.config(text=f"Error: {str(e)[:30]}", fg=self.colors['error'])
    
    def full_analysis(self):
        """Perform full lexical and syntactic analysis"""
        expression = self.get_input_text()
        if not expression:
            messagebox.showwarning("Empty Input", "Please enter an expression to analyze.")
            return
        
        try:
            result = self.analyzer.analyze(expression)
            # Show languages in header status
            if result.get('languages_detected'):
                lang_str = ', '.join(result['languages_detected'])
                self.header_status.config(text=f"Languages: {lang_str}", fg=self.colors['accent'])
            self.display_tokens(result['tokens'], result.get('languages_detected', []))
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
    
    def get_token_color(self, token_type: TokenType) -> str:
        """Get color for token type for syntax highlighting"""
        type_name = token_type.name
        if type_name.startswith('NOUN_'):
            return self.token_colors['NOUN']
        elif type_name.startswith('VERB_'):
            return self.token_colors['VERB']
        elif type_name.startswith('ADJ_'):
            return self.token_colors['ADJ']
        elif type_name.startswith('SLANG_'):
            return self.token_colors['SLANG']
        elif type_name.endswith('_PHRASE'):
            return self.token_colors['PHRASE']
        elif type_name == 'PREPOSITION':
            return self.token_colors['PREPOSITION']
        elif type_name == 'PRONOUN':
            return self.token_colors['PRONOUN']
        elif type_name == 'NUMBER':
            return self.token_colors['NUMBER']
        elif type_name == 'TIME':
            return self.token_colors['TIME']
        elif type_name == 'UNKNOWN':
            return self.token_colors['UNKNOWN']
        else:
            return self.colors['text_primary']
    
    def display_tokens(self, tokens: List[Token], languages: List[str] = None):
        """Display tokens in the tokens tab with syntax highlighting"""
        self.tokens_text.delete('1.0', tk.END)
        
        if not tokens:
            self.tokens_text.insert('1.0', "No tokens found.")
            return
        
        # Header
        self.tokens_text.insert('1.0', "TOKENIZED OUTPUT\n")
        self.tokens_text.insert(tk.END, "=" * 70 + "\n\n")
        
        expression = self.get_input_text()
        self.tokens_text.insert(tk.END, f"Original Expression: {expression}\n")
        self.tokens_text.insert(tk.END, f"Total Tokens: {len([t for t in tokens if t.type != TokenType.EOF])}\n")
        
        # Show languages detected
        if languages:
            self.tokens_text.insert(tk.END, f"🌍 Languages Detected: {', '.join(languages)}\n")
        
        self.tokens_text.insert(tk.END, "\n" + "-" * 70 + "\n\n")
        self.tokens_text.insert(tk.END, "Tokens:\n\n")
        
        # Configure tags for syntax highlighting
        for token_type in TokenType:
            color = self.get_token_color(token_type)
            self.tokens_text.tag_config(f"token_{token_type.name}", foreground=color, font=('Courier', 10, 'bold'))
        
        # Display tokens with color coding
        for i, token in enumerate(tokens, 1):
            if token.type != TokenType.EOF:
                line = f"{i:3}. {token.type.name:25} → '{token.value}'\n"
                start = self.tokens_text.index(tk.END + "-1c")
                self.tokens_text.insert(tk.END, line)
                end = self.tokens_text.index(tk.END + "-1c")
                # Highlight the token type
                self.tokens_text.tag_add(f"token_{token.type.name}", start, end)
        
        # Frequency analysis with visual bars
        frequency = self.analyzer.lexer.analyze_frequency(tokens)
        if frequency:
            self.tokens_text.insert(tk.END, "\n" + "-" * 70 + "\n\n")
            self.tokens_text.insert(tk.END, "Token Frequency:\n\n")
            
            sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
            max_count = sorted_freq[0][1] if sorted_freq else 1
            
            for token_info, count in sorted_freq:
                bar_length = int((count / max_count) * 30)
                bar = "█" * bar_length
                self.tokens_text.insert(tk.END, f"  {count:2}x {token_info:40} {bar}\n")
        
        # Scroll to top
        self.tokens_text.see('1.0')
    
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
        
        # Show languages detected
        languages = result.get('languages_detected', [])
        if languages:
            output.append(f"\n🌍 Languages Detected: {', '.join(languages)}")
        
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
        """Display enhanced statistics with visual bars"""
        self.stats_text.delete('1.0', tk.END)
        
        tokens = result.get('tokens', [])
        frequency = result.get('frequency', {})
        accepted = result.get('accepted', False)
        
        # Header
        self.stats_text.insert('1.0', "ANALYSIS STATISTICS\n")
        self.stats_text.insert(tk.END, "=" * 70 + "\n\n")
        
        # Status with color
        status_tag = "status_accepted" if accepted else "status_rejected"
        self.stats_text.tag_config("status_accepted", foreground=self.colors['success'], font=('Segoe UI', 10, 'bold'))
        self.stats_text.tag_config("status_rejected", foreground=self.colors['error'], font=('Segoe UI', 10, 'bold'))
        
        self.stats_text.insert(tk.END, f"Expression: {result.get('original', 'N/A')}\n")
        status_text = f"Status: {'✓ ACCEPTED' if accepted else '✗ REJECTED'}\n"
        start = self.stats_text.index(tk.END + "-1c")
        self.stats_text.insert(tk.END, status_text)
        end = self.stats_text.index(tk.END + "-1c")
        self.stats_text.tag_add(status_tag, start, end)
        
        self.stats_text.insert(tk.END, f"\nTotal Tokens: {len([t for t in tokens if t.type != TokenType.EOF])}\n")
        
        # Token type distribution with visual bars
        token_types = {}
        for token in tokens:
            if token.type != TokenType.EOF:
                token_types[token.type.name] = token_types.get(token.type.name, 0) + 1
        
        if token_types:
            self.stats_text.insert(tk.END, "\n" + "-" * 70 + "\n\n")
            self.stats_text.insert(tk.END, "Token Type Distribution:\n\n")
            
            max_count = max(token_types.values()) if token_types else 1
            for token_type, count in sorted(token_types.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len([t for t in tokens if t.type != TokenType.EOF])) * 100
                bar_length = int((count / max_count) * 40)
                bar = "█" * bar_length
                self.stats_text.insert(tk.END, f"  {token_type:30} {count:3} ({percentage:5.1f}%) {bar}\n")
        
        # Most frequent tokens
        if frequency:
            self.stats_text.insert(tk.END, "\n" + "-" * 70 + "\n\n")
            self.stats_text.insert(tk.END, "Most Frequent Tokens:\n\n")
            sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
            max_freq = sorted_freq[0][1] if sorted_freq else 1
            
            for token_info, count in sorted_freq[:10]:
                bar_length = int((count / max_freq) * 30)
                bar = "█" * bar_length
                self.stats_text.insert(tk.END, f"  {count:2}x {token_info:45} {bar}\n")
        
        # Scroll to top
        self.stats_text.see('1.0')
    
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
        self.char_count_label.config(text="0 characters")
        self.parse_status_label.config(
            text="No expression parsed yet",
            fg='#7f8c8d'
        )
        self.header_status.config(text="Ready to analyze", fg='#bdc3c7')
        self.last_analysis = None
        if self.analysis_timer:
            self.root.after_cancel(self.analysis_timer)
            self.analysis_timer = None
    
    def export_results(self):
        """Export analysis results to a text file"""
        if not self.last_analysis:
            messagebox.showwarning("No Data", "Please analyze an expression first before exporting.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Export Analysis Results"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("=" * 70 + "\n")
                    f.write("YAOUNDÉ URBAN COMMUNICATION ANALYSIS\n")
                    f.write("=" * 70 + "\n\n")
                    f.write(f"Expression: {self.last_analysis['original']}\n")
                    f.write(f"Status: {'✓ ACCEPTED' if self.last_analysis['accepted'] else '✗ REJECTED'}\n")
                    f.write(f"Parse Result: {self.last_analysis['parse_result']}\n\n")
                    
                    f.write("=" * 70 + "\n")
                    f.write("TOKENS\n")
                    f.write("=" * 70 + "\n\n")
                    for token in self.last_analysis['tokens']:
                        if token.type != TokenType.EOF:
                            f.write(f"{token.type.name:25} → '{token.value}'\n")
                    
                    f.write("\n" + "=" * 70 + "\n")
                    f.write("FREQUENCY ANALYSIS\n")
                    f.write("=" * 70 + "\n\n")
                    for token_info, count in sorted(self.last_analysis['frequency'].items(), 
                                                   key=lambda x: x[1], reverse=True):
                        f.write(f"{count:2}x {token_info}\n")
                    
                    if self.last_analysis['parse_tree']:
                        f.write("\n" + "=" * 70 + "\n")
                        f.write("PARSE TREE\n")
                        f.write("=" * 70 + "\n\n")
                        for i, step in enumerate(self.last_analysis['parse_tree'], 1):
                            f.write(f"{i:3}. {step}\n")
                
                messagebox.showinfo("Success", f"Results exported successfully to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export results:\n{str(e)}")

def main():
    """Launch the GUI application"""
    root = tk.Tk()
    app = YaoundeAnalyzerGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()

