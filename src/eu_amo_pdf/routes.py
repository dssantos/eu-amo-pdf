from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Página inicial com lista de ferramentas."""
    return render_template("index.html")


@main_bp.route("/merge")
def merge():
    """Página para mesclar PDFs."""
    return render_template("merge.html")


def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "pdf"


@main_bp.route("/api/merge", methods=["POST"])
def api_merge():
    """API para mesclar múltiplos PDFs."""
    # TODO: Implementar mesclagem de PDFs
    return jsonify({"error": "Funcionalidade ainda não implementada"}), 501
