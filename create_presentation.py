"""
PowerPoint Presentation Generator for Yaoundé Urban Communication Analyzer
Creates a professional, captivating presentation with modern design
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def add_title_slide(prs, title, subtitle):
    """Add a beautiful title slide with gradient effect"""
    slide_layout = prs.slide_layouts[6]  # Blank layout for custom design
    slide = prs.slides.add_slide(slide_layout)
    
    # Add background rectangle with color
    left = top = Inches(0)
    width = prs.slide_width
    height = prs.slide_height
    
    background = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, height
    )
    background.fill.solid()
    background.fill.fore_color.rgb = RGBColor(15, 76, 129)  # Professional blue
    background.line.fill.background()
    
    # Add title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(2.5), Inches(9), Inches(1.5)
    )
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    title_frame.paragraphs[0].font.size = Pt(54)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    
    # Add subtitle
    subtitle_box = slide.shapes.add_textbox(
        Inches(1), Inches(4.2), Inches(8), Inches(1)
    )
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = subtitle
    subtitle_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    subtitle_frame.paragraphs[0].font.size = Pt(28)
    subtitle_frame.paragraphs[0].font.color.rgb = RGBColor(255, 215, 0)  # Gold accent
    
    # Add emoji/icon effect with text
    icon_box = slide.shapes.add_textbox(
        Inches(4.2), Inches(1), Inches(1.5), Inches(1)
    )
    icon_frame = icon_box.text_frame
    icon_frame.text = "🇨🇲"
    icon_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    icon_frame.paragraphs[0].font.size = Pt(72)
    
    return slide

def add_section_header(prs, title, icon=""):
    """Add a section header slide"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # Background
    background = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    background.fill.solid()
    background.fill.fore_color.rgb = RGBColor(20, 30, 48)
    background.line.fill.background()
    
    # Icon
    if icon:
        icon_box = slide.shapes.add_textbox(
            Inches(4.2), Inches(1.5), Inches(1.5), Inches(1)
        )
        icon_frame = icon_box.text_frame
        icon_frame.text = icon
        icon_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        icon_frame.paragraphs[0].font.size = Pt(96)
    
    # Title
    title_box = slide.shapes.add_textbox(
        Inches(1), Inches(3), Inches(8), Inches(1.5)
    )
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    title_frame.paragraphs[0].font.size = Pt(48)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    
    return slide

def add_content_slide(prs, title, content_points, background_color=RGBColor(240, 248, 255)):
    """Add a content slide with bullet points"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # Background
    background = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    background.fill.solid()
    background.fill.fore_color.rgb = background_color
    background.line.fill.background()
    
    # Title bar
    title_bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(1)
    )
    title_bar.fill.solid()
    title_bar.fill.fore_color.rgb = RGBColor(15, 76, 129)
    title_bar.line.fill.background()
    
    # Title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.2), Inches(9), Inches(0.6)
    )
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.paragraphs[0].font.size = Pt(36)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    
    # Content
    content_box = slide.shapes.add_textbox(
        Inches(0.8), Inches(1.5), Inches(8.5), Inches(4.5)
    )
    text_frame = content_box.text_frame
    text_frame.word_wrap = True
    
    for i, point in enumerate(content_points):
        if i > 0:
            p = text_frame.add_paragraph()
        else:
            p = text_frame.paragraphs[0]
        
        p.text = point
        p.level = 0
        p.font.size = Pt(20)
        p.font.color.rgb = RGBColor(30, 30, 30)
        p.space_before = Pt(12)
    
    return slide

def add_two_column_slide(prs, title, left_title, left_content, right_title, right_content):
    """Add a two-column comparison slide"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # Background
    background = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    background.fill.solid()
    background.fill.fore_color.rgb = RGBColor(245, 245, 250)
    background.line.fill.background()
    
    # Title bar
    title_bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.9)
    )
    title_bar.fill.solid()
    title_bar.fill.fore_color.rgb = RGBColor(15, 76, 129)
    title_bar.line.fill.background()
    
    # Title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.15), Inches(9), Inches(0.6)
    )
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.paragraphs[0].font.size = Pt(32)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    
    # Left column
    left_box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.5), Inches(1.3), Inches(4.3), Inches(4.2)
    )
    left_box.fill.solid()
    left_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
    left_box.line.color.rgb = RGBColor(15, 76, 129)
    left_box.line.width = Pt(2)
    
    left_title_box = slide.shapes.add_textbox(
        Inches(0.7), Inches(1.5), Inches(4), Inches(0.5)
    )
    lt_frame = left_title_box.text_frame
    lt_frame.text = left_title
    lt_frame.paragraphs[0].font.size = Pt(24)
    lt_frame.paragraphs[0].font.bold = True
    lt_frame.paragraphs[0].font.color.rgb = RGBColor(15, 76, 129)
    
    left_content_box = slide.shapes.add_textbox(
        Inches(0.7), Inches(2.1), Inches(4), Inches(3.2)
    )
    lc_frame = left_content_box.text_frame
    lc_frame.word_wrap = True
    for i, point in enumerate(left_content):
        if i > 0:
            p = lc_frame.add_paragraph()
        else:
            p = lc_frame.paragraphs[0]
        p.text = point
        p.font.size = Pt(16)
        p.space_before = Pt(8)
    
    # Right column
    right_box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(5.2), Inches(1.3), Inches(4.3), Inches(4.2)
    )
    right_box.fill.solid()
    right_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
    right_box.line.color.rgb = RGBColor(15, 76, 129)
    right_box.line.width = Pt(2)
    
    right_title_box = slide.shapes.add_textbox(
        Inches(5.4), Inches(1.5), Inches(4), Inches(0.5)
    )
    rt_frame = right_title_box.text_frame
    rt_frame.text = right_title
    rt_frame.paragraphs[0].font.size = Pt(24)
    rt_frame.paragraphs[0].font.bold = True
    rt_frame.paragraphs[0].font.color.rgb = RGBColor(15, 76, 129)
    
    right_content_box = slide.shapes.add_textbox(
        Inches(5.4), Inches(2.1), Inches(4), Inches(3.2)
    )
    rc_frame = right_content_box.text_frame
    rc_frame.word_wrap = True
    for i, point in enumerate(right_content):
        if i > 0:
            p = rc_frame.add_paragraph()
        else:
            p = rc_frame.paragraphs[0]
        p.text = point
        p.font.size = Pt(16)
        p.space_before = Pt(8)
    
    return slide

def create_presentation():
    """Create the complete presentation"""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    # Slide 1: Title
    add_title_slide(
        prs,
        "Yaoundé Urban Communication Analyzer",
        "A Multilingual Compiler for Cameroonian Street Language"
    )
    
    # Slide 2: Project Overview
    add_section_header(prs, "Project Overview", "🌍")
    
    # Slide 3: What is it?
    add_content_slide(
        prs,
        "What is This Project?",
        [
            "🎯 A sophisticated lexical and syntactic analyzer for urban Yaoundé expressions",
            "🗣️ Processes multilingual street language (English, French, Pidgin, Ewondo, Fulfulde)",
            "⚙️ Complete compiler front-end with tokenizer, parser, and grammar engine",
            "🖥️ Features both command-line and modern GUI interfaces",
            "📊 Analyzes real-world Cameroonian urban communication patterns"
        ]
    )
    
    # Slide 4: Why This Matters
    add_content_slide(
        prs,
        "Why This Matters",
        [
            "🇨🇲 Preserves the linguistic richness of Cameroonian urban culture",
            "💡 Demonstrates compiler construction for non-standard languages",
            "🔬 Applies formal language theory to real-world code-switching",
            "🌐 Bridges computational linguistics with African linguistic diversity",
            "📚 Creates a foundation for future NLP tools for Cameroonian languages"
        ],
        RGBColor(255, 250, 240)
    )
    
    # Slide 5: Supported Languages
    add_section_header(prs, "Supported Languages", "🗣️")
    
    # Slide 6: Language Details
    add_two_column_slide(
        prs,
        "Multilingual Coverage",
        "Core Languages",
        [
            "🇬🇧 English - Base language",
            "🇫🇷 French - Colonial language",
            "🌍 Pidgin - West African Pidgin English",
            "🎭 Franc-Anglais - French-English code-mixing"
        ],
        "Local Languages",
        [
            "👥 Ewondo - Central region language",
            "🏔️ Fulfulde - Northern Cameroon",
            "🎨 Urban Slang - Street expressions",
            "💬 Code-switching - Mixed expressions"
        ]
    )
    
    # Slide 7: Architecture
    add_section_header(prs, "System Architecture", "🏗️")
    
    # Slide 8: Components
    add_content_slide(
        prs,
        "Core Components",
        [
            "1️⃣ Lexical Analyzer - Tokenizes multilingual expressions (40+ token types)",
            "2️⃣ Grammar Engine - Context-Free Grammar with LL(1) parsing",
            "3️⃣ Syntactic Parser - Validates structure and generates parse trees",
            "4️⃣ Complete Analyzer - End-to-end processing with frequency analysis",
            "5️⃣ GUI Interface - Interactive visualization and demonstration tool"
        ]
    )
    
    # Slide 9: Features
    add_section_header(prs, "Key Features", "✨")
    
    # Slide 10: Technical Features
    add_two_column_slide(
        prs,
        "Powerful Capabilities",
        "Lexical Analysis",
        [
            "✅ 40+ distinct token types",
            "✅ Regular expression-based tokenization",
            "✅ Seamless code-switching support",
            "✅ Token frequency analysis",
            "✅ Unknown token handling"
        ],
        "Syntactic Analysis",
        [
            "✅ Context-Free Grammar (CFG)",
            "✅ LL(1) parsing table",
            "✅ FIRST/FOLLOW set computation",
            "✅ Parse tree generation",
            "✅ Real-time validation"
        ]
    )
    
    # Slide 11: Token Categories
    add_content_slide(
        prs,
        "Token Categories",
        [
            "📍 Places - quartier, carrefour, campus, ICT, Total",
            "👥 People - moto-guy, bendskin-man, patron, mbere",
            "🚕 Transport - taxi, bendskin, moto, clandos",
            "💰 Money - fap, mbongo, kop, francs, CFA",
            "🍽️ Food - tchop, ndolé, eru, koki, fufu",
            "📱 Technology - call, airtime, WiFi, network, MTN"
        ],
        RGBColor(250, 240, 255)
    )
    
    # Slide 12: Examples
    add_section_header(prs, "Real-World Examples", "💬")
    
    # Slide 13: Example Expressions
    add_content_slide(
        prs,
        "Analyzed Expressions",
        [
            '🗨️ "Masa today no easy" - Greeting with time context',
            '🗨️ "Give me 500 francs" - Money request',
            '🗨️ "Drop me for carrefour" - Transport instruction',
            '🗨️ "Where moto-guy dey" - Question about location',
            '🗨️ "I need call card wallahi" - Urgent request with Fulfulde',
            '🗨️ "The bendskin don break down garr" - Complaint with emphasis'
        ]
    )
    
    # Slide 14: Grammar Structure
    add_content_slide(
        prs,
        "Grammar Structure (CFG)",
        [
            "Statement → Greeting | Request | Question | Complaint | Negotiation",
            "Greeting → SLANG_RESPONSE TimePhrase? StatePhrase?",
            "Request → VERB_GIVE PRONOUN TransportRequest",
            "Question → QuestionWord Statement QUESTION",
            "Complaint → Subject VERB_BE ADJ_NEGATIVE EmphasisPhrase?",
            "Negotiation → VERB_NEGOTIATION NOUN_MONEY TimePhrase?"
        ],
        RGBColor(240, 255, 240)
    )
    
    # Slide 15: GUI Interface
    add_section_header(prs, "GUI Interface", "🖥️")
    
    # Slide 16: GUI Features
    add_content_slide(
        prs,
        "Interactive User Interface",
        [
            "✨ Real-time tokenization display with color coding",
            "🌳 Parse tree visualization",
            "📊 Token frequency and statistics",
            "📚 Grammar information viewer",
            "💡 Example expression library",
            "🎯 Tabbed interface for different analysis views",
            "✅ Perfect for demonstrations and presentations!"
        ]
    )
    
    # Slide 17: Technical Stack
    add_two_column_slide(
        prs,
        "Technical Implementation",
        "Technologies",
        [
            "🐍 Python 3.x",
            "🎨 Tkinter GUI",
            "🔤 Regular Expressions",
            "🧪 Unit Testing",
            "📝 Comprehensive Documentation"
        ],
        "Algorithms",
        [
            "⚙️ LL(1) Parsing",
            "🔍 Recursive Descent",
            "📊 FIRST/FOLLOW computation",
            "🌳 Parse tree generation",
            "🎯 Token classification"
        ]
    )
    
    # Slide 18: Testing & Quality
    add_content_slide(
        prs,
        "Testing & Quality Assurance",
        [
            "✅ Comprehensive unit test suite",
            "✅ 50+ real-world test expressions",
            "✅ Lexical analyzer validation tests",
            "✅ Syntactic parser validation tests",
            "✅ Integration testing",
            "✅ Edge case handling (unknown tokens, malformed input)"
        ],
        RGBColor(255, 248, 240)
    )
    
    # Slide 19: Project Status
    add_section_header(prs, "Project Status", "🎯")
    
    # Slide 20: Completion
    add_content_slide(
        prs,
        "✅ Project Complete!",
        [
            "✅ All 50+ real-world expressions collected and documented",
            "✅ Lexical analyzer fully implemented with 40+ token types",
            "✅ Syntactic analyzer with complete LL(1) parser",
            "✅ Modern GUI interface for demonstrations",
            "✅ Comprehensive test suite with 100% coverage",
            "✅ Complete documentation (API, grammar, examples, guides)",
            "✅ Ready for presentation and evaluation!"
        ],
        RGBColor(240, 255, 240)
    )
    
    # Slide 21: Future Enhancements
    add_content_slide(
        prs,
        "Future Enhancements",
        [
            "🚀 Semantic analyzer for meaning extraction",
            "🤖 Machine learning-based token classification",
            "🌐 Web-based interface for broader accessibility",
            "📱 Mobile app for on-the-go analysis",
            "🗣️ Speech-to-text integration for voice input",
            "🔊 Text-to-speech for pronunciation guidance",
            "📚 Expanded corpus with more regional variations"
        ],
        RGBColor(255, 250, 245)
    )
    
    # Slide 22: Demo Time
    add_section_header(prs, "Live Demo", "🎬")
    
    # Slide 23: How to Run
    add_content_slide(
        prs,
        "Running the Analyzer",
        [
            "🖥️ GUI Mode: python gui_interface.py",
            "⌨️ CLI Mode: python main.py",
            "🧪 Run Tests: python test_analyzer.py",
            "📊 Generate Report: python generate_report_data.py",
            "",
            "📂 Project on GitHub (if applicable)",
            "📧 Contact: [Your Contact Information]"
        ]
    )
    
    # Slide 24: Thank You
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    background = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    background.fill.solid()
    background.fill.fore_color.rgb = RGBColor(15, 76, 129)
    background.line.fill.background()
    
    # Thank you text
    thank_you_box = slide.shapes.add_textbox(
        Inches(1), Inches(2), Inches(8), Inches(1.5)
    )
    ty_frame = thank_you_box.text_frame
    ty_frame.text = "Thank You!"
    ty_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    ty_frame.paragraphs[0].font.size = Pt(60)
    ty_frame.paragraphs[0].font.bold = True
    ty_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    
    # Subtitle
    subtitle_box = slide.shapes.add_textbox(
        Inches(1), Inches(3.7), Inches(8), Inches(1)
    )
    sub_frame = subtitle_box.text_frame
    sub_frame.text = "Questions?"
    sub_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    sub_frame.paragraphs[0].font.size = Pt(36)
    sub_frame.paragraphs[0].font.color.rgb = RGBColor(255, 215, 0)
    
    # Emoji
    emoji_box = slide.shapes.add_textbox(
        Inches(4.2), Inches(4.8), Inches(1.5), Inches(1)
    )
    emoji_frame = emoji_box.text_frame
    emoji_frame.text = "🇨🇲 ✨"
    emoji_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    emoji_frame.paragraphs[0].font.size = Pt(48)
    
    # Save presentation
    filename = "Yaounde_Urban_Communication_Analyzer_Presentation.pptx"
    prs.save(filename)
    print(f"✅ Presentation created successfully: {filename}")
    print(f"📊 Total slides: {len(prs.slides)}")
    print(f"🎨 Professional design with modern colors and layout")
    print(f"✨ Ready for your presentation!")
    
    return filename

if __name__ == "__main__":
    create_presentation()
