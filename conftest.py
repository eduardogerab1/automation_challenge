from selenium import webdriver
from pathlib import Path
import pytest
import time
from selenium.webdriver.chrome.options import Options as ChromeOptions
from utils.logger import log
import requests

LOG_FILE = Path("test_durations.log")

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Setup da duração dos testes"""
    item.start_time = time.time()
    item.start_str = time.strftime("%H:%M:%S", time.localtime())
    msg = f"\n[START] Test '{item.nodeid}' - {item.start_str}"
    print(msg)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")

@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item):
    """Teardown da duração dos testes"""
    duration = time.time() - item.start_time
    msg = f"[END] Test '{item.nodeid}' finished in {duration:.2f} seconds."
    print(msg)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")

@pytest.fixture(scope="session")
def wishlist_data():
    """Obtém token de acesso e retorna os dados da wishlist 'projeto_final'."""
    log.info("Autenticando com a API e passando requisição...")
    base_url = "http://127.0.0.1:8000"

    #1. Autentica e salva o token
    login_payload = {
        "username": "projeto",
        "email": "projeto@example.com",
        "password": "Senha123!"
    }
    try:
        login_response = requests.post(f"{base_url}/auth/login", json=login_payload)
        login_response.raise_for_status()
        token = login_response.json()["access_token"]
    except Exception as e:
        pytest.skip(f"Falha ao autenticar na API: {e}")

    # 2. Faz a requisição autenticada para a wishlist
    headers = {"Authorization": f"Bearer {token}"}
    try:
        #Primeiro, pega a lista de wishlists disponíveis
        wishlist_list_response = requests.get(f"{base_url}/wishlists", headers=headers)
        wishlist_list_response.raise_for_status()
        wishlist_list = wishlist_list_response.json()

        #Seleciona a primeira wishlist (ou filtra pelo nome 'projeto_final')
        wishlist_id = None
        for wl in wishlist_list:
            if wl.get("name") == "projeto_final":
                wishlist_id = wl.get("id")
                break

        if not wishlist_id:
            pytest.skip("Nenhuma wishlist chamada 'projeto_final' foi encontrada na API.")

        #Agora busca os detalhes completos dessa wishlist (com produtos)
        wishlist_details_response = requests.get(f"{base_url}/wishlists/{wishlist_id}/products", headers=headers)
        wishlist_details_response.raise_for_status()
        data = wishlist_details_response.json()
        log.info(f"Wishlist encontrada: {wishlist_id} — buscando detalhes em /wishlists/{wishlist_id}")
        return data

    except Exception as e:
        pytest.skip(f"Falha ao buscar wishlist: {e}")

@pytest.fixture(scope="function")
def driver(request):
    """Cria uma instância local do Chrome"""
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
