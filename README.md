# Research Portal – Financial Statement Extraction Tool

## Overview
This project implements a minimal research portal slice that extracts Income Statement line items from uploaded annual reports (PDF) and exports them into a structured Excel file for analyst use.

## Architecture

Upload PDF
→ Text Extraction (pdfplumber)
→ Regex-based Line Item Extraction
→ Normalization Mapping
→ Structured Data
→ Excel Export

## Design Decisions

- Used regex-based numeric extraction to prevent hallucinated financial values.
- Implemented normalization mapping for different line item names.
- Missing values are returned as null and appear as blank in Excel.
- Currency and reporting units are detected from document text.
- Year detection implemented using pattern matching.
- Excel output formatted for analyst readability.

## How to Run

1. Create virtual environment:
   python -m venv venv
   venv\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Run server:
   uvicorn main:app --reload

4. Open browser:
   http://127.0.0.1:8000/docs

5. Upload financial PDF via POST /upload/

## Output
An Excel file is generated:
outputs/income_statement.xlsx

The Excel file contains:
- Year
- Standardized income statement line items
- Currency
- Unit
- Confidence level
