import requests
import pytest
from utils.logger import log

URL = "http://127.0.0.1:8000"

@pytest.mark.api
@pytest.mark.order(4)
def test_user_login():
    """Testando o login de um usuário na API"""
    log.info("Fazendo o login na conta de um usuário existente...")
    request = (f"{URL}/auth/login")

    payload = {
        "email": "projeto@example.com",
        "password": "Senha123!"
    }
    try:
        log.info(f"Enviando requisição POST para: {request} com o payload: {payload}")
        response = requests.post(request, json=payload)

        if response.status_code == 200:
            log.info("Usuário logado com sucesso!")
            assert response.status_code == 200
            response_json = response.json()
            log.info(f"A resposta da API foi: {response_json}")
            log.info("Usuário logado e validado com sucesso!")

        else:
            log.error(f"Erro ao criar o usuário: {response.status_code}: {response.text}")
            pytest.fail(f"{response.status_code}: {response.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao criar o usuário: {e}")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(5)
def test_login_incorrect_password():
    """Testando login de um usuário com senha errada"""
    log.info("Realizando o login...")
    request = (f"{URL}/auth/login")

    payload = {
        "email": "projeto@example.com",
        "password": "123"
    }
    try:
        log.info(f"Enviando requisição POST para: {request} com o payload: {payload}")
        response = requests.post(request, json=payload)

        if response.status_code == 401:
            log.info("Validando senha errada!")
            assert response.status_code == 401
            response_json = response.json()
            log.info(f"A resposta da API foi: {response_json}")

        else:
            log.error(f"Erro ao criar o usuário: {response.status_code}: {response.text}")
            pytest.fail(f"{response.status_code}: {response.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao criar o usuário: {e}")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(6)
def test_login_with_nonexisting_email():
    """Login com um usuário que não existe"""
    log.info("Fazendo login com um usuário inexistente...")
    request_nonexisting_email = (f"{URL}/auth/login")
    payload_nonexisting_email = {
        "email": "emailusuariodocenario13@teste.com",
        "password": "senha123"
    }
    try:
        log.info(f"Enviando requisição POST para: {request_nonexisting_email} com o payload: {payload_nonexisting_email}")
        login_response = requests.post(request_nonexisting_email, json=payload_nonexisting_email)

        if login_response.status_code == 401:
            log.info("Validando senha errada!")
            assert login_response.status_code == 401
            response_json = login_response.json()
            log.info(f"A resposta da API foi: {response_json}")

        else:
            log.error(f"Erro ao criar o usuário: {login_response.status_code}: {login_response.text}")
            pytest.fail(f"{login_response.status_code}: {login_response.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao tentar fazer login: {e}")
        pytest.fail(f"{e}")


