from appium.webdriver.common.appiumby import AppiumBy
from mobile_automation.mobile_pages.base_page_mobile import BaseMethods
from mobile_automation.mobile_pages.cart_page import CartPage
from utils.logger import log
import time

class ProductPage(BaseMethods):
    def __init__(self, driver):
        super().__init__(driver)
        self.product_name_lbl = '//android.view.View[@content-desc and not(@content-desc="")][1]'
        self.zip_code_field = '//android.widget.EditText[@resource-id="Digite o CEP"]'
        self.calculate_btn = '//android.widget.Button[@content-desc="Calcular"]'
        self.error_msg = '//android.view.View[@content-desc="Campo obrigatório"]'
        self.product_search_btn = "//android.widget.ImageView[@clickable='true' and @enabled='true' and @focusable='true'][1]"
        self.product_price_lbl = "(//android.view.View[contains(@content-desc, 'R$') and not(contains(@content-desc, 'x de'))])[last()]"
        self.shipping_info_locator = '//android.view.View[starts-with(@content-desc, "Receba")]'
        self.buy_product_btn = '//android.view.View[@content-desc="comprar"]'
        self.product_qty = '//android.widget.EditText'
        self.plus_btn = '//android.widget.ImageView[@resource-id="Aumentar quantidade em 1"]'
        self.minus_btn = '//android.widget.ImageView[@resource-id="Reduzir quantidade em 1"]'
        self.add_to_cart = '//android.widget.Button[@content-desc="adicionar e continuar comprando"]'
        self.go_to_cart_btn = 'new UiSelector().resourceId("Carrinho")'

    def get_product_name(self):
        log.info("Pegando o nome do produto exibido na tela...")
        el = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.product_name_lbl, timeout=10)
        if el:
            name = el.get_attribute("contentDescription")
            log.info(f"Nome capturado da tela: {name}")
            return name
        else:
            log.error("Elemento do nome do produto não foi encontrado!")
            return ""

    def get_product_price(self):
        log.info("Pegando o preço do produto exibido na tela...")
        el = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.product_price_lbl, timeout=10)
        try:
            price = el.get_attribute("content-desc")
            log.info(f"Preço capturado: {price}")
            return price.strip()

        except Exception as e:
            log.error(f"Erro ao capturar preço do produto: {e}")
            return None

    def invalid_zip_code(self, invalid_zip="123", timeout: int = 5):
        """Testa um CEP inválido e valida a mensagem de erro."""
        log.info(f"Testando CEP inválido '{invalid_zip}' no campo de texto...")
        try:
            # Garante que o campo de CEP esteja visível (faz scroll se necessário)
            self.scroll_down()

            zip_field = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.zip_code_field, timeout)
            if not zip_field:
                raise Exception("Campo de CEP não encontrado após scroll.")

            # Limpa o campo e digita o CEP inválido
            try:
                self.clear_field(AppiumBy.XPATH, self.zip_code_field)
            except Exception:
                pass  # alguns campos não suportam clear()

            zip_field.send_keys(invalid_zip)
            log.info(f"CEP '{invalid_zip}' digitado no campo.")

            # Pressiona o botão 'Calcular'
            try:
                self.click_element(AppiumBy.XPATH, self.calculate_btn)
            except Exception:
                pass

            # Aguarda a mensagem de erro aparecer
            error_el = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.error_msg, timeout)
            if error_el:
                log.info("Mensagem de erro de CEP inválido exibida corretamente.")
                return True
            else:
                log.warning("Nenhuma mensagem de erro foi exibida para o CEP inválido.")
                return False

        except Exception as e:
            log.error(f"Ocorreu um erro ao inserir o CEP inválido: {e}", exc_info=True)
            return False

    def valid_zipcode_from_api(self, valid_zipcode: str, timeout: int = 5):
        """Testa um CEP válido (digitado direto da API)"""
        log.info(f"Testando CEP válido '{valid_zipcode}' no campo de texto.")
        try:
            zip_field = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.zip_code_field, timeout)
            if not zip_field:
                raise Exception("Campo de CEP não encontrado após scroll.")

            # Limpa o campo
            try:
                self.clear_field(AppiumBy.XPATH, self.zip_code_field)
                log.info("Campo de CEP limpo com sucesso.")
            except Exception:
                log.warning("Falha ao limpar campo de CEP (tentando sobrescrever mesmo assim).")

            # Tentativa 1: inserir o CEP diretamente
            try:
                zip_field.click()
                self.driver.execute_script("mobile: performEditorAction", {"action": "focus"})
                zip_field.send_keys(valid_zipcode)
                log.info(f"Tentativa de digitar o CEP via send_keys: {valid_zipcode}")

            except Exception as e:
                log.warning(f"Falha no send_keys: {e}")

            # Pressiona o botão 'Calcular'
            try:
                self.click_element(AppiumBy.XPATH, self.calculate_btn)
            except Exception:
                log.warning("Botão 'Calcular' não clicável — tentando continuar mesmo assim.")

            # Aguarda o retorno da informação de entrega
            delivery_info_element = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.shipping_info_locator, timeout=10)
            delivery_info = delivery_info_element.get_attribute("content-desc")
            log.info(f"Informações de entrega: {delivery_info}")

            return delivery_info

        except Exception as e:
            log.error(f"Ocorreu um erro ao tentar inserir um CEP válido: {e}")
            raise
    
    def check_product_in_the_pop_up(self, product_name: str):
        """Simula a compra de um produto com o popup de compra"""
        log.info(f"Testando a compra do produto {product_name}")
        try:
            #Clica no botão de compra para abrir o popup
            self.click_element(AppiumBy.XPATH, self.buy_product_btn)
            log.info("Botão de compra foi clicado!")

            popup_product_locator = f'//android.widget.ImageView[contains(@content-desc, "{product_name.split()[0]}") and contains(@content-desc, "R$")]'
            popup_element = self.wait_for_visibility_of_element(AppiumBy.XPATH, popup_product_locator)
            popup_content = popup_element.get_attribute("content-desc").replace("\n", " ")
            log.info("Produto checado!")
            return popup_content
            
        except Exception as e:
            log.error(f"Ocorreu um erro ao tentar checar o produto {product_name}. {e}")
            return None
    
    def increase_quantity(self):
        """Aumenta a quantidade do produto que vai ser adicionado ao carrinho"""
        log.info("Aumentando a quantidade do produto...")
        try:
            self.click_element(AppiumBy.XPATH, self.plus_btn)
            qty_element = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.product_qty)
            qty_value = qty_element.text.strip()
            return qty_value
        
        except Exception as e:
            log.error(f"Ocorreu um erro ao aumentar a quantidade do produto... {e}")
            return None

    def decrease_quantity(self):
        """Diminui a quantidade do produto que vai ser adicionado ao carrinho"""
        log.info("Diminuindo a quantidade do produto...")
        try:
            self.click_element(AppiumBy.XPATH, self.minus_btn)
            qty_element = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.product_qty)
            qty_value = qty_element.text.strip()
            return qty_value

        except Exception as e:
            log.error(f"Ocorreu um erro ao diminuir a quantidade do produto... {e}")
            return None
    
    def is_minus_button_disabled(self):
        """Verifica se o botão '-' está visualmente ou funcionalmente desativado."""
        try:
            minus_btn_element = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.minus_btn)

            # Tenta obter múltiplos atributos
            enabled = minus_btn_element.get_attribute("enabled")
            clickable = minus_btn_element.get_attribute("clickable")
            displayed = minus_btn_element.get_attribute("displayed")

            log.info(f"Botão '-' → enabled={enabled}, clickable={clickable}, displayed={displayed}")

            # Considera desativado se algum desses for falso
            if enabled == "false" or clickable == "false" or displayed == "false":
                return True
        
            # Se o clique "não funcionar" (mesmo estando true), testa de forma funcional:
            current_qty = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.product_qty).text.strip()
            minus_btn_element.click()
            time.sleep(1)
            new_qty = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.product_qty).text.strip()

            if current_qty == new_qty:
                log.info("Botão '-' clicado mas quantidade não mudou → funcionalmente desativado.")
                return True

            return False

        except Exception as e:
            log.error(f"Erro ao verificar estado do botão '-': {e}")
            return False

    def add_product_to_cart(self, product_name: str):
        log.info("Adicionando produto ao carrinho...")
        try:
            self.click_element(AppiumBy.XPATH, self.add_to_cart)
            self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.go_to_cart_btn)
            log.info("Produto adicionado ao carrinho!")
            return CartPage(self.driver)

        except Exception as e:
            log.info(f"Ocorreu um erro: {e} ao tentar adicionar o produto {product_name} ao carrinho")

    def go_back_to_home(self):
        log.info("Voltando para a home page do app...")
        self.driver.back()
        self.driver.back()
        self.driver.back()
        self.driver.back()
        self.driver.back()
        time.sleep(2)
    
