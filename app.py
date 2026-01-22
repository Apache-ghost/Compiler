# -*- coding: utf-8 -*-
"""
Yaoundé Multilingual Expression Analyzer - Web Application
Professional Flask-based web interface with modern design
ICT University - Compiler Construction Project
"""

from flask import Flask, render_template, request, jsonify, send_file
from lexical_analyzer import YaoundeLexer, Token, TokenType
from syntactic_analyzer import YaoundeGrammar, YaoundeParser
from main import YaoundeAnalyzer
import json
import os
from datetime import datetime
from collections import Counter

app = Flask(__name__)
app.secret_key = 'yaounde-analyzer-2024-ict-university'

# Initialize the analyzer
analyzer = YaoundeAnalyzer()

# Analysis history storage (in-memory for session)
analysis_history = []

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze a single expression"""
    try:
        data = request.get_json()
        expression = data.get('expression', '').strip()
        
        if not expression:
            return jsonify({'error': 'Empty expression'}), 400
        
        # Perform analysis
        result = analyzer.analyze(expression)
        
        # Convert tokens to serializable format
        tokens_data = []
        for token in result['tokens']:
            if token.type != TokenType.EOF:
                tokens_data.append({
                    'type': token.type.name,
                    'value': token.value,
                    'position': token.position,
                    'category': get_token_category(token.type)
                })
        
        # Detect languages using analyzer's method (more comprehensive)
        tokens_for_detection = analyzer.lexer.tokenize(expression)
        languages = analyzer.detect_languages(tokens_for_detection)
        
        # Build response
        response = {
            'original': result['original'],
            'accepted': result['accepted'],
            'parse_result': result['parse_result'],
            'tokens': tokens_data,
            'token_count': len(tokens_data),
            'frequency': result['frequency'],
            'parse_tree': result['parse_tree'][:30],  # Limit parse tree
            'languages_detected': languages,
            'timestamp': datetime.now().isoformat(),
            'statistics': compute_statistics(tokens_data)
        }
        
        # Add to history
        history_entry = {
            'expression': expression,
            'accepted': result['accepted'],
            'token_count': len(tokens_data),
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        analysis_history.append(history_entry)
        if len(analysis_history) > 50:  # Keep last 50 entries
            analysis_history.pop(0)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-batch', methods=['POST'])
def analyze_batch():
    """Analyze multiple expressions from file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file content
        content = file.read().decode('utf-8')
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        if not lines:
            return jsonify({'error': 'File is empty'}), 400
        
        # Analyze all expressions
        results = []
        all_tokens = []
        accepted_count = 0
        rejected_count = 0
        
        for expression in lines:
            result = analyzer.analyze(expression)
            
            tokens_data = []
            for token in result['tokens']:
                if token.type != TokenType.EOF:
                    token_info = {
                        'type': token.type.name,
                        'value': token.value,
                        'category': get_token_category(token.type)
                    }
                    tokens_data.append(token_info)
                    all_tokens.append(token_info)
            
            if result['accepted']:
                accepted_count += 1
            else:
                rejected_count += 1
            
            results.append({
                'expression': expression,
                'accepted': result['accepted'],
                'parse_result': result['parse_result'],
                'tokens': tokens_data,
                'token_count': len(tokens_data)
            })
        
        # Compute aggregate statistics
        aggregate_stats = {
            'total_expressions': len(lines),
            'accepted': accepted_count,
            'rejected': rejected_count,
            'acceptance_rate': round((accepted_count / len(lines)) * 100, 1) if lines else 0,
            'total_tokens': len(all_tokens),
            'unique_tokens': len(set(t['value'] for t in all_tokens)),
            'token_type_distribution': compute_type_distribution(all_tokens),
            'top_tokens': compute_top_tokens(all_tokens, 10)
        }
        
        return jsonify({
            'results': results,
            'statistics': aggregate_stats,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tokenize', methods=['POST'])
def tokenize_only():
    """Perform only lexical analysis"""
    try:
        data = request.get_json()
        expression = data.get('expression', '').strip()
        
        if not expression:
            return jsonify({'error': 'Empty expression'}), 400
        
        tokens = analyzer.lexer.tokenize(expression)
        frequency = analyzer.lexer.analyze_frequency(tokens)
        
        tokens_data = []
        for token in tokens:
            if token.type != TokenType.EOF:
                tokens_data.append({
                    'type': token.type.name,
                    'value': token.value,
                    'position': token.position,
                    'category': get_token_category(token.type)
                })
        
        # Detect languages using analyzer's method
        languages = analyzer.detect_languages(tokens)
        
        return jsonify({
            'original': expression,
            'tokens': tokens_data,
            'token_count': len(tokens_data),
            'frequency': frequency,
            'statistics': compute_statistics(tokens_data),
            'languages_detected': languages
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/parse', methods=['POST'])
def parse_only():
    """Perform only syntactic analysis"""
    try:
        data = request.get_json()
        expression = data.get('expression', '').strip()
        
        if not expression:
            return jsonify({'error': 'Empty expression'}), 400
        
        tokens = analyzer.lexer.tokenize(expression)
        accepted, message, parse_tree = analyzer.parser.parse(tokens)
        
        # Detect languages using analyzer's method
        languages = analyzer.detect_languages(tokens)
        
        return jsonify({
            'original': expression,
            'accepted': accepted,
            'parse_result': message,
            'parse_tree': parse_tree[:30],
            'languages_detected': languages
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/grammar')
def get_grammar():
    """Get grammar information"""
    try:
        grammar = analyzer.grammar
        
        # Format rules
        rules = {}
        for non_terminal, productions in grammar.rules.items():
            rules[non_terminal] = [' '.join(prod) for prod in productions]
        
        # Format FIRST sets (sample)
        first_sets = {}
        key_sets = ['Statement', 'Greeting', 'Request', 'Question', 'Complaint', 'Negotiation']
        for nt in key_sets:
            if nt in grammar.first_sets:
                first_sets[nt] = sorted(list(grammar.first_sets[nt]))[:15]
        
        # Format FOLLOW sets (sample)
        follow_sets = {}
        for nt in key_sets[:4]:
            if nt in grammar.follow_sets:
                follow_sets[nt] = sorted(list(grammar.follow_sets[nt]))
        
        return jsonify({
            'rules': rules,
            'first_sets': first_sets,
            'follow_sets': follow_sets,
            'parsing_table_size': len(grammar.parsing_table),
            'non_terminals': list(grammar.rules.keys())
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history')
def get_history():
    """Get analysis history"""
    return jsonify({'history': analysis_history[-20:]})  # Last 20 entries

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear analysis history"""
    global analysis_history
    analysis_history = []
    return jsonify({'status': 'cleared'})

@app.route('/api/examples')
def get_examples():
    """Get example expressions"""
    examples = [
        {"text": "bros drop me for Total", "category": "Transport"},
        {"text": "give me 500 francs", "category": "Money"},
        {"text": "masa network dey bad today", "category": "Complaint"},
        {"text": "je wanda how far ?", "category": "Question"},
        {"text": "walahi light don comot direct", "category": "Complaint"},
        {"text": "Je go campus now, you dey come?", "category": "Transport"},
        {"text": "Bros, na taxi or clando?", "category": "Transport"},
        {"text": "Je wan buy fufu, where e dey?", "category": "Food"},
        {"text": "Bros, you sabi the road for Total?", "category": "Question"},
        {"text": "C'est comment, network dey bad today.", "category": "Complaint"},
        {"text": "Massa, give me 200 francs change.", "category": "Money"},
        {"text": "You fit give me airtime?", "category": "Request"},
        {"text": "Bros, na bendskin dey pass here?", "category": "Transport"},
        {"text": "Je wan call my friend, phone no dey", "category": "Tech"},
        {"text": "ICT est mal scia bros", "category": "Complaint"}
    ]
    return jsonify({'examples': examples})


# ==================== HELPER FUNCTIONS ====================

def get_token_category(token_type: TokenType) -> str:
    """Map token types to broader categories for visualization"""
    type_name = token_type.name
    if type_name.startswith('NOUN_'):
        return 'noun'
    elif type_name.startswith('VERB_'):
        return 'verb'
    elif type_name.startswith('ADJ_'):
        return 'adjective'
    elif type_name.startswith('SLANG_'):
        return 'slang'
    elif type_name.endswith('_PHRASE'):
        return 'phrase'
    elif type_name in ['PREPOSITION', 'CONJUNCTION', 'DETERMINER', 'PRONOUN']:
        return 'grammar'
    elif type_name in ['NUMBER', 'TIME']:
        return 'value'
    elif type_name in ['QUESTION', 'EXCLAMATION', 'COMMA', 'PERIOD']:
        return 'punctuation'
    else:
        return 'other'

# Note: Language detection is now handled by analyzer.detect_languages() method
# This function is kept for backward compatibility but is no longer used
def detect_languages(tokens: list) -> list:
    """Detect which languages are present in the tokens (legacy function)"""
    # This function is deprecated - use analyzer.detect_languages() instead
    # Kept for backward compatibility
    languages = set()
    
    for token in tokens:
        token_type = token['type']
        value = token['value'].lower()
        
        # French indicators
        if token_type == 'FRENCH_PHRASE' or value in ['je', 'tu', 'vous', 'nous', 'avec', 'pour', 'c\'est', 'comment', 'mal', 'bon', 'bien', 'est', 'sont', 'gars', 'frère']:
            languages.add('French')
        
        # Pidgin indicators
        elif token_type == 'PIDGIN_PHRASE' or value in ['dey', 'na', 'wetin', 'waka', 'comot', 'abeg', 'how far', 'wan', 'fit', 'sabi']:
            languages.add('Pidgin')
        
        # Ewondo indicators
        elif token_type == 'EWONDO_PHRASE' or value in ['mbokesso', 'ndolo', 'akiba', 'a ye moan']:
            languages.add('Ewondo')
        
        # Fulfulde indicators
        elif token_type == 'FULFULDE_PHRASE' or value in ['wallahi', 'walahi', 'inshallah', 'allah', 'allah yai']:
            languages.add('Fulfulde')
        
        # English indicators
        elif value in ['give', 'me', 'you', 'drop', 'come', 'go', 'today', 'bad', 'good', 'network', 'phone', 'campus', 'total']:
            languages.add('English')
        
        # Slang (Franc-Anglais)
        elif token_type.startswith('SLANG_') or value in ['bros', 'masa', 'mass', 'garrr', 'ekiee', 'weh', 'chief', 'sango']:
            languages.add('Franc-Anglais')
    
    if not languages:
        languages.add('Mixed')
    
    return sorted(list(languages))

def compute_statistics(tokens: list) -> dict:
    """Compute detailed statistics for tokens"""
    if not tokens:
        return {}
    
    # Count by category
    categories = Counter(t['category'] for t in tokens)
    
    # Count by type
    types = Counter(t['type'] for t in tokens)
    
    # Top tokens by frequency
    values = Counter(t['value'] for t in tokens)
    top_tokens = values.most_common(10)
    
    return {
        'by_category': dict(categories),
        'by_type': dict(types),
        'top_tokens': [{'token': t[0], 'count': t[1]} for t in top_tokens],
        'unique_count': len(set(t['value'] for t in tokens)),
        'total_count': len(tokens)
    }

def compute_type_distribution(tokens: list) -> dict:
    """Compute token type distribution for batch analysis"""
    types = Counter(t['type'] for t in tokens)
    return dict(types)

def compute_top_tokens(tokens: list, n: int) -> list:
    """Get top N most frequent tokens"""
    values = Counter(t['value'] for t in tokens)
    return [{'token': t[0], 'count': t[1]} for t in values.most_common(n)]


# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("YAOUNDE MULTILINGUAL EXPRESSION ANALYZER")
    print("ICT University - Compiler Construction Project")
    print("="*60)
    print("\nStarting web server...")
    print("Open your browser to: http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
