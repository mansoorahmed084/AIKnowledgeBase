"""
Jupyter Notebook to HTML Converter
Converts a .ipynb notebook file to a readable HTML document with styling.
"""

import json
import html
import re
from pathlib import Path


def convert_notebook_to_html(notebook_path, output_path):
    """
    Convert a Jupyter notebook to HTML format with better markdown support.
    
    Args:
        notebook_path (str): Path to the input .ipynb file
        output_path (str): Path to the output .html file
    """
    
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Start building HTML
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Working with Different File Formats - Refresher Document</title>
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.7;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 4px solid #3498db;
            padding-bottom: 15px;
            margin-top: 40px;
            margin-bottom: 25px;
            font-size: 2.2em;
        }
        h2 {
            color: #34495e;
            margin-top: 35px;
            margin-bottom: 20px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 10px;
            font-size: 1.8em;
        }
        h3 {
            color: #555;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 1.4em;
        }
        h4 {
            color: #666;
            margin-top: 25px;
            margin-bottom: 12px;
            font-size: 1.2em;
        }
        code {
            background-color: #f4f4f4;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            color: #e74c3c;
        }
        pre {
            background-color: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 6px;
            overflow-x: auto;
            margin: 20px 0;
            border-left: 5px solid #3498db;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.5;
        }
        pre code {
            background-color: transparent;
            color: inherit;
            padding: 0;
            border: none;
        }
        .cell {
            margin: 25px 0;
            padding: 20px;
            border-radius: 6px;
            border-left: 5px solid;
        }
        .markdown-cell {
            background-color: #ffffff;
            border-left-color: #95a5a6;
        }
        .code-cell {
            background-color: #f8f9fa;
            border-left-color: #2ecc71;
        }
        .output-cell {
            background-color: #fffbf0;
            border-left: 5px solid #f39c12;
            margin-top: 15px;
            padding: 15px;
            font-size: 0.9em;
            border-radius: 4px;
        }
        .output-cell strong {
            display: block;
            margin-bottom: 10px;
            color: #d68910;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 25px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px 15px;
            text-align: left;
        }
        th {
            background-color: #3498db;
            color: white;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 0.5px;
        }
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        tr:hover {
            background-color: #e8f4f8;
        }
        .alert {
            padding: 18px;
            margin: 25px 0;
            border-radius: 6px;
            border-left: 5px solid;
        }
        .alert-info {
            background-color: #d1ecf1;
            border-color: #0c5460;
            color: #0c5460;
        }
        a {
            color: #3498db;
            text-decoration: none;
            border-bottom: 1px dotted #3498db;
        }
        a:hover {
            color: #2980b9;
            border-bottom: 1px solid #2980b9;
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 25px auto;
            border-radius: 6px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        ul, ol {
            margin: 15px 0;
            padding-left: 30px;
        }
        li {
            margin: 8px 0;
        }
        p {
            margin: 15px 0;
        }
        strong {
            color: #2c3e50;
            font-weight: 600;
        }
        .code-label {
            font-weight: 600;
            color: #27ae60;
            margin-bottom: 10px;
            display: block;
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .dataframe {
            width: 100%;
            margin: 20px 0;
        }
        @media print {
            body {
                background-color: white;
                padding: 0;
            }
            .container {
                box-shadow: none;
                padding: 20px;
            }
            .code-cell, .output-cell {
                page-break-inside: avoid;
            }
        }
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            .container {
                padding: 20px;
            }
            pre {
                font-size: 0.8em;
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
"""
    
    # Process each cell
    for idx, cell in enumerate(notebook['cells']):
        cell_type = cell['cell_type']
        
        if cell_type == 'markdown':
            source = ''.join(cell['source'])
            html_content += '<div class="cell markdown-cell">\n'
            html_content += convert_markdown_to_html(source)
            html_content += '</div>\n'
            
        elif cell_type == 'code':
            source = ''.join(cell['source'])
            html_content += '<div class="cell code-cell">\n'
            html_content += '<span class="code-label">Code:</span>\n'
            html_content += f'<pre><code>{html.escape(source)}</code></pre>\n'
            
            # Add outputs if any
            if 'outputs' in cell and cell['outputs']:
                html_content += '<div class="output-cell">\n<strong>Output:</strong>\n'
                for output in cell['outputs']:
                    output_type = output.get('output_type', '')
                    
                    if output_type == 'stream':
                        text = ''.join(output.get('text', []))
                        html_content += f'<pre style="background-color: #2d2d2d; color: #f8f8f2; padding: 10px; border-radius: 4px; margin: 10px 0;">{html.escape(text)}</pre>\n'
                    
                    elif output_type in ['execute_result', 'display_data']:
                        data = output.get('data', {})
                        
                        if 'text/html' in data:
                            # HTML output (like DataFrames)
                            html_content += '<div style="overflow-x: auto;">' + ''.join(data['text/html']) + '</div>\n'
                        elif 'text/plain' in data:
                            text = ''.join(data['text/plain'])
                            html_content += f'<pre style="background-color: #2d2d2d; color: #f8f8f2; padding: 10px; border-radius: 4px; margin: 10px 0;">{html.escape(text)}</pre>\n'
                    
                    elif output_type == 'error':
                        error_name = output.get('ename', 'Error')
                        error_value = ''.join(output.get('evalue', []))
                        html_content += f'<pre style="background-color: #ffe6e6; color: #c0392b; padding: 10px; border-radius: 4px; border-left: 4px solid #c0392b; margin: 10px 0;"><strong>{html.escape(error_name)}:</strong> {html.escape(error_value)}</pre>\n'
                
                html_content += '</div>\n'
            
            html_content += '</div>\n'
    
    html_content += """
    </div>
</body>
</html>
"""
    
    # Write HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Successfully converted notebook to HTML: {output_path}")


def convert_markdown_to_html(markdown_text):
    """
    Convert markdown text to HTML.
    
    Args:
        markdown_text (str): Markdown formatted text
        
    Returns:
        str: HTML formatted text
    """
    lines = markdown_text.split('\n')
    html_lines = []
    in_code_block = False
    code_block_content = []
    code_block_lang = ''
    in_list = False
    list_type = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Handle code blocks
        if stripped.startswith('```'):
            if in_code_block:
                # End code block
                lang_attr = f' class="language-{code_block_lang}"' if code_block_lang else ''
                html_lines.append(f'<pre><code{lang_attr}>{html.escape("".join(code_block_content))}</code></pre>')
                code_block_content = []
                code_block_lang = ''
                in_code_block = False
            else:
                # Start code block
                in_code_block = True
                code_block_lang = stripped.replace('```', '').strip()
        elif in_code_block:
            code_block_content.append(line + '\n')
        
        # Handle headers
        elif stripped.startswith('# '):
            if in_list:
                html_lines.append(f'</{list_type}>')
                in_list = False
            html_lines.append(f'<h1>{process_inline_markdown(stripped[2:])}</h1>')
        elif stripped.startswith('## '):
            if in_list:
                html_lines.append(f'</{list_type}>')
                in_list = False
            html_lines.append(f'<h2>{process_inline_markdown(stripped[3:])}</h2>')
        elif stripped.startswith('### '):
            if in_list:
                html_lines.append(f'</{list_type}>')
                in_list = False
            html_lines.append(f'<h3>{process_inline_markdown(stripped[4:])}</h3>')
        elif stripped.startswith('#### '):
            if in_list:
                html_lines.append(f'</{list_type}>')
                in_list = False
            html_lines.append(f'<h4>{process_inline_markdown(stripped[5:])}</h4>')
        
        # Handle lists
        elif stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
                list_type = 'ul'
            content = process_inline_markdown(stripped[2:])
            html_lines.append(f'<li>{content}</li>')
        elif re.match(r'^\d+\.\s', stripped):
            if not in_list or list_type != 'ol':
                if in_list:
                    html_lines.append(f'</{list_type}>')
                html_lines.append('<ol>')
                in_list = True
                list_type = 'ol'
            content = re.sub(r'^\d+\.\s', '', stripped)
            content = process_inline_markdown(content)
            html_lines.append(f'<li>{content}</li>')
        
        # Handle empty lines
        elif not stripped:
            if in_list:
                html_lines.append(f'</{list_type}>')
                in_list = False
            html_lines.append('<br>')
        
        # Handle HTML tags (pass through)
        elif '<' in line and '>' in line:
            html_lines.append(line)
        
        # Regular paragraph
        elif not in_code_block:
            processed = process_inline_markdown(line)
            if processed.strip():
                html_lines.append(f'<p>{processed}</p>')
        
        i += 1
    
    # Close any open list
    if in_list:
        html_lines.append(f'</{list_type}>')
    
    return '\n'.join(html_lines)


def process_inline_markdown(text):
    """
    Process inline markdown elements (bold, italic, code, links, images).
    
    Args:
        text (str): Text with inline markdown
        
    Returns:
        str: HTML formatted text
    """
    # Escape HTML first
    text = html.escape(text)
    
    # Bold (**text**)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Italic (*text*)
    text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', text)
    
    # Inline code (`code`)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # Links [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    
    # Images ![alt](url)
    text = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', r'<img src="\2" alt="\1">', text)
    
    return text


if __name__ == '__main__':
    import sys
    
    # Default paths
    if len(sys.argv) == 3:
        notebook_path = sys.argv[1]
        output_path = sys.argv[2]
    elif len(sys.argv) == 2:
        notebook_path = sys.argv[1]
        # Generate output path from input path
        input_path = Path(notebook_path)
        output_path = str(input_path.with_suffix('.html'))
    else:
        # Example usage
        notebook_path = r'c:\Users\IN009286\Downloads\PY0101EN-5 4_WorkingWithDifferent.ipynb'
        output_path = r'c:\temp\AI\WorkingWithDifferentFileFormats_Refresher.html'
    
    # Validate input file exists
    if not Path(notebook_path).exists():
        print(f"Error: Input file not found: {notebook_path}")
        sys.exit(1)
    
    # Convert notebook to HTML
    try:
        convert_notebook_to_html(notebook_path, output_path)
        print(f"\nConversion complete!")
        print(f"Input:  {notebook_path}")
        print(f"Output: {output_path}")
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)
