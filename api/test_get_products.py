import requests
import pytest
from utils.logger import log

URL = "http://127.0.0.1:8000"
PRODUCT = "iPhone"

@pytest.mark.api
@pytest.mark.order(18)
def test_retrieve_products_from_wishlist(auth_token):
    """Retornando todos os produtos de uma wishlist específica"""
    log.info("Testando o retorno dos produtos de uma wishlists")

    header = {"Authorization": f"Bearer {auth_token}"}

    try:
        retrieve_products = requests.get(f"{URL}/wishlists/1/products", headers=header)

        if retrieve_products.status_code == 200:
            log.info("Produtos retornados com sucesso.")
            assert retrieve_products.status_code == 200
            response_json = retrieve_products.json()
            log.info(f"A resposta da API foi: {response_json}")

        else:
            log.error(f"Erro ao retornar produtos da wishlist especificada: {retrieve_products.status_code}: {retrieve_products.text}")
            pytest.fail(f"{retrieve_products.status_code}: {retrieve_products.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar retornar produtos da wishlist especificada: {e}")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(19)
def test_retrieve_products_filter_by_name(auth_token):
    """Retornando produtos de uma wishlist filtrados pelo nome"""
    log.info("Filtrando produtos de uma wishlist pelo nome")

    header = {"Authorization": f"Bearer {auth_token}"}

    try:
        retrieve_products = requests.get(f"{URL}/wishlists/1/products?Product={PRODUCT}", headers=header)

        if retrieve_products.status_code == 200:
            log.info("Produtos retornados com sucesso.")
            assert retrieve_products.status_code == 200
            response_json = retrieve_products.json()
            log.info(f"A resposta da API foi: {response_json}")

            # === Valida se apenas produtos com "iPhone" estão na lista ===

            for product in response_json:
                product_name = product.get("Product", "").lower()
                assert PRODUCT.lower() in product_name, (
                    f"Produto fora do filtro encontrado: '{product_name}'"
                )

            log.info(f"Filtro de produtos validado com sucesso — todos contêm '{PRODUCT}' no nome!")

        else:
            log.error(f"Erro ao retornar produtos da wishlist especificada: {retrieve_products.status_code}: {retrieve_products.text}")
            pytest.fail(f"{retrieve_products.status_code}: {retrieve_products.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar retornar produtos da wishlist especificada: {e}")
        pytest.fail(f"{e}")    

@pytest.mark.api
@pytest.mark.order(20)
def test_retrieve_products_filter_by_status(auth_token):
    """Testando o filtro de produto pelo status is_purchased"""
    log.info("Filtrando os produtos de uma wishlist pelo status is_purchased")

    header = {"Authorization": f"Bearer {auth_token}"}

    try:
        retrieve_products = requests.get(f"{URL}/wishlists/1/products?is_purchased=true", headers=header)

        if retrieve_products.status_code == 200:
            log.info("Produtos retornados com sucesso.")
            assert retrieve_products.status_code == 200
            response_json = retrieve_products.json()
            log.info(f"A resposta da API foi: {response_json}")

        # === Valida se apenas produtos com a tag purchased=true estão na lista ===

            for product in response_json:
                purschased_tag = product.get("is_purchased", "true")
                assert purschased_tag == True, (
                    f"Produto fora do filtro encontrado: '{purschased_tag}'"
                )

            log.info(f"Filtro de produtos validado com sucesso — todos contêm a tag is_purchased=true")

        else:
            log.error(f"Erro ao retornar produtos da wishlist especificada: {retrieve_products.status_code}: {retrieve_products.text}")
            pytest.fail(f"{retrieve_products.status_code}: {retrieve_products.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar retornar produtos da wishlist especificada: {e}")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(21)
def test_retrieve_products_from_another_user_wishlist(new_user_token):
    """Testando se um usuário não pode retornar produtos na wishlist de outro"""
    log.info("Teste retornar produtos da wishlist de outro usuário")

    header = {"Authorization": f"Bearer {new_user_token}"}

    try:
        retrieve_products = requests.get(f"{URL}/wishlists/1/products", headers=header)

        if retrieve_products.status_code == 404:
            log.info("Produtos retornados com sucesso.")
            assert retrieve_products.status_code == 404
            response_json = retrieve_products.json()
            log.info(f"A resposta da API foi: {response_json}")

        else:
            log.error(f"Comportamento inesperado ao retornar produtos da wishlist especificada: {retrieve_products.status_code}: {retrieve_products.text}")
            pytest.fail(f"{retrieve_products.status_code}: {retrieve_products.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar retornar produtos da wishlist especificada: {e}")
        pytest.fail(f"{e}")    