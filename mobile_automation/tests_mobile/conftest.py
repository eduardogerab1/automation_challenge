import pytest
import requests
from appium import webdriver
from appium.options.common.base import AppiumOptions
from utils.logger import log

@pytest.fixture(scope="session")
def wishlist_data():
    log.info("Autenticando com a API e passando requisição...")
    """Obtém token de acesso e retorna os dados da wishlist 'projeto_final'."""
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
def driver():
    # --- SETUP PHASE ---
    log.info("Inicializando driver Appium para testes mobile...")
    options = AppiumOptions()
    options.load_capabilities({
        "platformName": "Android",
        "deviceName": "emulator-5554",
        "appPackage": "com.b2w.americanas",
        "appActivity": "com.b2w.americanas.MainActivity",
        "automationName": "UiAutomator2",
        "noReset": False,
        "fullReset": False,
        "unicodeKeyboard": True,
        "resetKeyboard": True
})

    try:
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        driver.implicitly_wait(10)
    except Exception as e:
        pytest.skip(f"Failed to create Appium driver: {e}")

    yield driver
    # --- TEARDOWN PHASE ---
    log.info("Quitting appium driver...")
    driver.quit()
