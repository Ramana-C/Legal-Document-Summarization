from flask import Flask, render_template, request, redirect, url_for, jsonify
from summarizer import summarize_legal_text
from simplify import simplify_text
from utils import extract_text_from_pdf
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
0
@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    #plain_mode = request.form.get('plain_mode', 'false').lower() == 'true'
    plain_mode=False
    # Save and extract text
    filepath = os.path.join("temp", file.filename)
    os.makedirs("temp", exist_ok=True)
    file.save(filepath)

    try:
        # Debug: Check if the file is saved correctly
        print(f"File saved at {filepath}")
        
        text = extract_text_from_pdf(filepath)
        
        # Debug: Check if text extraction is working
        #print(text)
        if not text:
            return jsonify({'error': 'Text extraction failed or is empty.'}), 500
        
        #print("Extracted Text:", text)  # Print first 500 characters for debugging

        summary = summarize_legal_text(text)
        if plain_mode:
            summary = simplify_text(summary)
        
        # Debug: Check if summary generation is successful
        if not summary:
            return jsonify({'error': 'Summarization failed.'}), 500
        
        return render_template('results.html', summary=summary)
    
    except Exception as e:
        # Catch any errors
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(filepath)

if __name__ == '__main__':
    app.run(debug=True)
