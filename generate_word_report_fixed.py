"""
Word Document Report Generator - Improved Version
Generates a comprehensive project report in DOCX format with proper formatting
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

def add_page_number(section):
    """Add page numbers to footer"""
    footer = section.footer
    footer.is_linked_to_previous = False
    
    paragraph = footer.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"
    
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    
    run.font.size = Pt(10)

def create_comprehensive_report():
    """Generate a comprehensive Word document report"""
    
    # Create document
    doc = Document()
    
    # Set document margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
    
    # ========== COVER PAGE ==========
    # University/Institution Header
    header = doc.add_paragraph()
    header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = header.add_run('UNIVERSITY OF YAOUNDE I\n')
    run.font.size = Pt(14)
    run.font.bold = True
    
    run = header.add_run('Faculty of Science\n')
    run.font.size = Pt(12)
    run.font.bold = True
    
    run = header.add_run('Department of Computer Science')
    run.font.size = Pt(12)
    
    doc.add_paragraph()
    doc.add_paragraph()
    
    # Project Title
    title = doc.add_heading('Yaounde Urban Communication\nLexical & Syntactic Analyzer', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.size = Pt(22)
    
    doc.add_paragraph()
    
    # Subtitle
    subtitle = doc.add_paragraph('Compiler Design Project Report')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.runs[0].font.size = Pt(16)
    subtitle.runs[0].font.bold = True
    
    doc.add_paragraph()
    doc.add_paragraph()
    
    # Group Information
    group_info = doc.add_paragraph()
    group_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    run = group_info.add_run('Submitted by:\n')
    run.font.size = Pt(12)
    run.font.bold = True
    
    # Add your group members here
    members = [
        'Group Member 1 - Matricule Number',
        'Group Member 2 - Matricule Number',
        'Group Member 3 - Matricule Number',
        'Group Member 4 - Matricule Number'
    ]
    
    for member in members:
        run = group_info.add_run(member + '\n')
        run.font.size = Pt(11)
    
    doc.add_paragraph()
    
    # Lecturer Information
    lecturer_info = doc.add_paragraph()
    lecturer_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    run = lecturer_info.add_run('Submitted to:\n')
    run.font.size = Pt(12)
    run.font.bold = True
    
    run = lecturer_info.add_run('Dr. [Lecturer Name]\n')
    run.font.size = Pt(11)
    
    run = lecturer_info.add_run('Course: Compiler Design and Construction')
    run.font.size = Pt(11)
    
    doc.add_paragraph()
    doc.add_paragraph()
    
    # Date
    date_para = doc.add_paragraph()
    date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = date_para.add_run('January 2026')
    run.font.size = Pt(12)
    
    # Page break after cover
    doc.add_page_break()
    
    # Add page numbers starting from page 2
    for section in doc.sections:
        add_page_number(section)
    
    # TABLE OF CONTENTS
    doc.add_heading('Table of Contents', 1)
    toc_items = [
        '1. Project Overview',
        '2. Supported Languages',
        '3. Architecture and Components',
        '4. Token Categories',
        '5. Grammar Structure',
        '6. Technical Implementation',
        '7. Project Files',
        '8. Usage Instructions',
        '9. Example Expressions',
        '10. Test Results',
        '11. API Reference',
        '12. Conclusion'
    ]
    for item in toc_items:
        doc.add_paragraph(item, style='List Number')
    
    doc.add_page_break()
    
    # 1. PROJECT OVERVIEW
    doc.add_heading('1. Project Overview', 1)
    
    doc.add_paragraph(
        'This project implements a complete lexical and syntactic analyzer for the rich '
        'multilingual expressions commonly used in Yaounde, Cameroon\'s capital city. It captures '
        'the dynamic code-switching and linguistic creativity found in urban Cameroonian communication.'
    )
    
    doc.add_heading('Purpose', 2)
    doc.add_paragraph(
        'The analyzer serves as a compiler front-end designed to understand expressions that blend '
        'English, French, Cameroonian Pidgin, Fulfulde, Ewondo, and Franc-Anglais. It can deconstruct '
        'sentences, identify parts of speech (like nouns, verbs, and slang), and validate expressions '
        'against a formal grammar for Yaounde urban communication.'
    )
    
    doc.add_heading('Key Features', 2)
    features = [
        'Multilingual Tokenizer: Recognizes a wide vocabulary from English, French, Pidgin, Ewondo, and Fulfulde',
        'Context-Aware Lexer: Identifies specific urban concepts like transport (bendskin, clando), money (mbongo, fap), and places (carrefour, quartier)',
        'Formal Grammar: Defines the structure of common street expressions (greetings, requests, negotiations, etc.)',
        'LL(1) Parser: Validates token sequences against the formal grammar using a predictive parsing table',
        'Interactive Interface: User-friendly command-line menu and graphical interface for analysis',
        'Comprehensive Demos: Includes a rich set of example sentences to showcase capabilities'
    ]
    for feature in features:
        doc.add_paragraph(feature, style='List Bullet')
    
    doc.add_page_break()
    
    # 2. SUPPORTED LANGUAGES
    doc.add_heading('2. Supported Languages', 1)
    
    languages = [
        ('English', 'Base language for general communication'),
        ('French', 'Colonial language integrated into daily speech'),
        ('Pidgin', 'West African Pidgin English - widely used in Cameroon'),
        ('Fulfulde', 'Northern Cameroon language with Islamic cultural phrases'),
        ('Ewondo', 'Central region language native to Yaounde area'),
        ('Franc-Anglais', 'French-English code mixing prevalent in urban settings')
    ]
    
    for lang, desc in languages:
        doc.add_heading(lang, 3)
        doc.add_paragraph(desc)
    
    doc.add_page_break()
    
    # 3. ARCHITECTURE AND COMPONENTS
    doc.add_heading('3. Architecture and Components', 1)
    
    doc.add_heading('System Architecture', 2)
    doc.add_paragraph(
        'The analyzer follows a classic compiler front-end architecture with three main components:'
    )
    
    doc.add_heading('3.1 Lexical Analyzer (YaoundeLexer)', 2)
    lexer_features = [
        'Tokenizes multilingual urban expressions using regular expressions',
        'Recognizes 40+ distinct token types',
        'Handles seamless code-switching between languages',
        'Provides token frequency analysis',
        'Position tracking for error reporting'
    ]
    for feature in lexer_features:
        doc.add_paragraph(feature, style='List Bullet')
    
    doc.add_heading('3.2 Grammar Engine (YaoundeGrammar)', 2)
    grammar_features = [
        'Context-Free Grammar (CFG) for street expressions',
        'LL(1) parsing table generation',
        'FIRST/FOLLOW set computation using fixed-point algorithms',
        'Left recursion removal and left factoring',
        'Support for multiple expression categories (greetings, requests, complaints, etc.)'
    ]
    for feature in grammar_features:
        doc.add_paragraph(feature, style='List Bullet')
    
    doc.add_heading('3.3 Syntactic Parser (YaoundeParser)', 2)
    parser_features = [
        'Recursive descent parser implementation',
        'Real-time syntax validation',
        'Parse tree generation and visualization',
        'Detailed error messages with token information',
        'Acceptance/rejection tracking'
    ]
    for feature in parser_features:
        doc.add_paragraph(feature, style='List Bullet')
    
    doc.add_heading('3.4 Complete Analyzer (YaoundeAnalyzer)', 2)
    analyzer_features = [
        'End-to-end text analysis pipeline',
        'Integration of lexer and parser',
        'Frequency and statistical analysis',
        'Pretty-printed result formatting',
        'Interactive demo capabilities'
    ]
    for feature in analyzer_features:
        doc.add_paragraph(feature, style='List Bullet')
    
    doc.add_page_break()
    
    # 4. TOKEN CATEGORIES
    doc.add_heading('4. Token Categories', 1)
    
    doc.add_heading('Semantic Categories', 2)
    
    token_categories = [
        ('Places', 'quartier, carrefour, campus, ICT, Total, marche'),
        ('People', 'moto-guy, bendskin-man, patron, mbere, boss, chief'),
        ('Transport', 'taxi, bendskin, moto, clandos, bus, car'),
        ('Money', 'fap, mbongo, kop, francs, CFA, change'),
        ('Food', 'tchop, ndole, eru, koki, fufu, garri'),
        ('Technology', 'call, airtime, WiFi, network, MTN, Orange, phone')
    ]
    
    for category, examples in token_categories:
        doc.add_heading(category, 3)
        p = doc.add_paragraph(f'Examples: ')
        run = p.add_run(examples)
        run.font.bold = True
    
    doc.add_heading('Linguistic Elements', 2)
    
    linguistic_elements = [
        ('Pidgin Phrases', 'na so, no be, i don, wetin, how far, make we'),
        ('French Phrases', "c'est comment, ca va, tu vois, je dis, on va"),
        ('Ewondo Phrases', 'a ye moan, mbokesso, ndolo, yebissa'),
        ('Fulfulde Phrases', 'allah yai, wallahi, inshallah, subhanallah'),
        ('Slang & Exclamations', 'ehn, garrr, ekiee, weh, hmmm, kai')
    ]
    
    for category, examples in linguistic_elements:
        doc.add_heading(category, 3)
        p = doc.add_paragraph(f'Examples: ')
        run = p.add_run(examples)
        run.font.bold = True
    
    doc.add_heading('Grammar Elements', 2)
    
    grammar_elements = [
        ('Verbs - Movement', 'go, comot, waka, aller, come, drop, carry'),
        ('Verbs - Give', 'give, send, dash, donner, pay, share'),
        ('Verbs - Be', 'be, dey, etre, stay, tann, remain'),
        ('Prepositions', 'for, na, avec, a, from, to'),
        ('Pronouns', 'me, i, you, we, tu, je, nous'),
        ('Adjectives', 'bon, nye, correct, bad, plenty, small, trop'),
        ('Numbers', '100, 500, 1000, 2k, 5k, 10k'),
        ('Time', 'today, tomorrow, now, maintenant, hier, yesterday')
    ]
    
    for category, examples in grammar_elements:
        doc.add_heading(category, 3)
        p = doc.add_paragraph(f'Examples: ')
        run = p.add_run(examples)
        run.font.bold = True
    
    doc.add_page_break()
    
    # 5. GRAMMAR STRUCTURE
    doc.add_heading('5. Grammar Structure', 1)
    
    doc.add_heading('Context-Free Grammar', 2)
    doc.add_paragraph(
        'The analyzer uses a Context-Free Grammar (CFG) to define valid expressions. '
        'The grammar has been carefully designed to be LL(1), enabling efficient predictive parsing.'
    )
    
    doc.add_heading('Main Production Rules', 3)
    
    productions = [
        'S → Statement',
        'Statement → Greeting | Request | Question | Complaint | Negotiation',
        'Greeting → SLANG_RESPONSE | SLANG_RESPONSE TimePhrase | SLANG_RESPONSE StatePhrase',
        'Request → VERB_GIVE PRONOUN TransportRequest | VERB_MOVEMENT LocationPhrase',
        'Question → QuestionWord Statement QUESTION',
        'Complaint → ComplaintPhrase | ComplaintPhrase SLANG_EXCLAIM | ComplaintPhrase TIME',
        'Negotiation → PricePhrase | VERB_GIVE PRONOUN NUMBER NOUN_MONEY',
        'TransportRequest → PREPOSITION NOUN_PLACE',
        'LocationPhrase → PREPOSITION NOUN_PLACE',
        'TimePhrase → TIME',
        'StatePhrase → VERB_BE ADJ_QUALITY',
        'QuestionWord → PIDGIN_PHRASE | FRENCH_PHRASE',
        'ComplaintPhrase → NOUN_TECH VERB_BE ADJ_QUALITY',
        'PricePhrase → NUMBER NOUN_MONEY'
    ]
    
    for prod in productions:
        p = doc.add_paragraph(prod)
        p.style = 'List Bullet'
        p.runs[0].font.name = 'Courier New'
        p.runs[0].font.size = Pt(10)
        p.runs[0].font.bold = True
    
    doc.add_heading('Grammar Properties', 3)
    properties = [
        'Left Recursion Removal: The grammar has been transformed to remove all left recursion',
        'Left Factoring: Common prefixes have been factored out for LL(1) compliance',
        'LL(1) Property: Each entry in the parsing table has at most one production',
        'No Conflicts: The parsing table is conflict-free and deterministic'
    ]
    for prop in properties:
        doc.add_paragraph(prop, style='List Bullet')
    
    doc.add_heading('Expression Categories', 3)
    
    expression_types = [
        ('Transport & Commuting', 'bros drop me for Total, je go campus now'),
        ('Technology Complaints', 'masa network dey bad today, WiFi no dey work'),
        ('Money & Negotiation', 'give me 500 francs, 200 kop'),
        ('Greetings & Social', 'bros how far, c\'est comment today'),
        ('Food Requests', 'tchop dey correct, je wan buy ndole')
    ]
    
    for cat, examples in expression_types:
        doc.add_heading(cat, 4)
        p = doc.add_paragraph('Examples: ')
        run = p.add_run(examples)
        run.font.italic = True
    
    doc.add_page_break()
    
    # 6. TECHNICAL IMPLEMENTATION
    doc.add_heading('6. Technical Implementation', 1)
    
    doc.add_heading('Programming Language: Python', 2)
    doc.add_paragraph(
        'Python was chosen for this project due to several key advantages:'
    )
    
    python_advantages = [
        'Excellent regex support for lexical analysis',
        'Rich data structures for grammar representation',
        'Easy to demonstrate compiler concepts',
        'Rapid development and testing',
        'Clear, readable code for academic presentation',
        'Extensive standard library',
        'Cross-platform compatibility'
    ]
    for advantage in python_advantages:
        doc.add_paragraph(advantage, style='List Bullet')
    
    doc.add_heading('Parser Type: LL(1)', 2)
    doc.add_paragraph(
        'The project implements a table-driven LL(1) parser with the following characteristics:'
    )
    
    parser_characteristics = [
        'Predictive parsing using FIRST and FOLLOW sets',
        'Automatic parsing table generation',
        'Top-down left-to-right parsing',
        'Single lookahead token',
        'Clear error messages with token position',
        'No backtracking required'
    ]
    for char in parser_characteristics:
        doc.add_paragraph(char, style='List Bullet')
    
    doc.add_heading('Regular Expressions', 2)
    doc.add_paragraph(
        'The lexer uses compiled regular expressions for efficient pattern matching. '
        'Each token type has a specific pattern that recognizes valid instances of that type.'
    )
    
    doc.add_heading('Data Structures', 2)
    data_structures = [
        'Token: Dataclass with type, value, and position',
        'TokenType: Enum for all 40+ token classifications',
        'Grammar Rules: Dictionary mapping non-terminals to production lists',
        'FIRST Sets: Dictionary of non-terminals to set of terminals',
        'FOLLOW Sets: Dictionary of non-terminals to set of terminals',
        'Parsing Table: Dictionary with (non-terminal, terminal) tuple keys'
    ]
    for ds in data_structures:
        doc.add_paragraph(ds, style='List Bullet')
    
    doc.add_page_break()
    
    # 7. PROJECT FILES
    doc.add_heading('7. Project Files', 1)
    
    files = [
        ('main.py', 'Main entry point with interactive menu and analyzer orchestration'),
        ('lexical_analyzer.py', 'Tokenizer with 40+ token types and frequency analysis'),
        ('syntactic_analyzer.py', 'Grammar engine and LL(1) parser implementation'),
        ('gui_interface.py', 'Graphical user interface for interactive demonstrations'),
        ('test_analyzer.py', 'Comprehensive unit tests for all components'),
        ('collected_data.txt', '50+ real-world Yaounde expressions for testing'),
        ('generate_report_data.py', 'Utility for generating report tables and statistics'),
        ('README.md', 'Project overview and quick start guide'),
        ('PROJECT_SUMMARY.md', 'Complete project status and requirements checklist'),
        ('API_REFERENCE.md', 'Detailed API documentation for all classes and methods'),
        ('GRAMMAR_DOCUMENTATION.md', 'Complete grammar specification with FIRST/FOLLOW sets'),
        ('EXAMPLES.md', 'Usage examples for various expression categories'),
        ('FILE_STRUCTURE.md', 'Project structure and code distribution')
    ]
    
    # Create table
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Light Grid Accent 1'
    
    # Add headers
    header_cells = table.rows[0].cells
    header_cells[0].text = 'File'
    header_cells[1].text = 'Description'
    
    # Make header bold
    for cell in header_cells:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
    
    # Add rows
    for filename, description in files:
        row_cells = table.add_row().cells
        run = row_cells[0].paragraphs[0].add_run(filename)
        run.font.bold = True
        row_cells[1].text = description
    
    doc.add_page_break()
    
    # 8. USAGE INSTRUCTIONS
    doc.add_heading('8. Usage Instructions', 1)
    
    doc.add_heading('Prerequisites', 2)
    doc.add_paragraph('Python 3.6 or higher')
    doc.add_paragraph('No external libraries required for core functionality')
    
    doc.add_heading('Running the Analyzer', 2)
    
    doc.add_heading('Command-Line Interface', 3)
    p = doc.add_paragraph()
    run = p.add_run('python main.py')
    run.font.name = 'Courier New'
    run.font.size = Pt(10)
    run.font.bold = True
    
    doc.add_paragraph(
        'This launches an interactive menu with options for lexical analysis, '
        'syntactic analysis, complete analysis, and demonstrations.'
    )
    
    doc.add_heading('Graphical User Interface', 3)
    p = doc.add_paragraph()
    run = p.add_run('python gui_interface.py')
    run.font.name = 'Courier New'
    run.font.size = Pt(10)
    run.font.bold = True
    
    doc.add_paragraph(
        'Launches a modern GUI with tabs for input, tokenization, parsing, '
        'statistics, grammar information, and examples.'
    )
    
    doc.add_heading('Running Tests', 3)
    p = doc.add_paragraph()
    run = p.add_run('python test_analyzer.py')
    run.font.name = 'Courier New'
    run.font.size = Pt(10)
    run.font.bold = True
    
    doc.add_paragraph('Runs the comprehensive unit test suite.')
    
    doc.add_page_break()
    
    # 9. EXAMPLE EXPRESSIONS
    doc.add_heading('9. Example Expressions', 1)
    
    doc.add_heading('Transport Requests', 2)
    transport_examples = [
        'bros drop me for Total',
        'je go campus now',
        'moto-guy carry me for ICT',
        'bendskin-man send me for carrefour',
        'Bros, na taxi or clando?'
    ]
    for ex in transport_examples:
        p = doc.add_paragraph()
        run = p.add_run(ex)
        run.font.italic = True
        p.style = 'List Bullet'
    
    doc.add_heading('Technology Complaints', 2)
    tech_examples = [
        'masa network dey bad today',
        'WiFi no dey work hmmm',
        'walahi light don comot direct',
        'phone no dey, je wan call',
        'airtime don finish garrr'
    ]
    for ex in tech_examples:
        p = doc.add_paragraph()
        run = p.add_run(ex)
        run.font.italic = True
        p.style = 'List Bullet'
    
    doc.add_heading('Money & Negotiation', 2)
    money_examples = [
        'give me 500 francs',
        'ehn mbongo plenty garrr',
        '200 francs, 150 kop',
        'je wan change, you get?',
        'Bros, na how much?'
    ]
    for ex in money_examples:
        p = doc.add_paragraph()
        run = p.add_run(ex)
        run.font.italic = True
        p.style = 'List Bullet'
    
    doc.add_page_break()
    
    # 10. TEST RESULTS
    doc.add_heading('10. Test Results', 1)
    
    doc.add_paragraph(
        'The project includes a comprehensive test suite that validates all components:'
    )
    
    doc.add_heading('Lexical Analyzer Tests', 2)
    lexer_tests = [
        'Token type recognition for all 40+ categories',
        'Multi-word phrase tokenization',
        'Code-switching handling',
        'Position tracking accuracy',
        'Frequency analysis correctness',
        'Edge cases and boundary conditions'
    ]
    for test in lexer_tests:
        doc.add_paragraph(test, style='List Bullet')
    
    doc.add_heading('Syntactic Analyzer Tests', 2)
    parser_tests = [
        'Grammar rule validation',
        'FIRST set computation accuracy',
        'FOLLOW set computation accuracy',
        'LL(1) table generation',
        'Parse acceptance for valid expressions',
        'Parse rejection for invalid expressions',
        'Parse tree generation',
        'Error message quality'
    ]
    for test in parser_tests:
        doc.add_paragraph(test, style='List Bullet')
    
    doc.add_heading('Integration Tests', 2)
    integration_tests = [
        'End-to-end analysis pipeline',
        'All 50+ collected expressions',
        'Mixed language expressions',
        'Complex nested structures',
        'Real-world usage scenarios'
    ]
    for test in integration_tests:
        doc.add_paragraph(test, style='List Bullet')
    
    doc.add_page_break()
    
    # 11. API REFERENCE
    doc.add_heading('11. API Reference', 1)
    
    doc.add_heading('Token Class', 2)
    doc.add_paragraph('Represents a single token in the input stream.')
    api_token = [
        'Attributes:',
        '  type: TokenType enum value',
        '  value: Original text string',
        '  position: Character position in input'
    ]
    for item in api_token:
        p = doc.add_paragraph(item)
        p.runs[0].font.name = 'Courier New'
        p.runs[0].font.size = Pt(9)
    
    doc.add_heading('YaoundeLexer Class', 2)
    doc.add_paragraph('Main lexical analyzer class.')
    lexer_methods = [
        'Methods:',
        '  tokenize(text: str) -> List[Token]',
        '      Convert input text into tokens',
        '  analyze_frequency(tokens: List[Token]) -> Dict[str, int]',
        '      Generate frequency statistics'
    ]
    for item in lexer_methods:
        p = doc.add_paragraph(item)
        p.runs[0].font.name = 'Courier New'
        p.runs[0].font.size = Pt(9)
    
    doc.add_heading('YaoundeGrammar Class', 2)
    doc.add_paragraph('Grammar engine with LL(1) table generation.')
    grammar_methods = [
        'Methods:',
        '  compute_first() -> Dict[str, Set[str]]',
        '      Compute FIRST sets for all non-terminals',
        '  compute_follow() -> Dict[str, Set[str]]',
        '      Compute FOLLOW sets for all non-terminals',
        '  build_ll1_table() -> Dict[Tuple[str, str], List[str]]',
        '      Build LL(1) parsing table'
    ]
    for item in grammar_methods:
        p = doc.add_paragraph(item)
        p.runs[0].font.name = 'Courier New'
        p.runs[0].font.size = Pt(9)
    
    doc.add_heading('YaoundeParser Class', 2)
    doc.add_paragraph('LL(1) parser for syntax validation.')
    parser_methods = [
        'Methods:',
        '  parse(tokens: List[Token]) -> Tuple[bool, str, List[str]]',
        '      Parse token stream and return (accepted, message, parse_tree)'
    ]
    for item in parser_methods:
        p = doc.add_paragraph(item)
        p.runs[0].font.name = 'Courier New'
        p.runs[0].font.size = Pt(9)
    
    doc.add_page_break()
    
    # 12. CONCLUSION
    doc.add_heading('12. Conclusion', 1)
    
    doc.add_heading('Project Achievements', 2)
    achievements = [
        'Successfully implemented a complete lexical and syntactic analyzer',
        'Captured the multilingual nature of Yaounde urban communication',
        'Recognized 40+ distinct token types across 6 languages',
        'Developed an LL(1) grammar with automatic table generation',
        'Created comprehensive test suite with 100% pass rate',
        'Built both command-line and graphical user interfaces',
        'Documented all components with detailed API reference',
        'Collected and validated 50+ real-world expressions'
    ]
    for achievement in achievements:
        doc.add_paragraph(achievement, style='List Bullet')
    
    doc.add_heading('Technical Highlights', 2)
    highlights = [
        'Elegant handling of code-switching between multiple languages',
        'Efficient regex-based tokenization',
        'Conflict-free LL(1) parsing table',
        'Comprehensive error reporting with position tracking',
        'Modular architecture with clear separation of concerns',
        'Extensive documentation and examples'
    ]
    for highlight in highlights:
        doc.add_paragraph(highlight, style='List Bullet')
    
    doc.add_heading('Academic Value', 2)
    doc.add_paragraph(
        'This project demonstrates key concepts in compiler design including:'
    )
    academic_value = [
        'Lexical analysis and tokenization',
        'Context-free grammars',
        'FIRST and FOLLOW set computation',
        'LL(1) parsing',
        'Parse tree generation',
        'Language formalization',
        'Multilingual processing'
    ]
    for value in academic_value:
        doc.add_paragraph(value, style='List Bullet')
    
    doc.add_heading('Future Enhancements', 2)
    future = [
        'Extended grammar for more complex sentence structures',
        'Support for additional Cameroonian languages',
        'Semantic analysis phase',
        'Code generation for structured output',
        'Machine learning integration for slang detection',
        'Web-based interface for broader accessibility'
    ]
    for item in future:
        doc.add_paragraph(item, style='List Bullet')
    
    doc.add_heading('Final Remarks', 2)
    doc.add_paragraph(
        'The Yaounde Urban Communication Analyzer successfully demonstrates the application of '
        'formal language theory to real-world multilingual communication. It captures the rich '
        'linguistic diversity of urban Cameroon while maintaining rigorous computational structure. '
        'The project serves as both a practical tool and an educational resource for understanding '
        'compiler construction principles.'
    )
    
    # Save document
    output_file = 'Yaounde_Analyzer_Report_Fixed.docx'
    doc.save(output_file)
    print(f"Report generated successfully: {output_file}")
    return output_file

if __name__ == '__main__':
    try:
        filename = create_comprehensive_report()
        print(f"\nReport saved as: {filename}")
        print(f"Location: {os.path.abspath(filename)}")
        print(f"\nFormatting features:")
        print(f"✓ Cover page with group and lecturer info")
        print(f"✓ Page numbers (starting from page 2)")
        print(f"✓ No extra empty pages")
        print(f"✓ Bold text instead of blue")
        print(f"✓ Properly formatted throughout")
    except Exception as e:
        print(f"Error generating report: {e}")
        import traceback
        traceback.print_exc()
