import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm
from reportlab.lib import colors
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed

app = FastAPI(title="Local Label Printing API")

# ------------------------------
# Pydantic models
# ------------------------------
class LabelItem(BaseModel):
    title: str
    price_original: str
    barcode: str
    price_sale: str = "1.000.000 so'm"
    logo_path: str = "logo.png"
    slogan: str = "CIHEVO - Italian"

class LabelRequest(BaseModel):
    items: List[LabelItem]

# ------------------------------
# PDF generation function
# ------------------------------
def generate_label_pdf(label: LabelItem, pdf_file: str):
    """Generate a single PDF label"""
    c = canvas.Canvas(pdf_file, pagesize=(40*mm, 30*mm))

    # Background
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, 40*mm, 30*mm, fill=1, stroke=0)

    # Logo
    logo_width = 20*mm
    logo_height = 12*mm
    try:
        c.drawImage(
            label.logo_path,
            (40*mm - logo_width)/2,
            30*mm - logo_height + 3,
            width=logo_width,
            height=logo_height,
            preserveAspectRatio=True,
            mask='auto'
        )
    except:
        pass  # skip if logo not found

    # Product Name
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(40*mm / 2, 30*mm - logo_height + 5, label.title)

    # Original Price
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.gray)
    c.drawCentredString(40*mm / 2, 30*mm - logo_height - mm, label.price_original)

    # Sale Price
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.red)
    c.drawCentredString(40*mm / 2, 30*mm - logo_height - 5*mm, label.price_sale)

    # Barcode
    barcode_obj = code128.Code128(label.barcode, barHeight=6*mm, barWidth=0.25*mm)
    x_barcode = (40*mm - barcode_obj.width) / 2
    y_barcode = 5.5*mm
    barcode_obj.drawOn(c, x_barcode, y_barcode)

    # Barcode number
    c.setFont("Helvetica", 6)
    c.setFillColor(colors.black)
    c.drawCentredString(40*mm / 2, y_barcode - 6, label.barcode)

    # Slogan/footer
    c.setFont("Helvetica", 5)
    c.setFillColor(colors.gray)
    c.drawCentredString(40*mm / 2, 1*mm, label.slogan)

    c.showPage()
    c.save()

# ------------------------------
# Print helper
# ------------------------------
def print_pdfs(pdf_paths: List[str]):
    if os.name == 'nt':  # Windows
        for pdf in pdf_paths:
            os.startfile(pdf, "print")
    elif os.name == 'posix':  # Linux/macOS
        # Print all PDFs in one command
        os.system(f"lp {' '.join(pdf_paths)}")

# ------------------------------
# API Endpoint
# ------------------------------
@app.post("/print-labels/")
async def print_labels(request: LabelRequest):
    temp_files = []

    try:
        # Step 1: Generate all PDFs asynchronously
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for item in request.items:
                tmp_pdf = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
                tmp_pdf.close()  # Close file so ReportLab can write
                temp_files.append(tmp_pdf.name)
                futures.append(executor.submit(generate_label_pdf, item, tmp_pdf.name))

            # Wait for all PDFs to be generated
            for f in as_completed(futures):
                f.result()

        # Step 2: Print all PDFs in one batch
        print_pdfs(temp_files)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Step 3: Delete temporary files
        for f in temp_files:
            try:
                os.remove(f)
            except:
                pass

    return {"status": "printed", "count": len(request.items)}
