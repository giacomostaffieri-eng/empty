from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
import io, sys

def stamp(path, label):
    r = PdfReader(path); n = len(r.pages); w = PdfWriter()
    for i, page in enumerate(r.pages):
        if i > 0:
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=A4)
            c.setStrokeColor(HexColor("#DFE6EC")); c.setLineWidth(0.5)
            c.line(14*mm, 11.5*mm, A4[0]-14*mm, 11.5*mm)
            c.setFont("Helvetica", 6.4); c.setFillColor(HexColor("#66788A"))
            c.drawString(14*mm, 8.6*mm, label)
            c.setFont("Helvetica-Bold", 6.4); c.setFillColor(HexColor("#0B2545"))
            c.drawRightString(A4[0]-14*mm, 8.6*mm, f"Page {i+1} of {n}")
            c.save(); buf.seek(0)
            page.merge_page(PdfReader(buf).pages[0])
        w.add_page(page)
    with open(path, "wb") as f: w.write(f)
    print(f"{path}: {n} pages")

stamp("/home/user/empty/Fungies_io_Master_Brief.pdf",
      "Fungies.io - Master Opportunity, Compliance & Risk Brief  |  CONFIDENTIAL - Internal Checkout.com use only")
stamp("/home/user/empty/Fungies_io_Prevet_Form.pdf",
      "Pre-vet Form for Direct Sellers - Fungies Inc.  |  CONFIDENTIAL - Internal Checkout.com use only")
