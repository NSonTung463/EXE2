from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from fpdf import FPDF
import os

from app.features.test.service import CreateExam

create_exam = CreateExam()
router = APIRouter()

# Specify a directory where the PDF files will be saved
SAVE_DIR = "saved_pdfs"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)  # Create the directory if it doesn't exist

@router.post("/creat_exam")
def create_exam_endpoint(request: Request):
    # Run the exam creation logic
    res = create_exam.run()

    exam_data = res  # Extract only the data part

    # Generate the PDF file
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Set the width for the cell, e.g., 190 mm (the width of the page minus the margins)
    width = 190  # Adjust width as necessary

    # Add each line of the exam content to the PDF using multi_cell for text wrapping
    pdf.multi_cell(width, 10, txt=exam_data, align="L")

    # Define the file path to save the PDF
    pdf_file = os.path.join(SAVE_DIR, "exam_output.pdf")
    pdf.output(pdf_file)

    # Return the PDF file as a response
    response = FileResponse(
        pdf_file,
        media_type='application/pdf',
        filename="exam_output.pdf"
    )

    return response
