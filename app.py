import os
from dotenv import load_dotenv
import hashlib
from flask import Flask, request, render_template, flash, redirect, url_for, jsonify, send_from_directory
import pandas as pd
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching
app.secret_key = os.environ['SECRET_KEY']

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Maximum file size: 16 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def pseudonymize(data, column):
    data[column] = data[column].apply(lambda x: hashlib.sha256(str(x).encode('utf-8')).hexdigest())

def redact(data, column):
    data[column] = 'REDACTED'

def reidentification_risk_score(data):
    # Calculate risk score using your preferred method or library
    # This example returns a placeholder value
    return 'low'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    try:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            
            if file and allowed_file(file.filename):
                filepath = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(filepath)
                data = pd.read_csv(filepath) if filepath.endswith('.csv') else pd.read_excel(filepath)
                columns = list(data.columns)
                return render_template('index.html', columns=columns, risk_score=reidentification_risk_score(data), filepath=filepath)
        return render_template('index.html')
        logging.info("Handling file upload")
    except Exception as e:
        logging.error(f"Error handling file upload: {e}")
        flash("An error occurred during file processing.")
        return redirect(request.url)

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    try:
        return send_from_directory(directory=UPLOAD_FOLDER, path=filename, as_attachment=True)
    except Exception as e:
        # Log the error or print more detailed error information
        print(f"Failed to send file: {e}")
        # Log the error or print more detailed error information
        print(f"Failed to send file: {e}")
        return f"Error: {e}"

@app.route('/anonymize', methods=['POST'])
def anonymize():
    actions = request.form.to_dict()
    filename = actions.pop('filename')
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    data = pd.read_csv(filepath) if filepath.endswith('.csv') else pd.read_excel(filepath)
    
    for column, action in actions.items():
        if action == 'pseudonymize':
            pseudonymize(data, column)
        elif action == 'redact':
            redact(data, column)
        elif action == 'remove':
            data.drop(column, axis=1, inplace=True)
    
    # Save the anonymized data to a new file
    anonymized_filename = f"anonymized_{os.path.basename(filename)}"
    anonymized_filepath = os.path.join(UPLOAD_FOLDER, anonymized_filename)

    if anonymized_filepath.endswith('.csv'):
        data.to_csv(anonymized_filepath, index=False)
    else:
        data.to_excel(anonymized_filepath, index=False)
    
    flash(f"Anonymized data saved to {anonymized_filepath}")

    # Instead of redirecting, return JSON with the necessary data:
    return jsonify({
        'risk_score': reidentification_risk_score(data),
        'filepath': anonymized_filename  # Send just the filename for URL creation
    })
    # Redirect to the download route
    #return redirect(url_for('download', filename=anonymized_filename))

if __name__ == '__main__':
    app.run(debug=True)