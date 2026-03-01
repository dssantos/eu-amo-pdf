"""Factory pattern para criação da aplicação Flask."""

import os
from typing import Optional
from flask import Flask


def create_app(test_config: Optional[dict] = None) -> Flask:
    """
    Cria e configura a aplicação Flask.

    Args:
        test_config: Configuração opcional para testes

    Returns:
        Aplicação Flask configurada
    """
    app = Flask(__name__, instance_relative_config=True)

    # Configurações padrão
    _load_config(app)
    _ensure_directories(app)
    _register_blueprints(app)

    # Configuração de teste
    if test_config is not None:
        app.config.update(test_config)

    return app


def _load_config(app: Flask) -> None:
    """Carrega configurações de ambiente."""
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key"),
        MAX_CONTENT_LENGTH=int(os.environ.get("MAX_UPLOAD_SIZE", 16 * 1024 * 1024)),  # 16MB default
    )

    # Pasta para uploads (se necessário no futuro)
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")


def _ensure_directories(app: Flask) -> None:
    """Garante que os diretórios necessários existam."""
    upload_folder = app.config.get("UPLOAD_FOLDER")
    if upload_folder:
        os.makedirs(upload_folder, exist_ok=True)


def _register_blueprints(app: Flask) -> None:
    """Registra os blueprints da aplicação."""
    from .routes import main_bp

    app.register_blueprint(main_bp)
