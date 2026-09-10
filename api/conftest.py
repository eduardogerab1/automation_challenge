import pytest
import requests

@pytest.fixture(scope="session")
def base_url():
    return "http://127.0.0.1:8000"

@pytest.fixture(scope="session")
def auth_token(base_url):
    """retorna o token do usuário padrão para ser usado durante todos os testes."""
    payload = {
        "email": "projeto@example.com",
        "password": "Senha123!"
    }

    response = requests.post(f"{base_url}/auth/login", json=payload)
    assert response.status_code == 200, "Falha ao fazer login para obter token"

    token = response.json().get("access_token")
    assert token is not None, "Token não foi retornado pela API"
    return token

@pytest.fixture(scope="session")
def new_user_token(base_url):

    payload = {
        "email": "novousuario@teste.com",
        "password": "senha123",
        "username": "novousuario"
    }

    # tenta registrar, mas NÃO falha se já existir
    requests.post(f"{base_url}/auth/register", json=payload)

    loginpayload = {
        "email": "novousuario@teste.com",
        "password": "senha123"
    }

    login_response = requests.post(f"{base_url}/auth/login", json=loginpayload)
    assert login_response.status_code == 200, "Falha ao fazer login para obter token do novo usuário"

    token = login_response.json().get("access_token")
    assert token is not None, "Token não foi retornado pela API"

    return token

@pytest.fixture(scope="session")
def no_wishlist_user(base_url):

    payload = {
        "email": "usuariosemwishlist@teste.com",
        "password": "senha123",
        "username": "usuariosemwishlist"
    }

    # tenta registrar, mas NÃO falha se já existir
    requests.post(f"{base_url}/auth/register", json=payload)

    loginpayload = {
        "email": "novousuario@teste.com",
        "password": "senha123"
    }

    login_response = requests.post(f"{base_url}/auth/login", json=loginpayload)
    assert login_response.status_code == 200, "Falha ao fazer login para obter token do novo usuário"

    token = login_response.json().get("access_token")
    assert token is not None, "Token não foi retornado pela API"

    return token

@pytest.fixture()
def auth_headers(auth_token):
    """Basta usar `auth_headers` no lugar de headers nos testes."""
    return {"Authorization": f"Bearer {auth_token}"}
