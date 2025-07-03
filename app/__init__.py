from flask import Flask, send_from_directory
from app.routes.chat import chat_bp
import os

def create_app():
    app = Flask(__name__, static_folder='../static', static_url_path='/static')
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")

    app.register_blueprint(chat_bp)

    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    return app
