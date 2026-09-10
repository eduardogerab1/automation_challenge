from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import log
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
import unicodedata
import re

class BaseMethods:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find_element(self, by, locator):
        return self.wait.until(EC.presence_of_element_located((by, locator)))
    
    def find_elements(self, by, locator):
        return self.wait.until(EC.presence_of_all_elements_located((by, locator)))
    
    def clear_field(self, by, locator):
        """Força limpeza total de campos EditText, mesmo com máscara."""
        try:
            element = self.wait_for_visibility_of_element(by, locator)
            if not element:
                log.warning(f"Elemento {locator} não encontrado para limpeza.")
                return

            log.info(f"Tentando limpar campo com locator: {locator}")
            element.click()

            # Tenta pegar o texto atual
            current_text = ""
            try:
                current_text = element.text or ""
                log.info(f"Texto atual do campo antes de limpar: '{current_text}'")
            except Exception:
                log.warning("Não foi possível capturar texto do campo antes do clear().")

            # .clear() padrão
            element.clear()
            self.driver.implicitly_wait(1)

            # Se ainda sobrou texto, força backspace
            if current_text:
                for _ in range(len(current_text)):
                    self.driver.press_keycode(67)  # KEYCODE_DEL
                log.info("Texto apagado manualmente com BACKSPACE loop.")

            # Verifica se realmente ficou vazio
            try:
                remaining = element.text
                if remaining:
                    log.warning(f"O campo ainda contém texto: '{remaining}' — tentando apagar novamente.")
                    for _ in range(len(remaining)):
                        self.driver.press_keycode(67)
                else:
                    log.info("Campo de texto completamente limpo!")
            except Exception:
                log.warning("Não foi possível verificar o texto após limpar.")

        except Exception as e:
            log.error(f"Erro ao limpar o campo {locator}: {e}", exc_info=True)

    def is_enabled(self, by, locator):
        try:
            return self.find_element(by, locator).is_enabled()
        except:
            return False
    
    def wait_for_element_to_be_clickable(self, by, locator):
        return self.wait.until(EC.element_to_be_clickable((by, locator)))

    def click_element(self, by, locator):
        log.info(f"Clicking element with locator: {locator}")
        try:
            self.wait_for_element_to_be_clickable(by, locator).click()
            log.info("Element clicked successfully.")
        except Exception as e:
            log.error(f"Failed to click element with locator: {locator}", exc_info=True)
            raise

    def send_keys_to_element(self, by, locator, text):
        self.find_element(by, locator).send_keys(text)

    def get_element_text(self, by, locator):
        return self.find_element(by, locator).text
    
    def get_elements_text(self, by, locator):
        try:
            elements = self.find_elements(by, locator)
            texts = [el.text for el in elements if el.text.strip() != ""]
            log.info(f"Textos capturados de {locator}: {texts}")
            return texts
        except Exception as e:
            log.error(
                f"Falha ao capturar textos dos elementos com locator: {locator}", 
                exc_info=True
            )
            return []
    
    def wait_for_visibility_of_element(self, by, locator, timeout=10):
        """Espera até que o elemento esteja visível na tela."""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.visibility_of_element_located((by, locator)))
            log.info(f"Elemento visível: {locator}")
            return element
        except TimeoutException:
            log.error(f"Elemento não ficou visível dentro de {timeout} segundos: {locator}")
            return None
        except StaleElementReferenceException:
            log.error("o elemento foi localizado antes, mas agora não pode mais ser acessado.")
            return None
        except NoSuchElementException:
            log.error("O elemento sendo requisitado não existe na tela.")
            return None

    def scroll_down(self):
        """Scroll suave para baixo."""
        log.info("Executando scroll suave para baixo...")

        try:
            size = self.driver.get_window_size()
            width = size["width"]
            height = size["height"]

            start_x = width // 2
            start_y = int(height * 0.75)  # perto da parte inferior
            end_y = int(height * 0.45)    # sobe até o meio

            self.driver.swipe(start_x, start_y, start_x, end_y, 400)  # 400ms -> suave e controlado
            log.info("Scroll suave realizado!")

        except Exception as e:
            log.error(f"Falha ao realizar o scroll: {e}")

    @staticmethod
    def normalize(text):
        if not text:
            return ""
        text = unicodedata.normalize("NFKD", text)
        text = "".join(c for c in text if not unicodedata.combining(c))
        return " ".join(text.lower().split())





        

