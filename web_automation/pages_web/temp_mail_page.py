from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from web_automation.pages_web.base_page_web import BaseMethods
from utils.logger import log
import pyperclip as pc
import time
import re

class TempMail(BaseMethods):

    URL = "https://temp-mail.io/en"

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.page_title = ('//*[@id="__nuxt"]/div[1]/main/h1')
        self.email = '//input[@id="email"]'
        self.copy_btn = ('//*[@id="__nuxt"]/div[1]/main/div[2]/div/div/div/div')
        self.copied_notification = '//*[@id="__nuxt"]/div[3]/div/div'
        self.code_sent_to_mail = ("//span[contains(text(), 'Seu código de acesso é')]")
        self.refresh_btn = "//button[@data-original-title='Refresh for new messages']"

    def open_page(self, new_tab: bool = False):
        """Open the temp-mail page. If new_tab is True, open in a new browser tab."""
        if new_tab:
            # open a new tab and navigate there
            self.open_new_tab(self.URL)
        else:
            self.navigate(self.URL)

    def get_page_title(self):
        return self.get_element_text(By.XPATH, self.page_title)

    def page_title_validation(self):
        title = self.get_page_title()
        return "Free Temporary Email" in title

    def copy_mail(self):
        """Click on the copy email button and return True if clicked"""
        try:
            self.click_element(By.XPATH, self.copy_btn)
            return True
        except Exception:
            log.error("Could not click copy button", exc_info=True)
            return False

    def is_copied_notification_visible(self):
        """Check if the 'Copied!' notification is visible"""
        try:
            element = self.find_element(By.XPATH, self.copied_notification)
            return element.is_displayed() and "Copied" in element.text
        except Exception:
            return False

    def user_email(self):
        """Captura o e-mail visível na tela"""
        # First try to get a valid email from the clipboard (fast and reliable
        # when the copy button has already been used).
        try:
            clipboard = pc.paste().strip()
            if clipboard and re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", clipboard):
                log.info("E-mail temporário obtido do clipboard: %s", clipboard)
                return clipboard
        except Exception:
            # ignore clipboard errors and fall back to DOM lookup
            pass

        # Fallback: try to read the email input on the page using multiple
        # strategies and a short wait.
        selectors = [self.email, "//input[contains(@id, 'email')]", "//input[@type='text' and contains(@class,'mail')]"]
        for sel in selectors:
            try:
                email_input = WebDriverWait(self.driver, 8).until(
                    EC.visibility_of_element_located((By.XPATH, sel))
                )
                email_value = email_input.get_attribute("value") or email_input.text
                if email_value and re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email_value):
                    log.info("E-mail temporário capturado (DOM): %s", email_value)
                    return email_value
            except Exception:
                continue

        log.error("Não foi possível capturar o e-mail temporário.")
        return None

    def copy_the_code_sent_to_mail(self, timeout: int = 60, last_text: str = None):
        """
        Atualiza a caixa de entrada e aguarda até um novo e-mail com código aparecer.
        Retorna o código numérico encontrado ou None se não houver.
        """
        try:
            log.info(f"Aguardando novo e-mail com código (timeout {timeout}s)...")
            end_time = time.time() + timeout
            novo_texto = None

            while time.time() < end_time:
                # Atualiza a caixa de entrada antes de verificar
                log.info("Atualizando a caixa de entrada...")
                self.click_element(By.XPATH, self.refresh_btn)
                time.sleep(3)  # dá tempo pro refresh surtir efeito

                elementos = self.driver.find_elements(By.XPATH, self.code_sent_to_mail)
                if not elementos:
                    log.debug("Nenhum e-mail encontrado ainda.")
                    time.sleep(2)
                    continue

                texto = elementos[0].text.strip()
                if not texto or texto == last_text:
                    log.debug("E-mail ainda não mudou, aguardando novo código...")
                    time.sleep(2)
                    continue

                novo_texto = texto
                break

            if not novo_texto:
                log.error("Nenhum novo e-mail com código foi encontrado a tempo.")
                return None

            log.info(f"Texto encontrado: {novo_texto}")

            # Extrai apenas números
            codigo = ''.join(ch for ch in novo_texto if ch.isdigit())
            if not codigo:
                log.error("Não foi possível extrair um código numérico.")
                return None

            try:
                pc.copy(codigo)
            except Exception:
                log.warning("Falha ao copiar para clipboard.")

            log.info(f"Código copiado: {codigo}")
            return codigo

        except Exception as e:
            log.error(f"Erro ao copiar código: {e}", exc_info=True)
            return None

