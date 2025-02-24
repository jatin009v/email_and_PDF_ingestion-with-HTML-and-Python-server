from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import PyPDF2

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(filepath)
            return jsonify({"filename": file.filename, "text": text})
        else:
            return jsonify({"filename": file.filename, "text": "Email processing not implemented"})
    return jsonify({"error": "File upload failed"}), 500

def extract_text_from_pdf(filepath):
    with open(filepath, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ''
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extract_text()
    return text

if __name__ == '__main__':
    app.run(debug=True)