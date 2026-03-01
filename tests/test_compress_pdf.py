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


def create_test_pdf(filename="test.pdf", num_pages=1):
    """Cria um PDF simples para testes."""
    writer = PdfWriter()
    for _ in range(num_pages):
        writer.add_blank_page(width=200, height=200)

    pdf_bytes = io.BytesIO()
    writer.write(pdf_bytes)
    pdf_bytes.seek(0)
    return (pdf_bytes, filename)


def test_compress_single_pdf_success(client):
    """Testa compressão de um PDF com sucesso."""
    pdf, filename = create_test_pdf("test.pdf", num_pages=3)

    data = {"file": (pdf, filename)}

    response = client.post(
        "/api/compress",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert response.content_type == "application/pdf"
    assert b"PDF" in response.data[:10]


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
    pdf, filename = create_test_pdf("test.pdf", num_pages=2)

    data = {"file": (pdf, filename)}

    response = client.post(
        "/api/compress",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    from pypdf import PdfReader
    pdf_reader = PdfReader(io.BytesIO(response.data))
    assert len(pdf_reader.pages) == 2  # Deve manter o mesmo número de páginas
