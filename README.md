# PDF to Markdown Extractor

A Python tool to extract both **narrative text** ** andtable/grid content** from PDF files and save them in well-formatted Markdown files.

This script uses [`pdfplumber`](https://github.com/jsvine/pdfplumber) for PDF parsing and [`tqdm`](https://github.com/tqdm/tqdm) for progress display.  
It works on all PDFs in a given `input` directory, saving Markdown results to a chosen `output` folder.

---

## Features

- Extracts regular text and all table/grid data from each page
- Converts tables to Markdown table syntax
- Handles pages with only text, only tables, or both
- Works in batch on all PDFs in a folder

---

## Installation

```sh
pip install pdfplumber pathlib tqdm
