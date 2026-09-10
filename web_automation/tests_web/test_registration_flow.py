from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from web_automation.pages_web.home_page import HomePage
from web_automation.pages_web.temp_mail_page import TempMail
from utils.logger import log
import json
from pathlib import Path
import time
import pytest

@pytest.mark.web
def test_registration_flow(driver):
    """Test the complete flow from homepage to temp-mail"""
    # 1. Start at home page
    home_page = HomePage(driver)
    home_page.open_page()
    log.info('Home page opened successfully')
    
    # 2. Close the banner
    home_page.close_banner()
    log.info('Banner closed successfully')
    
    # 3. Navigate to login page
    login_page = home_page.navigate_to_login_page()
    assert "login" in login_page.driver.current_url, "Failed to navigate to login page"
    main_window = driver.current_window_handle
    log.info('Navigated to login page')
    
    # 4. Open temp-mail in new tab
    temp_mail_page = TempMail(driver)
    temp_mail_page.open_page(new_tab=True)
    log.info('Opened temp-mail in new tab')
    assert temp_mail_page.page_title_validation(), "Temp-mail page title is not correct"
    log.info('Temp-mail page verified')
    
    # 5. Copy the email
    copied = temp_mail_page.copy_mail()
    assert copied, "Failed to copy email"
    log.info('Email copied successfully')

    # 6. Storing generated email
    email_gerado = temp_mail_page.user_email()
    assert email_gerado is not None, "Failed to capture generated temporary email"
    log.info(f"Temporary email stored for validation: {email_gerado}")
    
    # 7. Verify copied notification
    assert temp_mail_page.is_copied_notification_visible(), "Copy notification did not appear"
    log.info('Copy notification verified')
    
    # 8. Switch back to login page 
    driver.switch_to.window(main_window)
    log.info('Switched back to login page')
    assert "login" in driver.current_url, "Not back on login page"
    log.info('Back on login page, ready for registration')

    # 9. Paste the copied content on the "email" field
    login_page.paste_email_on_field()
    log.info('Email pasted onto the field')
    el = login_page.find_element(By.XPATH, login_page.email_field)
    email_value = el.get_attribute("value") or el.text
    assert email_value and "@" in email_value, f"Email was not pasted correctly: '{email_value}'"
    log.info(f'Email pasted onto the field: {email_value}')

    # 10. Switch back to the temp mail window
    driver.switch_to.window(driver.window_handles[-1])
    log.info('Switched back to temp mail page')
    assert "temp-mail" in driver.current_url, "Not back on temp mail page"
    log.info('Back on temp mail page, ready to go on')

    # 11. Copy the code sent to the email
    log.info(f"Current URL before trying to copy code: {driver.current_url}")
    codigo = temp_mail_page.copy_the_code_sent_to_mail(timeout=30)
    assert codigo is not None, "Failed to copy code from temp-mail"
    log.info("Code copied successfully: %s", codigo)

    # 12. switch back to the login page
    driver.switch_to.window(main_window)
    log.info('Switched back to login page')
    # Wait for page to be fully loaded after switch
    WebDriverWait(driver, 20).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )
    assert "login" in driver.current_url, "Not back on login page"
    log.info('Back on login page, ready for registration')

    # 13. paste the code on the field
    login_page.paste_code_sent_to_mail_on_code_field()
    log.info('Code pasted onto the field')
    code_el = login_page.find_element(By.XPATH, login_page.code_field)
    code_value = code_el.get_attribute("value") or code_el.text
    assert code_value and code_value.strip().isdigit(), f"Code was not pasted correctly: '{code_value}'"

    # 14. click on the confirm button and verify if we're back to the homepage
    login_page.end_registration()
    assert home_page.find_the_logo(), "Redirection failed — logo not found on homepage"
    log.info("Redirection to homepage confirmed successfully!")

    # 15. check if the user email is the same
    temp_mail = email_gerado
    WebDriverWait(driver, 20).until(
    lambda d: temp_mail.split('@')[0] in home_page.get_logged_user_email()
    )
    header_mail = home_page.get_logged_user_email()
    assert temp_mail is not None, "Temporary email not available for comparison"
    assert temp_mail.split('@')[0] in header_mail, f"O e-mail '{temp_mail}' não foi encontrado no header: '{header_mail}'"
    log.info("The email is the same!")

    # 16. navigate to the profile page
    profile_page = home_page.navigate_to_profile_page()
    WebDriverWait(driver, 20).until(
        lambda d: "profile" in d.current_url
    )
    assert "profile" in driver.current_url, "Not on the profile page"

    # 17. verify if the email on the profile page is correct
    actual_email = profile_page.get_email_on_page()
    expected_email = email_gerado
    assert actual_email == expected_email, (
        f"O e-mail exibido no perfil ('{actual_email}') "
        f"é diferente do e-mail gerado ('{expected_email}')"
    )

    # 18. click on the authentication button
    profile_page.navigate_to_authentication()
    assert 'authentication' in driver.current_url, "Not on authentication tab"
    main_window = driver.current_window_handle

    # 19. switch back to the temp mail page
    driver.switch_to.window(driver.window_handles[-1])
    log.info('Switched back to temp mail page')
    assert "temp-mail" in driver.current_url, "Not back on temp mail page"
    log.info('Back on temp mail page, ready to go on')
    time.sleep(10)

    # 20. copy the new code
    log.info(f"Current URL before trying to copy code: {driver.current_url}")
    codigo = temp_mail_page.copy_the_code_sent_to_mail(timeout=30)
    assert codigo is not None, "Failed to copy code from temp-mail"
    log.info("Code copied successfully: %s", codigo)

    # 21. switch back to the authentication page
    driver.switch_to.window(main_window)
    assert 'authentication' in driver.current_url, "Not on authentication tab"

    # 22. paste the new code onto the field
    profile_page.paste_new_code_sent_to_mail_on_set_password()
    log.info("pasting the new code onto the field")
    code_el = profile_page.find_element(By.XPATH, profile_page.code_field)
    code_value = code_el.get_attribute("value") or code_el.text
    assert code_value and code_value.strip().isdigit(), f"Code was not pasted correctly: '{code_value}'"

    # 23. Check all password possibilities
    passwords_path = Path("data/passwords.json")
    with passwords_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    log.info("Verificando comportamento do botão com diferentes combinações de senha")
    results = profile_page.check_passwords_possibilities(data)
    assert results["lower_case_letter"] is not None, "Botão deveria estar desabilitado (somente minúsculas)"
    assert results["lower_and_upper_case"] is not None, "Botão deveria estar desabilitado (maiúscula + minúscula)"
    assert results["lower_and_upper_case_with_number"] is not None, "Botão deveria estar desabilitado (letras + número)"
    assert results["8_characters_with_all_3_possibilities"] is None, "Botão deveria estar habilitado (senha válida)"
    log.info("Todos os comportamentos de senha foram validados com sucesso!")

    # 24. Enter a valid password
    log.info("Setting a valid password and saving it...")
    is_success = profile_page.enter_a_valid_password(data)
    assert is_success, "Failed to set a valid password — button might be disabled."
    log.info("Password saved successfully!")

    # 25 Checking if the * sequence appeared on the screen
    masked_text = profile_page.validate_the_asterisk_sequence()
    assert masked_text and "*" in masked_text, "Password masking not found (expected asterisks)."
    log.info("* sequence validated!")

    # 26 Back to the home page
    profile_page.back_to_home_page()
    assert home_page.find_the_logo()
    log.info("Back to the home page!")



    






