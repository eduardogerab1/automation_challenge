from mobile_automation.mobile_pages.app_home_page import HomePage
from mobile_automation.mobile_pages.base_page_mobile import BaseMethods
from utils.logger import log
import pytest

@pytest.mark.mobile
def test_login_with_incorrect_password(driver):
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

    assert login_page.logging_invalid_credentials()

    msg = BaseMethods.normalize(login_page.get_invalid_password_msg())
    assert msg == "insira uma senha valida"