from appium.webdriver.common.appiumby import AppiumBy
from mobile_automation.mobile_pages.base_page_mobile import BaseMethods
from utils.logger import log
import time

class FinishPurchasePage(BaseMethods):
    def __init__(self, driver):
        super().__init__(driver)
        self.email = '//android.view.View[@content-desc="Informe seu e-mail para continuar"]'

    def check_page_msg(self):
        """Checa se está na página de finalizar compra"""
        log.info("Checando se a página é a correta...")
        try:
            email = self.find_element(AppiumBy.XPATH, self.email).get_attribute("content-desc")
            return email

        except Exception as e:
            log.error(f"Ocorreu um erro e o usuário não está na página correta... {e}")
    
    def go_back_to_cart(self):
        log.info("Voltando para a tela da cesta do app...")
        self.driver.back()
        time.sleep(2)
