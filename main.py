"""
Yaoundé Urban Communication Lexical & Syntactic Analyzer
A compiler for multilingual Cameroonian street language
Supports: English, French, Pidgin, Fulfulde, Ewondo, and Franc-Anglais

This main module coordinates the lexical and syntactic analyzers.
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

def main():
    analyzer = YaoundeAnalyzer()
    
    # Sample Yaoundé expressions
    test_cases = [
        "bros drop me for Total",
        "masa network dey bad today",
        "give me 500 francs",
        "je wanda how far ?",
        "moto-guy go for ICT campus",
        "ehn mbongo plenty garrr",
        "WiFi no dey work hmmm",
        "bendskin-man send me for carrefour",
        "walahi light don comot direct",
        "tchop dey correct today bros"
    ]
    
    print("\n🇨🇲 YAOUNDÉ MULTILINGUAL EXPRESSION ANALYZER")
    print("Supporting: English • French • Pidgin • Fulfulde • Ewondo • Franc-Anglais")
    print("=" * 80 + "\n")
    
    for expression in test_cases:
        result = analyzer.analyze(expression)
        analyzer.print_analysis(result)
    
    # Show grammar info
    print("\n📚 GRAMMAR INFORMATION:")
    print("\nFIRST SETS (sample):")
    for non_terminal in list(analyzer.grammar.first_sets.keys())[:5]:
        print(f"  FIRST({non_terminal}) = {analyzer.grammar.first_sets[non_terminal]}")
    
    print("\nFOLLOW SETS (sample):")
    for non_terminal in list(analyzer.grammar.follow_sets.keys())[:5]:
        print(f"  FOLLOW({non_terminal}) = {analyzer.grammar.follow_sets[non_terminal]}")

if __name__ == "__main__":
    main()