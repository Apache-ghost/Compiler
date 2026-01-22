#!/usr/bin/env python3
"""
Test all example expressions from web interface
Shows which ones are accepted/rejected and why
"""

from main import YaoundeAnalyzer

# Example expressions from app.py
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
    "C'est comment, network dey bad today.",
    "Massa, give me 200 francs change.",
    "You fit give me airtime?",
    "Bros, na bendskin dey pass here?",
    "Je wan call my friend, phone no dey",
    "ICT est mal scia bros"
]

def test_examples():
    """Test all example expressions"""
    analyzer = YaoundeAnalyzer()
    
    print("="*80)
    print("TESTING EXAMPLE EXPRESSIONS FROM WEB INTERFACE")
    print("="*80)
    print()
    
    accepted = []
    rejected = []
    
    for expr in examples:
        result = analyzer.analyze(expr)
        tokens = analyzer.lexer.tokenize(expr)
        token_types = [t.type.name for t in tokens if t.type.name != 'EOF']
        
        if result['accepted']:
            accepted.append(expr)
            status = "✓ ACCEPTED"
        else:
            rejected.append(expr)
            status = "✗ REJECTED"
        
        print(f"{status}: {expr}")
        print(f"   Tokens: {' '.join(token_types[:8])}")
        if not result['accepted']:
            print(f"   Reason: {result['parse_result']}")
        print()
    
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total: {len(examples)}")
    print(f"Accepted: {len(accepted)} ({len(accepted)/len(examples)*100:.1f}%)")
    print(f"Rejected: {len(rejected)} ({len(rejected)/len(examples)*100:.1f}%)")
    print()
    
    if rejected:
        print("REJECTED EXPRESSIONS:")
        for expr in rejected:
            print(f"  - {expr}")
    
    return accepted, rejected

if __name__ == '__main__':
    test_examples()

