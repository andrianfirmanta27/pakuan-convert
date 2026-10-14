from flask import Flask, render_template, request, send_file, flash
import os, uuid
from pdf2docx import Converter
from werkzeug.utils import secure_filename

app = Flask(_name_)
app.secret_key = 'pakuan-2026'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        try:
            uid = str(uuid.uuid4())[:8]
            pdf_path = os.path.join(UPLOAD_FOLDER, f"{uid}_{secure_filename(file.filename)}")
            docx_path = pdf_path.replace('.pdf', '.docx')
            file.save(pdf_path)
            cv = Converter(pdf_path)
            cv.convert(docx_path)
            cv.close()
            os.remove(pdf_path)
            return send_file(docx_path, as_attachment=True)
        except Exception as e:
            flash(f'Gagal: {e}')
            return render_template('index.html')
    return render_template('index.html')

if _name_ == '_main_':
    app.run(debug=True)