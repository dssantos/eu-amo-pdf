import os
from flask import Flask


def create_app():
    """Factory pattern para criar a aplicação Flask."""
    app = Flask(__name__)

    # Configurações
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
    app.config["MAX_CONTENT_LENGTH"] = int(os.environ.get("MAX_UPLOAD_SIZE", 16 * 1024 * 1024))  # 16MB default
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")

    # Garantir que pasta de uploads existe
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Registrar blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
