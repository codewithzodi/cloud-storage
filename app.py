import os
import logging
from flask import Flask, request, send_from_directory, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
import zipfile
import io

# Configure the storage directory
STORAGE_DIR = os.path.abspath("cloud_storage")

# Ensure the storage directory exists
os.makedirs(STORAGE_DIR, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = STORAGE_DIR
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB limit

# Allowed extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'csv', 'docx', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable CORS
CORS(app)

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
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    filename = secure_filename(file.filename)
    file_path = os.path.join(STORAGE_DIR, filename)
    try:
        file.save(file_path)
        logger.info(f"File uploaded: {filename}")
        return jsonify({"message": "File uploaded successfully", "filename": filename}), 200
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return jsonify({"error": "File upload failed"}), 500

@app.route('/download_file', methods=['GET'])
def download_file():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"error": "No filename provided"}), 400
    try:
        filename = secure_filename(filename)
        return send_from_directory(STORAGE_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        logger.warning(f"File not found: {filename}")
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        return jsonify({"error": "Download failed"}), 500

@app.route('/list', methods=['GET'])
def list_files():
    try:
        files = os.listdir(STORAGE_DIR)
        return jsonify({"files": files}), 200
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        return jsonify({"error": "Failed to retrieve file list"}), 500

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    filename = secure_filename(filename)
    file_path = os.path.join(STORAGE_DIR, filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            logger.info(f"File deleted: {filename}")
            return jsonify({"message": "File deleted successfully"}), 200
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return jsonify({"error": "File deletion failed"}), 500
    else:
        logger.warning(f"File not found: {filename}")
        return jsonify({"error": "File not found"}), 404

@app.route('/rename', methods=['POST'])
def rename_file():
    data = request.get_json()
    old_name = data.get('old_name')
    new_name = data.get('new_name')
    if not old_name or not new_name:
        return jsonify({"error": "Both old_name and new_name are required."}), 400
    old_name = secure_filename(old_name)
    new_name = secure_filename(new_name)
    if not allowed_file(new_name):
        return jsonify({"error": "New file name has disallowed extension."}), 400
    old_path = os.path.join(STORAGE_DIR, old_name)
    new_path = os.path.join(STORAGE_DIR, new_name)
    if not os.path.exists(old_path):
        return jsonify({"error": "Original file does not exist."}), 404
    if os.path.exists(new_path):
        return jsonify({"error": "A file with the new name already exists."}), 409
    try:
        os.rename(old_path, new_path)
        logger.info(f"File renamed from {old_name} to {new_name}")
        return jsonify({"message": "File renamed successfully."}), 200
    except Exception as e:
        logger.error(f"Error renaming file: {str(e)}")
        return jsonify({"error": "File rename failed."}), 500

@app.route('/download_all', methods=['GET'])
def download_all():
    try:
        files = os.listdir(STORAGE_DIR)
        if not files:
            return jsonify({"error": "No files to download."}), 404
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for filename in files:
                file_path = os.path.join(STORAGE_DIR, filename)
                zf.write(file_path, arcname=filename)
        memory_file.seek(0)
        return send_file(memory_file, download_name='all_files.zip', as_attachment=True)
    except Exception as e:
        logger.error(f"Error creating ZIP: {str(e)}")
        return jsonify({"error": "Failed to create ZIP archive."}), 500

@app.errorhandler(413)
def file_too_large(e):
    return jsonify({"error": "File is too large. Max size is 50MB."}), 413

if __name__ == '__main__':
    app.run(port=5000, debug=True)
 