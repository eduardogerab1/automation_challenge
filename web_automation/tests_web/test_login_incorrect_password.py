from web_automation.pages_web.home_page import HomePage
from utils.logger import log
import pytest

@pytest.mark.web
def test_login_with_invalid_password(driver):
    """Testando login com senha inválida"""
    home_page = HomePage(driver)
    home_page.open_page()
    log.info("A home page do site foi aberta!")

    home_page.close_banner()
    log.info('Banner closed successfully')

    login_page = home_page.navigate_to_login_page()
    assert "login" in login_page.driver.current_url, "Failed to navigate to login page"
    log.info('Navigated to login page')

    login_page.enter_with_user_and_password()

    assert login_page.existing_user_wrong_password(), "Erro no login"