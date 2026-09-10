import requests
import pytest
from utils.logger import log

URL = "http://127.0.0.1:8000"

@pytest.mark.api
@pytest.mark.order(34)
def test_post_wishlist():
    """Testando se é possível retornar algo do endpoint post /wishlist passando um token inválido"""
    log.info("Passando requisição post com autenticação inválida para /wishlists.")

    header = {
        "Authorization": "Bearer invalidtoken123"
    }

    try:
        update_wishlists = requests.post(f"{URL}/wishlists", headers=header)

        if update_wishlists.status_code == 401:
            assert update_wishlists.status_code == 401
            update_wishlists_response = update_wishlists.json()
            log.info(f"a resposta da api foi: {update_wishlists.status_code} {update_wishlists_response}")

        else:
            log.error(f"Comportamento inesperado ao tentar passar a requisição {update_wishlists_response}.")
            pytest.fail(f"{update_wishlists.status_code}: {update_wishlists_response}")

    except Exception as e:
        log.error(f"ocorreu outro tipo de erro ao tentar passar a requisição.")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(35)
def test_get_wishlist():
    """Testando se é possível retornar algo do endpoint get /wishlist passando um token inválido."""
    log.info("Passando requisição get com autenticação inválida para /wishlists")

    header = {
        "Authorization": "Bearer invalidtoken123"
    }

    try:
        retrieve_wishlists = requests.get(f"{URL}/wishlists", headers=header)

        if retrieve_wishlists.status_code == 401:
            assert retrieve_wishlists.status_code == 401
            retrieve_wishlists_response = retrieve_wishlists.json()
            log.info(f"a resposta da api foi: {retrieve_wishlists.status_code} {retrieve_wishlists_response}")

        else:
            log.error(f"Comportamento inesperado ao tentar passar a requisição {retrieve_wishlists_response}.")
            pytest.fail(f"{retrieve_wishlists.status_code}: {retrieve_wishlists_response}")

    except Exception as e:
        log.error(f"ocorreu outro tipo de erro ao tentar passar a requisição.")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(36)
def test_post_wishlist_products():
    """Testando se é possível retornar algo do endpoint post /wishlist/id/products passando um token inválido."""
    log.info("Passando requisição post com atenticação inválida para /wishlist/id/products")

    header = {
        "Authorization": "Bearer invalidtoken123"
    }

    try:
        update_products = requests.post(f"{URL}/wishlists/1/products", headers=header)

        if update_products.status_code == 401:
            assert update_products.status_code == 401
            update_products_response = update_products.json()
            log.info(f"a resposta da api foi: {update_products.status_code} {update_products_response}")

        else:
            log.error(f"Comportamento inesperado ao tentar passar a requisição {update_products_response}.")
            pytest.fail(f"{update_products.status_code}: {update_products_response}")

    except Exception as e:
        log.error(f"ocorreu outro tipo de erro ao tentar passar a requisição.")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(37)
def test_put_products():
    """Testando se é possível retornar algo do endpoint put /products/id passando um token inválido."""
    log.info("Passando requisição put com autenticação inválida para /products/id")

    header = {
        "Authorization": "Bearer invalidtoken123"
    }

    try:
        edit_products = requests.put(f"{URL}/products/1", headers=header)

        if edit_products.status_code == 401:
            assert edit_products.status_code == 401
            edit_products_response = edit_products.json()
            log.info(f"a resposta da api foi: {edit_products.status_code} {edit_products_response}")

        else:
            log.error(f"Comportamento inesperado ao tentar passar a requisição {edit_products_response}.")
            pytest.fail(f"{edit_products.status_code}: {edit_products_response}")

    except Exception as e:
        log.error(f"ocorreu outro tipo de erro ao tentar passar a requisição.")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(38)
def test_delete_products():
    """Testando se é possível retornar algo do endpoint delete /products/id passando um token inválido."""
    log.info("Passando requisição delete com autenticação inválida para /products/id")

    header = {
        "Authorization": "Bearer invalidtoken123"
    }

    try:
        delete_products = requests.delete(f"{URL}/products/1", headers=header)

        if delete_products.status_code == 401:
            assert delete_products.status_code == 401
            delete_products_response = delete_products.json()
            log.info(f"a resposta da api foi: {delete_products.status_code} {delete_products_response}")

        else:
            log.error(f"Comportamento inesperado ao tentar passar a requisição {delete_products_response}.")
            pytest.fail(f"{delete_products.status_code}: {delete_products_response}")

    except Exception as e:
        log.error(f"ocorreu outro tipo de erro ao tentar passar a requisição.")
        pytest.fail(f"{e}")