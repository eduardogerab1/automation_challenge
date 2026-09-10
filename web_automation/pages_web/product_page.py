from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_automation.pages_web.base_page_web import BaseMethods
from utils.logger import log

class ProductPage(BaseMethods):
    
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
    
    def get_product_name(self):
        """Retorna o nome do produto na página de detalhes."""
        try:
            xpath_title = "//h1[contains(@class, 'ProductInfoCenter_title__')]"
            log.info("Aguardando título do produto ficar visível...")
            element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath_title)))
            self.product_name = element.text.strip()
            log.info(f"Título encontrado: {self.product_name}")
            return self.product_name
        except Exception as e:
            log.error(f"Erro ao capturar o título do produto: {e}", exc_info=True)
            return None

    def get_product_price(self):
        """Retorna o preço do produto na página de detalhes."""
        try:
            xpath_price = "//div[contains(@class, 'ProductPrice_productPrice__')]"
            log.info("Aguardando preço do produto ficar visível...")
            element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath_price)))
            # remove caracteres não numéricos (se necessário) depois
            self.product_price = element.text.strip()
            log.info(f"Preço encontrado: {self.product_price}")
            return self.product_price
        except Exception as e:
            log.error(f"Erro ao capturar o preço do produto: {e}", exc_info=True)
            return None