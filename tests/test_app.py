import pytest
from eu_amo_pdf import create_app


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


def test_index_route(client):
    """Testa se a rota principal retorna 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Eu Amo PDF" in response.data


def test_merge_route(client):
    """Testa se a rota de mesclagem retorna 200."""
    response = client.get("/merge")
    assert response.status_code == 200
    assert b"Mesclar PDFs" in response.data
