from flask import Flask, request, send_file, render_template
import os
import uuid
from pdf2docx import Converter

app = Flask(__name__)

# Upload folder (created at runtime)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# Word → PDF (disabled for server)
@app.route("/word-to-pdf", methods=["POST"])
def word_to_pdf():
    return "Word → PDF conversion is not available on this server. Please try locally on Windows."

# PDF → Word
@app.route("/pdf-to-word", methods=["POST"])
def pdf_to_word():
    file = request.files.get("file")
    if not file or not file.filename.endswith(".pdf"):
        return "Please upload a valid PDF file."

    # Save uploaded PDF
    pdf_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.pdf")
    docx_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.docx")
    file.save(pdf_path)

    # Convert PDF to Word
    try:
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()
    except Exception as e:
        return f"Conversion failed: {str(e)}"

    return send_file(docx_path, as_attachment=True)

# Run app
if __name__ == "__main__":
    app.run()
