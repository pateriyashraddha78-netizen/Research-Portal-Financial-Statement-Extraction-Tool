import re
import pdfplumber

STANDARD_ITEMS = {
    "Revenue": ["Revenue", "Total Sales", "Net Sales"],
    "Cost_of_Revenue": ["Cost of Revenue", "Cost of Sales"],
    "Gross_Profit": ["Gross Profit"],
    "Operating_Expenses": ["Operating Expenses", "Operating Costs"],
    "Operating_Income": ["Operating Income", "EBIT"],
    "Net_Income": ["Net Income", "Profit After Tax"],
    "EBITDA": ["EBITDA"],
    "EPS": ["Earnings Per Share", "EPS"]
}

def extract_text(file_path):
    with pdfplumber.open(file_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def detect_currency_unit(text):
    currency = None
    unit = None

    if "USD" in text:
        currency = "USD"
    elif "INR" in text:
        currency = "INR"
    elif "EUR" in text:
        currency = "EUR"

    if "millions" in text.lower():
        unit = "millions"
    elif "thousands" in text.lower():
        unit = "thousands"
    elif "billions" in text.lower():
        unit = "billions"

    return currency, unit

def detect_year(text):
    match = re.search(r"(20\d{2})", text)
    return match.group(1) if match else "Unknown"

def extract_income_statement(text):
    result = {}
    currency, unit = detect_currency_unit(text)
    year = detect_year(text)

    for standard_name, variations in STANDARD_ITEMS.items():
        value = None
        for variation in variations:
            pattern = rf"{variation}.*?(\d{{1,3}}(?:,\d{{3}})*(?:\.\d+)?)"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1)
                break

        result[standard_name] = value if value else None

    return {
        "currency": currency,
        "unit": unit,
        "year": year,
        "confidence": "medium",
        "data": result
    }