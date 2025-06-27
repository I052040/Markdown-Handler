# !pip install pdfplumber,pathlib,tqdm

import pdfplumber
from pathlib import Path
from tqdm import tqdm

def table_to_markdown(table):
    """
    Converts a 2D list table to Markdown table format
    """
    # skip empty tables
    if not table or not any(row for row in table):
        return None
    md = ""
    # Header
    header = table[0]
    md += "| " + " | ".join(str(h) if h is not None else "" for h in header) + " |\n"
    # Separator
    md += "| " + " | ".join("---" for _ in header) + " |\n"
    # Rows
    for row in table[1:]:
        md += "| " + " | ".join(str(cell) if cell is not None else "" for cell in row) + " |\n"
    return md

def pdf_to_markdown(pdf_path, markdown_path):
    with pdfplumber.open(pdf_path) as pdf:
        num_pages = len(pdf.pages)
        with markdown_path.open('w', encoding='utf-8') as md_file:
            with tqdm(total=num_pages, desc=f'Processing {pdf_path.name}', unit='page') as bar:
                for i, page in enumerate(pdf.pages):
                    page_content = []
                    
                    # Extract text content
                    text = page.extract_text()
                    if text:
                        page_content.append("## Extracted Text\n\n" + text)
                    
                    # Extract tables (as list of tables)
                    tables = page.extract_tables()
                    if tables:
                        for t_idx, table in enumerate(tables):
                            md_table = table_to_markdown(table)
                            if md_table:
                                page_content.append(f"## Table {t_idx + 1}\n\n{md_table}")
                    
                    if page_content:  # only write content if non-empty
                        md_file.write(f"# Page {i + 1}\n\n")
                        md_file.write('\n\n'.join(page_content))
                        md_file.write('\n\n')
                    bar.update(1)

def process_all_pdfs(input_dir, output_dir):
    input_dir_path = Path(input_dir)
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_dir_path.glob('*.pdf'))
    for pdf_file in pdf_files:
        markdown_file = output_dir_path / f'{pdf_file.stem}.md'
        pdf_to_markdown(pdf_file, markdown_file)
        if markdown_file.exists():
            print(f'Markdown file saved to {markdown_file}')

if __name__ == "__main__":
    input_directory = 'pdf_in'
    output_directory = 'md_out'
    process_all_pdfs(input_directory, output_directory)
