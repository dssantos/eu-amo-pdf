from flask import Blueprint, render_template, request, jsonify, current_app, send_file
from werkzeug.utils import secure_filename
from pypdf import PdfReader, PdfWriter
import io
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
    # Verificar se arquivos foram enviados
    if "files" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    files = request.files.getlist("files")

    # Verificar se há pelo menos 2 arquivos
    if len(files) < 2:
        return jsonify({"error": "É necessário enviar pelo menos 2 arquivos PDF"}), 400

    # Verificar se todos os arquivos são PDFs
    pdf_files = []
    for file in files:
        if file.filename == "":
            return jsonify({"error": "Arquivo sem nome"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Todos os arquivos devem ser PDF"}), 400

        # Ler o conteúdo do PDF
        try:
            pdf_content = file.read()
            pdf_reader = PdfReader(io.BytesIO(pdf_content))
            pdf_files.append(pdf_reader)
        except Exception as e:
            return jsonify({"error": f"Erro ao ler PDF {file.filename}: {str(e)}"}), 400

    # Mesclar os PDFs
    try:
        merger = PdfWriter()
        for pdf in pdf_files:
            for page in pdf.pages:
                merger.add_page(page)

        # Criar bytes do PDF mesclado
        merged_pdf = io.BytesIO()
        merger.write(merged_pdf)
        merged_pdf.seek(0)

        return send_file(
            merged_pdf,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="mesclado.pdf",
        )

    except Exception as e:
        return jsonify({"error": f"Erro ao mesclar PDFs: {str(e)}"}), 500
