import requests
import pytest
from utils.logger import log

URL = "http://127.0.0.1:8000"

@pytest.mark.api
@pytest.mark.order(22)
def test_update_a_product(auth_token):
    """Testando se é possível atualizar um produto na wishlist"""
    log.info("Tentando atualizar as informações de um produto...")

    header = {"Authorization": f"Bearer {auth_token}"}

    payload = {
        "Price": "100,00"
    }

    try:
        change_purchased_tag = requests.put(f"{URL}/products/1", json=payload, headers=header)

        if change_purchased_tag.status_code == 200:
            log.info("Dados alterados com sucesso.")
            assert change_purchased_tag.status_code == 200

        else:
            log.error(f"Erro ao tentar alterar dados dos produtos da wishlist especificada: {change_purchased_tag.status_code}: {change_purchased_tag.text}")
            pytest.fail(f"{change_purchased_tag.status_code}: {change_purchased_tag.text}")

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
@pytest.mark.order(23)
def test_update_unexistent_product(auth_token):
    """Testando a atualização de um produto inexistente"""
    log.info("Tentando atualizar um produto que não existe na wishlist...")

    header = {"Authorization": f"Bearer {auth_token}"}

    payload = {
        "Price": "100,00"
    }

    try:
        change_purchased_tag = requests.put(f"{URL}/products/999", json=payload, headers=header)

        if change_purchased_tag.status_code == 404:
            log.info("Não é possível alterar dados do produto, pois o produto não existe na wishlist.")
            assert change_purchased_tag.status_code == 404
            response_json = change_purchased_tag.json()
            log.info(f"A resposta da API foi: {change_purchased_tag.status_code} {response_json}")

        else:
            log.error(f"Comportamento inesperado ao tentar alterar dados dos produtos da wishlist especificada: {change_purchased_tag.status_code}: {change_purchased_tag.text}")
            pytest.fail(f"{change_purchased_tag.status_code}: {change_purchased_tag.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar retornar produtos da wishlist especificada: {e}")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(24)
def test_update_another_user_product(new_user_token):
    """Testando se usuários podem alterar produtos registrados em outras wishlists"""
    log.info("Testando se um usuário pode atualizar os produtos na wishlist de outro")

    header = {"Authorization": f"Bearer {new_user_token}"}

    payload = {
        "Zipcode": "99999999"
    }

    try:
        change_purchased_tag = requests.put(f"{URL}/products/1", json=payload, headers=header)

        if change_purchased_tag.status_code == 404:
            log.info("Não é possível alterar dados do produto, pois o produto não pode ser acessado.")
            assert change_purchased_tag.status_code == 404
            response_json = change_purchased_tag.json()
            log.info(f"A resposta da API foi: {change_purchased_tag.status_code} {response_json}")

        else:
            log.error(f"Comportamento inesperado ao tentar alterar dados dos produtos da wishlist especificada: {change_purchased_tag.status_code}: {change_purchased_tag.text}")
            pytest.fail(f"{change_purchased_tag.status_code}: {change_purchased_tag.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar retornar produtos da wishlist especificada: {e}")
        pytest.fail(f"{e}")