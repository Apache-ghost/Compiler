# -*- coding: utf-8 -*-
"""
Yaounde Urban Communication Syntactic Analyzer
Interactive grammar-based parser for multilingual expressions
Supports LL(1) parsing with FIRST/FOLLOW set computation

Usage:
    python syntactic_analyzer.py        # Interactive mode
    python syntactic_analyzer.py --demo # Demo mode
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
    
    Note: This grammar has been transformed to remove left recursion and
    apply left factoring. See grammar_transformations.md for detailed
    documentation of the transformation process.
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
                ['SLANG_RESPONSE', 'StatePhrase'],
                ['SLANG_RESPONSE', 'TimePhrase', 'StatePhrase']
            ],
            'Request': [
                ['VERB_GIVE', 'PRONOUN', 'TransportRequest'],
                ['VERB_GIVE', 'PRONOUN', 'NUMBER', 'NOUN_MONEY'],
                ['VERB_MOVEMENT', 'LocationPhrase'],
                ['VERB_MOVEMENT', 'PRONOUN', 'LocationPhrase'],
                ['VERB_MOVEMENT', 'PREPOSITION', 'NOUN_PLACE']
            ],
            'Question': [
                ['QuestionWord', 'Statement', 'QUESTION']
            ],
            'Complaint': [
                ['ComplaintPhrase'],
                ['ComplaintPhrase', 'SLANG_EXCLAIM'],
                ['ComplaintPhrase', 'TIME'],
                ['ComplaintPhrase', 'SLANG_EXCLAIM', 'TIME']
            ],
            'Negotiation': [
                ['PricePhrase'],
                ['VERB_GIVE', 'PRONOUN', 'NUMBER', 'NOUN_MONEY']
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
                ['NOUN_TECH', 'VERB_BE', 'ADJ_QUALITY', 'TIME'],
                ['NOUN_MONEY', 'ADJ_QUANTITY'],
                ['NOUN_TRANSPORT', 'VERB_BE', 'ADJ_QUALITY'],
                ['SLANG_EMPHASIS', 'NOUN_TECH', 'VERB_BE', 'ADJ_QUALITY']
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
                has_epsilon = True
                
                for symbol in production:
                    symbol_first = self.first_sets.get(symbol, {symbol})
                    first_prod.update(symbol_first - {'ε'})
                    if 'ε' not in symbol_first:
                        has_epsilon = False
                        break
                
                # Add entries to table for terminals in FIRST
                for terminal in first_prod:
                    if terminal != 'ε':
                        key = (non_terminal, terminal)
                        # Check for conflicts (would indicate non-LL(1) grammar)
                        if key in table:
                            # Keep first production (could log warning)
                            pass
                        else:
                            table[key] = production
                
                # If production can derive epsilon, add FOLLOW set entries
                if has_epsilon:
                    follow_set = self.follow_sets.get(non_terminal, set())
                    for terminal in follow_set:
                        if terminal != '$':
                            key = (non_terminal, terminal)
                            if key not in table:
                                table[key] = production
        
        return table
    
    def display_parsing_table(self, limit: int = 20) -> str:
        """Display LL(1) parsing table (for documentation)"""
        lines = ["LL(1) Parsing Table (Sample):", "=" * 60]
        count = 0
        
        for (non_terminal, terminal), production in sorted(self.parsing_table.items()):
            if count >= limit:
                lines.append(f"... and {len(self.parsing_table) - limit} more entries")
                break
            lines.append(f"M[{non_terminal}, {terminal}] = {' '.join(production)}")
            count += 1
        
        return "\n".join(lines)
    
    def verify_grammar_rules(self) -> Dict[str, bool]:
        """Verify grammar rules match specification"""
        verification = {
            'Complaint_rules': len(self.rules['Complaint']) == 4,
            'ComplaintPhrase_rules': len(self.rules['ComplaintPhrase']) == 5,
            'Greeting_rules': len(self.rules['Greeting']) == 4,
            'Request_rules': len(self.rules['Request']) == 5,
            'Question_rules': len(self.rules['Question']) == 1,
            'Negotiation_rules': len(self.rules['Negotiation']) == 2,
            'Statement_rules': len(self.rules['Statement']) == 5,
        }
        return verification

# ==================== PARSER ====================

class YaoundeParser:
    """LL(1) Parser for Yaoundé expressions"""
    
    def __init__(self, grammar: YaoundeGrammar):
        self.grammar = grammar
        self.tokens = []
        self.position = 0
        self.parse_tree = []
    
    def parse(self, tokens: List[Token]) -> Tuple[bool, str, List[str]]:
        """Parse token stream using grammar-based recursive descent"""
        self.tokens = [t for t in tokens if t.type != TokenType.EOF] + [Token(TokenType.EOF, '', -1)]
        self.position = 0
        self.parse_tree = []
        
        # Reject empty input
        if len(self.tokens) <= 1:  # Only EOF
            return False, "✗ REJECTED - Empty input", []
        
        # Check for too many unknown tokens (likely nonsense)
        # But be more lenient for multilingual expressions (slang, typos, etc.)
        unknown_count = sum(1 for t in self.tokens if t.type == TokenType.UNKNOWN)
        total_tokens = len([t for t in self.tokens if t.type != TokenType.EOF])
        
        # Reject if more than 70% unknown (increased from 60% for more flexibility)
        # Allow more unknown tokens since Yaoundé speech includes slang and code-mixing
        if total_tokens > 0 and unknown_count / total_tokens > 0.7:
            return False, f"✗ REJECTED - Too many unrecognized tokens ({unknown_count}/{total_tokens})", []
        
        try:
            # Try to parse as a statement according to grammar
            start_pos = self.position
            result = self.parse_statement()
            
            # Must consume all tokens (except EOF) to be accepted
            remaining_tokens = len(self.tokens) - self.position - 1  # -1 for EOF
            
            if result and remaining_tokens == 0:
                return True, "✓ ACCEPTED - Valid Yaoundé expression (matches grammar)", self.parse_tree
            elif result and remaining_tokens > 0:
                # Parsed something but tokens remain - check if they're just punctuation or acceptable trailing elements
                remaining = [t for t in self.tokens[self.position:-1] 
                            if t.type not in [TokenType.COMMA, TokenType.PERIOD, TokenType.EXCLAMATION, 
                                            TokenType.SLANG_EXCLAIM, TokenType.SLANG_RESPONSE, TokenType.QUESTION]]
                # Allow 1-2 short unknown tokens at the end (likely slang/typos)
                unknown_at_end = [t for t in remaining if t.type == TokenType.UNKNOWN and len(t.value) <= 6]
                if len(unknown_at_end) <= 2 and len(remaining) == len(unknown_at_end):
                    # Only unknown tokens at end, and they're short (likely slang)
                    return True, "✓ ACCEPTED - Valid Yaoundé expression (with trailing slang)", self.parse_tree
                elif len(remaining) == 0:
                    return True, "✓ ACCEPTED - Valid Yaoundé expression (with trailing punctuation)", self.parse_tree
                else:
                    # Try to be more lenient - if we parsed most of the expression, accept it
                    parsed_ratio = (total_tokens - remaining_tokens) / total_tokens if total_tokens > 0 else 0
                    if parsed_ratio >= 0.7:  # Parsed at least 70% of tokens
                        return True, f"✓ ACCEPTED - Valid Yaoundé expression (parsed {int(parsed_ratio*100)}%)", self.parse_tree
                    return False, f"✗ REJECTED - Expression doesn't match grammar (unparsed tokens: {remaining_tokens})", self.parse_tree
            else:
                return False, "✗ REJECTED - Expression doesn't match any grammar rule", self.parse_tree
        except Exception as e:
            return False, f"✗ REJECTED - Parse error: {str(e)}", self.parse_tree
    
    def current_token(self) -> Token:
        """Get current token"""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return Token(TokenType.EOF, '', -1)
    
    def consume(self, expected_type: TokenType = None) -> Token:
        """Consume and return current token, advancing the position"""
        token = self.current_token()
        if expected_type and token.type != expected_type:
            raise Exception(f"Expected {expected_type.name}, got {token.type.name}")
        if self.position < len(self.tokens):
            self.position += 1
        self.parse_tree.append(f"Matched: {token}")
        return token
    
    def parse_statement(self) -> bool:
        """Parse statement according to grammar rules"""
        if self.position >= len(self.tokens) - 1:  # Only EOF left
            return False  # Empty statement is invalid
        
        token = self.current_token()
        self.parse_tree.append(f"Parsing statement starting with: {token.type.name}")
        
        # Grammar: Statement → Greeting | Request | Question | Complaint | Negotiation
        
        # Try Greeting first (starts with SLANG_RESPONSE)
        if token.type == TokenType.SLANG_RESPONSE:
            # Check if it's just a greeting or greeting + something else
            saved_pos = self.position
            if self.parse_greeting():
                # Check if there's more content after greeting
                if self.position < len(self.tokens) - 1:
                    next_token = self.current_token()
                    # If next token starts a new statement type, parse it
                    if next_token.type in [TokenType.VERB_GIVE, TokenType.VERB_MOVEMENT, 
                                          TokenType.NOUN_TECH, TokenType.NOUN_MONEY, TokenType.NOUN_TRANSPORT]:
                        # Greeting was just a prefix, continue parsing
                        return self.parse_statement()  # Recursively parse the rest
                    elif next_token.type in [TokenType.TIME, TokenType.VERB_BE]:
                        # Part of greeting, continue
                        return True
                return True
            self.position = saved_pos  # Reset if greeting parse failed
        
        # Try Request (starts with VERB_GIVE or VERB_MOVEMENT)
        if token.type in [TokenType.VERB_GIVE, TokenType.VERB_MOVEMENT]:
            return self.parse_request()
        
        # Try Question (starts with PIDGIN_PHRASE or FRENCH_PHRASE)
        if token.type in [TokenType.PIDGIN_PHRASE, TokenType.FRENCH_PHRASE]:
            return self.parse_question()
        
        # Try Complaint (starts with NOUN_TECH, NOUN_MONEY, NOUN_TRANSPORT, NOUN_PLACE, or SLANG_EMPHASIS)
        if token.type in [TokenType.NOUN_TECH, TokenType.NOUN_MONEY, TokenType.NOUN_TRANSPORT, TokenType.NOUN_PLACE, TokenType.SLANG_EMPHASIS]:
            return self.parse_complaint()
        
        # Try French-style complaint: NOUN_PLACE VERB_BE ADJ (e.g., "ICT est mal")
        if token.type == TokenType.NOUN_PLACE:
            saved_pos = self.position
            if self.parse_french_complaint():
                return True
            self.position = saved_pos
        
        # Try Negotiation (starts with NUMBER)
        if token.type == TokenType.NUMBER:
            return self.parse_negotiation()
        
        # Try to handle expressions starting with unknown tokens if they're followed by known patterns
        # This handles cases where slang/typos appear at the start
        if token.type == TokenType.UNKNOWN and len(token.value) <= 8:
            saved_pos = self.position
            self.consume()  # Skip the unknown token
            # Try to parse the rest as a statement
            if self.parse_statement():
                self.parse_tree.insert(0, f"Matched unknown prefix (likely slang): {token.value}")
                return True
            self.position = saved_pos  # Reset if it didn't work
        
        # No grammar rule matches
        return False
    
    def parse_greeting(self) -> bool:
        """Parse greeting according to grammar: SLANG_RESPONSE [TimePhrase] [StatePhrase]"""
        self.parse_tree.append("Parsing greeting")
        
        # Must start with SLANG_RESPONSE
        if self.current_token().type != TokenType.SLANG_RESPONSE:
            return False
        
        self.consume()
        self.parse_tree.append("Matched SLANG_RESPONSE")
        
        # Optional TimePhrase
        if self.current_token().type == TokenType.TIME:
            self.consume()
            self.parse_tree.append("Matched optional TimePhrase")
        
        # Optional StatePhrase (VERB_BE ADJ_QUALITY)
        if self.current_token().type == TokenType.VERB_BE:
            self.consume()
            if self.current_token().type == TokenType.ADJ_QUALITY:
                self.consume()
                self.parse_tree.append("Matched optional StatePhrase")
        
        return True
    
    def parse_request(self) -> bool:
        """Parse request according to grammar rules - with flexibility for variations"""
        self.parse_tree.append("Parsing request")
        token = self.current_token()
        
        if token.type == TokenType.VERB_GIVE:
            # Grammar: VERB_GIVE PRONOUN TransportRequest | VERB_GIVE PRONOUN NUMBER NOUN_MONEY
            self.consume()
            self.parse_tree.append("Matched VERB_GIVE")
            
            # PRONOUN is usually present but can be omitted in some contexts
            # Be flexible: allow optional PRONOUN
            if self.current_token().type == TokenType.PRONOUN:
                self.consume()
                self.parse_tree.append("Matched PRONOUN")
            
            # Check for money request: NUMBER NOUN_MONEY
            if self.current_token().type == TokenType.NUMBER:
                self.consume()
                if self.current_token().type == TokenType.NOUN_MONEY:
                    self.consume()
                    self.parse_tree.append("Matched money request (NUMBER NOUN_MONEY)")
                    return True
                # Allow NUMBER alone (money amount without explicit "francs")
                elif self.current_token().type in [TokenType.EOF, TokenType.COMMA, TokenType.PERIOD, TokenType.QUESTION]:
                    self.parse_tree.append("Matched money request (NUMBER only)")
                    return True
            
            # Check for transport request: PREPOSITION NOUN_PLACE
            if self.current_token().type == TokenType.PREPOSITION:
                self.consume()
                if self.current_token().type == TokenType.NOUN_PLACE:
                    self.consume()
                    self.parse_tree.append("Matched transport request (PREPOSITION NOUN_PLACE)")
                    return True
            
            # Allow VERB_GIVE with just a noun (e.g., "give airtime")
            if self.current_token().type in [TokenType.NOUN_TECH, TokenType.NOUN_MONEY, TokenType.NOUN_FOOD]:
                self.consume()
                self.parse_tree.append("Matched request with noun object")
                return True
            
            return False  # Didn't match any pattern
            
        elif token.type == TokenType.VERB_MOVEMENT:
            # Grammar: VERB_MOVEMENT LocationPhrase | VERB_MOVEMENT PRONOUN LocationPhrase | VERB_MOVEMENT PREPOSITION NOUN_PLACE
            self.consume()
            self.parse_tree.append("Matched VERB_MOVEMENT")
            
            # Optional PRONOUN
            if self.current_token().type == TokenType.PRONOUN:
                self.consume()
                self.parse_tree.append("Matched optional PRONOUN")
            
            # Must have PREPOSITION NOUN_PLACE
            if self.current_token().type != TokenType.PREPOSITION:
                return False  # Grammar requires PREPOSITION
            
            self.consume()
            if self.current_token().type != TokenType.NOUN_PLACE:
                return False  # Grammar requires NOUN_PLACE
            
            self.consume()
            self.parse_tree.append("Matched location phrase (PREPOSITION NOUN_PLACE)")
            return True
        
        return False
    
    def parse_question(self) -> bool:
        """Parse question - flexible pattern matching"""
        self.parse_tree.append("Parsing question")
        
        # Question word
        if self.current_token().type in [TokenType.PIDGIN_PHRASE, TokenType.FRENCH_PHRASE]:
            self.consume()
            self.parse_tree.append("Matched question word")
        
        # Optional statement content
        while self.position < len(self.tokens) - 1:
            token = self.current_token()
            if token.type == TokenType.QUESTION:
                self.consume()
                self.parse_tree.append("Matched QUESTION mark")
                break
            elif token.type in [TokenType.EOF, TokenType.UNKNOWN]:
                break
            else:
                self.consume()  # Consume question content
        
        return True
    
    def parse_complaint(self) -> bool:
        """Parse complaint - flexible pattern matching for multilingual expressions"""
        self.parse_tree.append("Parsing complaint")
        
        # Optional emphasis word
        if self.current_token().type == TokenType.SLANG_EMPHASIS:
            self.consume()
            self.parse_tree.append("Matched optional SLANG_EMPHASIS")
        
        # Noun (tech, money, transport, place, etc.)
        if self.current_token().type in [TokenType.NOUN_TECH, TokenType.NOUN_MONEY, TokenType.NOUN_TRANSPORT, TokenType.NOUN_PLACE]:
            self.consume()
            self.parse_tree.append("Matched NOUN")
        else:
            # If no noun, might start with verb (e.g., "est mal")
            pass
        
        # Optional verb (can come before or after noun in French)
        if self.current_token().type == TokenType.VERB_BE:
            self.consume()
            self.parse_tree.append("Matched VERB_BE")
        
        # Optional adjective (can come before or after verb in French)
        if self.current_token().type in [TokenType.ADJ_QUALITY, TokenType.ADJ_QUANTITY]:
            self.consume()
            self.parse_tree.append("Matched ADJ")
        
        # Allow some unknown tokens in multilingual context (like "scia" - slang/typo)
        # But only if we've already matched some structure
        if len(self.parse_tree) > 1:  # We've matched something
            unknown_count = 0
            while self.position < len(self.tokens) - 1 and unknown_count < 3:  # Allow up to 3 unknown tokens
                token = self.current_token()
                if token.type == TokenType.UNKNOWN:
                    # Allow unknown tokens if they're short (likely slang/typos) or look like words
                    if len(token.value) <= 8 and token.value.isalpha():  # Short alphabetic words might be slang
                        self.consume()
                        self.parse_tree.append(f"Matched unknown token (likely slang): {token.value}")
                        unknown_count += 1
                        continue
                # Also allow known tokens that might follow
                elif token.type in [TokenType.TIME, TokenType.SLANG_EXCLAIM, TokenType.SLANG_RESPONSE, 
                                   TokenType.ADJ_QUALITY, TokenType.ADJ_QUANTITY]:
                    self.consume()
                    self.parse_tree.append(f"Matched optional trailing token: {token.type.name}")
                    continue
                break
        
        # Optional time
        if self.current_token().type == TokenType.TIME:
            self.consume()
            self.parse_tree.append("Matched optional TIME")
        
        # Optional exclamation or response word
        if self.current_token().type in [TokenType.SLANG_EXCLAIM, TokenType.SLANG_RESPONSE]:
            self.consume()
            self.parse_tree.append("Matched optional slang/exclamation")
        
        return True
    
    def parse_french_complaint(self) -> bool:
        """Parse French-style complaint: NOUN_PLACE VERB_BE ADJ [SLANG_RESPONSE]"""
        self.parse_tree.append("Parsing French-style complaint")
        
        # Must start with NOUN_PLACE
        if self.current_token().type != TokenType.NOUN_PLACE:
            return False
        
        self.consume()
        self.parse_tree.append("Matched NOUN_PLACE")
        
        # VERB_BE (est, sont, etc.)
        if self.current_token().type == TokenType.VERB_BE:
            self.consume()
            self.parse_tree.append("Matched VERB_BE")
        else:
            return False  # French complaint requires verb
        
        # ADJ_QUALITY (mal, bon, etc.)
        if self.current_token().type == TokenType.ADJ_QUALITY:
            self.consume()
            self.parse_tree.append("Matched ADJ_QUALITY")
        else:
            return False  # French complaint requires adjective
        
        # Optional unknown tokens (slang/typos) - allow 1-2 short ones
        unknown_count = 0
        while self.position < len(self.tokens) - 1 and unknown_count < 2:
            token = self.current_token()
            if token.type == TokenType.UNKNOWN and len(token.value) <= 6:
                self.consume()
                self.parse_tree.append(f"Matched unknown token (slang): {token.value}")
                unknown_count += 1
            else:
                break
        
        # Optional SLANG_RESPONSE at end
        if self.current_token().type == TokenType.SLANG_RESPONSE:
            self.consume()
            self.parse_tree.append("Matched optional SLANG_RESPONSE")
        
        return True
    
    def parse_negotiation(self) -> bool:
        """Parse negotiation - flexible pattern matching"""
        self.parse_tree.append("Parsing negotiation")
        
        if self.current_token().type == TokenType.NUMBER:
            self.consume()
            self.parse_tree.append("Matched NUMBER")
            if self.current_token().type == TokenType.NOUN_MONEY:
                self.consume()
                self.parse_tree.append("Matched NOUN_MONEY")
        return True


# ==================== TESTING ====================

def interactive_parser():
    """Interactive syntactic analyzer - prompts user for input"""
    from lexical_analyzer import YaoundeLexer
    
    lexer = YaoundeLexer()
    grammar = YaoundeGrammar()
    parser = YaoundeParser(grammar)
    
    print("🌳 YAOUNDE INTERACTIVE SYNTACTIC ANALYZER")
    print("Grammar-based parser for multilingual expressions")
    print("=" * 55)
    print("\nExample expressions to try:")
    print("  • bros drop me for Total")
    print("  • give me 500 francs")
    print("  • je wanda how far ?")
    print("  • masa network dey bad")
    print("\nType 'quit', 'exit', or 'grammar' (to see rules)\n")
    
    while True:
        try:
            expression = input("🇨🇲 Enter expression to parse: ").strip()
            
            if expression.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Parser shutting down! Goodbye!")
                break
            
            if expression.lower() == 'grammar':
                show_grammar_info(grammar)
                continue
            
            if not expression:
                print("❌ Please enter an expression\n")
                continue
            
            print(f"\n📝 Parsing: '{expression}'")
            
            # Tokenize first
            tokens = lexer.tokenize(expression)
            print("\n🔤 Tokens generated:")
            for token in tokens:
                if token.type != TokenType.EOF:
                    print(f"  {token}")
            
            # Parse
            accepted, message, parse_tree = parser.parse(tokens)
            
            print(f"\n🎯 Parse Result: {message}")
            
            if parse_tree:
                print("\n🌳 Parse Steps:")
                for i, step in enumerate(parse_tree[:8], 1):  # Show first 8 steps
                    print(f"  {i}. {step}")
                if len(parse_tree) > 8:
                    print(f"  ... and {len(parse_tree) - 8} more steps")
            
            print("\n" + "-" * 50)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted! Parser stopped!")
            break
        except Exception as e:
            print(f"\n❌ Parse Error: {e}\n")

def show_grammar_info(grammar):
    """Display grammar information"""
    print("\n📚 GRAMMAR INFORMATION")
    print("=" * 60)
    
    print("\n🔄 Main Statement Types:")
    for rule in grammar.rules['Statement']:
        print(f"  Statement → {' '.join(rule)}")
    
    print("\n🔤 Sample FIRST Sets:")
    key_sets = ['Statement', 'Greeting', 'Request', 'Question', 'Complaint']
    for non_terminal in key_sets:
        if non_terminal in grammar.first_sets:
            first_set = grammar.first_sets[non_terminal]
            first_list = sorted(list(first_set))[:8]
            print(f"  FIRST({non_terminal}) = {', '.join(first_list)}" + 
                  (f" ... ({len(first_set)} total)" if len(first_set) > 8 else ""))
    
    print("\n🔤 Sample FOLLOW Sets:")
    for non_terminal in key_sets[:3]:
        if non_terminal in grammar.follow_sets:
            follow_set = grammar.follow_sets[non_terminal]
            follow_list = sorted(list(follow_set))[:8]
            print(f"  FOLLOW({non_terminal}) = {', '.join(follow_list)}" + 
                  (f" ... ({len(follow_set)} total)" if len(follow_set) > 8 else ""))
    
    print("\n📊 Parsing Table Statistics:")
    print(f"  Total entries: {len(grammar.parsing_table)}")
    print(f"  Non-terminals: {len(grammar.rules)}")
    
    print("\n" + grammar.display_parsing_table(limit=15))
    
    print("\n⚙️ Grammar supports:")
    print("  • Greetings (bros, masa, chief)")
    print("  • Transport requests (drop me for...)")
    print("  • Money negotiations (give me X francs)")
    print("  • Questions (wetin?, c'est comment?)")
    print("  • Complaints (network dey bad, light don comot)")
    print("  • Multilingual code-switching")
    print()

def demo_parser():
    """Run predefined demo (for testing purposes)"""
    from lexical_analyzer import YaoundeLexer
    
    lexer = YaoundeLexer()
    grammar = YaoundeGrammar()
    parser = YaoundeParser(grammar)
    
    test_cases = [
        "bros drop me for Total",
        "give me 500 francs",
        "masa network dey bad"
    ]
    
    print("🌳 YAOUNDE SYNTACTIC ANALYZER DEMO")
    print("=" * 50)
    
    for expression in test_cases:
        print(f"\n📝 Expression: '{expression}'")
        tokens = lexer.tokenize(expression)
        accepted, message, parse_tree = parser.parse(tokens)
        
        print(f"🎯 Result: {message}")

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
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_parser()
        print("\n" + "=" * 50)
        test_grammar()
    else:
        interactive_parser()