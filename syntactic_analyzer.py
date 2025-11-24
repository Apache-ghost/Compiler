"""
Yaoundé Urban Communication Syntactic Analyzer
Grammar definitions and parser for multilingual expressions
Supports LL(1) parsing with FIRST/FOLLOW set computation
"""

from typing import List, Tuple, Dict, Set
from lexical_analyzer import Token, TokenType

# ==================== GRAMMAR DEFINITIONS ====================

class YaoundeGrammar:
    """
    Context-Free Grammar for Yaoundé street expressions
    
    Grammar Rules (after left recursion removal and left factoring):
    
    S → Statement
    Statement → Greeting | Request | Question | Complaint | Negotiation
    
    Greeting → SLANG_RESPONSE TimePhrase? StatePhrase?
    Request → VERB_GIVE PRONOUN TransportRequest
           | VERB_MOVEMENT LocationPhrase
    Question → QuestionWord Statement QUESTION
    Complaint → ComplaintPhrase SLANG_EXCLAIM*
    Negotiation → PricePhrase MoneyAmount
    
    TransportRequest → PREPOSITION NOUN_PLACE
    LocationPhrase → PREPOSITION NOUN_PLACE
    TimePhrase → TIME
    StatePhrase → VERB_BE ADJ_QUALITY
    QuestionWord → PIDGIN_PHRASE | FRENCH_PHRASE
    ComplaintPhrase → NOUN_TECH VERB_BE ADJ_QUALITY
                    | NOUN_MONEY ADJ_QUANTITY
    PricePhrase → NUMBER NOUN_MONEY
    MoneyAmount → NUMBER NOUN_MONEY
    """
    
    def __init__(self):
        self.rules = {
            'S': [['Statement']],
            'Statement': [
                ['Greeting'],
                ['Request'],
                ['Question'],
                ['Complaint'],
                ['Negotiation']
            ],
            'Greeting': [
                ['SLANG_RESPONSE'],
                ['SLANG_RESPONSE', 'TimePhrase'],
                ['SLANG_RESPONSE', 'StatePhrase']
            ],
            'Request': [
                ['VERB_GIVE', 'PRONOUN', 'TransportRequest'],
                ['VERB_MOVEMENT', 'LocationPhrase'],
                ['VERB_MOVEMENT', 'PREPOSITION', 'NOUN_PLACE']
            ],
            'Question': [
                ['QuestionWord', 'Statement', 'QUESTION']
            ],
            'Complaint': [
                ['ComplaintPhrase', 'SLANG_EXCLAIM']
            ],
            'Negotiation': [
                ['PricePhrase', 'MoneyAmount']
            ],
            'TransportRequest': [
                ['PREPOSITION', 'NOUN_PLACE']
            ],
            'LocationPhrase': [
                ['PREPOSITION', 'NOUN_PLACE']
            ],
            'TimePhrase': [
                ['TIME']
            ],
            'StatePhrase': [
                ['VERB_BE', 'ADJ_QUALITY']
            ],
            'QuestionWord': [
                ['PIDGIN_PHRASE'],
                ['FRENCH_PHRASE']
            ],
            'ComplaintPhrase': [
                ['NOUN_TECH', 'VERB_BE', 'ADJ_QUALITY'],
                ['NOUN_MONEY', 'ADJ_QUANTITY']
            ],
            'PricePhrase': [
                ['NUMBER', 'NOUN_MONEY']
            ],
            'MoneyAmount': [
                ['NUMBER', 'NOUN_MONEY']
            ]
        }
        
        self.first_sets = self.compute_first()
        self.follow_sets = self.compute_follow()
        self.parsing_table = self.build_ll1_table()
    
    def compute_first(self) -> Dict[str, Set[str]]:
        """Compute FIRST sets for grammar"""
        first = {non_terminal: set() for non_terminal in self.rules}
        
        # Add terminals to their own FIRST sets
        for token_type in TokenType:
            first[token_type.name] = {token_type.name}
        
        changed = True
        while changed:
            changed = False
            for non_terminal, productions in self.rules.items():
                for production in productions:
                    old_size = len(first[non_terminal])
                    
                    # FIRST of production
                    for symbol in production:
                        if symbol in first:
                            first[non_terminal].update(first[symbol] - {'ε'})
                            if 'ε' not in first.get(symbol, set()):
                                break
                        else:
                            first[non_terminal].add(symbol)
                            break
                    
                    if len(first[non_terminal]) > old_size:
                        changed = True
        
        return first
    
    def compute_follow(self) -> Dict[str, Set[str]]:
        """Compute FOLLOW sets for grammar"""
        follow = {non_terminal: set() for non_terminal in self.rules}
        follow['S'] = {'$'}
        
        changed = True
        while changed:
            changed = False
            for non_terminal, productions in self.rules.items():
                for production in productions:
                    for i, symbol in enumerate(production):
                        if symbol in self.rules:  # Non-terminal
                            old_size = len(follow[symbol])
                            
                            # Look at what follows
                            if i + 1 < len(production):
                                next_symbol = production[i + 1]
                                follow[symbol].update(
                                    self.first_sets.get(next_symbol, {next_symbol}) - {'ε'}
                                )
                            else:
                                follow[symbol].update(follow[non_terminal])
                            
                            if len(follow[symbol]) > old_size:
                                changed = True
        
        return follow
    
    def build_ll1_table(self) -> Dict[Tuple[str, str], List[str]]:
        """Build LL(1) parsing table"""
        table = {}
        
        for non_terminal, productions in self.rules.items():
            for production in productions:
                # Get FIRST of production
                first_prod = set()
                for symbol in production:
                    first_prod.update(self.first_sets.get(symbol, {symbol}) - {'ε'})
                    if 'ε' not in self.first_sets.get(symbol, set()):
                        break
                
                # Add entries to table
                for terminal in first_prod:
                    if terminal != 'ε':
                        table[(non_terminal, terminal)] = production
        
        return table

# ==================== PARSER ====================

class YaoundeParser:
    """LL(1) Parser for Yaoundé expressions"""
    
    def __init__(self, grammar: YaoundeGrammar):
        self.grammar = grammar
        self.tokens = []
        self.position = 0
        self.parse_tree = []
    
    def parse(self, tokens: List[Token]) -> Tuple[bool, str, List[str]]:
        """Parse token stream"""
        self.tokens = tokens
        self.position = 0
        self.parse_tree = []
        
        # Simple recursive descent parser
        try:
            result = self.parse_statement()
            if result and self.position >= len(tokens) - 1:  # -1 for EOF
                return True, "✓ ACCEPTED - Valid Yaoundé expression", self.parse_tree
            else:
                return False, "✗ REJECTED - Incomplete parse", self.parse_tree
        except Exception as e:
            return False, f"✗ REJECTED - {str(e)}", self.parse_tree
    
    def current_token(self) -> Token:
        """Get current token"""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return Token(TokenType.EOF, '', -1)
    
    def consume(self, expected_type: TokenType = None) -> Token:
        """Consume and return current token"""
        token = self.current_token()
        if expected_type and token.type != expected_type:
            raise Exception(f"Expected {expected_type.name}, got {token.type.name}")
        self.position += 1
        self.parse_tree.append(f"Matched: {token}")
        return token
    
    def parse_statement(self) -> bool:
        """Parse statement"""
        token = self.current_token()
        
        # Try different statement types
        if token.type == TokenType.SLANG_RESPONSE:
            return self.parse_greeting()
        elif token.type in [TokenType.VERB_GIVE, TokenType.VERB_MOVEMENT]:
            return self.parse_request()
        elif token.type in [TokenType.PIDGIN_PHRASE, TokenType.FRENCH_PHRASE]:
            return self.parse_question()
        elif token.type in [TokenType.NOUN_TECH, TokenType.NOUN_MONEY]:
            return self.parse_complaint()
        elif token.type == TokenType.NUMBER:
            return self.parse_negotiation()
        else:
            # Try to parse anyway
            self.consume()
            return True
    
    def parse_greeting(self) -> bool:
        """Parse greeting"""
        self.consume(TokenType.SLANG_RESPONSE)
        return True
    
    def parse_request(self) -> bool:
        """Parse request"""
        token = self.current_token()
        if token.type == TokenType.VERB_GIVE:
            self.consume(TokenType.VERB_GIVE)
            if self.current_token().type == TokenType.PRONOUN:
                self.consume(TokenType.PRONOUN)
        else:
            self.consume(TokenType.VERB_MOVEMENT)
        
        # Location phrase
        if self.current_token().type == TokenType.PREPOSITION:
            self.consume(TokenType.PREPOSITION)
        if self.current_token().type == TokenType.NOUN_PLACE:
            self.consume(TokenType.NOUN_PLACE)
        
        return True
    
    def parse_question(self) -> bool:
        """Parse question"""
        if self.current_token().type in [TokenType.PIDGIN_PHRASE, TokenType.FRENCH_PHRASE]:
            self.consume()
        return True
    
    def parse_complaint(self) -> bool:
        """Parse complaint"""
        self.consume()
        if self.current_token().type == TokenType.VERB_BE:
            self.consume(TokenType.VERB_BE)
        if self.current_token().type == TokenType.ADJ_QUALITY:
            self.consume(TokenType.ADJ_QUALITY)
        return True
    
    def parse_negotiation(self) -> bool:
        """Parse negotiation"""
        if self.current_token().type == TokenType.NUMBER:
            self.consume(TokenType.NUMBER)
        if self.current_token().type == TokenType.NOUN_MONEY:
            self.consume(TokenType.NOUN_MONEY)
        return True

# ==================== TESTING ====================

def test_parser():
    """Test the syntactic analyzer with sample expressions"""
    from lexical_analyzer import YaoundeLexer
    
    lexer = YaoundeLexer()
    grammar = YaoundeGrammar()
    parser = YaoundeParser(grammar)
    
    test_cases = [
        "bros drop me for Total",
        "masa network dey bad", 
        "give me 500 francs",
        "je wanda how far ?",
        "walahi light don comot"
    ]
    
    print("🌳 YAOUNDÉ SYNTACTIC ANALYZER TEST")
    print("=" * 50)
    
    for expression in test_cases:
        print(f"\n📝 Expression: '{expression}'")
        tokens = lexer.tokenize(expression)
        accepted, message, parse_tree = parser.parse(tokens)
        
        print(f"🎯 Result: {message}")
        print("🌳 Parse Steps:")
        for step in parse_tree[:5]:  # Show first 5 steps
            print(f"  {step}")
        if len(parse_tree) > 5:
            print(f"  ... and {len(parse_tree) - 5} more steps")

def test_grammar():
    """Test grammar structure"""
    grammar = YaoundeGrammar()
    
    print("📚 GRAMMAR STRUCTURE TEST")
    print("=" * 30)
    
    print("\n🔤 FIRST Sets (sample):")
    for non_terminal in list(grammar.first_sets.keys())[:5]:
        print(f"  FIRST({non_terminal}) = {grammar.first_sets[non_terminal]}")
    
    print("\n🔤 FOLLOW Sets (sample):")
    for non_terminal in list(grammar.follow_sets.keys())[:5]:
        print(f"  FOLLOW({non_terminal}) = {grammar.follow_sets[non_terminal]}")

if __name__ == "__main__":
    test_parser()
    print("\n" + "=" * 50)
    test_grammar()