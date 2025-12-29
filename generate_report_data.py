# -*- coding: utf-8 -*-
"""
Report Data Generator for Yaoundé Analyzer Project
Generates tables and data for the project report
"""

from lexical_analyzer import YaoundeLexer, TokenType
from syntactic_analyzer import YaoundeGrammar
import json

def generate_token_table():
    """Generate token table for report"""
    lexer = YaoundeLexer()
    
    print("=" * 80)
    print("TOKEN TABLE FOR REPORT")
    print("=" * 80)
    print("\nToken Type | Example Values | Regular Expression Pattern")
    print("-" * 80)
    
    # Group tokens by category
    categories = {
        "Nouns": [t for t in TokenType if t.name.startswith('NOUN_')],
        "Verbs": [t for t in TokenType if t.name.startswith('VERB_')],
        "Adjectives": [t for t in TokenType if t.name.startswith('ADJ_')],
        "Slang": [t for t in TokenType if t.name.startswith('SLANG_')],
        "Phrases": [t for t in TokenType if t.name.endswith('_PHRASE')],
        "Grammar": [t for t in TokenType if t.name in ['PREPOSITION', 'CONJUNCTION', 'DETERMINER', 'PRONOUN']],
        "Other": [t for t in TokenType if t.name in ['NUMBER', 'TIME', 'QUESTION', 'EXCLAMATION', 'COMMA', 'PERIOD', 'UNKNOWN', 'EOF']]
    }
    
    examples = {
        'NOUN_PLACE': 'quartier, carrefour, campus, Total',
        'NOUN_PERSON': 'moto-guy, bendskin-man, patron',
        'NOUN_TRANSPORT': 'taxi, bendskin, moto',
        'NOUN_MONEY': 'fap, mbongo, kop, francs',
        'NOUN_FOOD': 'tchop, ndolé, eru, koki',
        'NOUN_TECH': 'call, airtime, WiFi, network',
        'VERB_MOVEMENT': 'go, comot, waka, drop',
        'VERB_GIVE': 'give, send, dash',
        'VERB_BE': 'be, dey, être',
        'VERB_GENERAL': 'do, see, hear, tok',
        'ADJ_QUALITY': 'bon, good, bad, correct',
        'ADJ_QUANTITY': 'plenty, small, trop',
        'SLANG_EXCLAIM': 'ehn, hmmm, garrr, ekiee',
        'SLANG_EMPHASIS': 'direct, serious, correct',
        'SLANG_RESPONSE': 'masa, bros, chief, sango',
        'PIDGIN_PHRASE': 'na so, no be, i don, wetin',
        'FRENCH_PHRASE': "c'est comment, ça va, je wanda",
        'EWONDO_PHRASE': 'a ye moan, mbokesso',
        'FULFULDE_PHRASE': 'allah yai, wallahi',
        'PREPOSITION': 'for, na, avec, à',
        'CONJUNCTION': 'and, avec, na, but',
        'DETERMINER': 'the, di, le, some',
        'PRONOUN': 'me, i, you, we, tu, je',
        'NUMBER': '100, 500, 2k, 5k',
        'TIME': 'today, tomorrow, now',
    }
    
    for category, token_types in categories.items():
        if token_types:
            print(f"\n[{category}]")
            for token_type in token_types:
                example = examples.get(token_type.name, 'N/A')
                print(f"  {token_type.name:20} | {example:40} | [Pattern in code]")
    
    print("\n" + "=" * 80)

def generate_regular_expressions():
    """Generate regular expressions table"""
    lexer = YaoundeLexer()
    
    print("\n" + "=" * 80)
    print("REGULAR EXPRESSIONS FOR REPORT")
    print("=" * 80)
    print("\nToken Type | Regular Expression")
    print("-" * 80)
    
    # Extract patterns from lexer
    pattern_map = {
        'NUMBER': r'\d+k|\d+\.\d+|\d+',
        'NOUN_PLACE': r'\b(quartier|carrefour|campus|ICT|université?|rond[- ]?point|marché|market|chop|rue|avenue|Total|station)\b',
        'NOUN_PERSON': r'\b(moto[- ]?guy|bendskin[- ]?man|patron|boss|driver|mbere|sauveteur|gars|ndjangui|combi)\b',
        'NOUN_TRANSPORT': r'\b(taxi|bendskin|moto|clandos?|car|bus|voiture|machine)\b',
        'NOUN_MONEY': r'\b(fap|mbongo|kop|francs?|CFA|sousous?|money|argent|change)\b',
        'NOUN_FOOD': r'\b(tchop|ndolé?|eru|koki|fufu|water[- ]?fufu|achu|banga|mbanga|plantain|pof[- ]?pof)\b',
        'NOUN_TECH': r'\b(call|airtime|crédit|WiFi|réseau|network|MTN|Orange|Camtel|internet|charger)\b',
        'VERB_MOVEMENT': r'\b(go|comot|waka|aller|venir|come|reach|arrive|drop|descend|mount|pass|move|enter)\b',
        'VERB_GIVE': r'\b(give|send|dash|donner|envoy[eé]|pay|di[eé])\b',
        'VERB_BE': r'\b(be|dey|[eé]tre|sef|stay|tann?|trouve)\b',
        'VERB_GENERAL': r'\b(do|see|hear|tok|parler|dire|mek|make|know|savoir|take|wan|want|need|get|avoir|sor)\b',
        'PIDGIN_PHRASE': r'\b(na so|no be|i don|you don|we don|no dey|weti|wetin|how far|how no|man no|I beg|abeg|my broda|yi mass[aé])\b',
        'FRENCH_PHRASE': r'\b(c\'?est comment|ça va|tu vois|on dit|je dis|mon frère|frèrot|même|là[- ]?bas|c\'?est bon|c\'?est ca|pourquoi|tu fais comment|on va faire comment|tu connais|je wanda)\b',
        'SLANG_EXCLAIM': r'\b(ehn|eh|hmmm|hmm|garrr|garr|ekiee|eki|oyee|oye|ayee|weh|chei|kai|ah[iy]a?|hein)\b',
        'SLANG_EMPHASIS': r'\b(direct|serious|sérieux|correct|zéro[- ]?zéro|même pas|trop|vraiment|total|carrément|sharp|tight|bad)\b',
        'SLANG_RESPONSE': r'\b(masa|mass|bros|brother|chief|sango|paddy|padi|guy|gars|nnem)\b',
        'ADJ_QUALITY': r'\b(bon|good|nye|nice|correct|bad|mauvais|beau|fine|better|bonne?|chaud|cool|nayo)\b',
        'ADJ_QUANTITY': r'\b(plenty|small|petit|grand|big|beaucoup|peu|trop|many|some|all|tout)\b',
        'TIME': r'\b(today|tomorrow|yesterday|now|maintenant|hier|demain|aujourd\'?hui|tantôt|après|avant|morning|soir|night)\b',
        'PREPOSITION': r'\b(for|na|avec|à|from|depuis|to|till|until|jusqu\'?à|en|dans|chez|on|sur|of|de|inside|behind|front)\b',
        'CONJUNCTION': r'\b(and|avec|na|but|mais|or|ou|so|donc|because|parce que|if|si|when|quand|that|que)\b',
        'DETERMINER': r'\b(the|di|le|la|les|un|une|des|some|any|this|that|ce|cette|my|ton|ma|your)\b',
        'PRONOUN': r'\b(me|i|you|we|dem|he|she|it|they|tu|je|nous|vous|ils|elles|on|am|ma|yi)\b',
    }
    
    for token_name, pattern in sorted(pattern_map.items()):
        print(f"{token_name:20} | {pattern}")
    
    print("\n" + "=" * 80)

def generate_grammar_rules():
    """Generate grammar rules for report"""
    grammar = YaoundeGrammar()
    
    print("\n" + "=" * 80)
    print("GRAMMAR RULES FOR REPORT")
    print("=" * 80)
    print("\nProduction Rules:")
    print("-" * 80)
    
    for non_terminal, productions in sorted(grammar.rules.items()):
        print(f"\n{non_terminal} →")
        for i, production in enumerate(productions):
            arrow = "|" if i > 0 else " "
            print(f"  {arrow} {' '.join(production)}")
    
    print("\n" + "=" * 80)

def generate_first_follow_sets():
    """Generate FIRST and FOLLOW sets for report"""
    grammar = YaoundeGrammar()
    
    print("\n" + "=" * 80)
    print("FIRST AND FOLLOW SETS FOR REPORT")
    print("=" * 80)
    
    print("\nFIRST Sets:")
    print("-" * 80)
    for non_terminal in sorted(grammar.first_sets.keys()):
        if non_terminal in grammar.rules:  # Only show non-terminals
            first_set = grammar.first_sets[non_terminal]
            first_list = sorted(list(first_set))
            print(f"FIRST({non_terminal}) = {{{', '.join(first_list[:10])}" + 
                  (f", ... ({len(first_list)} total)" if len(first_list) > 10 else "") + "}")
    
    print("\nFOLLOW Sets:")
    print("-" * 80)
    for non_terminal in sorted(grammar.follow_sets.keys()):
        if non_terminal in grammar.rules:  # Only show non-terminals
            follow_set = grammar.follow_sets[non_terminal]
            follow_list = sorted(list(follow_set))
            print(f"FOLLOW({non_terminal}) = {{{', '.join(follow_list)}}}")
    
    print("\n" + "=" * 80)

def generate_parsing_table_sample():
    """Generate sample parsing table for report"""
    grammar = YaoundeGrammar()
    
    print("\n" + "=" * 80)
    print("LL(1) PARSING TABLE SAMPLE FOR REPORT")
    print("=" * 80)
    print("\nM[Non-terminal, Terminal] = Production")
    print("-" * 80)
    
    count = 0
    for (non_terminal, terminal), production in sorted(grammar.parsing_table.items()):
        if count >= 30:  # Limit for report
            remaining = len(grammar.parsing_table) - 30
            print(f"\n... and {remaining} more entries")
            break
        print(f"M[{non_terminal:15}, {terminal:20}] = {' '.join(production)}")
        count += 1
    
    print(f"\nTotal entries in parsing table: {len(grammar.parsing_table)}")
    print("\n" + "=" * 80)

def generate_test_results():
    """Generate test results summary"""
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    # Load collected data
    try:
        with open('collected_data.txt', 'r', encoding='utf-8') as f:
            expressions = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        expressions = []
    
    analyzer = YaoundeAnalyzer()
    
    print(f"\nTotal collected expressions: {len(expressions)}")
    print("\nExpression | Tokens | Accepted | Parse Result")
    print("-" * 80)
    
    accepted_count = 0
    for expr in expressions[:15]:  # Show first 15
        result = analyzer.analyze(expr)
        token_count = len([t for t in result['tokens'] if t.type != TokenType.EOF])
        status = "✓" if result['accepted'] else "✗"
        if result['accepted']:
            accepted_count += 1
        
        # Truncate long expressions
        display_expr = expr[:50] + "..." if len(expr) > 50 else expr
        print(f"{display_expr:50} | {token_count:6} | {status:8} | {result['parse_result'][:30]}")
    
    print(f"\nAcceptance rate: {accepted_count}/{min(15, len(expressions))} ({100*accepted_count/min(15, len(expressions)):.1f}%)")
    print("\n" + "=" * 80)

def main():
    """Generate all report data"""
    print("\n" + "=" * 80)
    print("YAOUNDÉ ANALYZER - REPORT DATA GENERATOR")
    print("=" * 80)
    print("\nThis script generates tables and data for your project report.")
    print("Copy the output sections into your report document.\n")
    
    generate_token_table()
    generate_regular_expressions()
    generate_grammar_rules()
    generate_first_follow_sets()
    generate_parsing_table_sample()
    generate_test_results()
    
    print("\n✅ Report data generation complete!")
    print("\nNext steps:")
    print("  1. Copy each section into your report")
    print("  2. Format tables in your document editor")
    print("  3. Add screenshots from running the analyzer")
    print("  4. Include discussion on linguistic complexity")

if __name__ == '__main__':
    main()

