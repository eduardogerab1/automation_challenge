import requests
import pytest
import uuid
from utils.logger import log

URL = "http://127.0.0.1:8000"

@pytest.mark.api
@pytest.mark.order(7)
def test_create_wishlist(new_user_token):
    """Testando a criação de wishlists na API"""
    log.info("Criando uma nova wishlist...")

    header = {"Authorization": f"Bearer {new_user_token}"}

    payload = {
        "name": f"Minha Nova Wishlist {uuid.uuid4().hex[:6]}"
    }

    try:
        create_wishlist_request = requests.post(f"{URL}/wishlists", headers=header, json=payload)

        if create_wishlist_request.status_code == 200:
            log.info("Wishlist criada com sucesso.")
            assert create_wishlist_request.status_code == 200
            response_json = create_wishlist_request.json()
            log.info(f"A resposta da API foi: {response_json}")

        else:
            log.error(f"Erro ao criar wishlist: {create_wishlist_request.status_code}: {create_wishlist_request.text}")
            pytest.fail(f"{create_wishlist_request.status_code}: {create_wishlist_request.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar criar a wishlist: {e}")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(8)
def test_wishlists_duplicate_name(new_user_token):
    """Testando wishlists duplicadas na API"""
    log.info("Validando a duplicação de wishlists...")

    header = {"Authorization": f"Bearer {new_user_token}"}

    payload = {
        "name": f"Minha Wishlist Duplicada"
    }

    try:
        create_wishlist_request = requests.post(f"{URL}/wishlists", headers=header, json=payload)

        if create_wishlist_request.status_code == 200:
            log.info("Wishlist criada com sucesso.")
            assert create_wishlist_request.status_code == 200
            response_json = create_wishlist_request.json()
            log.info(f"A resposta da API foi: {response_json}")

        elif create_wishlist_request.status_code == 409:
            log.info("O nome da wishlist conflita com outra")
            assert create_wishlist_request.status_code == 409
            response_json = create_wishlist_request.json()
            log.info(f"A resposta da API foi: {response_json}")

        else:
            log.error(f"Erro ao criar wishlist: {create_wishlist_request.status_code}: {create_wishlist_request.text}")
            pytest.fail(f"{create_wishlist_request.status_code}: {create_wishlist_request.text}")
        
    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao criar a wishlist: {e}")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(9)
def test_wishlist_unauthenticated():
    """Testando a criação de uma wishlist sem autenticação na API"""
    log.info("Tentando criar uma nova wishlist sem autenticar...")

    payload = {
        "name": f"Minha Wishlist"
    }

    try:
        create_wishlist_request = requests.post(f"{URL}/wishlists", json=payload)

        if create_wishlist_request.status_code == 401:
            log.info("Validando a autenticação do usuário ao criar wishlist sem autenticação...")
            assert create_wishlist_request.status_code == 401
            response_json = create_wishlist_request.json()
            log.info(f"A resposta da API foi: {response_json}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao criar a wishlist: {e}")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(10)
def test_create_wishlist_invalid_data(new_user_token):
    """Testando a criação de uma wishlist sem nome"""
    log.info("Tentando criar uma wishlist sem um nome...")

    payload = {

    }

    header = {"Authorization": f"Bearer {new_user_token}"}

    try:
        create_wishlist_request = requests.post(f"{URL}/wishlists", headers=header, json=payload)

        if create_wishlist_request.status_code == 422:
            log.info("Validando criação da wishlist sem nome...")
            assert create_wishlist_request.status_code == 422
            response_json = create_wishlist_request.json()
            log.info(f"A resposta da API foi: {response_json}")

        else:
            log.error(f"Erro ao criar wishlist: {create_wishlist_request.status_code}: {create_wishlist_request.text}")
            pytest.fail(f"{create_wishlist_request.status_code}: {create_wishlist_request.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao criar a wishlist: {e}")
        pytest.fail(f"{e}")    
