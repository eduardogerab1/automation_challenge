from appium.webdriver.common.appiumby import AppiumBy
from mobile_automation.mobile_pages.base_page_mobile import BaseMethods
from mobile_automation.mobile_pages.product_page import ProductPage
from mobile_automation.mobile_pages.app_login_page import LoginPage
from utils.logger import log
from rapidfuzz import fuzz
import re
import time

class HomePage(BaseMethods):
    def __init__(self, driver):
        super().__init__(driver)
        self.search_bar = '//android.view.View[@content-desc="busque aqui seu produto"]'
        self.search_btn = '//android.view.View[@resource-id="Pesquisar"]'
        self.search_bar_input = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.ImageView'
        self.clear_search_btn = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View[1]/android.widget.ImageView[2]'
        self.close_banner_btn = '//android.widget.TextView[@resource-id="com.b2w.americanas:id/closeBt"]'
        self.banner = '//android.view.View[@resource-id="ins-responsive-banner"]'
        self.dialog = '//android.widget.LinearLayout[@resource-id="com.android.permissioncontroller:id/grant_dialog"]'
        self.allow_location_permission_btn = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_foreground_only_button"]'
        self.allow_notifications_btn = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]'
        self.allow_camera_permission_btn = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_foreground_only_button"]'
        self.list_view_btn = '//android.widget.ImageView[@clickable="true" and @enabled="true"][last()]'
        self.account_btn = '//android.widget.ImageView[@resource-id="account"]'

    def close_permission_notifications(self, timeout: int = 20):
        """Fecha as notificações de permissão de uso de gps, câmera e o envio de notificações"""
        log.info("Verificando se as notificações de sistema apareceram...")
        try:
            dialogs_btn = [
                self.allow_location_permission_btn,
                self.allow_notifications_btn,
                self.allow_camera_permission_btn
            ]

            for button in dialogs_btn:
                dialog = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.dialog, timeout)
                if dialog:
                    log.info(f"Permissão detectada, clicando em: {button}")
                    self.click_element(AppiumBy.XPATH, button)
                    time.sleep(1)
            log.info("As notificações de permissão foram fechadas!")

        except Exception as e:
            log.info("As notificações de sistema não apareceram.")
            pass

    def close_the_banner(self, timeout: int = 5):
        """Fecha o banner de oferta, se ele estiver visível."""
        log.info("Verificando se o banner de oferta está visível...")
        try:
            banner = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.banner, timeout)
            if banner:
                log.info("Banner apareceu! tentando fechar...")
                self.click_element(AppiumBy.XPATH, self.close_banner_btn)
                log.info("Banner fechado com sucesso.")
        except Exception as e:
            log.info("Banner não foi encontrado!")
            pass

    def search_product(self, product_name: str, timeout: int = 10):
        """Abre a busca, limpa o campo, digita o produto e tenta selecioná-lo."""
        log.info(f"Iniciando busca pelo produto: {product_name}")
        try:
            # Garante que esteja na tela inicial antes de abrir a busca
            time.sleep(1)
            self.click_element(AppiumBy.XPATH, self.search_bar)

            # Espera o campo de texto aparecer
            input_el = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.search_bar_input, timeout)
            if not input_el:
                raise Exception("Campo de busca não apareceu.")

            # === LIMPA A BUSCA ANTERIOR ===
            try:
                self.click_element(AppiumBy.XPATH, self.search_btn)
                clear_btn = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.clear_search_btn, timeout=3)
                if clear_btn:
                    log.info("Botão de limpar busca encontrado — clicando...")
                    clear_btn.click()
                    time.sleep(1)
                else:
                    log.info("Botão de limpar não encontrado, tentando limpar texto via .clear()...")
                    input_el.clear()
            except Exception:
                log.warning("Falha ao limpar busca — seguindo assim mesmo.")
                try:
                    input_el.clear()
                except:
                    pass

            # === DIGITA E PESQUISA ===
            input_el.send_keys(product_name)
            log.info(f"Texto digitado no campo de busca: {product_name}")

            # Pressiona Enter (Keycode 66 = ENTER)
            self.driver.press_keycode(66)
            log.info("Busca realizada, listando resultados...")

            time.sleep(5)  # pequena pausa pro app listar os resultados

            # Agora pega todos os resultados exibidos na tela
            result_items = self.find_elements(
                AppiumBy.XPATH, "//android.view.View[@content-desc]"
            )

            normalized_target = BaseMethods.normalize(product_name)
            best_match = None
            best_score = 0

            for item in result_items:
                desc = item.get_attribute("content-desc")
                score = fuzz.token_set_ratio(normalized_target, BaseMethods.normalize(desc))
                if score > best_score:
                    best_score = score
                    best_match = item

            log.info(f"Melhor similaridade encontrada: {best_score}%")

            if not best_match or best_score < 60:
                raise Exception(f"Produto não encontrado com similaridade suficiente (score {best_score}%).")

            best_match.click()
            log.info(f"Produto '{product_name}' selecionado com sucesso!")
            return True

        except Exception as e:
            log.error(f"Erro ao buscar produto '{product_name}': {e}", exc_info=True)
            return False

    def load_results(self, product_name: str, timeout: int = 10):
        """Procura por um produto e espera os resultados aparecerem (sem clicar neles)."""
        try:
            log.info(f"Buscando produto: {product_name}")

            # Abre a barra de busca
            self.click_element(AppiumBy.XPATH, self.search_bar)

            # Espera o campo de texto aparecer
            input_el = self.wait_for_visibility_of_element(AppiumBy.XPATH, self.search_bar_input, timeout)
            if not input_el:
                raise Exception("Campo de busca não apareceu.")

            # Limpa e digita o produto
            input_el.clear()
            input_el.send_keys(product_name)
            log.info(f"Texto digitado no campo de busca: {product_name}")

            # Pressiona Enter (Keycode 66 = ENTER)
            self.driver.press_keycode(66)
            log.info("Busca enviada — aguardando resultados aparecerem...")

            # Aguarda o carregamento dos produtos
            self.wait_for_visibility_of_element(AppiumBy.XPATH, '//android.view.View[contains(@content-desc, "R$")]', timeout=timeout)
            log.info("Resultados carregados com sucesso.")

        except Exception as e:
            log.error(f"Erro ao buscar produto '{product_name}': {e}", exc_info=True)
            raise

    def get_product_info(self, product_name: str):
        """Retorna nome e preço usando fuzzy match no content-desc."""
        log.info("Capturando informações do produto com fuzzy match...")

        try:
            normalized_target = BaseMethods.normalize(product_name)

            # Pega todos os cards com desc visível
            result_items = self.find_elements(AppiumBy.XPATH, "//android.view.View[@content-desc]")
            if not result_items:
                raise Exception("Nenhum item com content-desc encontrado na tela.")

            best_item = None
            best_score = 0

            for item in result_items:
                desc = item.get_attribute("content-desc")
                score = fuzz.token_set_ratio(normalized_target, BaseMethods.normalize(desc))
                if score > best_score:
                    best_score = score
                    best_item = desc

            log.info(f"Melhor similaridade: {best_score}%")

            if best_score < 60:
                raise Exception(f"Produto não corresponde (score {best_score}%).")

            # Quebra o content-desc em linhas
            parts = [p.strip() for p in best_item.split("\n") if p.strip()]

            # 1ª linha pode ser desconto → então nome é a próxima
            if parts[0].startswith("-") and "%" in parts[0]:
                name = parts[1]
            else:
                name = parts[0]

            # Preço é a última linha que contém "R$"
            price_candidates = [p for p in parts if "R$" in p]
            price_raw = price_candidates[-1]

            # Converte pra float corretamente
            price = float(re.sub(r"[^\d,]", "", price_raw).replace(".", "").replace(",", "."))

            return {"name": name, "price": price}

        except Exception as e:
            log.error(f"Erro ao capturar informações do produto: {e}", exc_info=True)
            raise
    
    def switch_to_list_view(self):
        """Troca para visualização em lista no app (com fallback e espera)."""
        try:
            log.info("Tentando trocar para visualização em lista...")

            # XPath relacional: pega o 3º ImageView dentro do container da barra de ações
            self.list_view_btn = (
                '(//android.widget.ImageView[@clickable="true" and @enabled="true"])[3]'
            )

            # Espera o botão ficar visível e clicável
            btn = self.wait_for_element_to_be_clickable(AppiumBy.XPATH, self.list_view_btn)
            if btn:
                log.info("Botão encontrado — tentando clicar...")
                btn.click()
                log.info("Visualização em lista ativada com sucesso!")
            else:
                raise Exception("Botão não encontrado na tela.")

        except Exception as e:
            log.error(f"Erro ao tentar trocar para visualização em lista: {e}", exc_info=True)

    def open_product(self, product_name: str):
        """Abre o produto usando fuzzy match."""
        try:
            log.info("Abrindo produto usando fuzzy match...")

            normalized_target = BaseMethods.normalize(product_name)
            result_items = self.find_elements(AppiumBy.XPATH, "//android.view.View[@content-desc]")

            best_item = None
            best_score = 0

            for item in result_items:
                desc = item.get_attribute("content-desc")
                score = fuzz.token_set_ratio(normalized_target, BaseMethods.normalize(desc))
                if score > best_score:
                    best_score = score
                    best_item = item

            if not best_item or best_score < 60:
                raise Exception(f"Produto não encontrado com precisão suficiente (score {best_score}%).")

            best_item.click()
            return ProductPage(self.driver)

        except Exception as e:
            log.error(f"Erro ao abrir produto: {e}", exc_info=True)
            raise

    def navigate_to_login(self):
        """Navegando para a tela de login..."""
        log.info("Clicando na aba de conta")
        try:
            self.click_element(AppiumBy.XPATH, self.account_btn)
            return LoginPage(self.driver)

        except Exception as e:
            log.error(f"Ocorreu um erro ao tentar navegar para a aba de conta. {e}")
    
    def back_to_last_screen(self):
        """Voltando para a tela anterior"""
        log.info("Retornado para a tela passada")
        self.driver.back()
        self.driver.back()
        self.driver.back()
        time.sleep(2)







