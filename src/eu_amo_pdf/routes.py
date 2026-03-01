"""Rotas da aplicação Flask."""

from flask import Blueprint, render_template, request, jsonify, send_file
from typing import List

from .services import MergeService, CompressService, ConversionService
from .validators import FileValidator
from .exceptions import PDFProcessingError

main_bp = Blueprint("main", __name__)


# Rotas de páginas HTML
@main_bp.route("/")
def index():
    """Página inicial com lista de ferramentas."""
    return render_template("index.html")


@main_bp.route("/merge")
def merge():
    """Página para mesclar PDFs."""
    return render_template("merge.html")


@main_bp.route("/compress")
def compress():
    """Página para comprimir PDFs."""
    return render_template("compress.html")


@main_bp.route("/pdf-to-doc")
def pdf_to_doc():
    """Página para converter PDF para DOC."""
    return render_template("pdf-to-doc.html")


# Rotas da API
@main_bp.route("/api/merge", methods=["POST"])
def api_merge():
    """
    API para mesclar múltiplos PDFs.

    Request:
        files: Lista de arquivos PDF (mínimo 2)

    Returns:
        PDF mesclado ou erro
    """
    try:
        # Validar entrada
        if "files" not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400

        files: List = request.files.getlist("files")
        FileValidator.validate_pdf_files(files, min_count=2)

        # Processar mesclagem
        merged_pdf = MergeService.merge_pdfs(files)

        return send_file(
            merged_pdf,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="mesclado.pdf",
        )

    except PDFProcessingError as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@main_bp.route("/api/compress", methods=["POST"])
def api_compress():
    """
    API para comprimir PDF.

    Request:
        file: Arquivo PDF
        level: Nível de compressão (low, medium, high)

    Returns:
        PDF comprimido ou erro
    """
    try:
        # Validar entrada
        if "file" not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400

        file = request.files["file"]
        FileValidator.validate_pdf_file(file)

        level = request.form.get("level", "medium")

        # Processar compressão
        compressed_pdf = CompressService.compress_pdf(file, level)

        return send_file(
            compressed_pdf,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="comprimido.pdf",
        )

    except PDFProcessingError as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@main_bp.route("/api/pdf-to-doc", methods=["POST"])
def api_pdf_to_doc():
    """
    API para converter PDF para DOCX.

    Request:
        file: Arquivo PDF

    Returns:
        Documento DOCX ou erro
    """
    try:
        # Validar entrada
        if "file" not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400

        file = request.files["file"]
        FileValidator.validate_pdf_file(file)

        # Processar conversão
        docx = ConversionService.pdf_to_docx(file)

        output_filename = file.filename.replace(".pdf", ".docx")

        return send_file(
            docx,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name=output_filename,
        )

    except PDFProcessingError as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500
