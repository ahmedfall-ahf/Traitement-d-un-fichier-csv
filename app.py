from flask import Flask, render_template, request, send_from_directory
import os
from cleaning import process_csv
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', cleaned=None)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        try:
            cleaned_file_path = process_csv(filepath, filename)
            cleaned_filename = os.path.basename(cleaned_file_path)
            return render_template('index.html', cleaned=cleaned_filename)
        except ValueError as e:
            return render_template('index.html', cleaned=None, error=str(e))

    return render_template('index.html', cleaned=None, error="Aucun fichier reçu.")

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
