#!/usr/bin/env python3
"""
Analyze collected_data.txt expressions against grammar rules
Shows which expressions match which production rules
"""

from main import YaoundeAnalyzer
from lexical_analyzer import TokenType

def analyze_expressions():
    """Analyze all collected expressions"""
    analyzer = YaoundeAnalyzer()
    
    # Load expressions
    with open('collected_data.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    expressions = []
    current_category = "General"
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            if line.startswith('#') and '===' in line:
                current_category = line.replace('#', '').replace('=', '').strip()
            continue
        expressions.append((line, current_category))
    
    print("="*80)
    print("ANALYSIS OF COLLECTED DATA AGAINST GRAMMAR RULES")
    print("="*80)
    print(f"\nTotal Expressions: {len(expressions)}\n")
    
    # Categorize by grammar rule type
    by_rule_type = {
        'Greeting': [],
        'Request': [],
        'Question': [],
        'Complaint': [],
        'Negotiation': [],
        'Rejected': []
    }
    
    for expr, category in expressions:
        result = analyzer.analyze(expr)
        tokens = analyzer.lexer.tokenize(expr)
        
        # Try to identify which rule type it matches
        rule_type = identify_rule_type(tokens, result, analyzer)
        
        if result['accepted']:
            by_rule_type[rule_type].append({
                'expression': expr,
                'category': category,
                'tokens': [t for t in tokens if t.type != TokenType.EOF],
                'languages': analyzer.detect_languages(tokens)
            })
        else:
            by_rule_type['Rejected'].append({
                'expression': expr,
                'category': category,
                'reason': result['parse_result'],
                'tokens': [t for t in tokens if t.type != TokenType.EOF]
            })
    
    # Print results
    for rule_type, matches in by_rule_type.items():
        if not matches:
            continue
        
        print(f"\n{'='*80}")
        print(f"{rule_type.upper()} RULE MATCHES: {len(matches)}")
        print(f"{'='*80}\n")
        
        for i, match in enumerate(matches[:10], 1):  # Show first 10
            print(f"{i}. {match['expression']}")
            if 'languages' in match:
                print(f"   Languages: {', '.join(match['languages'])}")
            if 'tokens' in match:
                token_types = [t.type.name for t in match['tokens']]
                print(f"   Token pattern: {' '.join(token_types[:8])}...")
            print()
        
        if len(matches) > 10:
            print(f"   ... and {len(matches) - 10} more\n")
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}\n")
    
    total_accepted = sum(len(v) for k, v in by_rule_type.items() if k != 'Rejected')
    total_rejected = len(by_rule_type['Rejected'])
    total = total_accepted + total_rejected
    
    print(f"Total Expressions: {total}")
    print(f"Accepted: {total_accepted} ({total_accepted/total*100:.1f}%)")
    print(f"Rejected: {total_rejected} ({total_rejected/total*100:.1f}%)\n")
    
    print("By Rule Type:")
    for rule_type in ['Greeting', 'Request', 'Question', 'Complaint', 'Negotiation']:
        count = len(by_rule_type[rule_type])
        if count > 0:
            print(f"  {rule_type}: {count}")
    
    print(f"\n{'='*80}")
    print("REJECTED EXPRESSIONS (Need Grammar Adjustments)")
    print(f"{'='*80}\n")
    
    for match in by_rule_type['Rejected'][:15]:  # Show first 15
        print(f"✗ {match['expression']}")
        print(f"  Category: {match['category']}")
        print(f"  Reason: {match['reason']}")
        if 'tokens' in match:
            token_types = [t.type.name for t in match['tokens']]
            print(f"  Tokens: {' '.join(token_types)}")
        print()
    
    if len(by_rule_type['Rejected']) > 15:
        print(f"  ... and {len(by_rule_type['Rejected']) - 15} more rejected\n")

def identify_rule_type(tokens, result, analyzer):
    """Try to identify which grammar rule type matches"""
    if not result['accepted']:
        return 'Rejected'
    
    token_types = [t.type for t in tokens if t.type != TokenType.EOF]
    if not token_types:
        return 'Rejected'
    
    first_token = token_types[0]
    
    # Check for Greeting (starts with SLANG_RESPONSE)
    if first_token == TokenType.SLANG_RESPONSE:
        return 'Greeting'
    
    # Check for Question (has QUESTION token or starts with QuestionWord)
    if TokenType.QUESTION in token_types:
        return 'Question'
    if first_token in [TokenType.PIDGIN_PHRASE, TokenType.FRENCH_PHRASE]:
        return 'Question'
    
    # Check for Request (starts with VERB_GIVE or VERB_MOVEMENT)
    if first_token in [TokenType.VERB_GIVE, TokenType.VERB_MOVEMENT]:
        return 'Request'
    
    # Check for Complaint (starts with NOUN_TECH, NOUN_MONEY, NOUN_TRANSPORT, or SLANG_EMPHASIS)
    if first_token in [TokenType.NOUN_TECH, TokenType.NOUN_MONEY, TokenType.NOUN_TRANSPORT, TokenType.SLANG_EMPHASIS]:
        return 'Complaint'
    
    # Check for Negotiation (starts with NUMBER or VERB_GIVE with NUMBER)
    if first_token == TokenType.NUMBER:
        return 'Negotiation'
    if first_token == TokenType.VERB_GIVE and TokenType.NUMBER in token_types:
        return 'Negotiation'
    
    return 'Rejected'

if __name__ == '__main__':
    analyze_expressions()

