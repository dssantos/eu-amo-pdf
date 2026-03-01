import pytest
import io
import os
from eu_amo_pdf import create_app
from pypdf import PdfWriter, PdfReader

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
            return (io.BytesIO(f.read()), filename)
    else:
        # Fallback: criar PDF simples em memória
        writer = PdfWriter()
        writer.add_blank_page(width=200, height=200)
        pdf_bytes = io.BytesIO()
        writer.write(pdf_bytes)
        pdf_bytes.seek(0)
        return (pdf_bytes, filename)


def test_merge_two_pdfs_success(client):
    """Testa mesclagem de dois PDFs com conteúdo real."""
    pdf1, filename1 = get_example_pdf("relatorio_negocios.pdf")
    pdf2, filename2 = get_example_pdf("documento_tecnico.pdf")

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

    # Verificar se o PDF mesclado tem páginas
    pdf_reader = PdfReader(io.BytesIO(response.data))
    assert len(pdf_reader.pages) >= 2  # Pelo menos 2 páginas


def test_merge_three_pdfs_success(client):
    """Testa mesclagem de três PDFs com conteúdo real."""
    pdf1, filename1 = get_example_pdf("relatorio_negocios.pdf")
    pdf2, filename2 = get_example_pdf("documento_tecnico.pdf")
    pdf3, filename3 = get_example_pdf("folheto_marketing.pdf")

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
    assert len(pdf_reader.pages) >= 3  # Pelo menos 3 páginas


def test_merge_various_document_types(client):
    """Testa mesclagem de diferentes tipos de documentos."""
    pdf1, _ = get_example_pdf("contrato_juridico.pdf")
    pdf2, _ = get_example_pdf("artigo_cientifico.pdf")
    pdf3, _ = get_example_pdf("folheto_marketing.pdf")

    data = {
        "files": [
            (pdf1, "contrato_juridico.pdf"),
            (pdf2, "artigo_cientifico.pdf"),
            (pdf3, "folheto_marketing.pdf"),
        ]
    }

    response = client.post(
        "/api/merge",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    pdf_reader = PdfReader(io.BytesIO(response.data))
    assert len(pdf_reader.pages) >= 3


def test_merge_single_pdf_returns_error(client):
    """Testa que mesclar apenas um PDF retorna erro."""
    pdf1, filename1 = get_example_pdf("relatorio_curto.pdf")

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
    pdf1, filename1 = get_example_pdf("relatorio_curto.pdf")
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
