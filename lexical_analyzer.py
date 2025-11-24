"""
Yaoundé Urban Communication Lexical Analyzer
Tokenizes multilingual Cameroonian street language
Supports: English, French, Pidgin, Fulfulde, Ewondo, and Franc-Anglais
"""

import re
from typing import List, Tuple, Dict, Set
from dataclasses import dataclass
from enum import Enum, auto

# ==================== TOKEN DEFINITIONS ====================

class TokenType(Enum):
    # Nouns - Yaoundé specific
    NOUN_PLACE = auto()        # quartier, carrefour, campus
    NOUN_PERSON = auto()       # moto-guy, mbere, patron
    NOUN_TRANSPORT = auto()    # taxi, bendskin, moto
    NOUN_MONEY = auto()        # fap, mbongo, kop, francs
    NOUN_FOOD = auto()         # tchop, ndole, eru, koki
    NOUN_TECH = auto()         # call, airtime, WiFi
    
    # Verbs - Mixed language actions
    VERB_MOVEMENT = auto()     # go, comot, waka, aller
    VERB_GIVE = auto()         # give, send, dash, donner
    VERB_BE = auto()           # be, dey, etre
    VERB_GENERAL = auto()      # do, see, hear, mek
    
    # Adjectives & States
    ADJ_QUALITY = auto()       # bon, nye, correct, bad
    ADJ_QUANTITY = auto()      # plenty, small, trop
    
    # Slang & Exclamations
    SLANG_EXCLAIM = auto()     # ehn, hmmm, garrr, ekiee, walai
    SLANG_EMPHASIS = auto()    # direct, serious, weh
    SLANG_RESPONSE = auto()    # masa, bros, chief, sango
    
    # Code-mixed expressions
    PIDGIN_PHRASE = auto()     # na so, no be, i don
    FRENCH_PHRASE = auto()     # c'est comment, ça va pas
    EWONDO_PHRASE = auto()     # a ye moan, mbokesso
    FULFULDE_PHRASE = auto()   # allah yai, wallahi
    
    # Grammar elements
    PREPOSITION = auto()       # for, na, avec, à
    CONJUNCTION = auto()       # and, avec, na, but
    DETERMINER = auto()        # the, di, le, some
    PRONOUN = auto()           # me, we, i, you, tu
    
    # Numbers & Quantities
    NUMBER = auto()            # 100, 500, 2k, 5k
    TIME = auto()              # today, tomorrow, now
    
    # Punctuation
    QUESTION = auto()          # ?
    EXCLAMATION = auto()       # !
    COMMA = auto()             # ,
    PERIOD = auto()            # .
    
    # Special
    UNKNOWN = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: str
    position: int
    
    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}')"

# ==================== LEXICAL ANALYZER ====================

class YaoundeLexer:
    """Tokenizes Yaoundé multilingual urban expressions"""
    
    def __init__(self):
        # Define token patterns with regex
        self.patterns = [
            # Numbers (must come before general words)
            (TokenType.NUMBER, r'\d+k|\d+\.\d+|\d+'),
            
            # Nouns - Places
            (TokenType.NOUN_PLACE, r'\b(quartier|carrefour|campus|ICT|université?|rond[- ]?point|marché|market|chop|rue|avenue|Total|station)\b'),
            
            # Nouns - People
            (TokenType.NOUN_PERSON, r'\b(moto[- ]?guy|bendskin[- ]?man|patron|boss|driver|mbere|sauveteur|gars|ndjangui|combi)\b'),
            
            # Nouns - Transport
            (TokenType.NOUN_TRANSPORT, r'\b(taxi|bendskin|moto|clandos?|car|bus|voiture|machine)\b'),
            
            # Nouns - Money
            (TokenType.NOUN_MONEY, r'\b(fap|mbongo|kop|francs?|CFA|sousous?|money|argent|change)\b'),
            
            # Nouns - Food
            (TokenType.NOUN_FOOD, r'\b(tchop|ndolé?|eru|koki|fufu|water[- ]?fufu|achu|banga|mbanga|plantain|pof[- ]?pof)\b'),
            
            # Nouns - Tech
            (TokenType.NOUN_TECH, r'\b(call|airtime|crédit|WiFi|réseau|network|MTN|Orange|Camtel|internet|charger)\b'),
            
            # Verbs - Movement
            (TokenType.VERB_MOVEMENT, r'\b(go|comot|waka|aller|venir|come|reach|arrive|drop|descend|mount|pass|move|enter)\b'),
            
            # Verbs - Give
            (TokenType.VERB_GIVE, r'\b(give|send|dash|donner|envoy[eé]|pay|di[eé])\b'),
            
            # Verbs - Be
            (TokenType.VERB_BE, r'\b(be|dey|[eé]tre|sef|stay|tann?|trouve)\b'),
            
            # Verbs - General
            (TokenType.VERB_GENERAL, r'\b(do|see|hear|tok|parler|dire|mek|make|know|savoir|take|wan|want|need|get|avoir|sor)\b'),
            
            # Pidgin Phrases
            (TokenType.PIDGIN_PHRASE, r'\b(na so|no be|i don|you don|we don|no dey|weti|wetin|how far|how no|man no|I beg|abeg|my broda|yi mass[aé])\b'),
            
            # French Phrases
            (TokenType.FRENCH_PHRASE, r'\b(c\'?est comment|ça va|tu vois|on dit|je dis|mon frère|frèrot|même|là[- ]?bas|c\'?est bon|c\'?est ca|pourquoi|tu fais comment|on va faire comment|tu connais|je wanda)\b'),
            
            # Ewondo Phrases
            (TokenType.EWONDO_PHRASE, r'\b(a ye moan|mbokesso|a sala|ndolo|yaa|me dzo|atè|akiba)\b'),
            
            # Fulfulde Phrases
            (TokenType.FULFULDE_PHRASE, r'\b(allah yai|wallahi|walahi|inshallah|mashallah|ai)\b'),
            
            # Slang - Exclamations
            (TokenType.SLANG_EXCLAIM, r'\b(ehn|eh|hmmm|hmm|garrr|garr|ekiee|eki|oyee|oye|ayee|weh|chei|kai|ah[iy]a?|hein)\b'),
            
            # Slang - Emphasis
            (TokenType.SLANG_EMPHASIS, r'\b(direct|serious|sérieux|correct|zéro[- ]?zéro|même pas|trop|vraiment|total|carrément|sharp|tight|bad)\b'),
            
            # Slang - Response
            (TokenType.SLANG_RESPONSE, r'\b(masa|mass|bros|brother|chief|sango|paddy|padi|guy|gars|nnem)\b'),
            
            # Adjectives - Quality
            (TokenType.ADJ_QUALITY, r'\b(bon|good|nye|nice|correct|bad|mauvais|beau|fine|better|bonne?|chaud|cool|nayo)\b'),
            
            # Adjectives - Quantity
            (TokenType.ADJ_QUANTITY, r'\b(plenty|small|petit|grand|big|beaucoup|peu|trop|many|some|all|tout)\b'),
            
            # Time
            (TokenType.TIME, r'\b(today|tomorrow|yesterday|now|maintenant|hier|demain|aujourd\'?hui|tantôt|après|avant|morning|soir|night)\b'),
            
            # Prepositions
            (TokenType.PREPOSITION, r'\b(for|na|avec|à|from|depuis|to|till|until|jusqu\'?à|en|dans|chez|on|sur|of|de|inside|behind|front)\b'),
            
            # Conjunctions
            (TokenType.CONJUNCTION, r'\b(and|avec|na|but|mais|or|ou|so|donc|because|parce que|if|si|when|quand|that|que)\b'),
            
            # Determiners
            (TokenType.DETERMINER, r'\b(the|di|le|la|les|un|une|des|some|any|this|that|ce|cette|my|ton|ma|your)\b'),
            
            # Pronouns
            (TokenType.PRONOUN, r'\b(me|i|you|we|dem|he|she|it|they|tu|je|nous|vous|ils|elles|on|am|ma|yi)\b'),
            
            # Punctuation
            (TokenType.QUESTION, r'\?'),
            (TokenType.EXCLAMATION, r'!'),
            (TokenType.COMMA, r','),
            (TokenType.PERIOD, r'\.'),
        ]
    
    def tokenize(self, text: str) -> List[Token]:
        """Convert text into tokens"""
        text = text.lower().strip()
        tokens = []
        position = 0
        
        while position < len(text):
            # Skip whitespace
            if text[position].isspace():
                position += 1
                continue
            
            # Try to match each pattern
            matched = False
            for token_type, pattern in self.patterns:
                regex = re.compile(pattern, re.IGNORECASE)
                match = regex.match(text, position)
                
                if match:
                    value = match.group(0)
                    tokens.append(Token(token_type, value, position))
                    position = match.end()
                    matched = True
                    break
            
            # If no pattern matched, treat as unknown
            if not matched:
                # Find next space or end
                end = position + 1
                while end < len(text) and not text[end].isspace():
                    end += 1
                value = text[position:end]
                tokens.append(Token(TokenType.UNKNOWN, value, position))
                position = end
        
        tokens.append(Token(TokenType.EOF, '', position))
        return tokens
    
    def analyze_frequency(self, tokens: List[Token]) -> Dict[str, int]:
        """Analyze token frequency"""
        freq = {}
        for token in tokens:
            if token.type != TokenType.EOF:
                key = f"{token.type.name}: {token.value}"
                freq[key] = freq.get(key, 0) + 1
        return freq

# ==================== TESTING ====================

def test_lexer():
    """Test the lexical analyzer with sample expressions"""
    lexer = YaoundeLexer()
    
    test_cases = [
        "bros drop me for Total",
        "masa network dey bad today", 
        "give me 500 francs",
        "je wanda how far ?",
        "walahi light don comot direct"
    ]
    
    print("🔤 YAOUNDÉ LEXICAL ANALYZER TEST")
    print("=" * 50)
    
    for expression in test_cases:
        print(f"\n📝 Expression: '{expression}'")
        tokens = lexer.tokenize(expression)
        
        print("🔤 Tokens:")
        for token in tokens:
            if token.type != TokenType.EOF:
                print(f"  {token}")
        
        frequency = lexer.analyze_frequency(tokens)
        print("📊 Frequency:")
        for token_info, count in frequency.items():
            print(f"  {token_info}: {count}")

if __name__ == "__main__":
    test_lexer()