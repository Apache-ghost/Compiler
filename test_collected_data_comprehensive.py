# -*- coding: utf-8 -*-
"""
Comprehensive Test of All Collected Data
Tests all expressions from collected_data.txt and generates detailed report
"""

from main import YaoundeAnalyzer
from lexical_analyzer import TokenType

def test_all_collected_data():
    """Test all collected expressions and generate comprehensive report"""
    analyzer = YaoundeAnalyzer()
    
    # Load collected data
    try:
        with open('collected_data.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("❌ Error: collected_data.txt not found")
        return
    
    # Parse expressions by category
    expressions_by_category = {}
    current_category = "General"
    expressions_by_category[current_category] = []
    
    all_expressions = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            # Extract category name
            if '===' in line:
                current_category = line.replace('#', '').replace('=', '').strip()
                if current_category not in expressions_by_category:
                    expressions_by_category[current_category] = []
            continue
        expressions_by_category[current_category].append(line)
        all_expressions.append(line)
    
    print("=" * 80)
    print("COMPREHENSIVE COLLECTED DATA TEST REPORT")
    print("=" * 80)
    print(f"\nTotal Expressions Collected: {len(all_expressions)}")
    print(f"Categories: {len(expressions_by_category)}\n")
    
    # Test all expressions
    results = {
        'accepted': 0,
        'rejected': 0,
        'by_category': {},
        'languages_detected': set(),
        'rejected_details': []
    }
    
    for category, expressions in expressions_by_category.items():
        if not expressions:
            continue
        
        print(f"\n{'='*80}")
        print(f"Category: {category}")
        print(f"{'='*80}")
        print(f"Expressions in category: {len(expressions)}\n")
        
        category_results = {'accepted': 0, 'rejected': 0, 'details': []}
        
        for expr in expressions:
            result = analyzer.analyze(expr)
            languages = result.get('languages_detected', [])
            results['languages_detected'].update(languages)
            
            status = "✓" if result['accepted'] else "✗"
            lang_str = ', '.join(languages) if languages else 'None'
            
            print(f"{status} {expr[:60]}")
            print(f"    Languages: {lang_str}")
            print(f"    Result: {result['parse_result']}")
            
            if result['accepted']:
                category_results['accepted'] += 1
                results['accepted'] += 1
            else:
                category_results['rejected'] += 1
                results['rejected'] += 1
                category_results['details'].append({
                    'expression': expr,
                    'reason': result['parse_result']
                })
                results['rejected_details'].append({
                    'category': category,
                    'expression': expr,
                    'reason': result['parse_result']
                })
        
        results['by_category'][category] = category_results
        
        # Category summary
        total = len(expressions)
        rate = (category_results['accepted'] / total * 100) if total > 0 else 0
        print(f"\n  Category Summary: {category_results['accepted']}/{total} accepted ({rate:.1f}%)")
    
    # Overall Summary
    print(f"\n{'='*80}")
    print("OVERALL SUMMARY")
    print(f"{'='*80}")
    
    total = len(all_expressions)
    acceptance_rate = (results['accepted'] / total * 100) if total > 0 else 0
    
    print(f"\nTotal Expressions: {total}")
    print(f"Accepted: {results['accepted']} ({acceptance_rate:.1f}%)")
    print(f"Rejected: {results['rejected']} ({100-acceptance_rate:.1f}%)")
    
    print(f"\nLanguages Detected:")
    for lang in sorted(results['languages_detected']):
        count = sum(1 for expr in all_expressions 
                   if lang in analyzer.detect_languages(analyzer.lexer.tokenize(expr)))
        print(f"  {lang}: {count} expressions")
    
    print(f"\n{'='*80}")
    print("CATEGORY BREAKDOWN")
    print(f"{'='*80}")
    
    for category, cat_results in results['by_category'].items():
        total = cat_results['accepted'] + cat_results['rejected']
        if total > 0:
            rate = (cat_results['accepted'] / total * 100)
            print(f"\n{category}:")
            print(f"  Accepted: {cat_results['accepted']}/{total} ({rate:.1f}%)")
            if cat_results['details']:
                print(f"  Rejected examples:")
                for detail in cat_results['details'][:3]:  # Show first 3
                    print(f"    - {detail['expression'][:50]}: {detail['reason']}")
    
    if results['rejected_details']:
        print(f"\n{'='*80}")
        print("REJECTED EXPRESSIONS ANALYSIS")
        print(f"{'='*80}")
        print(f"\nTotal Rejected: {len(results['rejected_details'])}")
        print("\nRejection Reasons:")
        reasons = {}
        for detail in results['rejected_details']:
            reason_key = detail['reason'].split('-')[0] if '-' in detail['reason'] else detail['reason']
            reasons[reason_key] = reasons.get(reason_key, 0) + 1
        
        for reason, count in sorted(reasons.items(), key=lambda x: x[1], reverse=True):
            print(f"  {reason}: {count}")
    
    print(f"\n{'='*80}")
    print("CONCLUSION")
    print(f"{'='*80}")
    print(f"\n✅ Acceptance Rate: {acceptance_rate:.1f}%")
    print(f"✅ Languages Detected: {len(results['languages_detected'])}")
    print(f"✅ Categories Covered: {len(expressions_by_category)}")
    
    if acceptance_rate >= 80:
        print("\n🎉 Excellent! High acceptance rate indicates robust grammar.")
    elif acceptance_rate >= 60:
        print("\n✅ Good! Acceptable acceptance rate for real-world data.")
    else:
        print("\n⚠️  Warning: Low acceptance rate. Consider grammar adjustments.")
    
    return results

if __name__ == '__main__':
    test_all_collected_data()

