import pytest
import io
import os
from eu_amo_pdf import create_app
from pypdf import PdfWriter

# Caminho para os PDFs de exemplo
EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "examples")


@pytest.fixture
def app():
    """Cria uma aplicação Flask para testes."""
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Cria um cliente de teste."""
    return app.test_client()


def get_example_pdf(filename):
    """Retorna um PDF de exemplo como bytes."""
    filepath = os.path.join(EXAMPLES_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            return io.BytesIO(f.read())
    else:
        # Fallback: criar PDF simples em memória
        writer = PdfWriter()
        for _ in range(2):
            writer.add_blank_page(width=200, height=200)
        pdf_bytes = io.BytesIO()
        writer.write(pdf_bytes)
        pdf_bytes.seek(0)
        return pdf_bytes


def test_compress_business_report_success(client):
    """Testa compressão de um relatório de negócios real."""
    pdf_content = get_example_pdf("relatorio_negocios.pdf")

    data = {"file": (pdf_content, "relatorio_negocios.pdf"), "level": "medium"}

    response = client.post(
        "/api/compress",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert response.content_type == "application/pdf"
    assert b"PDF" in response.data[:10]


def test_compress_technical_document_success(client):
    """Testa compressão de um documento técnico real."""
    pdf_content = get_example_pdf("documento_tecnico.pdf")

    data = {"file": (pdf_content, "documento_tecnico.pdf"), "level": "high"}

    response = client.post(
        "/api/compress",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert response.content_type == "application/pdf"


def test_compress_legal_document_success(client):
    """Testa compressão de um documento jurídico real."""
    pdf_content = get_example_pdf("contrato_juridico.pdf")

    data = {"file": (pdf_content, "contrato_juridico.pdf"), "level": "low"}

    response = client.post(
        "/api/compress",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert response.content_type == "application/pdf"


def test_compress_no_file_returns_error(client):
    """Testa que não enviar arquivo retorna erro."""
    response = client.post("/api/compress")

    assert response.status_code == 400
    assert "arquivo" in response.json["error"]


def test_compress_with_non_pdf_returns_error(client):
    """Testa que enviar arquivo não-PDF retorna erro."""
    txt_file = (io.BytesIO(b"Texto qualquer"), "test.txt")

    data = {"file": txt_file}

    response = client.post(
        "/api/compress",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert "PDF" in response.json["error"]


def test_compress_returns_valid_pdf(client):
    """Testa que o arquivo retornado é um PDF válido."""
    pdf_content = get_example_pdf("artigo_cientifico.pdf")

    data = {"file": (pdf_content, "artigo_cientifico.pdf"), "level": "medium"}

    response = client.post(
        "/api/compress",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    from pypdf import PdfReader

    pdf_reader = PdfReader(io.BytesIO(response.data))
    assert len(pdf_reader.pages) >= 1  # Deve ter pelo menos 1 página
