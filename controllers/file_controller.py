from flask import Blueprint, request, jsonify, send_file, current_app
from services.file_service import save_file, update_file, delete_file
from models.uploaded_file import UploadedFile
import uuid, os, logging

file_bp = Blueprint('file_bp', __name__)

# POST — Upload
@file_bp.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'message': 'No file uploaded'}), 400
        file = request.files['file']
        folder = os.path.join(current_app.config['UPLOAD_FOLDER'], uuid.uuid4().hex)
        uploaded = save_file(file, folder)
        return jsonify({'message': 'Upload successful','id': uploaded.id,'path': uploaded.filepath}), 201
    except Exception as e:
        logging.error(f"Upload error: {e}")
        return jsonify({'message': str(e)}), 400

# GET — Download
@file_bp.route('/file/<int:file_id>', methods=['GET'])
def get_file(file_id):
    try:
        file_record = UploadedFile.query.get(file_id)
        if not file_record:
            return jsonify({'message': 'File not found'}), 404
        return send_file(file_record.filepath, as_attachment=True)
    except Exception as e:
        logging.error(f"Get error: {e}")
        return jsonify({'message': str(e)}), 400

# PUT — Update
@file_bp.route('/file/<int:file_id>', methods=['PUT'])
def update_uploaded_file(file_id):
    try:
        if 'file' not in request.files:
            return jsonify({"message": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"message": "No selected file"}), 400

        updated_record = update_file(file_id, file)
        return jsonify({
            "message": "File updated successfully",
            "id": updated_record.id,
            "path": updated_record.filepath
        }), 200

    except Exception as e:
        logging.error(str(e))
        return jsonify({"message": str(e)}), 500

# DELETE — Delete
@file_bp.route('/file/<int:file_id>', methods=['DELETE'])
def delete_existing_file(file_id):
    try:
        delete_file(file_id)
        return jsonify({'message': 'File deleted successfully'}), 200
    except Exception as e:
        logging.error(f"Delete error: {e}")
        return jsonify({'message': str(e)}), 400
