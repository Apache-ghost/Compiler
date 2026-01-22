#!/usr/bin/env python3
"""
Enhanced Console Demo Mode for Presentations
Perfect for demonstrating the compiler project without web interface
"""

from main import YaoundeAnalyzer
from lexical_analyzer import TokenType
import time
import sys

def print_header():
    """Print a nice header"""
    print("\n" + "="*80)
    print(" " * 20 + "🇨🇲 YAOUNDÉ MULTILINGUAL EXPRESSION ANALYZER")
    print(" " * 15 + "Compiler Construction Project - Console Demo")
    print("="*80)
    print("\nSupporting: English • French • Pidgin • Fulfulde • Ewondo • Franc-Anglais")
    print("="*80 + "\n")

def print_section(title):
    """Print a section header"""
    print("\n" + "─"*80)
    print(f"  {title}")
    print("─"*80)

def demo_expression(analyzer, expression, delay=0.5):
    """Demonstrate analysis of a single expression with nice formatting"""
    print_section(f"DEMO: Analyzing Expression")
    print(f"\n📝 Input: \"{expression}\"")
    print("\n" + "─"*80)
    
    # Step 1: Tokenization
    print("\n🔤 STEP 1: LEXICAL ANALYSIS (Tokenization)")
    print("─"*80)
    tokens = analyzer.lexer.tokenize(expression)
    token_list = [t for t in tokens if t.type != TokenType.EOF]
    
    print(f"\nFound {len(token_list)} tokens:")
    for i, token in enumerate(token_list, 1):
        print(f"  {i}. {token.type.name:20s} → \"{token.value}\"")
    
    time.sleep(delay)
    
    # Step 2: Language Detection
    print("\n🌍 STEP 2: LANGUAGE DETECTION")
    print("─"*80)
    languages = analyzer.detect_languages(tokens)
    print(f"\nLanguages Detected: {', '.join(languages) if languages else 'None'}")
    print(f"Multilingual: {'Yes' if len(languages) > 1 else 'No'} ({len(languages)} languages)")
    
    time.sleep(delay)
    
    # Step 3: Syntactic Analysis
    print("\n🌳 STEP 3: SYNTACTIC ANALYSIS (Parsing)")
    print("─"*80)
    result = analyzer.analyze(expression)
    
    if result['accepted']:
        print(f"\n✓ ACCEPTED - Valid Yaoundé expression")
        print(f"  Matches grammar rule: {result['parse_result']}")
    else:
        print(f"\n✗ REJECTED - Expression doesn't match grammar")
        print(f"  Reason: {result['parse_result']}")
    
    # Show parse tree (first few steps)
    if result['parse_tree']:
        print(f"\nParse Tree (showing first 5 steps):")
        for step in result['parse_tree'][:5]:
            print(f"  → {step}")
        if len(result['parse_tree']) > 5:
            print(f"  ... and {len(result['parse_tree']) - 5} more steps")
    
    time.sleep(delay)
    
    # Step 4: Statistics
    print("\n📊 STEP 4: STATISTICS")
    print("─"*80)
    frequency = result['frequency']
    print(f"\nToken Frequency:")
    for token, count in sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {token}: {count}x")
    
    print(f"\nTotal Tokens: {len(token_list)}")
    print(f"Unique Tokens: {len(set(t.value for t in token_list))}")
    
    print("\n" + "="*80)
    input("\nPress ENTER to continue to next demo...")
    print()

def run_presentation_demo():
    """Run a complete presentation demo"""
    analyzer = YaoundeAnalyzer()
    
    print_header()
    
    print("This demo will show:")
    print("  1. Lexical Analysis (Tokenization)")
    print("  2. Language Detection")
    print("  3. Syntactic Analysis (Parsing)")
    print("  4. Statistics and Results")
    print("\n" + "="*80)
    input("\nPress ENTER to start the demo...")
    
    # Demo expressions covering different patterns
    demo_expressions = [
        {
            "expression": "bros drop me for Total",
            "description": "Simple Request - English + Franc-Anglais"
        },
        {
            "expression": "masa network dey bad today",
            "description": "Complaint - English + Pidgin + Franc-Anglais"
        },
        {
            "expression": "ICT est mal scia gars",
            "description": "French-style Complaint - French + Franc-Anglais"
        },
        {
            "expression": "give me 500 francs",
            "description": "Request/Negotiation - English + French"
        },
        {
            "expression": "walahi light don comot direct",
            "description": "Complex Complaint - Fulfulde + Pidgin + English"
        }
    ]
    
    for i, demo in enumerate(demo_expressions, 1):
        print(f"\n{'='*80}")
        print(f"DEMO {i}/{len(demo_expressions)}: {demo['description']}")
        print(f"{'='*80}")
        demo_expression(analyzer, demo['expression'])
    
    # Final summary
    print_section("DEMO COMPLETE - Summary")
    print("\n✅ Demonstrated:")
    print("  • Lexical Analysis (Tokenization using Regular Expressions)")
    print("  • Syntactic Analysis (Parsing using Context-Free Grammar)")
    print("  • Language Detection (Multilingual code-switching)")
    print("  • Grammar Validation (LL(1)-like recursive descent parsing)")
    print("\n✅ Key Features:")
    print("  • Handles 6 languages/codes: English, French, Pidgin, Fulfulde, Ewondo, Franc-Anglais")
    print("  • Processes informal urban communication")
    print("  • Validates expressions against formal grammar rules")
    print("  • Provides detailed analysis and statistics")
    print("\n" + "="*80)
    print("\n🎓 Thank you for watching the demo!")
    print("="*80 + "\n")

def interactive_mode():
    """Interactive mode for testing expressions"""
    analyzer = YaoundeAnalyzer()
    
    print_header()
    print("INTERACTIVE MODE")
    print("Enter expressions to analyze, or 'quit' to exit\n")
    
    while True:
        try:
            expression = input("🇨🇲 Enter expression: ").strip()
            
            if expression.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            if not expression:
                continue
            
            # Quick analysis
            result = analyzer.analyze(expression)
            languages = analyzer.detect_languages(analyzer.lexer.tokenize(expression))
            
            print(f"\n{'─'*80}")
            print(f"Result: {'✓ ACCEPTED' if result['accepted'] else '✗ REJECTED'}")
            print(f"Languages: {', '.join(languages) if languages else 'None'}")
            print(f"Tokens: {len([t for t in result['tokens'] if t.type != TokenType.EOF])}")
            print(f"Message: {result['parse_result']}")
            print(f"{'─'*80}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

def quick_demo():
    """Quick demo without pauses"""
    analyzer = YaoundeAnalyzer()
    
    expressions = [
        "bros drop me for Total",
        "masa network dey bad today",
        "ICT est mal scia gars",
        "give me 500 francs"
    ]
    
    print_header()
    print("QUICK DEMO - Showing Results Only\n")
    
    for expr in expressions:
        result = analyzer.analyze(expr)
        languages = analyzer.detect_languages(analyzer.lexer.tokenize(expr))
        status = "✓" if result['accepted'] else "✗"
        
        print(f"{status} {expr}")
        print(f"   Languages: {', '.join(languages)}")
        print(f"   Result: {result['parse_result'][:60]}...")
        print()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == 'interactive' or mode == 'i':
            interactive_mode()
        elif mode == 'quick' or mode == 'q':
            quick_demo()
        else:
            print("Usage: python demo_console.py [presentation|interactive|quick]")
            print("  presentation (default) - Full demo with pauses")
            print("  interactive (i) - Interactive mode")
            print("  quick (q) - Quick results only")
    else:
        run_presentation_demo()

