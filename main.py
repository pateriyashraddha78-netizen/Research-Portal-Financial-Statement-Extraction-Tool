from fastapi import FastAPI, UploadFile, File
import pandas as pd
import os
from extractor import extract_text, extract_income_statement
from openpyxl.styles import Font

app = FastAPI(title="Research Portal - Financial Statement Extraction")

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    contents = await file.read()

    temp_path = "temp.pdf"
    with open(temp_path, "wb") as f:
        f.write(contents)

    text = extract_text(temp_path)
    extracted = extract_income_statement(text)

    df = pd.DataFrame([extracted["data"]])
    df["Year"] = extracted["year"]
    df["Currency"] = extracted["currency"]
    df["Unit"] = extracted["unit"]
    df["Confidence"] = extracted["confidence"]

    output_path = os.path.join(OUTPUT_DIR, "income_statement.xlsx")

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Income Statement")
        sheet = writer.sheets["Income Statement"]

        # Bold header
        for cell in sheet[1]:
            cell.font = Font(bold=True)

    return {
        "message": "Excel generated successfully",
        "file_path": output_path
    }