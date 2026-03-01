import pytest
import io
from eu_amo_pdf import create_app
from pypdf import PdfWriter


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


def create_test_pdf_with_text(filename="test.pdf"):
    """Cria um PDF com texto para testes."""
    from pypdf import PdfWriter

    # Cria um PDF simples com uma página em branco
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)

    pdf_bytes = io.BytesIO()
    writer.write(pdf_bytes)
    pdf_bytes.seek(0)
    return (pdf_bytes, filename)


def test_convert_pdf_to_doc_success(client):
    """Testa conversão de PDF para DOC com sucesso."""
    pdf, filename = create_test_pdf_with_text("test.pdf")

    data = {"file": (pdf, filename)}

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
    pdf, filename = create_test_pdf_with_text("test.pdf")

    data = {"file": (pdf, filename)}

    response = client.post(
        "/api/pdf-to-doc",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    # Verificar se é um arquivo DOCX válido pelo cabeçalho
    assert response.data[:4] == b"PK\x03\x04"  # Cabeçalho de ZIP (DOCX é um ZIP)
