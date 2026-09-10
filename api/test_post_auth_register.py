import requests
import pytest
import uuid
from utils.logger import log

URL = "http://127.0.0.1:8000"

@pytest.mark.api
@pytest.mark.order(1)
def test_create_new_user_in_the_api():
    """Testando a criação de um novo usuário na API"""
    log.info("Criando um novo usuário...")
    request = (f"{URL}/auth/register")

    # Gera um email único por teste, gera identificadores únicos universais (UUIDs)
    # .hex converte o UUID em uma string hexadecimal contínua 
    # [:8] e [:6] pegam os 8 primeiros e 6 primeiros caracteres
    unique_email = f"usuario_teste_email{uuid.uuid4().hex[:8]}@exemplo.com"

    payload = {
        "email": unique_email,
        "password": "senha123",
        "username": f"usuario_{uuid.uuid4().hex[:6]}"
    }
    try:
        log.info(f"Enviando requisição POST para: {request} com o payload: {payload}")
        response = requests.post(request, json=payload)

        if response.status_code == 200:
            log.info("Usuário criado com sucesso!")
            assert response.status_code == 200

            response_json = response.json()
            log.info(f"A resposta da API foi: {response_json}")

            assert "id" in response_json, "O campo 'id' não foi retornado na resposta"
            assert response_json["id"], "O campo 'id' está vazio"
            log.info("ID validado!")

            assert response_json["email"] == unique_email, (
            f"E-mail incorreto: esperado '{unique_email}', obtido '{response_json['email']}'"
            )
            log.info("Email validado!")

            assert "password" not in response_json, "O campo de senha não deve estar presente na resposta"
            log.info("Senha não está presente!")
            log.info("Usuário criado e validado com sucesso!")

        else:
            log.error(f"Erro ao criar o usuário: {response.status_code}: {response.text}")
            pytest.fail(f"{response.status_code}: {response.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao criar o usuário: {e}")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(2)
def test_existing_user_email():
    """Testando a criação de usuário com um email já cadastrado"""
    log.info("Criando um novo usuário...")
    request = (f"{URL}/auth/register")
    payload = {
        "email": "projeto@example.com",
        "password": "Senha123!",
        "username": "usuarioerrado"
    }
    try:
        log.info(f"Enviando requisição POST para: {request} com o payload: {payload}")
        response = requests.post(request, json=payload)

        if response.status_code == 200:
            log.info("Usuário foi criado com sucesso!")
            response_json = response.json()
            log.info(f"A resposta da API foi: {response_json}")
            assert response.status_code == 200 and response.text == "User registered successfully"

        elif response.status_code == 400:
            log.info("Usuário não pôde ser criado, já existe um usuário com esse email.")
            response_json = response.json()
            log.info(f"A resposta da API foi: {response_json}")
            assert response.status_code == 400 and response_json["detail"] == "Email already registered"

        else:
            log.error(f"Erro ao criar o usuário: {response.status_code}: {response.text}")
            pytest.fail(f"{response.status_code}: {response.text}")

    except Exception as e:
        log.error(f"Ocorreu outro tipo de erro ao criar o usuário: {e}")
        pytest.fail(f"{e}")

@pytest.mark.api
@pytest.mark.order(3)
def test_register_user_invalid_format():
    """Testando a criação de usuário com um formato de email inválido"""
    log.info("Criando um novo usuário...")
    request = (f"{URL}/auth/register")
    payload = {
        "email": "usuariodetestecenario9",
        "password": "senha123",
        "username": "usuariodocenario9"
    }
    try:
        log.info(f"Enviando requisição POST para: {request} com o payload: {payload}")
        response = requests.post(request, json=payload)

        if response.status_code == 422:
            log.info("Validando criação de usuário com formato inválido de email...")
            response_json = response.json()
            log.info(f"A resposta da API foi: {response_json}")
            assert response.status_code == 422
            log.info("O formato do email do usuário é realmente inválido")

        payload_without_password = {
            "email": "usuariodetestecenario10@teste.com",
            "username": "usuariodocenario10"
        }

        log.info(f"Enviando requisição POST para: {request} com o payload: {payload_without_password}")
        response_without_password = requests.post(request, json=payload_without_password)

        if response_without_password.status_code == 422:
            log.info("Validando mensagem de erro de senha faltante...")
            response_without_password_json = response_without_password.json()
            log.info(f"A resposta da API foi: {response_without_password_json}")
            assert response_without_password.status_code == 422
            log.info("A senha não foi inserida pelo usuário")

    except Exception as e:
        log.error(f"Ocorreu um erro durante a criação de usuário {e}")
        pytest.fail(f"{e}")
    


    
