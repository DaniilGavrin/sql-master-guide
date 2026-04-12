#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор PDF шпаргалки для SQL Master Guide
Использует Liberation Sans (аналог Arial) для корректного отображения кириллицы
"""

import os
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Явные пути к шрифтам Liberation Sans (аналог Arial)
FONT_REGULAR = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
FONT_NAME = 'LiberationSans'

def register_fonts():
    """Регистрирует шрифты для использования в PDF"""
    try:
        # Проверяем существование файлов
        if not os.path.exists(FONT_REGULAR):
            raise FileNotFoundError(f"Шрифт не найден: {FONT_REGULAR}")
        if not os.path.exists(FONT_BOLD):
            raise FileNotFoundError(f"Шрифт не найден: {FONT_BOLD}")
        
        # Регистрируем шрифты
        pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_REGULAR))
        pdfmetrics.registerFont(TTFont(f'{FONT_NAME}-Bold', FONT_BOLD))
        
        print(f"✓ Шрифты успешно зарегистрированы:")
        print(f"  - {FONT_NAME} (Regular)")
        print(f"  - {FONT_NAME}-Bold")
        return True
    except Exception as e:
        print(f"✗ Ошибка регистрации шрифтов: {e}")
        print("  Используем встроенный Helvetica (кириллица может не отображаться)")
        return False

def parse_markdown(filepath):
    """
    Парсит Markdown файл и возвращает структурированные данные
    Возвращает список кортежей: (section_title, subsection_title, content_lines)
    """
    sections = []
    current_section = None
    current_subsection = None
    current_content = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    skip_next_toc = False
    
    for line in lines:
        line = line.rstrip()
        
        # Пропускаем главный заголовок
        if line.startswith('# SQL Master Guide'):
            continue
        
        # Пропускаем оглавление
        if line == 'Оглавление':
            skip_next_toc = True
            continue
        if skip_next_toc and (line.startswith('[') or line.strip() == '---'):
            continue
        if line.strip() == '---' and not current_section:
            continue
        
        # Заголовок раздела (##)
        if line.startswith('## '):
            # Сохраняем предыдущий раздел
            if current_section is not None:
                sections.append((current_section, current_subsection, current_content))
            
            current_section = line[3:]
            current_subsection = None
            current_content = []
            continue
        
        # Подзаголовок (###)
        if line.startswith('### '):
            # Сохраняем предыдущий подраздел
            if current_section and current_content:
                sections.append((current_section, current_subsection, current_content))
                current_content = []
            
            current_subsection = line[4:]
            continue
        
        # Добавляем контент в текущий раздел
        if current_section is not None:
            current_content.append(line)
    
    # Добавляем последний раздел
    if current_section:
        sections.append((current_section, current_subsection, current_content))
    
    return sections

def create_table_from_lines(lines):
    """Создает таблицу из списка строк (команда + описание)"""
    data = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Разделяем по табуляции или множественным пробелам (2+)
        parts = line.split('\t')
        if len(parts) < 2:
            parts = re.split(r'\s{2,}', line)
        
        if len(parts) >= 2:
            cmd = parts[0].strip().replace('`', '')
            desc = parts[1].strip()
            data.append([cmd, desc])
        elif len(parts) == 1 and parts[0]:
            data.append([parts[0].strip(), ''])
    
    if not data:
        return None
    
    # Создаем таблицу
    table = Table(data, colWidths=[4.5*cm, 11*cm], repeatRows=0)
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    
    return table

def process_content(content_lines, style_normal):
    """Обрабатывает строки контента и возвращает список элементов для PDF"""
    elements = []
    in_code_block = False
    code_lines = []
    
    for line in content_lines:
        stripped = line.strip()
        
        # Обработка блоков кода
        if stripped.startswith('```'):
            if in_code_block:
                # Конец блока кода
                if code_lines:
                    # Пытаемся создать таблицу если это список команд
                    is_table_like = any(
                        '\t' in cl or len(re.split(r'\s{2,}', cl)) >= 2 
                        for cl in code_lines if cl.strip()
                    )
                    
                    if is_table_like and len(code_lines) > 1:
                        table = create_table_from_lines(code_lines)
                        if table:
                            elements.append(table)
                            elements.append(Spacer(1, 0.3*cm))
                    else:
                        # Выводим как обычный текст
                        for code_line in code_lines:
                            if code_line.strip():
                                elements.append(Paragraph(code_line.strip(), style_normal))
                                elements.append(Spacer(1, 0.1*cm))
                
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
            continue
        
        if in_code_block:
            code_lines.append(stripped)
            continue
        
        # Пропускаем пустые строки
        if not stripped:
            continue
        
        # Форматируем строку
        formatted_text = stripped
        
        # Обрабатываем списки
        if stripped.startswith('- '):
            formatted_text = f"• {stripped[2:]}"
        
        # Обрабатываем жирный текст **text**
        formatted_text = formatted_text.replace('**', '<b>')
        
        # Создаем параграф
        try:
            p = Paragraph(formatted_text, style_normal)
            elements.append(p)
            elements.append(Spacer(1, 0.15*cm))
        except Exception as e:
            # Если ошибка, добавляем как есть
            elements.append(Paragraph(stripped, style_normal))
            elements.append(Spacer(1, 0.15*cm))
    
    return elements

def generate_pdf(input_md, output_pdf):
    """Генерирует PDF файл из Markdown"""
    
    # Регистрируем шрифты
    fonts_ok = register_fonts()
    font_name = FONT_NAME if fonts_ok else "Helvetica"
    font_bold = f"{font_name}-Bold" if fonts_ok else "Helvetica-Bold"
    
    # Создаем документ
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title="SQL Master Guide"
    )
    
    # Стили
    styles = getSampleStyleSheet()
    
    # Заголовок раздела: 12pt, жирный, по центру
    style_h1 = ParagraphStyle(
        'SectionTitle',
        parent=styles['Normal'],
        fontName=font_bold,
        fontSize=12,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceBefore=0.5*cm,
        spaceAfter=0.5*cm,
    )
    
    # Подзаголовок: 11pt, жирный, слева
    style_h2 = ParagraphStyle(
        'SubsectionTitle',
        parent=styles['Normal'],
        fontName=font_bold,
        fontSize=11,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceBefore=0.4*cm,
        spaceAfter=0.3*cm,
    )
    
    # Основной текст: 10pt
    style_normal = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        alignment=TA_LEFT,
        textColor=colors.black,
        leading=12,
        spaceAfter=0.1*cm,
    )
    
    # Парсим Markdown
    print(f"Чтение файла: {input_md}")
    sections = parse_markdown(input_md)
    print(f"Найдено разделов: {len(sections)}")
    
    # Формируем содержимое
    story = []
    first = True
    
    for section_title, subsection_title, content_lines in sections:
        # Разрыв страницы между разделами
        if not first:
            story.append(PageBreak())
        first = False
        
        # Заголовок раздела
        story.append(Paragraph(section_title, style_h1))
        
        # Подзаголовок (если есть)
        if subsection_title:
            story.append(Paragraph(subsection_title, style_h2))
        
        # Контент
        content_elements = process_content(content_lines, style_normal)
        story.extend(content_elements)
    
    # Собираем PDF
    doc.build(story)
    print(f"✓ PDF успешно создан: {output_pdf}")

if __name__ == "__main__":
    input_file = "to_print/sql_master_guide_content.md"
    output_file = "to_print/sql_master_guide.pdf"
    
    if not os.path.exists(input_file):
        print(f"✗ Ошибка: Файл {input_file} не найден")
        exit(1)
    
    generate_pdf(input_file, output_file)
