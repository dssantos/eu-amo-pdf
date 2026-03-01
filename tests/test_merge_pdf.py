import pytest
import io
from eu_amo_pdf import create_app
from pypdf import PdfWriter, PdfReader


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


def create_test_pdf(filename="test.pdf", content="Test PDF Content"):
    """Cria um PDF simples para testes."""
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)

    pdf_bytes = io.BytesIO()
    writer.write(pdf_bytes)
    pdf_bytes.seek(0)
    return (pdf_bytes, filename)


def test_merge_two_pdfs_success(client):
    """Testa mesclagem de dois PDFs com sucesso."""
    pdf1, filename1 = create_test_pdf("test1.pdf")
    pdf2, filename2 = create_test_pdf("test2.pdf")

    data = {
        "files": [
            (pdf1, filename1),
            (pdf2, filename2),
        ]
    }

    response = client.post(
        "/api/merge",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert response.content_type == "application/pdf"
    assert b"PDF" in response.data[:10]

    # Verificar se o PDF mesclado tem 2 páginas (1 de cada PDF)
    pdf_reader = PdfReader(io.BytesIO(response.data))
    assert len(pdf_reader.pages) == 2


def test_merge_three_pdfs_success(client):
    """Testa mesclagem de três PDFs com sucesso."""
    pdf1, filename1 = create_test_pdf("test1.pdf")
    pdf2, filename2 = create_test_pdf("test2.pdf")
    pdf3, filename3 = create_test_pdf("test3.pdf")

    data = {
        "files": [
            (pdf1, filename1),
            (pdf2, filename2),
            (pdf3, filename3),
        ]
    }

    response = client.post(
        "/api/merge",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    pdf_reader = PdfReader(io.BytesIO(response.data))
    assert len(pdf_reader.pages) == 3


def test_merge_single_pdf_returns_error(client):
    """Testa que mesclar apenas um PDF retorna erro."""
    pdf1, filename1 = create_test_pdf("test1.pdf")

    data = {
        "files": [
            (pdf1, filename1),
        ]
    }

    response = client.post(
        "/api/merge",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert "pelo menos 2" in response.json["error"]


def test_merge_no_files_returns_error(client):
    """Testa que não enviar arquivos retorna erro."""
    response = client.post("/api/merge")

    assert response.status_code == 400
    assert "arquivo" in response.json["error"]


def test_merge_with_non_pdf_returns_error(client):
    """Testa que enviar arquivo não-PDF retorna erro."""
    pdf1, filename1 = create_test_pdf("test1.pdf")
    txt_file = (io.BytesIO(b"Texto qualquer"), "test.txt")

    data = {
        "files": [
            (pdf1, filename1),
            txt_file,
        ]
    }

    response = client.post(
        "/api/merge",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert "PDF" in response.json["error"]
