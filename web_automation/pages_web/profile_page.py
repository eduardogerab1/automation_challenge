from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from web_automation.pages_web.base_page_web import BaseMethods
import pyperclip as pc
from utils.logger import log

class ProfilePage(BaseMethods):
    URL = "https://www.americanas.com.br/account#/profile"
    AUTHENTICATION_URL = "https://www.americanas.com.br/account#/authentication"

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.profile_email = "//div[contains(@class, 'emailContainer')]//div[contains(text(), '@')]"
        self.authetication_btn = '//*[@href="#/authentication"]'
        self.set_password_btn = "//div[normalize-space(text())='Definir senha']"
        self.code_field = "//div[contains(@class, 'codeInput_container')]//input[@type='text']"
        self.password_field = "//div[contains(@class, 'newPassInput_container')]//input[@type='password']"
        self.save_password_btn = "//button[.//div[normalize-space(text())='Salvar senha']]"
        self.masked_password = "//div[contains(@class, 'vtex-my-authentication-1-x-maskedPassword_content')]"
        self.logo_btn = "//a[.//img[@alt='Americanas']]"

    def open_page(self):
        """Navigate directly to the profile page"""
        self.navigate(self.URL)
    
    def open_authentication_page(self):
        """Navigate directly to authentication page"""
        self.navigate(self.AUTHENTICATION_URL)
    
    def get_email_on_page(self):
        """armazena o valor do email mostrado no campo de email"""
        try:
            email_element = self.get_element_text(By.XPATH, self.profile_email)
            email_text = email_element.strip()
            log.info(f"The email found was: '{email_text}'")
            return email_text

        except Exception as e:
            log.error(f'Could not find the email: {e}')
    
    def navigate_to_authentication(self):
        try:
            log.info("clicking on the authetication tab...")
            self.wait_for_overlay_to_disappear()
            self.click_element(By.XPATH, self.authetication_btn)
            log.info("authetication tab button clicked!")

            self.wait_for_overlay_to_disappear()
            log.info("clicking on the set password button...")
            self.click_element(By.XPATH, self.set_password_btn)
            log.info("set password button cliked!")

        except Exception as e:
            log.error("Falha ao clicar no botão 'Definir senha'", exc_info=True)
        return False
    
    def paste_new_code_sent_to_mail_on_set_password(self):
        """Cola o código copiado do Temp Mail no campo de código na tela de autenticação."""
        try:
            if "authentication" not in self.driver.current_url:
                log.warning("Not on authentication page, navigating...")
                self.open_authentication_page()
            # Use a longer local wait for this flow
            wait = WebDriverWait(self.driver, 45)
            log.info("Aguardando campo de código ficar disponível...")

            # Ensure the page is fully loaded before searching for dynamic elements
            wait.until(lambda d: d.execute_script("return document.readyState") == 'complete')

            code_input = wait.until(EC.visibility_of_element_located((By.XPATH, self.code_field)))

            if code_input is None:
                raise TimeoutException("Could not find code input field with the selector")

            code_value = pc.paste().strip()
            if not code_value or not code_value.isdigit():
                log.error("Código inválido ou ausente no clipboard: '%s'", code_value)
                return False

            log.info("Código obtido do clipboard: %s", code_value)

            code_input.clear()
            code_input.send_keys(code_value)
            log.info("Código colado com sucesso no campo.")
            return True

        except TimeoutException:
            log.error("Campo de código não apareceu a tempo.")
            return False
        except Exception:
            log.error("Erro ao tentar colar o código no campo de login.", exc_info=True)
            return False
    
    def check_passwords_possibilities(self, data):
        """
        Testa várias combinações de senhas e retorna um dicionário com o estado do botão 'Salvar senha'
        para cada senha.
        """
        results = {}
        try:
            password_input = self.find_element(By.XPATH, self.password_field)

            for key, password in data.items():
                log.info(f"Testando senha '{key}': '{password}'")

                # limpa o campo e digita a senha
                password_input.clear()
                password_input.send_keys(password)

                # verifica o estado do botão
                save_btn = self.find_element_present(By.XPATH, self.save_password_btn)
                is_disabled = save_btn.get_attribute("disabled")

                # guarda o resultado
                results[key] = is_disabled
                log.info(f"Atributo 'disabled' para '{key}': {is_disabled}")
            return results

        except Exception:
            log.error("Erro ao testar as combinações de senha", exc_info=True)
            raise

    def enter_a_valid_password(self, data):
        """Testa o input de uma senha válida e clica no botão de salvar senha"""
        try:
            log.info("Trying to enter a valid password...")

            # Digita a senha válida
            password_input = self.find_element(By.XPATH, self.password_field)
            password_input.clear()
            valid_password = data["8_characters_with_all_3_possibilities"]
            password_input.send_keys(valid_password)
            log.info(f"Password entered: '{valid_password}'")

            # Garante que o botão esteja habilitado antes de clicar
            save_btn = self.find_element(By.XPATH, self.save_password_btn)
            is_disabled = save_btn.get_attribute("disabled")

            if is_disabled:
                log.error("Save Password button is still disabled — password may not meet requirements.")
                raise Exception("Button disabled — cannot save password")

            # Clica no botão
            self.click_element(By.XPATH, self.save_password_btn)
            log.info("Clicked 'Save Password' button successfully!")
            return True

        except Exception as e:
            log.error("Failed to set a valid password", exc_info=True)
            return False

    def validate_the_asterisk_sequence(self):
        try: 
            log.info("Validate that the * sequence appeared after inputing valid password.")
            masked_password = self.find_element(By.XPATH, self.masked_password)
            masked_text = masked_password.text.strip()
            return masked_text
        except Exception as e:
            log.error("The sequence did not appear on the screen")
            return None
        
    def back_to_home_page(self):
        """Clica na logo das americanas para voltar para a home page"""
        try:
            log.info("Tentando retornar para a home page...")
            self.wait_for_overlay_to_disappear()
            self.click_element(By.XPATH, self.logo_btn)
            log.info("Clique na logo realizado com sucesso!")

        except Exception as e:
            log.error(f"Erro ao retornar para a home page: {e}")
    
    
