#!/usr/bin/env python3
"""Create TuntasUMKM PPT v5 - synchronized with revised script."""
import json
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BG = "0a0a0a"
TITLE = "f5f5f5"
SUBTITLE = "a3a3a3"
BODY = "d4d4d4"
BLUE = "3b82f6"
GREEN = "22c55e"
ORANGE = "f97316"
RED = "ef4444"
PURPLE = "8b5cf6"
TEAL = "14b8a6"
AMBER = "f59e0b"
CARD_BG = "141414"
CARD_BORDER = "2a2a2a"

def set_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(color)

def add_text(slide, l, t, w, h, text, size=20, color=BODY, bold=False, align=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = RGBColor.from_string(color)
    p.alignment = align
    return txBox

def add_rect(slide, l, t, w, h, fill, text="", tc="f5f5f5", fs=14, border=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(fill)
    if border:
        shape.line.color.rgb = RGBColor.from_string(border)
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()
    if text:
        tf = shape.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(fs)
        p.font.color.rgb = RGBColor.from_string(tc)
        p.alignment = PP_ALIGN.CENTER
    return shape

def add_arrow(slide, l, t, w, h, color="525252"):
    shape = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(color)
    shape.line.fill.background()
    return shape

def add_right_arrow(slide, l, t, w, h, color="525252"):
    shape = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(color)
    shape.line.fill.background()
    return shape

def add_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text

def title_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 2.0, 11.7, 1.5, spec["title"], 72, TITLE, True, PP_ALIGN.CENTER)
    if spec.get("subtitle"):
        add_text(slide, 0.8, 3.8, 11.7, 2.0, spec["subtitle"], 28, SUBTITLE, False, PP_ALIGN.CENTER)
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def solution_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    if spec.get("subtitle"):
        add_text(slide, 0.8, 1.1, 11.7, 0.5, spec["subtitle"], 20, SUBTITLE)
    add_rect(slide, 0.8, 1.8, 5.5, 5.0, CARD_BG, border=GREEN)
    add_text(slide, 1.0, 2.0, 5.0, 0.5, "AI-Assisted (TuntasUMKM)", 20, GREEN, True)
    add_text(slide, 1.0, 2.6, 5.0, 3.5,
        "\u2713 AI searches products\n\u2713 AI creates draft order\n\u2713 Human approves transaction\n\u2713 Backend executes effects\n\u2713 Full audit trail\n\nAI has bounded authority.\nHuman holds the gate.",
        16, GREEN)
    add_rect(slide, 7.0, 1.8, 5.5, 5.0, CARD_BG, border=RED)
    add_text(slide, 7.2, 2.0, 5.0, 0.5, "AI-Autonomous (Dangerous)", 20, RED, True)
    add_text(slide, 7.2, 2.6, 5.0, 3.5,
        "\u2717 AI approves own orders\n\u2717 AI deducts stock directly\n\u2717 AI sends messages directly\n\u2717 No human oversight\n\u2717 No audit trail\n\nAI has full authority.\nNo human control.",
        16, RED)
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def arch_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    if spec.get("subtitle"):
        add_text(slide, 0.8, 1.1, 11.7, 0.5, spec["subtitle"], 20, SUBTITLE)
    fx, fw, bh, gap = 1.5, 2.0, 0.6, 0.35
    add_rect(slide, fx, 2.0, fw, bh, "1a1a1a", "Customer", "94a3b8", 14, "94a3b8")
    add_arrow(slide, fx+0.85, 2.6, 0.3, gap)
    add_rect(slide, fx, 2.95, fw, bh, "1a1a1a", "Hermes Agent", BLUE, 14, BLUE)
    add_arrow(slide, fx+0.85, 3.55, 0.3, gap)
    add_rect(slide, fx, 3.9, fw, bh, "1a1a1a", "MCP Tools", PURPLE, 14, PURPLE)
    add_arrow(slide, fx+0.85, 4.5, 0.3, gap)
    add_rect(slide, fx, 4.85, fw, bh, "1a1a1a", "Order Draft", AMBER, 14, AMBER)
    add_arrow(slide, fx+0.85, 5.45, 0.3, gap, ORANGE)
    add_rect(slide, fx, 5.8, fw, bh, "1a1a1a", "Human Approval", ORANGE, 14, ORANGE)
    px, pw = 5.0, 7.5
    add_rect(slide, px, 2.0, pw, 2.2, CARD_BG, border=CARD_BORDER)
    add_text(slide, px+0.3, 2.2, pw-0.6, 0.4, "Available to Agent", 16, GREEN, True)
    add_text(slide, px+0.3, 2.7, pw-0.6, 1.4, "\u2713 search_catalog\n\u2713 check_inventory\n\u2713 calculate_order_total\n\u2713 create_order_draft", 16, GREEN)
    add_rect(slide, px, 4.5, pw, 2.2, CARD_BG, border=CARD_BORDER)
    add_text(slide, px+0.3, 4.7, pw-0.6, 0.4, "Not Available to Agent", 16, RED, True)
    add_text(slide, px+0.3, 5.2, pw-0.6, 1.4, "\u2717 approve_order\n\u2717 reject_order\n\u2717 deduct_stock\n\u2717 send_customer_message", 16, RED)
    add_rect(slide, fx, 7.0, fw, bh, "1a1a1a", "Backend", GREEN, 14, GREEN)
    add_rect(slide, fx+2.5, 7.0, fw, bh, "1a1a1a", "Audit Trail", "64748b", 14, "64748b")
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def user_intent_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    if spec.get("subtitle"):
        add_text(slide, 0.8, 1.1, 11.7, 0.5, spec["subtitle"], 20, SUBTITLE)
    add_rect(slide, 2.0, 2.5, 9.0, 2.0, CARD_BG, border=BLUE)
    add_text(slide, 2.5, 2.8, 8.0, 0.5, "Customer says:", 16, BLUE, True)
    add_text(slide, 2.5, 3.3, 8.0, 1.0, "\"Saya mau pesan Sarung Tenun Samarinda 1 pcs\"", 32, TITLE, True)
    add_arrow(slide, 6.3, 4.7, 0.3, 0.5, BLUE)
    add_rect(slide, 2.0, 5.5, 9.0, 1.0, "1a1a1a", "Hermes Agent receives intent and starts working...", BLUE, 16, BLUE)
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def agent_execution_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    if spec.get("subtitle"):
        add_text(slide, 0.8, 1.1, 11.7, 0.5, spec["subtitle"], 20, SUBTITLE)
    steps = [
        ("USER INTENT", "94a3b8"),
        ("search_catalog", TEAL),
        ("check_inventory", TEAL),
        ("calculate_order_total", TEAL),
        ("create_order_draft", AMBER),
        ("PENDING APPROVAL", ORANGE),
    ]
    for i, (text, color) in enumerate(steps):
        y = 1.8 + i * 0.85
        add_rect(slide, 3.5, y, 6.0, 0.6, "1a1a1a", text, color, 16, color)
        if i < len(steps) - 1:
            add_arrow(slide, 6.3, y + 0.6, 0.3, 0.25, color)
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def boundary_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    if spec.get("subtitle"):
        add_text(slide, 0.8, 1.1, 11.7, 0.5, spec["subtitle"], 20, SUBTITLE)
    add_rect(slide, 2.5, 2.0, 8.0, 1.5, "1a1a1a", "pending_approval", ORANGE, 48, ORANGE)
    add_rect(slide, 2.5, 4.0, 8.0, 2.5, CARD_BG, border=ORANGE)
    add_text(slide, 2.8, 4.2, 7.5, 0.5, "Agent stops here", 24, ORANGE, True)
    add_text(slide, 2.8, 4.8, 7.5, 1.5,
        "\u2022 No stock deduction\n\u2022 No transaction final\n\u2022 No customer notification\n\u2022 Order menunggu persetujuan manusia",
        18, BODY)
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def human_approval_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    if spec.get("subtitle"):
        add_text(slide, 0.8, 1.1, 11.7, 0.5, spec["subtitle"], 20, SUBTITLE)
    add_rect(slide, 0.8, 2.0, 2.5, 1.0, "1a1a1a", "Dashboard\nApproval Queue", BLUE, 14, BLUE)
    add_right_arrow(slide, 3.5, 2.3, 0.6, 0.4, "525252")
    add_rect(slide, 4.3, 2.0, 2.5, 1.0, "1a1a1a", "Human Reviews\nOrder Detail", ORANGE, 14, ORANGE)
    add_right_arrow(slide, 7.0, 2.3, 0.6, 0.4, "525252")
    add_rect(slide, 7.8, 2.0, 2.5, 1.0, "1a1a1a", "Approve\nConfirm", GREEN, 14, GREEN)
    add_right_arrow(slide, 10.5, 2.3, 0.6, 0.4, "525252")
    add_rect(slide, 11.3, 2.0, 1.5, 1.0, "1a1a1a", "Status:\napproved", GREEN, 14, GREEN)
    add_rect(slide, 0.8, 3.5, 11.7, 3.0, CARD_BG, border=CARD_BORDER)
    add_text(slide, 1.0, 3.7, 11.0, 0.5, "What Human Sees in Dashboard:", 18, TITLE, True)
    add_text(slide, 1.0, 4.3, 11.0, 2.0,
        "\u2022 Order details: product, SKU, quantity, price\n\u2022 Stock information\n\u2022 Audit trail\n\u2022 Approve / Reject buttons\n\u2022 Confirmation dialog with consequences",
        16, BODY)
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def real_effect_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    if spec.get("subtitle"):
        add_text(slide, 0.8, 1.1, 11.7, 0.5, spec["subtitle"], 20, SUBTITLE)
    add_rect(slide, 1.5, 2.0, 3.0, 2.0, "1a1a1a", "Stock Before\n\n5", GREEN, 36, GREEN)
    add_right_arrow(slide, 4.8, 2.7, 1.0, 0.6, ORANGE)
    add_rect(slide, 6.0, 2.0, 3.0, 2.0, "1a1a1a", "Stock After\n\n4", ORANGE, 36, ORANGE)
    add_rect(slide, 1.5, 4.5, 3.0, 1.5, CARD_BG, border=GREEN)
    add_text(slide, 1.7, 4.7, 2.6, 1.0, "\u2713 Customer notified\n\u2713 Audit trail recorded", 14, GREEN)
    add_rect(slide, 6.0, 4.5, 3.0, 1.5, CARD_BG, border=ORANGE)
    add_text(slide, 6.2, 4.7, 2.6, 1.0, "\u2713 Transaction committed\n\u2713 Status: approved", 14, ORANGE)
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def audit_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    if spec.get("subtitle"):
        add_text(slide, 0.8, 1.1, 11.7, 0.5, spec["subtitle"], 20, SUBTITLE)
    entries = [
        ("1", "agent", "create_draft", "Order created as pending_approval", BLUE),
        ("2", "human", "APPROVE_ORDER", "Human approves via UI", ORANGE),
        ("3", "agent", "DEDUCT_STOCK", "Stock deducted: 5 \u2192 4", GREEN),
        ("4", "agent", "NOTIFY_CUSTOMER", "Customer notified via WhatsApp", TEAL),
    ]
    for i, (num, actor, action, desc, color) in enumerate(entries):
        y = 1.5 + i * 1.3
        add_rect(slide, 0.8, y, 0.6, 0.6, color, num, "0a0a0a", 16)
        add_rect(slide, 1.6, y, 1.2, 0.6, "1a1a1a", actor, color, 12, color)
        add_text(slide, 3.0, y, 2.5, 0.6, action, 16, color, True)
        add_text(slide, 5.5, y, 7.0, 0.6, desc, 16, BODY)
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def attack_boundary_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    if spec.get("subtitle"):
        add_text(slide, 0.8, 1.1, 11.7, 0.5, spec["subtitle"], 20, SUBTITLE)
    add_rect(slide, 0.8, 1.8, 5.5, 2.5, CARD_BG, border=GREEN)
    add_text(slide, 1.0, 2.0, 5.0, 0.5, "Available Tools", 20, GREEN, True)
    add_text(slide, 1.0, 2.6, 5.0, 1.5,
        "\u2713 search_catalog\n\u2713 check_inventory\n\u2713 calculate_order_total\n\u2713 create_order_draft",
        16, GREEN)
    add_rect(slide, 7.0, 1.8, 5.5, 2.5, CARD_BG, border=RED)
    add_text(slide, 7.2, 2.0, 5.0, 0.5, "Not Available Tools", 20, RED, True)
    add_text(slide, 7.2, 2.6, 5.0, 1.5,
        "\u2717 approve_order\n\u2717 reject_order\n\u2717 deduct_stock\n\u2717 send_customer_message",
        16, RED)
    add_rect(slide, 0.8, 4.8, 11.7, 1.5, "1a1a1a", border=AMBER)
    add_text(slide, 1.0, 5.0, 11.0, 1.0,
        "\"Bukan karena prompt-nya melarang agent.\nTool-nya memang tidak ada di MCP registry.\"",
        24, AMBER, True, PP_ALIGN.CENTER)
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def content_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    if spec.get("subtitle"):
        add_text(slide, 0.8, 1.1, 11.7, 0.5, spec["subtitle"], 20, SUBTITLE)
    if spec.get("bullets"):
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
        tf = txBox.text_frame
        tf.word_wrap = True
        for i, bullet in enumerate(spec["bullets"]):
            if isinstance(bullet, str):
                text, bc = bullet, BODY
            else:
                text, bc = bullet.get("text", ""), bullet.get("color", BODY)
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = text
            p.font.size = Pt(22)
            p.font.color.rgb = RGBColor.from_string(bc)
            p.space_after = Pt(16)
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide


def arch_3layer_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    if spec.get("subtitle"):
        add_text(slide, 0.8, 1.1, 11.7, 0.5, spec["subtitle"], 20, SUBTITLE)
    
    # Layer 1 - Human/UI (top)
    add_rect(slide, 1.5, 1.8, 10.0, 1.2, CARD_BG, border=ORANGE)
    add_text(slide, 1.7, 2.0, 9.6, 0.4, "Layer 1: HUMAN / UI", 18, ORANGE, True)
    add_text(slide, 1.7, 2.4, 9.6, 0.5, "Approve / Reject  |  Business Authorization Gate", 14, BODY)
    
    # Arrow down
    add_arrow(slide, 6.3, 3.0, 0.3, 0.4, "525252")
    
    # Layer 2 - Backend (middle)
    add_rect(slide, 1.5, 3.4, 10.0, 1.2, CARD_BG, border=GREEN)
    add_text(slide, 1.7, 3.6, 9.6, 0.4, "Layer 2: BACKEND", 18, GREEN, True)
    add_text(slide, 1.7, 4.0, 9.6, 0.5, "Transaction Boundary  |  Stock / Notification  |  Audit Log", 14, BODY)
    
    # Arrow down
    add_arrow(slide, 6.3, 4.6, 0.3, 0.4, "525252")
    
    # Layer 3 - Hermes Agent (bottom)
    add_rect(slide, 1.5, 5.0, 10.0, 1.8, CARD_BG, border=BLUE)
    add_text(slide, 1.7, 5.2, 9.6, 0.4, "Layer 3: HERMES AGENT (MCP Exposure)", 18, BLUE, True)
    add_text(slide, 1.7, 5.7, 9.6, 1.0,
        "✓ search_catalog  ✓ check_inventory  ✓ calculate_order_total  ✓ create_order_draft\n\n"
        "✗ approve_order  ✗ reject_order  ✗ deduct_stock  ✗ send_customer_message",
        14, BODY)
    
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def create_deck(spec_path, output_path):
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    for slide_spec in spec["slides"]:
        layout = slide_spec.get("layout", "title_content")
        if layout == "title":
            title_slide(prs, slide_spec)
        elif layout == "solution":
            solution_slide(prs, slide_spec)
        elif layout == "architecture":
            arch_slide(prs, slide_spec)
        elif layout == "architecture_3layer":
            arch_3layer_slide(prs, slide_spec)
        elif layout == "user_intent":
            user_intent_slide(prs, slide_spec)
        elif layout == "agent_execution":
            agent_execution_slide(prs, slide_spec)
        elif layout == "boundary":
            boundary_slide(prs, slide_spec)
        elif layout == "human_approval":
            human_approval_slide(prs, slide_spec)
        elif layout == "real_effect":
            real_effect_slide(prs, slide_spec)
        elif layout == "audit":
            audit_slide(prs, slide_spec)
        elif layout == "attack_boundary":
            attack_boundary_slide(prs, slide_spec)
        else:
            content_slide(prs, slide_spec)
    prs.save(output_path)
    print(json.dumps({"ok": True, "output": output_path, "slides": len(prs.slides._sldIdLst)}))

if __name__ == "__main__":
    import sys
    create_deck(sys.argv[1], sys.argv[2])
