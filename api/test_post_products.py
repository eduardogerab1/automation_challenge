import requests
import pytest
import uuid
from utils.logger import log

URL = "http://127.0.0.1:8000"

@pytest.mark.api
@pytest.mark.order(14)
def test_add_a_product(new_user_token):
    """Testando a adição de um produto à wishlist"""
    log.info("Tentando adicionar um produto na wishlist...")

    header = {"Authorization": f"Bearer {new_user_token}"}

    payload = {
        "Product": f"Novo Produto {uuid.uuid4().hex[:6]}",
        "Price": "99.999,99",
        "Zipcode": "50710330",
        "delivery_estimate": "12 dias uteis",
        "shipping_fee": "Gratis",
        "purchased": "false"
    }

    try:
        add_product = requests.post(f"{URL}/wishlists/2/products", headers=header, json=payload)

        if add_product.status_code == 200:
            log.info("Produto adicionado com sucesso.")
            assert add_product.status_code == 200
            response_json = add_product.json()
            log.info(f"A resposta da API foi: {response_json}")

        else:
            log.error(f"Erro ao adicionar o produto na wishlist: {add_product.status_code}: {add_product.text}")
            pytest.fail(f"{add_product.status_code}: {add_product.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar adicionar o produto na wishlist: {e}")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(15)
def test_add_product_nonexistent_wishlist(new_user_token):
    """Testando a adição de um produto à uma wishlist que não existe"""
    log.info("Tentando adicionar um produto na wishlist inexistente...")

    header = {"Authorization": f"Bearer {new_user_token}"}

    payload = {
        "Product": f"Produto {uuid.uuid4().hex[:6]}",
        "Price": "99.999,99",
        "Zipcode": "50710330",
        "delivery_estimate": "12 dias uteis",
        "shipping_fee": "Gratis",
        "purchased": "false"
    }

    try:
        add_product = requests.post(f"{URL}/wishlists/9999/products", headers=header, json=payload)

        if add_product.status_code == 404:
            log.info("Produto não pôde ser adicionado porque a wishlist não existe.")
            assert add_product.status_code == 404
            response_json = add_product.json()
            log.info(f"A resposta da API foi: {response_json}")

        else:
            log.error(f"Erro ao adicionar o produto na wishlist: {add_product.status_code}: {add_product.text}")
            pytest.fail(f"{add_product.status_code}: {add_product.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar adicionar o produto na wishlist: {e}")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(16)
def test_add_to_another_user_wishlist(new_user_token):
    """Testando se um usuário consegue adicionar um prouto na wishlist de outro"""
    log.info("Tentando adicionar produto na wishlist de outro usuário...")

    header = {"Authorization": f"Bearer {new_user_token}"}

    payload = {
        "Product": f"Produto {uuid.uuid4().hex[:6]}",
        "Price": "99.999,99",
        "Zipcode": "50710330",
        "delivery_estimate": "12 dias uteis",
        "shipping_fee": "Gratis",
        "purchased": "false"
    }

    try:
        add_product = requests.post(f"{URL}/wishlists/1/products", headers=header, json=payload)

        if add_product.status_code == 404:
            log.info("Wishlist não foi encontrada no registro desse usuário.")
            assert add_product.status_code == 404
            response_json = add_product.json()
            log.info(f"A resposta da API foi: {response_json}")

        else:
            log.error(f"Comportamento inesperado ao adicionar o produto na wishlist de outra pessoa: {add_product.status_code}: {add_product.text}")
            pytest.fail(f"{add_product.status_code}: {add_product.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar adicionar o produto na wishlist: {e}")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(17)
def test_add_product_missing_data(new_user_token):
    """Testando se um produto pode ser adicionado à uma wishlist com informações faltantes"""
    log.info("Tentando adicionar um produto com informações faltantes")

    header = {"Authorization": f"Bearer {new_user_token}"}

    payload = {
        "Zipcode": "50710330",
        "delivery_estimate": "12 dias uteis",
        "shipping_fee": "Gratis",
        "purchased": "false"
    }

    try:
        add_product = requests.post(f"{URL}/wishlists/2/products", headers=header, json=payload)

        if add_product.status_code == 422:
            log.info("Wishlist não foi encontrada no registro desse usuário.")
            assert add_product.status_code == 422
            response_json = add_product.json()
            log.info(f"A resposta da API foi: {response_json}")

        else:
            log.error(f"Comportamento inesperado ao tentar adicionar um produto com informações faltantes: {add_product.status_code}: {add_product.text}")
            pytest.fail(f"{add_product.status_code}: {add_product.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar adicionar um produto com informações faltantes: {e}")
        pytest.fail(f"{e}")