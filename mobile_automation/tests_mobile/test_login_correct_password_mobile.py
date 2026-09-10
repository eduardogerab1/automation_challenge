from mobile_automation.mobile_pages.app_home_page import HomePage
from utils.logger import log
import json
from pathlib import Path
import pytest

@pytest.mark.mobile
def test_login_with_correct_password(driver):
    """Testando login com senha válida"""
    home_page = HomePage(driver)
    home_page.close_permission_notifications()
    log.info("Notificações do sistema fechadas")

    home_page.close_the_banner()
    log.info("Banner fechado!")

    login_page = home_page.navigate_to_login()

    page_title = login_page.get_page_title().lower().strip()
    log.info(f"Título da página capturado: '{page_title}'")
    assert "entre ou cadastre-se" in page_title, (
        f"Título incorreto! Esperado conter 'entre ou cadastre-se', mas obtido '{page_title}'"
    )
    log.info("Tela de login validada com sucesso!")

    login_page.click_enter_with_mail()
    login_page.click_enter_with_email_and_password()

    assert login_page.log_into_account_valid_credentials(), "Ocorreu um erro de login"

    login_page.click_personal_data()

    user_email = login_page.get_user_email().strip().lower()

    # Lê o e-mail salvo no arquivo JSON
    base_path = Path(__file__).resolve().parents[2] / "data"
    with open(base_path / "email.json", encoding="utf-8") as f:
        expected_email = json.load(f)["email"].strip().lower()

    log.info(f"Comparando email exibido '{user_email}' com o esperado '{expected_email}'")

    assert user_email == expected_email, (
        f"O email exibido ('{user_email}') não corresponde ao esperado ('{expected_email}')"
    )


    

