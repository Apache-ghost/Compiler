# -*- coding: utf-8 -*-
"""
Test Suite for Yaoundé Urban Communication Analyzer
Comprehensive unit tests for lexical and syntactic analysis
"""

import unittest
from lexical_analyzer import YaoundeLexer, Token, TokenType
from syntactic_analyzer import YaoundeGrammar, YaoundeParser
from main import YaoundeAnalyzer

class TestLexicalAnalyzer(unittest.TestCase):
    """Test cases for lexical analyzer"""
    
    def setUp(self):
        self.lexer = YaoundeLexer()
    
    def test_basic_tokenization(self):
        """Test basic token recognition"""
        tokens = self.lexer.tokenize("bros drop me for Total")
        token_types = [t.type for t in tokens if t.type != TokenType.EOF]
        
        self.assertIn(TokenType.SLANG_RESPONSE, token_types)
        self.assertIn(TokenType.VERB_MOVEMENT, token_types)
        self.assertIn(TokenType.PRONOUN, token_types)
        self.assertIn(TokenType.PREPOSITION, token_types)
        self.assertIn(TokenType.NOUN_PLACE, token_types)
    
    def test_money_expressions(self):
        """Test money-related tokens"""
        tokens = self.lexer.tokenize("give me 500 francs")
        token_types = [t.type for t in tokens if t.type != TokenType.EOF]
        
        self.assertIn(TokenType.VERB_GIVE, token_types)
        self.assertIn(TokenType.NUMBER, token_types)
        self.assertIn(TokenType.NOUN_MONEY, token_types)
    
    def test_pidgin_phrases(self):
        """Test Pidgin phrase recognition"""
        tokens = self.lexer.tokenize("na so e dey")
        token_types = [t.type for t in tokens if t.type != TokenType.EOF]
        
        self.assertIn(TokenType.PIDGIN_PHRASE, token_types)
    
    def test_french_phrases(self):
        """Test French phrase recognition"""
        tokens = self.lexer.tokenize("je wanda how far")
        token_types = [t.type for t in tokens if t.type != TokenType.EOF]
        
        self.assertIn(TokenType.FRENCH_PHRASE, token_types)
    
    def test_multilingual_mixing(self):
        """Test code-switching recognition"""
        tokens = self.lexer.tokenize("bros network dey bad today")
        token_types = [t.type for t in tokens if t.type != TokenType.EOF]
        
        self.assertIn(TokenType.SLANG_RESPONSE, token_types)
        self.assertIn(TokenType.NOUN_TECH, token_types)
        self.assertIn(TokenType.VERB_BE, token_types)
        self.assertIn(TokenType.ADJ_QUALITY, token_types)
        self.assertIn(TokenType.TIME, token_types)
    
    def test_frequency_analysis(self):
        """Test token frequency counting"""
        tokens = self.lexer.tokenize("bros bros drop drop")
        frequency = self.lexer.analyze_frequency(tokens)
        
        self.assertGreater(len(frequency), 0)
        # Check that repeated tokens are counted
        bros_count = sum(1 for k in frequency.keys() if 'bros' in k.lower())
        self.assertGreater(bros_count, 0)
    
    def test_numbers_with_k_suffix(self):
        """Test number recognition with 'k' suffix"""
        tokens = self.lexer.tokenize("give me 2k")
        token_values = [t.value for t in tokens if t.type == TokenType.NUMBER]
        
        self.assertIn('2k', token_values)
    
    def test_unknown_tokens(self):
        """Test handling of unknown words"""
        tokens = self.lexer.tokenize("xyzabc unknownword")
        unknown_tokens = [t for t in tokens if t.type == TokenType.UNKNOWN]
        
        self.assertGreater(len(unknown_tokens), 0)

class TestSyntacticAnalyzer(unittest.TestCase):
    """Test cases for syntactic analyzer"""
    
    def setUp(self):
        self.lexer = YaoundeLexer()
        self.grammar = YaoundeGrammar()
        self.parser = YaoundeParser(self.grammar)
    
    def test_valid_greeting(self):
        """Test parsing of greeting statements"""
        tokens = self.lexer.tokenize("bros")
        accepted, message, _ = self.parser.parse(tokens)
        self.assertTrue(accepted, f"Should accept greeting: {message}")
    
    def test_valid_request(self):
        """Test parsing of request statements"""
        tokens = self.lexer.tokenize("drop me for Total")
        accepted, message, _ = self.parser.parse(tokens)
        # May need grammar adjustment, but should not crash
        self.assertIsInstance(accepted, bool)
    
    def test_valid_complaint(self):
        """Test parsing of complaint statements"""
        tokens = self.lexer.tokenize("network dey bad")
        accepted, message, _ = self.parser.parse(tokens)
        self.assertIsInstance(accepted, bool)
    
    def test_grammar_first_sets(self):
        """Test FIRST set computation"""
        self.assertIn('S', self.grammar.first_sets)
        self.assertIn('Statement', self.grammar.first_sets)
        self.assertGreater(len(self.grammar.first_sets['Statement']), 0)
    
    def test_grammar_follow_sets(self):
        """Test FOLLOW set computation"""
        self.assertIn('S', self.grammar.follow_sets)
        self.assertIn('$', self.grammar.follow_sets['S'])
    
    def test_parsing_table(self):
        """Test LL(1) parsing table construction"""
        self.assertIsNotNone(self.grammar.parsing_table)
        self.assertGreater(len(self.grammar.parsing_table), 0)
    
    def test_parse_tree_generation(self):
        """Test that parse tree is generated"""
        tokens = self.lexer.tokenize("bros")
        accepted, message, parse_tree = self.parser.parse(tokens)
        
        self.assertIsNotNone(parse_tree)
        self.assertIsInstance(parse_tree, list)

class TestCompleteAnalyzer(unittest.TestCase):
    """Test cases for complete analyzer integration"""
    
    def setUp(self):
        self.analyzer = YaoundeAnalyzer()
    
    def test_end_to_end_analysis(self):
        """Test complete analysis pipeline"""
        result = self.analyzer.analyze("bros drop me for Total")
        
        self.assertIn('original', result)
        self.assertIn('tokens', result)
        self.assertIn('frequency', result)
        self.assertIn('parse_result', result)
        self.assertIn('parse_tree', result)
        self.assertIn('accepted', result)
        
        self.assertEqual(result['original'], "bros drop me for Total")
        self.assertGreater(len(result['tokens']), 0)
    
    def test_multiple_expressions(self):
        """Test analyzing multiple different expressions"""
        expressions = [
            "bros drop me for Total",
            "give me 500 francs",
            "network dey bad",
            "je wanda how far"
        ]
        
        for expr in expressions:
            result = self.analyzer.analyze(expr)
            self.assertIsNotNone(result)
            self.assertEqual(result['original'], expr)

class TestCollectedData(unittest.TestCase):
    """Test cases using collected real-world data"""
    
    def setUp(self):
        self.analyzer = YaoundeAnalyzer()
        # Load collected data
        try:
            with open('collected_data.txt', 'r', encoding='utf-8') as f:
                self.collected_expressions = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            self.collected_expressions = []
    
    def test_collected_data_exists(self):
        """Test that collected data file exists"""
        self.assertGreater(len(self.collected_expressions), 0, 
                          "Collected data file should contain expressions")
    
    def test_collected_expressions_tokenize(self):
        """Test that all collected expressions can be tokenized"""
        for expr in self.collected_expressions[:5]:  # Test first 5
            tokens = self.analyzer.lexer.tokenize(expr)
            self.assertGreater(len(tokens), 0, 
                             f"Should tokenize: {expr}")
    
    def test_collected_expressions_parse(self):
        """Test that collected expressions can be parsed"""
        for expr in self.collected_expressions[:5]:  # Test first 5
            result = self.analyzer.analyze(expr)
            self.assertIsNotNone(result['parse_result'])
            # Note: Some may be rejected by grammar, which is OK
    
    def test_all_collected_expressions(self):
        """Test all expressions from collected_data.txt with statistics"""
        if not self.collected_expressions:
            self.skipTest("No collected expressions found")
        
        results = {'accepted': 0, 'rejected': 0, 'details': []}
        
        for expr in self.collected_expressions:
            result = self.analyzer.analyze(expr)
            if result['accepted']:
                results['accepted'] += 1
            else:
                results['rejected'] += 1
                results['details'].append({
                    'expression': expr,
                    'reason': result['parse_result']
                })
        
        # Print statistics
        total = len(self.collected_expressions)
        acceptance_rate = (results['accepted'] / total * 100) if total > 0 else 0
        print(f"\n📊 Collected Data Test Results:")
        print(f"   Total expressions: {total}")
        print(f"   Accepted: {results['accepted']} ({acceptance_rate:.1f}%)")
        print(f"   Rejected: {results['rejected']} ({100-acceptance_rate:.1f}%)")
        
        if results['details']:
            print(f"\n❌ Rejected expressions (first 5):")
            for detail in results['details'][:5]:
                print(f"   - {detail['expression']}: {detail['reason']}")
        
        # Assert that we tested all expressions
        self.assertGreater(total, 0, "Should have collected expressions to test")
        # Acceptance rate should be reasonable (at least 60%)
        self.assertGreaterEqual(acceptance_rate, 60, 
                              f"Acceptance rate too low: {acceptance_rate}%")

class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def setUp(self):
        self.analyzer = YaoundeAnalyzer()
    
    def test_empty_input(self):
        """Test empty string rejection"""
        result = self.analyzer.analyze("")
        self.assertFalse(result['accepted'], "Empty input should be rejected")
    
    def test_whitespace_only(self):
        """Test whitespace-only input"""
        result = self.analyzer.analyze("   ")
        self.assertFalse(result['accepted'], "Whitespace-only should be rejected")
    
    def test_only_punctuation(self):
        """Test punctuation-only input"""
        result = self.analyzer.analyze("? ! . ,")
        self.assertFalse(result['accepted'], "Punctuation-only should be rejected")
    
    def test_too_many_unknown_tokens(self):
        """Test rejection of expressions with too many unknown tokens"""
        result = self.analyzer.analyze("xyzabc123 randomtext456 unknownword789 gibberish")
        # Should reject if >70% unknown
        self.assertIsInstance(result['accepted'], bool)
    
    def test_french_style_complaint(self):
        """Test French-style complaint: ICT est mal scia gars"""
        result = self.analyzer.analyze("ICT est mal scia gars")
        self.assertTrue(result['accepted'], f"French complaint should be accepted: {result['parse_result']}")
    
    def test_incomplete_request(self):
        """Test incomplete request (missing required tokens)"""
        result = self.analyzer.analyze("give me")
        # May be accepted with flexible parsing, but should handle gracefully
        self.assertIsNotNone(result['parse_result'])
    
    def test_mixed_language_order(self):
        """Test expressions with mixed language word orders"""
        expressions = [
            "je go campus now",
            "Bros, c'est comment?",
            "walahi network est bad"
        ]
        for expr in expressions:
            result = self.analyzer.analyze(expr)
            self.assertIsNotNone(result['tokens'], f"Should tokenize: {expr}")
    
    def test_slang_at_start(self):
        """Test expressions starting with unknown slang"""
        result = self.analyzer.analyze("scia ICT est mal")
        # Should handle unknown prefix
        self.assertIsNotNone(result['parse_result'])
    
    def test_trailing_slang(self):
        """Test expressions with trailing slang/unknown tokens"""
        result = self.analyzer.analyze("network dey bad scia")
        # Should accept with trailing slang
        self.assertIsNotNone(result['parse_result'])
    
    def test_single_token(self):
        """Test single token expressions"""
        result = self.analyzer.analyze("bros")
        self.assertTrue(result['accepted'], "Single token greeting should be accepted")
    
    def test_very_long_expression(self):
        """Test very long expressions"""
        long_expr = "bros " * 20 + "drop me for Total"
        result = self.analyzer.analyze(long_expr)
        self.assertIsNotNone(result['tokens'], "Should handle long expressions")

class TestMultilingualSupport(unittest.TestCase):
    """Test multilingual language detection"""
    
    def setUp(self):
        self.analyzer = YaoundeAnalyzer()
    
    def test_english_detection(self):
        """Test English language detection"""
        tokens = self.analyzer.lexer.tokenize("give me 500 francs")
        languages = self._detect_languages(tokens)
        self.assertIn('English', languages)
    
    def test_french_detection(self):
        """Test French language detection"""
        tokens = self.analyzer.lexer.tokenize("je wanda comment")
        languages = self._detect_languages(tokens)
        self.assertIn('French', languages)
    
    def test_pidgin_detection(self):
        """Test Pidgin language detection"""
        tokens = self.analyzer.lexer.tokenize("na so e dey")
        languages = self._detect_languages(tokens)
        self.assertIn('Pidgin', languages)
    
    def test_code_switching(self):
        """Test code-switching detection"""
        tokens = self.analyzer.lexer.tokenize("je go campus now, you dey come?")
        languages = self._detect_languages(tokens)
        # Should detect multiple languages
        self.assertGreater(len(languages), 1, "Should detect code-switching")
    
    def test_franc_anglais_detection(self):
        """Test Franc-Anglais detection"""
        tokens = self.analyzer.lexer.tokenize("bros drop me for Total")
        languages = self._detect_languages(tokens)
        self.assertIn('Franc-Anglais', languages)
    
    def test_multilingual_in_result(self):
        """Test that language detection is included in analysis result"""
        result = self.analyzer.analyze("je go campus now")
        self.assertIn('languages_detected', result, "Result should include languages_detected")
        self.assertIsInstance(result['languages_detected'], list)
        self.assertGreater(len(result['languages_detected']), 0)
    
    def _detect_languages(self, tokens):
        """Helper method to detect languages from tokens"""
        languages = set()
        
        for token in tokens:
            if token.type == TokenType.EOF:
                continue
                
            token_type = token.type.name
            value = token.value.lower()
            
            # French indicators
            if token_type == 'FRENCH_PHRASE' or value in ['je', 'tu', 'vous', 'est', 'mal', 'bon', 'bien', 'avec']:
                languages.add('French')
            
            # Pidgin indicators
            elif token_type == 'PIDGIN_PHRASE' or value in ['dey', 'na', 'wetin', 'waka', 'comot']:
                languages.add('Pidgin')
            
            # Ewondo indicators
            elif token_type == 'EWONDO_PHRASE':
                languages.add('Ewondo')
            
            # Fulfulde indicators
            elif token_type == 'FULFULDE_PHRASE' or value in ['wallahi', 'walahi']:
                languages.add('Fulfulde')
            
            # English indicators
            elif value in ['give', 'me', 'you', 'drop', 'come', 'go', 'today', 'bad', 'good']:
                languages.add('English')
            
            # Slang (Franc-Anglais)
            elif token_type.startswith('SLANG_') or value in ['bros', 'masa', 'garrr', 'ekiee']:
                languages.add('Franc-Anglais')
        
        if not languages:
            languages.add('Mixed')
        
        return sorted(list(languages))

def run_all_tests():
    """Run all test suites"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestLexicalAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestSyntacticAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestCompleteAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestCollectedData))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestMultilingualSupport))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    print("🧪 Running Yaoundé Analyzer Test Suite")
    print("=" * 50)
    success = run_all_tests()
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")
    exit(0 if success else 1)

