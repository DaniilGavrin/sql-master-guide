import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def register_font():
    font_name = 'Arial'
    font_path = 'arial.ttf'
    bold_path = 'arial-bold.ttf'
    
    try:
        # Попытка найти шрифт в системных путях
        import platform
        system = platform.system()
        if system == "Windows":
            font_path = r"C:\Windows\Fonts\arial.ttf"
            bold_path = r"C:\Windows\Fonts\arialbd.ttf"
        elif system == "Darwin":
            font_path = "/Library/Fonts/Arial.ttf"
            bold_path = "/Library/Fonts/Arial-Bold.ttf"
        else:
            # Linux - используем Liberation Sans как аналог Arial
            font_path = "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
            bold_path = "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
        
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('Arial', font_path))
            if os.path.exists(bold_path):
                pdfmetrics.registerFont(TTFont('Arial-Bold', bold_path))
            else:
                pdfmetrics.registerFont(TTFont('Arial-Bold', font_path))
            return 'Arial'
        else:
            print("Шрифт не найден, используем встроенный Helvetica")
            return 'Helvetica'
    except Exception as e:
        print(f"Ошибка при регистрации шрифта: {e}")
        return 'Helvetica'

def create_pdf(input_md, output_pdf):
    font_family = register_font()
    font_bold = f'{font_family}-Bold' if font_family == 'Arial' else 'Helvetica-Bold'
    
    doc = SimpleDocTemplate(output_pdf, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    
    styles = getSampleStyleSheet()
    
    # Заголовки H1: 12 кегль, по центру, жирный
    style_h1 = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontName=font_bold,
        fontSize=12,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceAfter=15,
        spaceBefore=15
    )
    
    # Заголовки H2: 11 кегль, по центру, жирный
    style_h2 = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontName=font_bold,
        fontSize=11,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Заголовки H3: 10 кегль, слева, жирный
    style_h3 = ParagraphStyle(
        'Heading3',
        parent=styles['Normal'],
        fontName=font_bold,
        fontSize=10,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceAfter=8,
        spaceBefore=10
    )
    
    # Основной текст: 10 кегль, слева
    style_normal = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontName=font_family,
        fontSize=10,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceAfter=6,
        leading=12
    )
    
    # Текст кода: моноширинный
    style_code = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=9,
        alignment=TA_LEFT,
        textColor=colors.darkgrey,
        spaceAfter=8,
        leading=11
    )
    
    story = []
    in_code_block = False
    code_content = []
    
    try:
        with open(input_md, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Файл {input_md} не найден!")
        return

    for line in lines:
        line_stripped = line.strip()
        
        # Обработка блоков кода
        if line_stripped.startswith('```'):
            if in_code_block:
                for code_line in code_content:
                    story.append(Paragraph(code_line, style_code))
                code_content = []
                in_code_block = False
            else:
                in_code_block = True
            continue
        
        if in_code_block:
            code_content.append(line_stripped)
            continue
        
        # Пропуск пустых строк
        if not line_stripped:
            story.append(Spacer(1, 0.2*cm))
            continue
        
        # Обработка заголовков
        if line_stripped.startswith('# '):
            story.append(Paragraph(line_stripped[2:], style_h1))
            story.append(Spacer(1, 0.3*cm))
        elif line_stripped.startswith('## '):
            story.append(Paragraph(line_stripped[3:], style_h2))
            story.append(Spacer(1, 0.2*cm))
        elif line_stripped.startswith('### '):
            story.append(Paragraph(line_stripped[4:], style_h3))
        elif line_stripped.startswith('- '):
            story.append(Paragraph(f"• {line_stripped[2:]}", style_normal))
        elif line_stripped.startswith('|'):
            # Обработка таблиц
            if '|---' in line_stripped:
                continue
            cells = [cell.strip() for cell in line_stripped.split('|') if cell.strip()]
            if len(cells) >= 2:
                table = Table([cells], colWidths=[4*cm, 8*cm])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), font_family),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
                ]))
                story.append(table)
                story.append(Spacer(1, 0.1*cm))
        else:
            story.append(Paragraph(line_stripped, style_normal))
    
    doc.build(story)
    print(f"PDF успешно создан: {output_pdf}")

if __name__ == "__main__":
    input_file = "sql_master_guide_content.md"
    output_file = "sql_master_guide.pdf"
    
    if os.path.exists(input_file):
        create_pdf(input_file, output_file)
    else:
        print(f"Ошибка: Файл {input_file} не найден.")
