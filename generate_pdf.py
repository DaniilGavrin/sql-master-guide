#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_NAME = 'Helvetica'
BOLD_FONT_NAME = 'Helvetica-Bold'

def register_fonts():
    global FONT_NAME, BOLD_FONT_NAME
    paths = ['/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    bold_paths = ['/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
    for p in paths:
        if os.path.exists(p):
            try:
                pdfmetrics.registerFont(TTFont('CustomFont', p))
                FONT_NAME = 'CustomFont'
                print(f"Found font: {p}")
                break
            except: pass
    for p in bold_paths:
        if os.path.exists(p):
            try:
                pdfmetrics.registerFont(TTFont('CustomFontBold', p))
                BOLD_FONT_NAME = 'CustomFontBold'
                print(f"Found bold font: {p}")
                break
            except: pass

def parse_md(content):
    lines = content.split('\n')
    elements = []
    code_block = []
    in_code = False
    styles = getSampleStyleSheet()
    
    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName=BOLD_FONT_NAME, fontSize=12, alignment=TA_CENTER, spaceAfter=14, leading=14)
    h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName=BOLD_FONT_NAME, fontSize=11, alignment=TA_CENTER, spaceAfter=12, leading=13)
    h3 = ParagraphStyle('H3', parent=styles['Heading3'], fontName=BOLD_FONT_NAME, fontSize=10, alignment=TA_LEFT, spaceAfter=8, leading=12)
    normal = ParagraphStyle('N', parent=styles['Normal'], fontName=FONT_NAME, fontSize=10, alignment=TA_LEFT, spaceAfter=6, leading=12)
    code_style = ParagraphStyle('C', parent=styles['Normal'], fontName='Courier', fontSize=9, textColor=colors.darkblue, leftIndent=10, rightIndent=10, backColor=colors.Color(0.95,0.95,0.95), leading=11)
    sep = ParagraphStyle('S', parent=styles['Normal'], fontName=FONT_NAME, fontSize=8, alignment=TA_CENTER, textColor=colors.gray, spaceAfter=10, spaceBefore=10)

    for line in lines:
        if line.startswith('```'):
            if in_code:
                txt = '\n'.join(code_block).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
                elements.append(Preformatted(txt, code_style))
                elements.append(Spacer(1, 0.15*cm))
                code_block = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_block.append(line)
            continue
        if not line.strip():
            elements.append(Spacer(1, 0.1*cm))
            continue
        if line.strip() == '---':
            elements.append(Paragraph('─'*50, sep))
            elements.append(Spacer(1, 0.2*cm))
            continue
        if line.startswith('# '):
            t = line[2:].strip().replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            elements.append(Paragraph(t, h1))
            elements.append(Spacer(1, 0.2*cm))
        elif line.startswith('## '):
            t = line[3:].strip().replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            elements.append(Paragraph(t, h2))
        elif line.startswith('### '):
            t = line[4:].strip().replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            elements.append(Paragraph(t, h3))
        else:
            t = line.strip().replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
            if t: elements.append(Paragraph(t, normal))
    return elements

def create_pdf(inp, out):
    register_fonts()
    with open(inp, 'r', encoding='utf-8') as f: content = f.read()
    elems = parse_md(content)
    doc = SimpleDocTemplate(out, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
    doc.build(elems)
    print(f"OK: {out} ({os.path.getsize(out)/1024:.1f} KB)")

if __name__ == "__main__":
    create_pdf("to_print/sql_full_cheatsheet.md", "to_print/sql_master_guide.pdf")
