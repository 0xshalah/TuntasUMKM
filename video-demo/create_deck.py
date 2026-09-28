#!/usr/bin/env python3
"""Create TuntasUMKM PPT with diagrams on multiple slides."""
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
    add_rect(slide, fx, 3.9, fw, bh, "1a1a1a", "MCP", PURPLE, 14, PURPLE)
    add_arrow(slide, fx+0.85, 4.5, 0.3, gap)
    add_rect(slide, fx-0.3, 4.85, fw+0.6, bh, "1a1a1a", "Bounded Tools", TEAL, 14, TEAL)
    add_arrow(slide, fx+0.85, 5.45, 0.3, gap)
    add_rect(slide, fx, 5.8, fw, bh, "1a1a1a", "Order Draft", AMBER, 14, AMBER)
    add_arrow(slide, fx+0.85, 6.4, 0.3, gap, ORANGE)
    add_rect(slide, fx, 6.75, fw, bh, "1a1a1a", "Human Approval", ORANGE, 14, ORANGE)
    px, pw = 5.0, 7.5
    add_rect(slide, px, 2.0, pw, 2.2, CARD_BG, border=CARD_BORDER)
    add_text(slide, px+0.3, 2.2, pw-0.6, 0.4, "Available to Agent", 16, GREEN, True)
    add_text(slide, px+0.3, 2.7, pw-0.6, 1.4, "✓ search_catalog\n✓ check_inventory\n✓ calculate_order_total\n✓ create_order_draft", 16, GREEN)
    add_rect(slide, px, 4.5, pw, 2.2, CARD_BG, border=CARD_BORDER)
    add_text(slide, px+0.3, 4.7, pw-0.6, 0.4, "Not Exposed to Agent", 16, RED, True)
    add_text(slide, px+0.3, 5.2, pw-0.6, 1.4, "✕ approve_order\n✕ reject_order\n✕ deduct_stock\n✕ send_customer_message", 16, RED)
    add_rect(slide, fx, 7.0, fw, bh, "1a1a1a", "Backend", GREEN, 14, GREEN)
    add_rect(slide, fx+2.5, 7.0, fw, bh, "1a1a1a", "Audit Trail", "64748b", 14, "64748b")
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def problem_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    add_rect(slide, 0.8, 1.5, 2.5, 0.8, CARD_BG, "WhatsApp", "94a3b8", 14, "94a3b8")
    add_rect(slide, 0.8, 2.5, 2.5, 0.8, CARD_BG, "Instagram", "94a3b8", 14, "94a3b8")
    add_rect(slide, 0.8, 3.5, 2.5, 0.8, CARD_BG, "Tokopedia", "94a3b8", 14, "94a3b8")
    add_right_arrow(slide, 3.5, 2.3, 0.8, 0.4, "525252")
    add_rect(slide, 4.5, 1.8, 3.5, 2.0, "1a1a1a", "Chaos:\nMultiple channels\nManual processes\nNo audit trail", RED, 16, RED)
    add_right_arrow(slide, 8.2, 2.3, 0.8, 0.4, "525252")
    add_rect(slide, 9.2, 1.8, 3.5, 2.0, "1a1a1a", "Solution:\nAI Agent + HITL\nBounded authority\nFull audit trail", GREEN, 16, GREEN)
    if spec.get("bullets"):
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(4.5), Inches(11.7), Inches(2.5))
        tf = txBox.text_frame
        tf.word_wrap = True
        for i, bullet in enumerate(spec["bullets"]):
            if isinstance(bullet, str):
                text, bc = bullet, BODY
            else:
                text, bc = bullet.get("text", ""), bullet.get("color", BODY)
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = text
            p.font.size = Pt(20)
            p.font.color.rgb = RGBColor.from_string(bc)
            p.space_after = Pt(12)
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def bounded_authority_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    add_rect(slide, 0.8, 1.5, 5.5, 5.0, CARD_BG, border=BLUE)
    add_text(slide, 1.0, 1.7, 5.0, 0.5, "Agent Authority Zone", 20, BLUE, True)
    add_text(slide, 1.0, 2.3, 5.0, 3.5, "✓ Search catalog\n✓ Check inventory\n✓ Calculate order total\n✓ Create order draft\n\nAgent CAN:\n• Understand user intent\n• Query business data\n• Prepare order draft\n• Stop at approval gate", 16, GREEN)
    add_rect(slide, 7.0, 1.5, 5.5, 5.0, CARD_BG, border=ORANGE)
    add_text(slide, 7.2, 1.7, 5.0, 0.5, "Human Authority Zone", 20, ORANGE, True)
    add_text(slide, 7.2, 2.3, 5.0, 3.5, "✓ Approve order\n✓ Reject order\n✓ Deduct stock\n✓ Send customer message\n\nHuman CAN:\n• Make transactional decisions\n• Execute business effects\n• Override agent suggestions", 16, ORANGE)
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def hitl_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    add_rect(slide, 0.8, 1.8, 3.0, 1.0, "1a1a1a", "Agent creates\ndraft order", BLUE, 16, BLUE)
    add_right_arrow(slide, 4.0, 2.1, 0.8, 0.4, "525252")
    add_rect(slide, 5.0, 1.8, 3.0, 1.0, "1a1a1a", "Human reviews\n& approves", ORANGE, 16, ORANGE)
    add_right_arrow(slide, 8.2, 2.1, 0.8, 0.4, "525252")
    add_rect(slide, 9.2, 1.8, 3.0, 1.0, "1a1a1a", "Backend executes\n& audits", GREEN, 16, GREEN)
    add_rect(slide, 0.8, 3.2, 3.0, 2.5, CARD_BG, border=BLUE)
    add_text(slide, 1.0, 3.4, 2.6, 2.0, "Agent:\n• search_catalog\n• create_order_draft\n• Status: pending_approval\n• No stock deduction", 14, BLUE)
    add_rect(slide, 5.0, 3.2, 3.0, 2.5, CARD_BG, border=ORANGE)
    add_text(slide, 5.2, 3.4, 2.6, 2.0, "Human:\n• Reviews order details\n• Approves or rejects\n• Decision is final\n• Cannot be overridden by agent", 14, ORANGE)
    add_rect(slide, 9.2, 3.2, 3.0, 2.5, CARD_BG, border=GREEN)
    add_text(slide, 9.4, 3.4, 2.6, 2.0, "Backend:\n• Deducts stock\n• Sends notification\n• Writes audit log\n• Transactional commit", 14, GREEN)
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def mcp_tools_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    tools = [
        ("search_catalog", "Search product catalog\nby name or SKU", TEAL),
        ("check_inventory", "Check stock level\nfor a specific SKU", TEAL),
        ("calculate_order_total", "Calculate total price\nfor order lines", TEAL),
        ("create_order_draft", "Create pending_approval\norder draft", AMBER),
    ]
    for i, (name, desc, color) in enumerate(tools):
        x = 0.8 + i * 3.1
        add_rect(slide, x, 1.8, 2.8, 2.5, CARD_BG, border=color)
        add_text(slide, x+0.2, 2.0, 2.4, 0.5, name, 16, color, True)
        add_text(slide, x+0.2, 2.6, 2.4, 1.5, desc, 14, BODY)
    add_rect(slide, 0.8, 4.8, 11.7, 1.5, CARD_BG, border=AMBER)
    add_text(slide, 1.0, 5.0, 11.0, 0.4, "P2.5 Actual Execution", 16, AMBER, True)
    add_text(slide, 1.0, 5.5, 11.0, 0.8, "Tools used: search_catalog → create_order_draft\nTools available but NOT used: check_inventory, calculate_order_total", 16, BODY)
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def evidence_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    add_rect(slide, 0.8, 1.5, 5.5, 4.5, CARD_BG, border=AMBER)
    add_text(slide, 1.0, 1.7, 5.0, 0.4, "Order Details", 18, AMBER, True)
    add_text(slide, 1.0, 2.3, 5.0, 3.5, "Order ID: ORD-20260927-35BD8E\nProduct: Sarung Tenun Samarinda\nSKU: SRG-TNN-04\nQuantity: 1\nPrice: Rp 520.000\nStatus: pending_approval → approved\nChannel: MCP Agent", 16, BODY)
    add_rect(slide, 7.0, 1.5, 5.5, 2.0, CARD_BG, border=GREEN)
    add_text(slide, 7.2, 1.7, 5.0, 0.4, "Stock Transition", 18, GREEN, True)
    add_text(slide, 7.2, 2.3, 5.0, 1.0, "Before: 3\nAfter: 2\nDeduction: 1", 20, BODY)
    add_rect(slide, 7.0, 3.8, 5.5, 2.2, CARD_BG, border="64748b")
    add_text(slide, 7.2, 4.0, 5.0, 0.4, "Audit Trail (4 entries)", 18, "64748b", True)
    add_text(slide, 7.2, 4.6, 5.0, 1.2, "1. agent — create_draft\n2. human — APPROVE_ORDER\n3. agent — DEDUCT_STOCK\n4. agent — NOTIFY_CUSTOMER", 14, BODY)
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def audit_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    entries = [
        ("1", "agent", "create_draft", "Order created as pending_approval", BLUE),
        ("2", "human", "APPROVE_ORDER", "Human approves via UI", ORANGE),
        ("3", "agent", "DEDUCT_STOCK", "Stock deducted: 3 → 2", GREEN),
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

def security_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    add_rect(slide, 0.8, 1.5, 5.5, 5.0, CARD_BG, border=GREEN)
    add_text(slide, 1.0, 1.7, 5.0, 0.5, "Agent Boundary (Safe)", 20, GREEN, True)
    add_text(slide, 1.0, 2.3, 5.0, 3.5, "✓ Read-only queries\n✓ Create draft orders\n✓ Stop at approval gate\n\nAgent CANNOT:\n• Approve/reject orders\n• Deduct stock\n• Send messages\n• Access database directly", 16, GREEN)
    add_rect(slide, 7.0, 1.5, 5.5, 5.0, CARD_BG, border=RED)
    add_text(slide, 7.2, 1.7, 5.0, 0.5, "Forbidden Zone", 20, RED, True)
    add_text(slide, 7.2, 2.3, 5.0, 3.5, "✕ Direct database access\n✕ Transactional commits\n✕ Stock mutation\n✕ Customer communication\n\nAll transactional operations\nrequire human approval", 16, RED)
    if spec.get("notes"):
        add_notes(slide, spec["notes"])
    return slide

def comparison_slide(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, spec.get("background", BG))
    add_text(slide, 0.8, 0.3, 11.7, 0.8, spec["title"], 40, TITLE, True)
    add_rect(slide, 0.8, 1.5, 5.5, 5.0, CARD_BG, border=RED)
    add_text(slide, 1.0, 1.7, 5.0, 0.5, "Traditional Chatbot", 20, RED, True)
    add_text(slide, 1.0, 2.3, 5.0, 3.5, "• Generates text responses\n• No tool integration\n• No business logic\n• No audit trail\n• Cannot execute actions\n• No authority boundaries", 16, BODY)
    add_rect(slide, 7.0, 1.5, 5.5, 5.0, CARD_BG, border=GREEN)
    add_text(slide, 7.2, 1.7, 5.0, 0.5, "TuntasUMKM Agent", 20, GREEN, True)
    add_text(slide, 7.2, 2.3, 5.0, 3.5, "• Tool-calling via MCP\n• Bounded business tools\n• Human-in-the-Loop gate\n• Full audit trail\n• Executes draft creation\n• Clear authority boundaries", 16, GREEN)
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
        elif layout == "architecture":
            arch_slide(prs, slide_spec)
        elif layout == "problem":
            problem_slide(prs, slide_spec)
        elif layout == "bounded_authority":
            bounded_authority_slide(prs, slide_spec)
        elif layout == "hitl":
            hitl_slide(prs, slide_spec)
        elif layout == "mcp_tools":
            mcp_tools_slide(prs, slide_spec)
        elif layout == "evidence":
            evidence_slide(prs, slide_spec)
        elif layout == "audit":
            audit_slide(prs, slide_spec)
        elif layout == "security":
            security_slide(prs, slide_spec)
        elif layout == "comparison":
            comparison_slide(prs, slide_spec)
        else:
            content_slide(prs, slide_spec)
    prs.save(output_path)
    print(json.dumps({"ok": True, "output": output_path, "slides": len(prs.slides._sldIdLst)}))

if __name__ == "__main__":
    import sys
    create_deck(sys.argv[1], sys.argv[2])
