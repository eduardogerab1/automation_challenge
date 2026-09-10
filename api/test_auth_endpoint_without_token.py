import requests
import pytest
from utils.logger import log

URL = "http://127.0.0.1:8000"

@pytest.mark.api
@pytest.mark.order(28)
def test_post_wishlists_without_authentication_token():
    """Testando se é possível retornar algo de post /wishlists, sem se autenticar."""
    log.info("Passando requisição post sem autenticação para /wishlists.")

    try:
        update_wishlists = requests.post(f"{URL}/wishlists")

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
@pytest.mark.order(29)
def test_get_wishlists_without_authentication_token():
    """Testando se é possível retornar algo de get /wishlists, sem se autenticar."""
    log.info("Passando requisição get sem autenticação para /wishlists.")

    try:
        retrieve_wishlists = requests.get(f"{URL}/wishlists")

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
@pytest.mark.order(30)
def test_post_wishlist_products():
    """Testando se é possível retornar algo de post /wishlist/id/products, sem se autenticar."""
    log.info("Passando requisição post sem autenticação para /wishlist/id/products.")

    try:
        update_products = requests.post(f"{URL}/wishlists/1/products")

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
@pytest.mark.order(31)
def test_get_wishlist_products():
    """Testando se é possível retornar algo de get /wishlist/id/products, sem se autenticar."""
    log.info("Passando requisição get sem autenticação para /wishlist/id/products.")

    try:
        retrieve_products = requests.get(f"{URL}/wishlists/1/products")

        if retrieve_products.status_code == 401:
            assert retrieve_products.status_code == 401
            retrieve_products_response = retrieve_products.json()
            log.info(f"a resposta da api foi: {retrieve_products.status_code} {retrieve_products_response}")

        else:
            log.error(f"Comportamento inesperado ao tentar passar a requisição {retrieve_products_response}.")
            pytest.fail(f"{retrieve_products.status_code}: {retrieve_products_response}")

    except Exception as e:
        log.error(f"ocorreu outro tipo de erro ao tentar passar a requisição.")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(32)
def test_put_products():
    """Testando se é possível retornar algo de put /products/id, sem se autenticar."""
    log.info("Passando requisição put sem autenticação para /products/id")

    try:
        edit_product = requests.put(f"{URL}/products/1")

        if edit_product.status_code == 401:
            assert edit_product.status_code == 401
            edit_products_response = edit_product.json()
            log.info(f"a resposta da api foi: {edit_product.status_code} {edit_products_response}")

        else:
            log.error(f"Comportamento inesperado ao tentar passar a requisição {edit_products_response}.")
            pytest.fail(f"{edit_product.status_code}: {edit_products_response}")

    except Exception as e:
        log.error(f"ocorreu outro tipo de erro ao tentar passar a requisição.")
        pytest.fail(f"{e}")   

@pytest.mark.api
@pytest.mark.order(33)
def test_delete_product():
    """Testando se é possível retornar algo de delete /products/id, sem se autenticar."""
    log.info("Passando requisição delete sem autenticação para /products/id")

    try:
        delete_product = requests.delete(f"{URL}/products/1")

        if delete_product.status_code == 401:
            assert delete_product.status_code == 401
            delete_products_response = delete_product.json()
            log.info(f"a resposta da api foi: {delete_product.status_code} {delete_products_response}")

        else:
            log.error(f"Comportamento inesperado ao tentar passar a requisição {delete_products_response}.")
            pytest.fail(f"{delete_product.status_code}: {delete_products_response}")

    except Exception as e:
        log.error(f"ocorreu outro tipo de erro ao tentar passar a requisição.")
        pytest.fail(f"{e}")

# não foi possível fazer o teste para o endpoint PATCH /products/{product_id}/toggle