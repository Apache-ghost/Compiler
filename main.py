# -*- coding: utf-8 -*-
"""
Yaounde Urban Communication Lexical & Syntactic Analyzer
Interactive compiler for multilingual Cameroonian street language
Supports: English, French, Pidgin, Fulfulde, Ewondo, and Franc-Anglais

This main module provides an interactive menu-driven interface
to coordinate the lexical and syntactic analyzers.

Usage:
    python main.py        # Interactive menu mode
    python main.py --demo # Demo mode
"""

from typing import Dict
from lexical_analyzer import YaoundeLexer, Token, TokenType
from syntactic_analyzer import YaoundeGrammar, YaoundeParser

# ==================== MAIN ANALYZER ====================

class YaoundeAnalyzer:
    """Complete analyzer for Yaoundé urban communication"""
    
    def __init__(self):
        self.lexer = YaoundeLexer()
        self.grammar = YaoundeGrammar()
        self.parser = YaoundeParser(self.grammar)
    
    def analyze(self, text: str) -> Dict:
        """Complete analysis of text"""
        # Lexical analysis
        tokens = self.lexer.tokenize(text)
        frequency = self.lexer.analyze_frequency(tokens)
        
        # Syntactic analysis
        accepted, message, parse_tree = self.parser.parse(tokens)
        
        return {
            'original': text,
            'tokens': tokens,
            'frequency': frequency,
            'parse_result': message,
            'parse_tree': parse_tree,
            'accepted': accepted
        }
    
    def print_analysis(self, result: Dict):
        """Pretty print analysis results"""
        print("=" * 80)
        print("YAOUNDÉ URBAN COMMUNICATION ANALYSIS")
        print("=" * 80)
        print(f"\n📝 Original: {result['original']}")
        print(f"\n{result['parse_result']}")
        
        print("\n🔤 TOKENS:")
        for token in result['tokens']:
            if token.type != TokenType.EOF:
                print(f"  {token}")
        
        print("\n📊 FREQUENCY:")
        for token, count in sorted(result['frequency'].items()):
            print(f"  {token}: {count}")
        
        print("\n🌳 PARSE TRACE:")
        for step in result['parse_tree'][:10]:  # Show first 10 steps
            print(f"  {step}")
        
        print("\n" + "=" * 80 + "\n")

# ==================== TEST CASES ====================

def interactive_analyzer():
    """Interactive main analyzer with menu options"""
    analyzer = YaoundeAnalyzer()
    
    print("\n🇨🇲 YAOUNDE MULTILINGUAL EXPRESSION ANALYZER")
    print("Supporting: English • French • Pidgin • Fulfulde • Ewondo • Franc-Anglais")
    print("=" * 75)
    
    print("\n🚀 What would you like to do?")
    print("  1. Analyze expressions (full analysis)")
    print("  2. Tokenize only (lexical analysis)")
    print("  3. Parse only (syntactic analysis)")
    print("  4. Show grammar information")
    print("  5. Run demo with examples")
    print("  6. Exit")
    
    while True:
        try:
            choice = input("\n🎯 Select option (1-6): ").strip()
            
            if choice == '1':
                full_analysis_mode(analyzer)
            elif choice == '2':
                lexical_only_mode(analyzer)
            elif choice == '3':
                syntactic_only_mode(analyzer)
            elif choice == '4':
                show_grammar_info(analyzer)
            elif choice == '5':
                run_demo(analyzer)
            elif choice == '6':
                print("\n👋 Au revoir! Goodbye! Merci beaucoup!")
                break
            else:
                print("❌ Invalid option. Please choose 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted! Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

def full_analysis_mode(analyzer):
    """Interactive full analysis mode"""
    print("\n🔍 FULL ANALYSIS MODE")
    print("Enter expressions for complete lexical + syntactic analysis")
    print("Type 'back' to return to main menu\n")
    
    while True:
        expression = input("🇨🇲 Expression: ").strip()
        
        if expression.lower() == 'back':
            break
        
        if not expression:
            continue
            
        result = analyzer.analyze(expression)
        analyzer.print_analysis(result)

def lexical_only_mode(analyzer):
    """Interactive lexical-only mode"""
    print("\n🔤 LEXICAL ANALYSIS MODE")
    print("Tokenization only (no syntax checking)")
    print("Type 'back' to return to main menu\n")
    
    while True:
        expression = input("🇨🇲 Expression to tokenize: ").strip()
        
        if expression.lower() == 'back':
            break
            
        if not expression:
            continue
            
        tokens = analyzer.lexer.tokenize(expression)
        frequency = analyzer.lexer.analyze_frequency(tokens)
        
        print(f"\n📝 Original: {expression}")
        print("\n🔤 TOKENS:")
        for token in tokens:
            if token.type != TokenType.EOF:
                print(f"  {token}")
        
        print("\n📊 FREQUENCY:")
        for token, count in sorted(frequency.items()):
            print(f"  {count}x {token}")
        print()

def syntactic_only_mode(analyzer):
    """Interactive syntax-only mode"""
    print("\n🌳 SYNTACTIC ANALYSIS MODE") 
    print("Grammar parsing only (assumes valid tokens)")
    print("Type 'back' to return to main menu\n")
    
    while True:
        expression = input("🇨🇲 Expression to parse: ").strip()
        
        if expression.lower() == 'back':
            break
            
        if not expression:
            continue
            
        tokens = analyzer.lexer.tokenize(expression)
        accepted, message, parse_tree = analyzer.parser.parse(tokens)
        
        print(f"\n📝 Original: {expression}")
        print(f"\n🎯 {message}")
        
        if parse_tree:
            print("\n🌳 PARSE TRACE:")
            for step in parse_tree[:8]:
                print(f"  {step}")
            if len(parse_tree) > 8:
                print(f"  ... and {len(parse_tree) - 8} more steps")
        print()

def show_grammar_info(analyzer):
    """Show grammar information"""
    print("\n📚 GRAMMAR INFORMATION")
    print("=" * 30)
    
    print("\nFIRST SETS (sample):")
    for non_terminal in list(analyzer.grammar.first_sets.keys())[:5]:
        first_set = analyzer.grammar.first_sets[non_terminal]
        print(f"  FIRST({non_terminal}) = {', '.join(sorted(list(first_set))[:4])}...")
    
    print("\nFOLLOW SETS (sample):")
    for non_terminal in list(analyzer.grammar.follow_sets.keys())[:5]:
        follow_set = analyzer.grammar.follow_sets[non_terminal]
        print(f"  FOLLOW({non_terminal}) = {', '.join(sorted(list(follow_set)))}")
    
    print("\nGRAMMAR RULES:")
    print("  Statement → Greeting | Request | Question | Complaint | Negotiation")
    print("  Greeting → SLANG_RESPONSE [TimePhrase] [StatePhrase]")
    print("  Request → VERB_GIVE PRONOUN TransportRequest | VERB_MOVEMENT LocationPhrase")
    print("  Question → QuestionWord Statement QUESTION")
    print()

def run_demo(analyzer):
    """Run demo with predefined examples"""
    test_cases = [
        "bros drop me for Total",
        "masa network dey bad today",
        "give me 500 francs",
        "je wanda how far ?",
        "walahi light don comot direct"
    ]
    
    print("\n🎬 RUNNING DEMO WITH SAMPLE EXPRESSIONS")
    print("=" * 45)
    
    for expression in test_cases:
        result = analyzer.analyze(expression)
        analyzer.print_analysis(result)
    
    input("\n⏸️ Press Enter to continue...")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        analyzer = YaoundeAnalyzer()
        run_demo(analyzer)
    else:
        interactive_analyzer()