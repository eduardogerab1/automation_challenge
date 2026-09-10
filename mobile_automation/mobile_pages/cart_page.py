from appium.webdriver.common.appiumby import AppiumBy
from mobile_automation.mobile_pages.base_page_mobile import BaseMethods
from mobile_automation.mobile_pages.finish_purchase_page import FinishPurchasePage
from utils.logger import log
import re

class CartPage(BaseMethods):
    def __init__(self, driver):
        super().__init__(driver)
        self.product_name_in_cart = '//android.widget.ImageView[@resource-id="Card Produto"]'
        self.product_price_in_cart = '(//android.view.View[contains(@content-desc, "R$")])[1]'
        self.product_qty_in_cart = '//android.widget.EditText'
        self.finish_purchase_btn = '//android.view.View[contains(@content-desc, "fechar pedido")]'
        self.zipcode_in_cart = '//android.widget.EditText[@resource-id="Digite o CEP"]'
        self.shipping_info_in_cart = '//android.view.View[starts-with(@content-desc, "Receba")]'
        self.calculate_btn_in_cart = '//android.widget.Button[@content-desc="Calcular"]'
        self.error_msg_in_cart = '//android.view.View[@content-desc="Campo obrigatório"]'
        self.clear_cart_btn = '//android.view.View[@resource-id="Limpar carrinho"]'
        self.confirm_clear_btn = '//android.widget.Button[@content-desc="Remover e continuar"]'
        self.empty_cart = '//android.view.View[@content-desc="sua cesta está vazia"]'

    def get_product_name_in_cart(self):
        log.info("Pegando o nome do produto exibido no carrinho...")
        try:
            el = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.product_name_in_cart, timeout=10)
            name = el.get_attribute("contentDescription")
            log.info(f"Nome capturado no carrinho: {name}")
            return name.strip()

        except Exception as e:
            log.error(f"Erro ao capturar o nome do produto: {e}")
            return ""

    def get_product_price_in_cart(self):
        log.info("Pegando o preço do produto exibido no carrinho...")

        el = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.product_price_in_cart, timeout=10)
        try:
            price_str = el.get_attribute("content-desc")

            if not price_str:
                raise ValueError("Elemento encontrado, mas sem atributo 'content-desc'.")

            log.info(f"Preço capturado (raw): {price_str}")

            # Se tiver múltiplas linhas (caso com promo), split
            parts = price_str.split("\n")

            # Regra: se existir linha começando com "Por", ela é o preço válido
            selected = None
            for p in parts:
                if p.strip().startswith("Por"):
                    selected = p
                    break

            # Se não achou preço "Por", usa a primeira linha com "R$"
            if not selected:
                selected = next((p for p in parts if "R$" in p), parts[0])

            log.info(f"Linha selecionada para preço: {selected}")

            # Normalização
            clean = re.sub(r"[^\d,]", "", selected)
            price_float = float(clean.replace(".", "").replace(",", "."))

            log.info(f"Preço convertido para float: {price_float}")
            return price_float

        except Exception as e:
            log.error(f"Erro ao capturar preço do produto: {e}", exc_info=True)
            return None

    def check_quantity_in_cart(self):
        log.info("Checando a quantidade do produto no carrinho...")
        el = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.product_qty_in_cart, timeout=10)
        try:
            qty_text = el.get_attribute("text").strip()
            log.info(f"Quantidade capturada (texto): {qty_text}")

            # Conversão para inteiro
            qty_int = int(qty_text)
            log.info(f"Quantidade convertida para inteiro: {qty_int}")
            return qty_int

        except ValueError:
            log.error(f"Não foi possível converter a quantidade '{qty_text}' para inteiro.")
            return None

        except Exception as e:
            log.error(f"Erro ao capturar a quantidade do produto: {e}")
            return None
    
    def invalid_zip_code(self, invalid_zip="123", timeout: int = 5):
        """Testa um CEP inválido e valida a mensagem de erro."""
        log.info(f"Testando CEP inválido '{invalid_zip}' no campo de texto...")
        try:
            zip_field = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.zipcode_in_cart, timeout)
            if not zip_field:
                raise Exception("Campo de CEP não encontrado após scroll.")

            # Limpa o campo e digita o CEP inválido
            try:
                self.clear_field(AppiumBy.XPATH, self.zipcode_in_cart)
            except Exception:
                pass  # alguns campos não suportam clear()

            zip_field.send_keys(invalid_zip)
            log.info(f"CEP '{invalid_zip}' digitado no campo.")

            # Pressiona o botão 'Calcular'
            try:
                self.click_element(AppiumBy.XPATH, self.calculate_btn_in_cart)
            except Exception:
                pass

            # Aguarda a mensagem de erro aparecer
            error_el = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.error_msg_in_cart, timeout)
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
            zip_field = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.zipcode_in_cart, timeout)
            if not zip_field:
                raise Exception("Campo de CEP não encontrado após scroll.")

            # Limpa o campo
            try:
                self.clear_field(AppiumBy.XPATH, self.zipcode_in_cart)
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
                self.click_element(AppiumBy.XPATH, self.calculate_btn_in_cart)
            except Exception:
                log.warning("Botão 'Calcular' não clicável — tentando continuar mesmo assim.")

            # Aguarda o retorno da informação de entrega
            delivery_info_element = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.shipping_info_in_cart, timeout=10)
            delivery_info = delivery_info_element.get_attribute("content-desc")
            log.info(f"Informações de entrega: {delivery_info}")

            return delivery_info

        except Exception as e:
            log.error(f"Ocorreu um erro ao tentar inserir um CEP válido: {e}")
            raise
    
    def finish_purchase(self):
        """Finaliza a compra do produto"""
        log.info("Finalizando a compra...")
        try:
            self.click_element(AppiumBy.XPATH, self.finish_purchase_btn)
            return FinishPurchasePage(self.driver)

        except Exception as e:
            log.error(f"Houve uma falha ao finalizar a compra. {e}")

    def clear_cart(self):
        """Limpa a cesta"""
        log.info("Limpando a cesta para as próximas compras...")
        try:
            self.click_element(AppiumBy.XPATH, self.clear_cart_btn)
            self.click_element(AppiumBy.XPATH, self.confirm_clear_btn)
            msg = self.find_element(AppiumBy.XPATH, self.empty_cart).get_attribute("content-desc")
            return msg

        except Exception as e:
            log.error(f"Houve um erro ao tentar limpar a cesta. {e}")


    
