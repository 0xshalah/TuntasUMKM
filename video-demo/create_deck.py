#!/usr/bin/env python3
"""Create TuntasUMKM PPT with proper text colors on dark background."""
import json
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

# Colors
BG = "0a0a0a"
TITLE_COLOR = "f5f5f5"
SUBTITLE_COLOR = "a3a3a3"
BODY_COLOR = "d4d4d4"
ACCENT_BLUE = "3b82f6"
ACCENT_GREEN = "22c55e"
ACCENT_ORANGE = "f97316"
ACCENT_RED = "ef4444"
ACCENT_PURPLE = "8b5cf6"

def set_text_color(text_frame, color_hex):
    """Set color for all runs in a text frame."""
    for para in text_frame.paragraphs:
        for run in para.runs:
            run.font.color.rgb = RGBColor.from_string(color_hex)

def add_slide_title(slide, title_text, color=TITLE_COLOR):
    """Add a title textbox with proper color."""
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.0))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor.from_string(color)
    return txBox

def add_slide_body(slide, bullets, color=BODY_COLOR, top=1.6, left=0.8, width=11.7, height=5.0):
    """Add body text with bullets and proper color."""
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, bullet in enumerate(bullets):
        if isinstance(bullet, str):
            text = bullet
            bullet_color = color
        else:
            text = bullet.get("text", "")
            bullet_color = bullet.get("color", color)
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = text
        p.font.size = Pt(20)
        p.font.color.rgb = RGBColor.from_string(bullet_color)
        p.space_after = Pt(12)
    return txBox

def add_slide_subtitle(slide, subtitle_text, color=SUBTITLE_COLOR):
    """Add subtitle with proper color."""
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.8))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = subtitle_text
    p.font.size = Pt(24)
    p.font.color.rgb = RGBColor.from_string(color)
    return txBox

def set_background(slide, color_hex):
    """Set solid background color."""
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(color_hex)

def add_notes(slide, notes_text):
    """Add speaker notes."""
    slide.notes_slide.notes_text_frame.text = notes_text

def create_deck(spec_path, output_path):
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout (index 6)
    blank_layout = prs.slide_layouts[6]
    
    for slide_spec in spec["slides"]:
        slide = prs.slides.add_slide(blank_layout)
        set_background(slide, slide_spec.get("background", BG))
        
        layout = slide_spec.get("layout", "title_content")
        
        if layout == "title":
            # Title slide - centered
            txBox = slide.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(11.7), Inches(1.5))
            tf = txBox.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = slide_spec["title"]
            p.font.size = Pt(72)
            p.font.bold = True
            p.font.color.rgb = RGBColor.from_string(TITLE_COLOR)
            p.alignment = PP_ALIGN.CENTER
            
            if slide_spec.get("subtitle"):
                txBox2 = slide.shapes.add_textbox(Inches(0.8), Inches(3.8), Inches(11.7), Inches(2.0))
                tf2 = txBox2.text_frame
                tf2.word_wrap = True
                p2 = tf2.paragraphs[0]
                p2.text = slide_spec["subtitle"]
                p2.font.size = Pt(28)
                p2.font.color.rgb = RGBColor.from_string(SUBTITLE_COLOR)
                p2.alignment = PP_ALIGN.CENTER
        else:
            # Content slide
            if slide_spec.get("title"):
                add_slide_title(slide, slide_spec["title"])
            
            if slide_spec.get("subtitle"):
                add_slide_subtitle(slide, slide_spec["subtitle"])
            
            if slide_spec.get("bullets"):
                add_slide_body(slide, slide_spec["bullets"])
        
        if slide_spec.get("notes"):
            add_notes(slide, slide_spec["notes"])
    
    prs.save(output_path)
    print(json.dumps({"ok": True, "output": output_path, "slides": len(prs.slides._sldIdLst)}))

if __name__ == "__main__":
    import sys
    create_deck(sys.argv[1], sys.argv[2])
