import markdown
from weasyprint import HTML, CSS
import os

# Читаем Markdown
with open('to_print/sql_master_guide_content.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Конвертируем в HTML
html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'toc'])

# Полный HTML шаблон с ИСПРАВЛЕННЫМИ стилями
full_html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>SQL Master Guide - Памятка</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        body {{
            font-family: Arial, sans-serif;
            font-size: 10pt;
            line-height: 1.4;
            color: #000000;
        }}
        h1 {{
            font-size: 14pt;
            text-align: center;
            font-weight: bold;
            color: #000000;
            page-break-after: avoid;
            margin-bottom: 20px;
        }}
        h2 {{
            font-size: 12pt;
            text-align: center;
            font-weight: bold;
            color: #000000;
            page-break-after: avoid;
            margin-top: 24px;
            margin-bottom: 12px;
            border-bottom: 1px solid #000;
            padding-bottom: 5px;
        }}
        h3 {{
            font-size: 11pt;
            text-align: left;
            font-weight: bold;
            color: #000000;
            page-break-after: avoid;
            margin-top: 18px;
            margin-bottom: 8px;
        }}
        h4 {{
            font-size: 10pt;
            font-weight: bold;
            color: #000000;
            margin-top: 12px;
            margin-bottom: 6px;
        }}
        p {{
            margin-bottom: 8px;
            text-align: justify;
        }}
        ul, ol {{
            margin-bottom: 8px;
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 4px;
        }}
        code {{
            font-family: 'Courier New', Courier, monospace;
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-size: 9pt;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 9pt;
            border: 1px solid #ddd;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
            font-size: 9pt;
        }}
        th, td {{
            border: 1px solid #000;
            padding: 6px;
            text-align: left;
        }}
        th {{
            background-color: #e0e0e0;
            font-weight: bold;
            text-align: center;
        }}
        blockquote {{
            border-left: 4px solid #000;
            margin: 10px 0;
            padding-left: 15px;
            font-style: italic;
            background-color: #f9f9f9;
        }}
        .toc {{
            page-break-after: always;
        }}
    </style>
</head>
<body>
    <h1>SQL MASTER GUIDE<br><span style="font-size:10pt; font-weight:normal;">Полная памятка для печати</span></h1>
    <div class="toc">
        <h2>ОГЛАВЛЕНИЕ</h2>
        {markdown.markdown("[TOC]", extensions=['toc'])} 
        <!-- Оглавление генерируется автоматически внутри body при наличии маркера, но здесь мы упростим -->
    </div>
    {html_body}
</body>
</html>
"""

# Сохраняем промежуточный HTML для проверки
with open('to_print/sql_master_guide.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

# Генерируем PDF
html_obj = HTML(string=full_html, base_url='.')
html_obj.write_pdf('to_print/sql_master_guide.pdf')

print("✅ PDF успешно сгенерирован с исправленными стилями!")
