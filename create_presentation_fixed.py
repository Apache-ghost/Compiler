"""
Modern PowerPoint Presentation Generator - Fixed Version
Creates a captivating, professional presentation with modern design
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def add_gradient_background(slide, prs, color1, color2):
    """Add gradient background to slide"""
    background = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    fill = background.fill
    fill.gradient()
    fill.gradient_angle = 90.0
    fill.gradient_stops[0].color.rgb = color1
    fill.gradient_stops[1].color.rgb = color2
    background.line.fill.background()
    
    # Send to back
    slide.shapes._spTree.remove(background._element)
    slide.shapes._spTree.insert(2, background._element)
    
    return background

def add_modern_title_slide(prs, title, subtitle):
    """Add a stunning title slide with gradient and modern design"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # Gradient background
    add_gradient_background(
        slide, prs,
        RGBColor(10, 25, 47),
        RGBColor(20, 66, 114)
    )
    
    # Modern accent shape
    accent = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.5), Inches(1.5), Inches(9), Inches(4.5)
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = RGBColor(255, 255, 255)
    accent.fill.transparency = 0.1
    accent.line.fill.background()
    
    # Flag icon
    flag_box = slide.shapes.add_textbox(
        Inches(4.3), Inches(0.8), Inches(1.5), Inches(1)
    )
    flag_frame = flag_box.text_frame
    flag_frame.text = "🇨🇲"
    flag_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    flag_frame.paragraphs[0].font.size = Pt(80)
    
    # Title
    title_box = slide.shapes.add_textbox(
        Inches(0.8), Inches(2.2), Inches(8.4), Inches(1.5)
    )
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    title_frame.paragraphs[0].font.size = Pt(48)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    
    # Subtitle
    subtitle_box = slide.shapes.add_textbox(
        Inches(1), Inches(4), Inches(8), Inches(1.2)
    )
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = subtitle
    subtitle_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    subtitle_frame.paragraphs[0].font.size = Pt(26)
    subtitle_frame.paragraphs[0].font.color.rgb = RGBColor(255, 193, 7)
    
    # Decorative line
    line = slide.shapes.add_connector(
        1, Inches(3), Inches(3.8), Inches(7), Inches(3.8)
    )
    line.line.color.rgb = RGBColor(255, 193, 7)
    line.line.width = Pt(3)
    
    return slide

def add_section_divider(prs, title, icon="", accent_color=RGBColor(255, 193, 7)):
    """Add a modern section divider slide"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # Gradient background
    add_gradient_background(
        slide, prs,
        RGBColor(15, 32, 56),
        RGBColor(32, 58, 95)
    )
    
    # Large icon
    if icon:
        icon_box = slide.shapes.add_textbox(
            Inches(4), Inches(1.2), Inches(2), Inches(1.5)
        )
        icon_frame = icon_box.text_frame
        icon_frame.text = icon
        icon_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        icon_frame.paragraphs[0].font.size = Pt(120)
    
    # Title
    title_box = slide.shapes.add_textbox(
        Inches(1), Inches(3.5), Inches(8), Inches(1.5)
    )
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    title_frame.paragraphs[0].font.size = Pt(54)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    
    # Accent line
    line = slide.shapes.add_connector(
        1, Inches(2.5), Inches(5.2), Inches(7.5), Inches(5.2)
    )
    line.line.color.rgb = accent_color
    line.line.width = Pt(4)
    
    return slide

def add_modern_content_slide(prs, title, content_points, icon="", bg_theme="light"):
    """Add a modern content slide with cards"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # Background
    if bg_theme == "light":
        add_gradient_background(
            slide, prs,
            RGBColor(248, 250, 252),
            RGBColor(241, 245, 249)
        )
        title_bg = RGBColor(30, 58, 138)
        card_bg = RGBColor(255, 255, 255)
        text_color = RGBColor(30, 41, 59)
    else:
        add_gradient_background(
            slide, prs,
            RGBColor(15, 23, 42),
            RGBColor(30, 41, 59)
        )
        title_bg = RGBColor(59, 130, 246)
        card_bg = RGBColor(51, 65, 85)
        text_color = RGBColor(248, 250, 252)
    
    # Title bar
    title_shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.3), Inches(0.3), Inches(9.4), Inches(0.8)
    )
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = title_bg
    title_shape.line.fill.background()
    
    # Icon on title bar
    if icon:
        icon_box = slide.shapes.add_textbox(
            Inches(0.6), Inches(0.4), Inches(0.6), Inches(0.6)
        )
        icon_frame = icon_box.text_frame
        icon_frame.text = icon
        icon_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        icon_frame.paragraphs[0].font.size = Pt(32)
    
    # Title text
    title_box = slide.shapes.add_textbox(
        Inches(1.3) if icon else Inches(0.6),
        Inches(0.4),
        Inches(8) if icon else Inches(8.7),
        Inches(0.6)
    )
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.paragraphs[0].font.size = Pt(32)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    title_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # Content cards
    card_height = min(0.65, 4.8 / len(content_points))
    for i, point in enumerate(content_points):
        # Card background
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.8), Inches(1.5 + i * (card_height + 0.15)), 
            Inches(8.4), Inches(card_height)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = card_bg
        card.line.fill.background()
        
        # Extract emoji and text
        bullet = point[0:2] if len(point) > 2 and point[1] in '️🏽🇬🇫🌍🎭👥🏔🎨💬' else point[0]
        text_content = point[2:].strip() if bullet in point[:2] else point
        
        # Bullet/emoji
        bullet_box = slide.shapes.add_textbox(
            Inches(1), Inches(1.5 + i * (card_height + 0.15)), 
            Inches(0.4), Inches(card_height)
        )
        bullet_frame = bullet_box.text_frame
        bullet_frame.text = bullet
        bullet_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        bullet_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        bullet_frame.paragraphs[0].font.size = Pt(24)
        
        # Content text
        text_box = slide.shapes.add_textbox(
            Inches(1.5), Inches(1.5 + i * (card_height + 0.15)), 
            Inches(7.5), Inches(card_height)
        )
        text_frame = text_box.text_frame
        text_frame.text = text_content
        text_frame.paragraphs[0].font.size = Pt(18)
        text_frame.paragraphs[0].font.color.rgb = text_color
        text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        text_frame.word_wrap = True
    
    return slide

def add_two_column_modern(prs, title, left_title, left_items, right_title, right_items):
    """Add modern two-column comparison slide"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # Gradient background
    add_gradient_background(
        slide, prs,
        RGBColor(245, 247, 250),
        RGBColor(237, 242, 247)
    )
    
    # Title bar
    title_shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.3), Inches(0.3), Inches(9.4), Inches(0.7)
    )
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = RGBColor(99, 102, 241)
    title_shape.line.fill.background()
    
    title_box = slide.shapes.add_textbox(
        Inches(0.6), Inches(0.4), Inches(8.8), Inches(0.5)
    )
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.paragraphs[0].font.size = Pt(30)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    title_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    # Left column
    left_card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.5), Inches(1.3), Inches(4.4), Inches(5.2)
    )
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = RGBColor(255, 255, 255)
    left_card.line.color.rgb = RGBColor(59, 130, 246)
    left_card.line.width = Pt(3)
    
    # Left header
    left_header = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.5), Inches(1.3), Inches(4.4), Inches(0.6)
    )
    left_header.fill.solid()
    left_header.fill.fore_color.rgb = RGBColor(59, 130, 246)
    left_header.line.fill.background()
    
    left_title_box = slide.shapes.add_textbox(
        Inches(0.7), Inches(1.35), Inches(4), Inches(0.5)
    )
    lt_frame = left_title_box.text_frame
    lt_frame.text = left_title
    lt_frame.paragraphs[0].font.size = Pt(24)
    lt_frame.paragraphs[0].font.bold = True
    lt_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    lt_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    # Left content
    y_pos = 2.1
    for item in left_items:
        item_box = slide.shapes.add_textbox(
            Inches(0.8), Inches(y_pos), Inches(4), Inches(0.5)
        )
        item_frame = item_box.text_frame
        item_frame.text = item
        item_frame.paragraphs[0].font.size = Pt(16)
        item_frame.paragraphs[0].font.color.rgb = RGBColor(30, 41, 59)
        y_pos += 0.6
    
    # Right column
    right_card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(5.1), Inches(1.3), Inches(4.4), Inches(5.2)
    )
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = RGBColor(255, 255, 255)
    right_card.line.color.rgb = RGBColor(168, 85, 247)
    right_card.line.width = Pt(3)
    
    # Right header
    right_header = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(5.1), Inches(1.3), Inches(4.4), Inches(0.6)
    )
    right_header.fill.solid()
    right_header.fill.fore_color.rgb = RGBColor(168, 85, 247)
    right_header.line.fill.background()
    
    right_title_box = slide.shapes.add_textbox(
        Inches(5.3), Inches(1.35), Inches(4), Inches(0.5)
    )
    rt_frame = right_title_box.text_frame
    rt_frame.text = right_title
    rt_frame.paragraphs[0].font.size = Pt(24)
    rt_frame.paragraphs[0].font.bold = True
    rt_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    rt_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    # Right content
    y_pos = 2.1
    for item in right_items:
        item_box = slide.shapes.add_textbox(
            Inches(5.4), Inches(y_pos), Inches(4), Inches(0.5)
        )
        item_frame = item_box.text_frame
        item_frame.text = item
        item_frame.paragraphs[0].font.size = Pt(16)
        item_frame.paragraphs[0].font.color.rgb = RGBColor(30, 41, 59)
        y_pos += 0.6
    
    return slide

def create_fixed_presentation():
    """Create the presentation without problematic transitions"""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    print("Creating beautiful modern presentation...")
    
    # Slide 1: Title
    add_modern_title_slide(
        prs,
        "Yaounde Urban Communication Analyzer",
        "A Multilingual Compiler for Cameroonian Street Language"
    )
    print("✓ Title slide")
    
    # Slide 2: Overview
    add_section_divider(prs, "Project Overview", "🌍")
    print("✓ Overview section")
    
    # Slide 3: What is it
    add_modern_content_slide(
        prs,
        "What is This Project?",
        [
            "🎯 Sophisticated lexical and syntactic analyzer for urban Yaounde expressions",
            "🗣️ Processes multilingual street language (6 languages)",
            "⚙️ Complete compiler front-end with tokenizer and parser",
            "🖥️ Modern GUI and command-line interfaces",
            "📊 Analyzes real-world Cameroonian communication patterns"
        ],
        "🎯"
    )
    print("✓ What is it")
    
    # Slide 4: Why
    add_modern_content_slide(
        prs,
        "Why This Matters",
        [
            "🇨🇲 Preserves linguistic richness of Cameroonian urban culture",
            "💡 Demonstrates compiler construction for non-standard languages",
            "🔬 Applies formal language theory to real-world code-switching",
            "🌐 Bridges computational linguistics with African diversity",
            "📚 Foundation for future NLP tools for Cameroonian languages"
        ],
        "💡"
    )
    print("✓ Why it matters")
    
    # Slide 5: Languages
    add_section_divider(prs, "Supported Languages", "🗣️", RGBColor(76, 175, 80))
    
    # Slide 6: Language details
    add_two_column_modern(
        prs,
        "Multilingual Coverage",
        "Core Languages",
        [
            "🇬🇧 English - Base language",
            "🇫🇷 French - Colonial language",
            "🌍 Pidgin - West African Pidgin",
            "🎭 Franc-Anglais - Code-mixing"
        ],
        "Local Languages",
        [
            "👥 Ewondo - Central region",
            "🏔️ Fulfulde - Northern Cameroon",
            "🎨 Urban Slang - Street expressions",
            "💬 Seamless code-switching"
        ]
    )
    print("✓ Languages")
    
    # Slide 7: Architecture
    add_section_divider(prs, "System Architecture", "🏗️", RGBColor(255, 152, 0))
    
    # Slide 8: Components
    add_modern_content_slide(
        prs,
        "Core Components",
        [
            "1️⃣ Lexical Analyzer - Tokenizes expressions (40+ types)",
            "2️⃣ Grammar Engine - Context-Free Grammar with LL(1)",
            "3️⃣ Syntactic Parser - Structure validation and parse trees",
            "4️⃣ Complete Analyzer - End-to-end processing",
            "5️⃣ GUI Interface - Interactive visualization tool"
        ],
        "🏗️"
    )
    print("✓ Components")
    
    # Slide 9: Features
    add_section_divider(prs, "Key Features", "✨", RGBColor(233, 30, 99))
    
    # Slide 10: Technical
    add_two_column_modern(
        prs,
        "Powerful Capabilities",
        "Lexical Analysis",
        [
            "✅ 40+ distinct token types",
            "✅ Regex-based tokenization",
            "✅ Code-switching support",
            "✅ Frequency analysis",
            "✅ Position tracking"
        ],
        "Syntactic Analysis",
        [
            "✅ Context-Free Grammar",
            "✅ LL(1) parsing table",
            "✅ FIRST/FOLLOW sets",
            "✅ Parse tree generation",
            "✅ Real-time validation"
        ]
    )
    print("✓ Features")
    
    # Slide 11: Tokens
    add_modern_content_slide(
        prs,
        "Token Categories",
        [
            "📍 Places - quartier, carrefour, campus, ICT, Total",
            "👥 People - moto-guy, bendskin-man, patron, mbere",
            "🚕 Transport - taxi, bendskin, moto, clandos",
            "💰 Money - fap, mbongo, kop, francs, CFA",
            "🍽️ Food - tchop, ndole, eru, koki, fufu",
            "📱 Technology - call, airtime, WiFi, network"
        ],
        "🔤"
    )
    print("✓ Tokens")
    
    # Slide 12: Examples
    add_section_divider(prs, "Real-World Examples", "💬", RGBColor(0, 188, 212))
    
    # Slide 13: Example expressions
    add_modern_content_slide(
        prs,
        "Analyzed Expressions",
        [
            '🗨️ "Masa today no easy" - Greeting with time',
            '🗨️ "Give me 500 francs" - Money request',
            '🗨️ "Drop me for carrefour" - Transport instruction',
            '🗨️ "Where moto-guy dey" - Location question',
            '🗨️ "I need call card wallahi" - Urgent request',
            '🗨️ "The bendskin don break down garr" - Complaint'
        ],
        "💬"
    )
    print("✓ Examples")
    
    # Slide 14: Grammar
    add_modern_content_slide(
        prs,
        "Grammar Structure (CFG)",
        [
            "Statement → Greeting | Request | Question | Complaint",
            "Greeting → SLANG_RESPONSE TimePhrase?",
            "Request → VERB_GIVE PRONOUN TransportRequest",
            "Question → QuestionWord Statement QUESTION",
            "Complaint → Subject VERB_BE ADJ_NEGATIVE",
            "✓ LL(1) compliant - No conflicts"
        ],
        "📐"
    )
    print("✓ Grammar")
    
    # Slide 15: GUI
    add_section_divider(prs, "GUI Interface", "🖥️", RGBColor(156, 39, 176))
    
    # Slide 16: GUI features
    add_modern_content_slide(
        prs,
        "Interactive User Interface",
        [
            "✨ Real-time tokenization with color coding",
            "🌳 Parse tree visualization",
            "📊 Token frequency and statistics",
            "📚 Grammar information viewer",
            "💡 Example expression library",
            "🎯 Perfect for demonstrations!"
        ],
        "🖥️"
    )
    print("✓ GUI")
    
    # Slide 17: Tech stack
    add_two_column_modern(
        prs,
        "Technical Implementation",
        "Technologies",
        [
            "🐍 Python 3.x",
            "🎨 Tkinter GUI",
            "🔤 Regular Expressions",
            "🧪 Unit Testing",
            "📝 Documentation"
        ],
        "Algorithms",
        [
            "⚙️ LL(1) Parsing",
            "🔍 Recursive Descent",
            "📊 FIRST/FOLLOW",
            "🌳 Parse Trees",
            "🎯 Classification"
        ]
    )
    print("✓ Tech stack")
    
    # Slide 18: Testing
    add_modern_content_slide(
        prs,
        "Testing & Quality Assurance",
        [
            "✅ Comprehensive unit test suite",
            "✅ 50+ real-world test expressions",
            "✅ Lexical analyzer validation",
            "✅ Syntactic parser validation",
            "✅ Integration testing",
            "✅ Edge case handling"
        ],
        "🧪"
    )
    print("✓ Testing")
    
    # Slide 19: Status
    add_section_divider(prs, "Project Status", "🎯", RGBColor(76, 175, 80))
    
    # Slide 20: Complete
    add_modern_content_slide(
        prs,
        "Project Complete!",
        [
            "✅ 50+ real-world expressions collected",
            "✅ Lexical analyzer with 40+ token types",
            "✅ Complete LL(1) parser implemented",
            "✅ Modern GUI interface created",
            "✅ Comprehensive test suite",
            "✅ Complete documentation",
            "✅ Ready for presentation!"
        ],
        "✅"
    )
    print("✓ Status")
    
    # Slide 21: Future
    add_modern_content_slide(
        prs,
        "Future Enhancements",
        [
            "🚀 Semantic analyzer for meaning extraction",
            "🤖 Machine learning token classification",
            "🌐 Web-based interface",
            "📱 Mobile app development",
            "🗣️ Speech-to-text integration",
            "📚 Expanded regional corpus"
        ],
        "🚀"
    )
    print("✓ Future")
    
    # Slide 22: Demo
    add_section_divider(prs, "Live Demo", "🎬", RGBColor(244, 67, 54))
    
    # Slide 23: How to run
    add_modern_content_slide(
        prs,
        "Running the Analyzer",
        [
            "🖥️ GUI Mode: python gui_interface.py",
            "⌨️ CLI Mode: python main.py",
            "🧪 Run Tests: python test_analyzer.py",
            "📊 Generate Report: python generate_report_data.py"
        ],
        "▶️"
    )
    print("✓ How to run")
    
    # Slide 24: Thank you
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    add_gradient_background(
        slide, prs,
        RGBColor(10, 25, 47),
        RGBColor(88, 28, 135)
    )
    
    # Circle
    circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(3), Inches(1.5), Inches(4), Inches(4)
    )
    circle.fill.solid()
    circle.fill.fore_color.rgb = RGBColor(255, 255, 255)
    circle.fill.transparency = 0.1
    circle.line.fill.background()
    
    thank_you_box = slide.shapes.add_textbox(
        Inches(3), Inches(2.5), Inches(4), Inches(1)
    )
    ty_frame = thank_you_box.text_frame
    ty_frame.text = "Thank You!"
    ty_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    ty_frame.paragraphs[0].font.size = Pt(54)
    ty_frame.paragraphs[0].font.bold = True
    ty_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    
    emoji_box = slide.shapes.add_textbox(
        Inches(4), Inches(3.6), Inches(2), Inches(0.8)
    )
    emoji_frame = emoji_box.text_frame
    emoji_frame.text = "🇨🇲 ✨"
    emoji_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    emoji_frame.paragraphs[0].font.size = Pt(48)
    
    subtitle_box = slide.shapes.add_textbox(
        Inches(2), Inches(5.8), Inches(6), Inches(0.8)
    )
    sub_frame = subtitle_box.text_frame
    sub_frame.text = "Questions?"
    sub_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    sub_frame.paragraphs[0].font.size = Pt(36)
    sub_frame.paragraphs[0].font.color.rgb = RGBColor(255, 193, 7)
    
    print("✓ Thank you")
    
    # Save
    filename = "Yaounde_Analyzer_Modern_Presentation_Fixed.pptx"
    prs.save(filename)
    
    print(f"\n{'='*60}")
    print(f"✅ Beautiful presentation created successfully!")
    print(f"📁 Filename: {filename}")
    print(f"📊 Total slides: {len(prs.slides)}")
    print(f"🎨 Features:")
    print(f"   • Gradient backgrounds")
    print(f"   • Modern card-based layouts")
    print(f"   • Professional color schemes")
    print(f"   • Icon integration")
    print(f"   • Rounded corners")
    print(f"   • No XML errors - fully compatible!")
    print(f"✨ Ready to present!")
    print(f"{'='*60}\n")
    
    return filename

if __name__ == "__main__":
    import os
    print(f"Working directory: {os.getcwd()}\n")
    create_fixed_presentation()
