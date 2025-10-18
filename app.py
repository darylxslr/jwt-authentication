from flask import Flask
from config import Config
from extensions import db
from controllers.file_controller import file_bp
from models.uploaded_file import UploadedFile # 
import logging, os

# forda logs
log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_folder, "app.log")),
        logging.StreamHandler()
    ]
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(file_bp)
    with app.app_context():
        db.create_all()
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
