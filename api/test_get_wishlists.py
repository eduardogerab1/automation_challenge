import requests
import pytest
from utils.logger import log

URL = "http://127.0.0.1:8000"

@pytest.mark.api
@pytest.mark.order(11)
def test_retrieve_all_wishlists(new_user_token):
    """Testando o retorno de todas as wishlists"""
    log.info("Validando o retorno de todas as wishlists...")

    header = {"Authorization": f"Bearer {new_user_token}"}

    try:
        retrieve_wishlists = requests.get(f"{URL}/wishlists", headers=header)

        if retrieve_wishlists.status_code == 200:
            log.info("Wishlists retornadas com sucesso.")
            assert retrieve_wishlists.status_code == 200
            response_json = retrieve_wishlists.json()
            log.info(f"A resposta da API foi: {response_json}")

        else:
            log.error(f"Erro ao criar wishlist: {retrieve_wishlists.status_code}: {retrieve_wishlists.text}")
            pytest.fail(f"{retrieve_wishlists.status_code}: {retrieve_wishlists.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar puxar a wishlist: {e}")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(12)
def test_retrieve_nonexistent_wishlists(no_wishlist_user):
    """Testando o retorno de wishlist inexistente"""
    log.info("Validando o retorno de nenhuma wishlist criada na conta do usuário")

    header = {"Authorization": f"Bearer {no_wishlist_user}"}

    try:
        retrieve_wishlists = requests.get(f"{URL}/wishlists", headers=header)

        if retrieve_wishlists.status_code == 200:
            log.info("Requisição ok, mas wishlist não existe")
            assert retrieve_wishlists.status_code == 200
            response_json = retrieve_wishlists.json()
            log.info(f"A resposta da API foi: {response_json}")

        else:
            log.error(f"Erro ao tentar retornar a wishlist: {retrieve_wishlists.status_code}: {retrieve_wishlists.text}")
            pytest.fail(f"{retrieve_wishlists.status_code}: {retrieve_wishlists.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar puxar a wishlist: {e}")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(13)
def test_unauthenticated_user_retrieve():
    """Testando se um usuário sem autenticação não pode puxar as wishlists"""
    log.info("Validando usuário não autenticado")

    try:
        retrieve_wishlists = requests.get(f"{URL}/wishlists")

        if retrieve_wishlists.status_code == 401:
            log.info("Usuário não está autenticado.")
            assert retrieve_wishlists.status_code == 401
            response_json = retrieve_wishlists.json()
            log.info(f"A resposta da API foi: {response_json}")

        else:
            log.error(f"Erro ao tentar retornar a wishlist: {retrieve_wishlists.status_code}: {retrieve_wishlists.text}")
            pytest.fail(f"{retrieve_wishlists.status_code}: {retrieve_wishlists.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar puxar a wishlist: {e}")
        pytest.fail(f"{e}")