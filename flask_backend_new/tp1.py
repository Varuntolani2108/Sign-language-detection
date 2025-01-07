# install required modules
# !pip install Flask
# !pip install Flask-CORS
# !pip install Werkzeug
# !pip install torch
# !pip install transformers

# Import necessary modules
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import torch
from transformers import CLIPProcessor, CLIPModel

# Initialize the Flask app with the correct variable __name__
app = Flask(__name__)
CORS(app)

# Load the model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")  # Replace with your fine-tuned model
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

UPLOAD_FOLDER = r"/Users/karan/WebstormProjects/transformers-backend/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions for file uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to upload an image
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        res = { "filename": filename }
        return jsonify(res)

    return jsonify({"error": "Not a valid file type"}), 400

# Route to serve processed images
@app.route('/<filename>')
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Run the Flask app, using the correct variable __name__
if __name__ == '__main__':
    app.run(debug=True)