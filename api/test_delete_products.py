import requests
import pytest
from utils.logger import log

URL = "http://127.0.0.1:8000"

@pytest.mark.api
@pytest.mark.order(25)
def test_delete_product_from_wishlist(new_user_token):
    """Tentando deletar um produto da wishlist especificada"""
    log.info("Deletando produto da wishlist...")

    header = {"Authorization": f"Bearer {new_user_token}"}

    try:
        delete_product = requests.delete(f"{URL}/products/4", headers=header)

        if delete_product.status_code == 204:
            log.info("Produto deletado com sucesso.")
            assert delete_product.status_code == 204
            log.info("A API retornou 204 No Content")

        elif delete_product.status_code == 404:
            log.info("O produto já foi deletado. Prosseguindo com os testes...")
            assert delete_product.status_code == 404
            response_json = delete_product.json()
            log.info(f"A resposta da API foi: {response_json}")

        else:
            log.error(f"Erro ao tentar apagar os produtos da wishlist especificada: {delete_product.status_code}: {delete_product.text}")
            pytest.fail(f"{delete_product.status_code}: {delete_product.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar apagar os produtos da wishlist especificada: {e}")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(26)
def test_delete_non_existent_product(new_user_token):
    """Testando deletar um produto que não existe"""
    log.info("Deletando produto inexistente...")

    header = {"Authorization": f"Bearer {new_user_token}"}

    try:
        delete_product = requests.delete(f"{URL}/products/9999", headers=header)

        if delete_product.status_code == 404:
            log.info("O produto não existe")
            assert delete_product.status_code == 404
            response_json = delete_product.json()
            log.info(f"A resposta da API foi: {response_json}")
        else:
            log.error(f"Comportamento inesperado ao tentar apagar produtos que não existem: {delete_product.status_code}: {delete_product.text}")
            pytest.fail(f"{delete_product.status_code}: {delete_product.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar apagar os produtos da wishlist especificada: {e}")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(27)
def test_delete_another_user_product(new_user_token):
    """Testando deletar produtos de outro usuário"""
    log.info("Deletando produtos pertencentes a outro usuário...")

    header = {"Authorization": f"Bearer {new_user_token}"}

    try:
        delete_product = requests.delete(f"{URL}/products/1", headers=header)

        if delete_product.status_code == 404:
            log.info("O produto não pode ser deletado porque está na wishlist de outra pessoa.")
            assert delete_product.status_code == 404
            response_json = delete_product.json()
            log.info(f"A resposta da API foi: {response_json}")
        else:
            log.error(f"Comportamento inesperado ao tentar apagar produtos que não existem: {delete_product.status_code}: {delete_product.text}")
            pytest.fail(f"{delete_product.status_code}: {delete_product.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar apagar os produtos da wishlist especificada: {e}")
        pytest.fail(f"{e}")