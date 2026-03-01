import pytest
import io
import os
from eu_amo_pdf import create_app
from pypdf import PdfWriter


# Caminho para os PDFs de exemplo
EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'examples')


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
        with open(filepath, 'rb') as f:
            return io.BytesIO(f.read())
    else:
        # Fallback: criar PDF simples em memória
        writer = PdfWriter()
        writer.add_blank_page(width=200, height=200)
        pdf_bytes = io.BytesIO()
        writer.write(pdf_bytes)
        pdf_bytes.seek(0)
        return pdf_bytes


def test_convert_business_report_to_docx(client):
    """Testa conversão de um relatório de negócios real."""
    pdf_content = get_example_pdf("relatorio_negocios.pdf")

    data = {"file": (pdf_content, "relatorio_negocios.pdf")}

    response = client.post(
        "/api/pdf-to-doc",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert response.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def test_convert_technical_document_to_docx(client):
    """Testa conversão de um documento técnico real."""
    pdf_content = get_example_pdf("documento_tecnico.pdf")

    data = {"file": (pdf_content, "documento_tecnico.pdf")}

    response = client.post(
        "/api/pdf-to-doc",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert response.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def test_convert_marketing_brochure_to_docx(client):
    """Testa conversão de um folheto de marketing real."""
    pdf_content = get_example_pdf("folheto_marketing.pdf")

    data = {"file": (pdf_content, "folheto_marketing.pdf")}

    response = client.post(
        "/api/pdf-to-doc",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert response.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def test_convert_no_file_returns_error(client):
    """Testa que não enviar arquivo retorna erro."""
    response = client.post("/api/pdf-to-doc")

    assert response.status_code == 400
    assert "arquivo" in response.json["error"]


def test_convert_with_non_pdf_returns_error(client):
    """Testa que enviar arquivo não-PDF retorna erro."""
    txt_file = (io.BytesIO(b"Texto qualquer"), "test.txt")

    data = {"file": txt_file}

    response = client.post(
        "/api/pdf-to-doc",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert "PDF" in response.json["error"]


def test_convert_returns_valid_docx(client):
    """Testa que o arquivo retornado é um DOCX válido."""
    pdf_content = get_example_pdf("contrato_juridico.pdf")

    data = {"file": (pdf_content, "contrato_juridico.pdf")}

    response = client.post(
        "/api/pdf-to-doc",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    # Verificar se é um arquivo DOCX válido pelo cabeçalho
    assert response.data[:4] == b"PK\x03\x04"  # Cabeçalho de ZIP (DOCX é um ZIP)
