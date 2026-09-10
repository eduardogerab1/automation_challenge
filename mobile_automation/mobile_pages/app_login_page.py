from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from mobile_automation.mobile_pages.base_page_mobile import BaseMethods
from selenium.common.exceptions import TimeoutException
from utils.logger import log
import json
from pathlib import Path
import time

class LoginPage(BaseMethods):
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.login_btn = '//android.view.View[@resource-id="Entrar com e-mail"]'
        self.email_and_password_btn = '//android.widget.Button[@content-desc="Entrar com e-mail e senha"]'
        self.email_field = '//android.widget.EditText[@resource-id="E-mail"]'
        self.password_field = '//android.widget.EditText[@resource-id="Senha"]'
        self.enter_btn = '//android.view.View[@resource-id="Entrar"]'
        self.home_page_btn = '//android.widget.ImageView[@resource-id="home"]'
        self.personal_data_button = '//android.view.View[@content-desc="Editar dados pessoais"]'
        self.email_value = '//android.view.View[@resource-id="E-mail"]'
        self.page_title = '//android.view.View[contains(@content-desc, "entre ou cadastre-se")]'
        self.incorret_password = '//android.view.View[@content-desc="Insira uma senha válida"]'

    def get_page_title(self):
        return self.find_element(AppiumBy.XPATH, self.page_title).get_attribute("content-desc")

    def click_enter_with_mail(self):
        """Clica no botão de entrar com email"""
        log.info("Clicando no botão de entrar com email...")
        try:
            self.click_element(AppiumBy.XPATH, self.login_btn)
            log.info("Botão de entrar com email clicado!")

        except Exception as e:
            log.error(f"Ocorreu um erro ao tentar clicar no botão de entrar com email! {e}")

    def click_enter_with_email_and_password(self):
        """Clica no botão de entrar com email e senha"""
        log.info("Clicando no botão de fazer login com uma conta configurada")
        try:
            self.click_element(AppiumBy.XPATH, self.email_and_password_btn)
            log.info("Botão de entrar com conta criada clicado!")

        except Exception as e:
            log.error(f"Ocorreu um erro ao tentar clicar no botão de entrar com email e senha! {e}")
        
    def log_into_account_valid_credentials(self):
        """Faz o login na conta com as informações corretas"""
        log.info("Iniciando processo de login...")
        try:
            email_field = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.email_field)
            password_field = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.password_field)

            # Carrega o e-mail e senha dos arquivos JSON
            base_path = Path(__file__).resolve().parents[2] / "data"
            with open(base_path / "email.json", encoding="utf-8") as f:
                email = json.load(f)["email"]
            with open(base_path / "passwords.json", encoding="utf-8") as f:
                password = json.load(f)["8_characters_with_all_3_possibilities"]

            # Preenche o formulário
            email_field.click()
            email_field.clear()
            email_field.send_keys(email)
            log.info(f"E-mail '{email}' inserido com sucesso.")

            password_field.click()
            password_field.clear()
            password_field.send_keys(password)
            log.info("Senha inserida com sucesso.")

            # Clica no botão de Login
            self.click_element(AppiumBy.XPATH, self.enter_btn)
            log.info("Botão 'Entrar' clicado com sucesso.")
            log.info("Login realizado com sucesso.")
            return True
        
        except TimeoutException:
            log.error("Timeout: campo de email ou senha não apareceu a tempo.")
            return False

        except Exception as e:
            log.error(f"Ocorreu um erro durante o login: {e}", exc_info=True)
            raise

    def logging_invalid_credentials(self):
        """Faz o login na conta com as informações corretas"""
        log.info("Iniciando processo de login...")
        try:
            email_field = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.email_field)
            password_field = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.password_field)

            # Carrega o e-mail e senha dos arquivos JSON
            base_path = Path(__file__).resolve().parents[2] / "data"
            with open(base_path / "email.json", encoding="utf-8") as f:
                email = json.load(f)["email"]
            with open(base_path / "passwords.json", encoding="utf-8") as f:
                password = json.load(f)["lower_and_upper_case_with_number"]

            # Preenche o formulário
            email_field.click()
            email_field.clear()
            email_field.send_keys(email)
            log.info(f"E-mail '{email}' inserido com sucesso.")

            password_field.click()
            password_field.clear()
            password_field.send_keys(password)
            log.info("Senha inserida com sucesso.")

            # Clica no botão de Login
            self.click_element(AppiumBy.XPATH, self.enter_btn)
            log.info("Botão 'Entrar' clicado com sucesso.")
            log.info("Login realizado com sucesso.")
            return True
        
        except TimeoutException:
            log.error("Timeout: campo de email ou senha não apareceu a tempo.")
            return False

        except Exception as e:
            log.error(f"Ocorreu um erro durante o login: {e}", exc_info=True)
            raise
    
    def click_personal_data(self):
        """Clicando no botão de editar dados pessoais..."""
        try:
            log.info("Abrindo os dados pessoais do usuário")
            self.click_element(AppiumBy.XPATH, self.personal_data_button)
            log.info("Botão clicado com sucesso!")

        except Exception as e:
            log.error(f"Ocorreu um erro ao tentar clicar no botão de dados pessoais {e}")

    def get_user_email(self):
        """Captura o email da tela de dados pessoais..."""
        log.info("Capturando o email...")
        try:
            email = self.get_element_text(AppiumBy.XPATH, self.email_value)
            return email
        
        except Exception as e:
            log.error(f"Ocorreu um erro ao tentar capturar o email do usuário. {e}")

    def get_invalid_password_msg(self):
        """Captura a mensagem de senha errada"""
        log.info("Capturando a mensagem...")
        try:
            incorret_msg = self.find_element(AppiumBy.XPATH, self.incorret_password)
            incorrect_str = incorret_msg.get_attribute("content-desc")
            return incorrect_str

        except Exception as e:
            log.error("Erro ao tentar colocar a senha inválida.")


    

    




