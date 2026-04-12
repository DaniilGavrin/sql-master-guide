import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Настройка шрифтов
FONT_NAME = 'Arial'
# Пытаемся найти шрифт Arial в системе
def find_arial_font():
    paths_to_check = [
        '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf', # Аналог Arial в Linux
        '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf',
        '/usr/share/fonts/TTF/DejaVuSans.ttf',
        '/Library/Fonts/Arial.ttf', # macOS
        'C:/Windows/Fonts/arial.ttf', # Windows
        './arial.ttf' # Локально
    ]
    for path in paths_to_check:
        if os.path.exists(path):
            return path
    return None

font_path = find_arial_font()
if font_path:
    try:
        pdfmetrics.registerFont(TTFont(FONT_NAME, font_path))
        print(f"Шрифт найден: {font_path}")
    except Exception as e:
        print(f"Ошибка регистрации шрифта: {e}")
        FONT_NAME = 'Helvetica' # Fallback
else:
    print("Шрифт Arial не найден, используем Helvetica")
    FONT_NAME = 'Helvetica'

def create_pdf(input_md, output_pdf):
    doc = SimpleDocTemplate(
        output_pdf, 
        pagesize=A4,
        rightMargin=1.5*cm, 
        leftMargin=1.5*cm,
        topMargin=1.5*cm, 
        bottomMargin=1.5*cm
    )
    
    styles = getSampleStyleSheet()
    
    # Стили согласно требованиям
    # Заголовки (##): 12 кегль, по центру, жирный
    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName=f"{FONT_NAME}-Bold",
        fontSize=12,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceAfter=14,
        spaceBefore=14,
        leading=14
    )
    
    # Подзаголовки (###): 11 кегль, по центру, жирный
    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName=f"{FONT_NAME}-Bold",
        fontSize=11,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceAfter=10,
        spaceBefore=10,
        leading=13
    )
    
    # Основной текст: 10 кегль, слева
    style_normal = ParagraphStyle(
        'Normal_Custom',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=10,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceAfter=4,
        leading=12
    )
    
    # Стиль для разделителей
    style_sep = ParagraphStyle(
        'Separator',
        parent=style_normal,
        alignment=TA_CENTER,
        fontSize=8,
        spaceAfter=8,
        spaceBefore=8,
        textColor=colors.gray
    )

    story = []
    
    try:
        with open(input_md, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Файл {input_md} не найден!")
        return

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            story.append(Spacer(1, 0.2*cm))
            continue
        
        # Обработка заголовков
        if line_stripped.startswith('# '):
            # Главный заголовок файла (игнорируем или делаем большим)
            text = line_stripped[2:]
            p_style = ParagraphStyle('Title', parent=style_h1, fontSize=16, spaceAfter=20)
            story.append(Paragraph(text, p_style))
            story.append(PageBreak())
        elif line_stripped.startswith('## '):
            text = line_stripped[3:]
            story.append(Paragraph(text, style_h1))
        elif line_stripped.startswith('### '):
            text = line_stripped[4:]
            story.append(Paragraph(text, style_h2))
        elif line_stripped.startswith('---'):
            story.append(Paragraph('• • •', style_sep))
            story.append(Spacer(1, 0.3*cm))
        else:
            # Обычный текст
            # Убираем символы форматирования markdown, так как они ломают HTML парсер
            # Заменяем ** и * на пустоту или просто оставляем текст чистым
            formatted_line = line_stripped.replace('**', '').replace('*', '')
            # Экранируем специальные HTML символы если они есть
            formatted_line = formatted_line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            story.append(Paragraph(formatted_line, style_normal))

    doc.build(story)
    print(f"PDF успешно создан: {output_pdf}")

if __name__ == "__main__":
    input_file = "to_print/sql_full_cheatsheet.md"
    output_file = "to_print/sql_master_guide.pdf"
    
    if os.path.exists(input_file):
        create_pdf(input_file, output_file)
    else:
        print(f"Ошибка: Файл {input_file} не найден.")
