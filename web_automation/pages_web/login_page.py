from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from web_automation.pages_web.base_page_web import BaseMethods
from utils.logger import log
import pyperclip as pc
from pathlib import Path
import json
import time

class LoginPage(BaseMethods):

    URL = "https://www.americanas.com.br/login"

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.login_title = '//h2[contains(text(), "login do cliente")]'
        self.email_field = (
        '//input[contains(@class, "vtex-styleguide-9-x-input") '
        'and contains(@placeholder, "exemplo@mail.com")]'
        )
        self.password_field = (
        '//input[contains(@class, "vtex-styleguide-9-x-input") '
        'and @type="password"]'
        )
        self.code_field = '//input[contains(@placeholder, "código") or contains(@aria-label, "código")]'

        # Centralized fallback selectors for the verification/code input
        self.code_input_selectors = [
            self.code_field,
            "//input[contains(@class, 'code')]",
            "//input[contains(@class, 'verification')]",
            "//form//input[not(@type='email')]"
        ]
        self.enter_btn = '//button[contains(@type, "submit")]'
        self.user_and_password_btn = '//button[.//span[contains(text(), "Entrar com email e senha")]]'
        self.confirm_code_btn = '//button[contains(text(), "Confirmar") or contains(@type, "submit")]'
        self.login_btn = '//button[@type="submit" and (contains(., "Entrar") or contains(., "Login"))]'
        self.wrong_password_alert = '//div[contains(text(), "Usuário") and contains(text(), "senha")]'

    def open_page(self):
        """Navigate directly to the login page"""
        self.navigate(self.URL)
  
    def get_login_title(self):
        return self.get_element_text(By.XPATH, self.login_title)

    def login_title_validation(self):
        title = self.get_login_title()
        return "login do cliente" in title

    def click_enter_btn(self):
        """Click the enter button to create an account"""
        try:
            self.wait_for_overlay_to_disappear()
            # Ensure we're on the login page
            if "login" not in self.driver.current_url:
                log.warning("Not on login page, navigating...")
                self.open_page()

            # Try to click the login button
            self.click_element(By.XPATH, self.enter_btn)
            return True
        except Exception as e:
            log.error("failed to click login button", exc_info=True)
            raise

    def paste_email_on_field(self):
        try:
            if "login" not in self.driver.current_url:
                log.warning("Not on login page, navigating...")
                self.open_page()

            email_value = pc.paste()  # Get the email from clipboard
            self.find_element(By.XPATH, self.email_field).send_keys(email_value)
            self.find_element(By.XPATH, self.email_field).send_keys(Keys.ENTER)
        except Exception as e:
            log.error('could not paste the email onto the field correctly')

    def paste_code_sent_to_mail_on_code_field(self):
        """Cola o código copiado do Temp Mail no campo de código na tela de login."""
        try:
            if "login" not in self.driver.current_url:
                log.warning("Not on login page, navigating...")
                self.open_page()
            # Use a longer local wait for this flow
            wait = WebDriverWait(self.driver, 45)
            log.info("Aguardando campo de código e botão de confirmação ficarem disponíveis...")

            # Ensure the page is fully loaded before searching for dynamic elements
            wait.until(lambda d: d.execute_script("return document.readyState") == 'complete')

            # Find the first visible & enabled selector from the list
            code_input = None
            for xpath in self.code_input_selectors:
                try:
                    elm = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                    if elm.is_enabled():
                        code_input = elm
                        self.code_field = xpath  # remember the working selector
                        log.info("Found code input field using selector: %s", xpath)
                        break
                except Exception:
                    # element didn't appear with this selector; try next
                    continue

            if code_input is None:
                raise TimeoutException("Could not find code input field with any selector")

            code_value = pc.paste().strip()
            if not code_value or not code_value.isdigit():
                log.error("Código inválido ou ausente no clipboard: '%s'", code_value)
                return False

            log.info("Código obtido do clipboard: %s", code_value)

            code_input.clear()
            code_input.send_keys(code_value)
            log.info("Código colado com sucesso no campo.")

            # Wait for and click the confirm button using the same wait
            confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, self.confirm_code_btn)))
            confirm_button.click()
            log.info("Botão de confirmação clicado com sucesso.")
            return True

        except TimeoutException:
            log.error("Campo de código ou botão de confirmação não apareceu a tempo.")
            return False
        except Exception:
            log.error("Erro ao tentar colar o código no campo de login.", exc_info=True)
            return False
    
    def end_registration(self):
        try:
            # Ensure we're on the login page
            if "login" not in self.driver.current_url:
                log.warning("Not on login page, navigating...")
                self.open_page()
            
            old_url = self.driver.current_url

            # Try to click the confim button
            self.click_element(By.XPATH, self.confirm_code_btn)
            log.info("Confirm button clicked. Waiting to be redirected...")

            # Espera até a URL mudar (máx 10 segundos)
            WebDriverWait(self.driver, 10).until(EC.url_changes(old_url))
            log.info("Redirection detected — login successful.")
            return True

        except Exception as e:
            log.error("failed to click confirm button", exc_info=True)
            raise

    def enter_with_user_and_password(self):
        """Função para clicar no botão de login com senha."""
        try:
            log.info("Clicando no botão de login com usuário e senha")
            self.click_element(By.XPATH, self.user_and_password_btn)

        except Exception as e:
            log.error(f"Erro ao clicar no botão de login com senha: {e}")

    def existing_user_login(self):
        """Faz login com usuário e senha já existentes."""
        try:
            log.info("Iniciando login com email e senha...")

            # Aguarda o React renderizar o novo formulário (o anterior deve sumir)
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            time.sleep(2)

            # Aguarda o campo de email aparecer (tela anterior deve desaparecer)
            log.info("Aguardando campo de e-mail do formulário de login aparecer...")
            email_field = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.email_field))
            )
            password_field = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.password_field))
            )

            log.info("Campos de login localizados — preenchendo credenciais.")

            # Carrega o e-mail e senha dos arquivos JSON
            base_path = Path(__file__).resolve().parents[2] / "data"
            with open(base_path / "email.json", encoding="utf-8") as f:
                email = json.load(f)["email"]
            with open(base_path / "passwords.json", encoding="utf-8") as f:
                password = json.load(f)["8_characters_with_all_3_possibilities"]

            # Preenche o formulário
            email_field.clear()
            email_field.send_keys(email)
            log.info(f"E-mail '{email}' inserido com sucesso.")

            password_field.clear()
            password_field.send_keys(password)
            log.info("Senha inserida com sucesso.")

            # Clica no botão de login
            self.click_element(By.XPATH, self.login_btn)
            log.info("Botão 'Entrar' clicado com sucesso.")
            log.info("Login realizado com sucesso.")
            return True

        except TimeoutException:
            log.error("Timeout: campo de email ou senha não apareceu a tempo.")
            return False

        except Exception as e:
            log.error(f"Ocorreu um erro durante o login: {e}", exc_info=True)
            raise

    def existing_user_wrong_password(self):
        """Faz login com usuário já existente e senha errada."""
        try:
            log.info("Iniciando login com email e senha...")

            # Aguarda o React renderizar o novo formulário (o anterior deve sumir)
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            time.sleep(2)

            # Aguarda o campo de email aparecer (tela anterior deve desaparecer)
            log.info("Aguardando campo de e-mail do formulário de login aparecer...")
            email_field = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.email_field))
            )
            password_field = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.password_field))
            )

            log.info("Campos de login localizados — preenchendo credenciais.")

            # Carrega o e-mail e senha dos arquivos JSON
            base_path = Path(__file__).resolve().parents[2] / "data"
            with open(base_path / "email.json", encoding="utf-8") as f:
                email = json.load(f)["email"]
            with open(base_path / "passwords.json", encoding="utf-8") as f:
                password = json.load(f)["lower_and_upper_case_with_number"]

            # Preenche o formulário
            email_field.clear()
            email_field.send_keys(email)
            log.info(f"E-mail '{email}' inserido com sucesso.")

            password_field.clear()
            password_field.send_keys(password)
            log.info("Senha inserida com sucesso.")

            # Clica no botão de login 
            self.click_element(By.XPATH, self.login_btn)
            log.info("Botão 'Entrar' foi clicado com sucesso.")
            self.find_element(By.XPATH, self.wrong_password_alert)
            log.info("A mensagem apareceu")
            return True

        except TimeoutException:
            log.error("Timeout: campo de email ou senha não apareceu a tempo.")
            return False

        except Exception as e:
            log.error(f"Ocorreu um erro durante o login: {e}", exc_info=True)
            raise