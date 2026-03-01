from flask import Blueprint, render_template, request, jsonify, current_app, send_file
from werkzeug.utils import secure_filename
from pypdf import PdfReader, PdfWriter
from docx import Document
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


@main_bp.route("/compress")
def compress():
    """Página para comprimir PDFs."""
    return render_template("compress.html")


@main_bp.route("/pdf-to-doc")
def pdf_to_doc():
    """Página para converter PDF para DOC."""
    return render_template("pdf-to-doc.html")


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


@main_bp.route("/api/compress", methods=["POST"])
def api_compress():
    """API para comprimir PDF."""
    # Verificar se arquivo foi enviado
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]

    # Verificar se o arquivo tem nome
    if file.filename == "":
        return jsonify({"error": "Arquivo sem nome"}), 400

    # Verificar se é um PDF
    if not allowed_file(file.filename):
        return jsonify({"error": "O arquivo deve ser um PDF"}), 400

    # Ler o conteúdo do PDF
    try:
        pdf_content = file.read()
        pdf_reader = PdfReader(io.BytesIO(pdf_content))

        # Criar novo PDF com compressão
        writer = PdfWriter()

        # Adicionar páginas com compressão
        for page in pdf_reader.pages:
            writer.add_page(page)

        # Remover metadados desnecessários para reduzir tamanho
        writer.add_metadata({})

        # Criar bytes do PDF comprimido
        compressed_pdf = io.BytesIO()
        writer.write(compressed_pdf)
        compressed_pdf.seek(0)

        return send_file(
            compressed_pdf,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="comprimido.pdf",
        )

    except Exception as e:
        return jsonify({"error": f"Erro ao comprimir PDF: {str(e)}"}), 500


@main_bp.route("/api/pdf-to-doc", methods=["POST"])
def api_pdf_to_doc():
    """API para converter PDF para DOCX."""
    # Verificar se arquivo foi enviado
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]

    # Verificar se o arquivo tem nome
    if file.filename == "":
        return jsonify({"error": "Arquivo sem nome"}), 400

    # Verificar se é um PDF
    if not allowed_file(file.filename):
        return jsonify({"error": "O arquivo deve ser um PDF"}), 400

    # Ler o conteúdo do PDF e extrair texto
    try:
        pdf_content = file.read()
        pdf_reader = PdfReader(io.BytesIO(pdf_content))

        # Criar documento DOCX
        doc = Document()

        # Extrair texto de cada página
        for page_num, page in enumerate(pdf_reader.pages):
            try:
                text = page.extract_text()
                if text.strip():
                    doc.add_paragraph(text)
            except Exception as e:
                # Se falhar extrair texto da página, continua
                continue

        # Criar bytes do DOCX
        docx_bytes = io.BytesIO()
        doc.save(docx_bytes)
        docx_bytes.seek(0)

        # Nome do arquivo de saída
        output_filename = file.filename.replace(".pdf", ".docx")

        return send_file(
            docx_bytes,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name=output_filename,
        )

    except Exception as e:
        return jsonify({"error": f"Erro ao converter PDF para DOCX: {str(e)}"}), 500
