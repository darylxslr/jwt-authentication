import os
import uuid
import logging
from werkzeug.utils import secure_filename
from extensions import db
from models.uploaded_file import UploadedFile

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, base_folder):
    if not allowed_file(file.filename):
        raise ValueError("File type not allowed")

    os.makedirs(base_folder, exist_ok=True)
    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    save_path = os.path.join(base_folder, unique_name)
    file.save(save_path)

    new_file = UploadedFile(filename=filename, filepath=save_path)
    db.session.add(new_file)
    db.session.commit()

    logging.info(f"File saved: {save_path}")
    return new_file

def update_file(file_id, file):
    record = UploadedFile.query.get(file_id)
    if not record:
        raise ValueError(f"File with ID {file_id} not found")

    if not allowed_file(file.filename):
        raise ValueError("File type not allowed")

    # delete old file if it exists
    if os.path.exists(record.filepath):
        os.remove(record.filepath)
        logging.info(f"Old file removed: {record.filepath}")

    # save the new file in the same folder
    folder = os.path.dirname(record.filepath)
    filename = secure_filename(file.filename)
    save_path = os.path.join(folder, filename)
    file.save(save_path)

    # update database record
    record.filename = filename
    record.filepath = save_path
    db.session.commit()

    logging.info(f"File updated: ID={file_id}, Path={save_path}")
    return record

def delete_file(file_id):
    record = UploadedFile.query.get(file_id)
    if not record:
        raise ValueError(f"File with ID {file_id} not found")

    if os.path.exists(record.filepath):
        os.remove(record.filepath)
        logging.info(f"File deleted from storage: {record.filepath}")

    db.session.delete(record)
    db.session.commit()

    logging.info(f"Record deleted: ID={file_id}")
    return True
