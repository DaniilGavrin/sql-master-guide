import re

# Чтение Markdown файла
with open('to_print/sql_master_guide_content.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Чтение HTML шаблона
with open('to_print/template.html', 'r', encoding='utf-8') as f:
    html_template = f.read()

# Конвертация Markdown в HTML (упрощенная)
def md_to_html(md):
    lines = md.split('\n')
    html_lines = []
    in_code_block = False
    in_list = False
    list_type = None
    
    for line in lines:
        # Code blocks
        if line.startswith('```'):
            if in_code_block:
                html_lines.append('</code></pre>')
                in_code_block = False
            else:
                html_lines.append('<pre><code>')
                in_code_block = True
            continue
        
        if in_code_block:
            html_lines.append(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
            continue
            
        # Headers
        if line.startswith('## '):
            if in_list:
                html_lines.append('</ul>' if list_type == 'ul' else '</ol>')
                in_list = False
            html_lines.append(f'<h2>{line[3:]}</h2>')
            continue
        elif line.startswith('### '):
            if in_list:
                html_lines.append('</ul>' if list_type == 'ul' else '</ol>')
                in_list = False
            html_lines.append(f'<h3>{line[4:]}</h3>')
            continue
        elif line.startswith('#### '):
            if in_list:
                html_lines.append('</ul>' if list_type == 'ul' else '</ol>')
                in_list = False
            html_lines.append(f'<h4>{line[5:]}</h4>')
            continue
            
        # Lists
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list or list_type != 'ul':
                if in_list:
                    html_lines.append('</ol>' if list_type == 'ol' else '</ul>')
                html_lines.append('<ul>')
                in_list = True
                list_type = 'ul'
            item = line.strip()[2:]
            html_lines.append(f'<li>{item}</li>')
            continue
        elif re.match(r'^\d+\.\s', line.strip()):
            if not in_list or list_type != 'ol':
                if in_list:
                    html_lines.append('</ul>' if list_type == 'ul' else '</ol>')
                html_lines.append('<ol>')
                in_list = True
                list_type = 'ol'
            item = re.sub(r'^\d+\.\s', '', line.strip())
            html_lines.append(f'<li>{item}</li>')
            continue
        else:
            if in_list:
                html_lines.append('</ul>' if list_type == 'ul' else '</ol>')
                in_list = False
            
            # Tables
            if '|' in line and line.strip().startswith('|'):
                cells = [c.strip() for c in line.split('|')[1:-1]]
                if '---' in line:
                    continue  # Skip separator line
                if line.strip().startswith('|---'):
                    continue
                row_type = 'th' if any(c.startswith('**') and c.endswith('**') for c in cells) or len(html_lines) > 0 and '<h2>' in ''.join(html_lines[-5:]) else 'td'
                row_html = ''.join([f'<{row_type}>{c.replace("**", "")}</{row_type}>' for c in cells])
                html_lines.append(f'<tr>{row_html}</tr>')
                continue
            
            # Bold and Code
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'`(.*?)`', r'<code>\1</code>', line)
            
            # Warnings and Tips
            if line.startswith('> **WARNING**') or line.startswith('> ⚠️'):
                html_lines.append(f'<div class="warning">{line.replace("> **WARNING**:", "").replace("> ⚠️ ", "")}</div>')
                continue
            elif line.startswith('> **TIP**') or line.startswith('> 💡'):
                html_lines.append(f'<div class="tip">{line.replace("> **TIP**:", "").replace("> 💡 ", "")}</div>')
                continue
            elif line.startswith('>'):
                line = f'<em>{line[1:].strip()}</em>'
            
            if line.strip():
                html_lines.append(f'<p>{line}</p>')
    
    if in_list:
        html_lines.append('</ul>' if list_type == 'ul' else '</ol>')
    
    return '\n'.join(html_lines)

html_content = md_to_html(md_content)

# Замена плейсхолдера
final_html = html_template.replace('{{ content }}', html_content)

# Сохранение HTML
with open('to_print/sql_master_guide.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("HTML файл успешно сгенерирован!")
print("Теперь запускаем WeasyPrint для создания PDF...")

# Генерация PDF через weasyprint
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

font_config = FontConfiguration()
css = CSS(string='''
    @page { size: A4; margin: 2cm }
    body { font-family: Arial; font-size: 10pt }
    h2 { font-size: 12pt; text-align: center; font-weight: bold }
    h3 { font-size: 11pt; font-weight: bold }
''', font_config=font_config)

HTML(filename='to_print/sql_master_guide.html').write_pdf('to_print/sql_master_guide.pdf', stylesheets=[css], font_config=font_config)

print("PDF файл успешно создан: to_print/sql_master_guide.pdf")
