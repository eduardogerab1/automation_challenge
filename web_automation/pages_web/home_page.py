from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_automation.pages_web.base_page_web import BaseMethods
from web_automation.pages_web.login_page import LoginPage
from web_automation.pages_web.profile_page import ProfilePage
from web_automation.pages_web.product_page import ProductPage
from utils.logger import log
from pathlib import Path
import json

class HomePage(BaseMethods):

    URL = "https://www.americanas.com.br"
    
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.close_the_banner = '//*[@id="close-button-1454703513200"]'
        self.login_btn = ('//*[@id="__next"]/header/div/section[1]/div/a[2]/div[2]')
        self.profile_btn = ('//*[@href="/account#/" or contains(@aria-label, "link para a página de login")]')
        self.logo_americanas = "//*[@title='Americanas' or contains(@aria-label, 'Logo da Americanas')]"
        self.header_email = '//div[contains(@class, "ButtonLogin_textContainer")]'
        self.search_bar = "//input[contains(@placeholder, 'busque') and contains(@placeholder, 'produto')]"
        self.list_view_btn = "//span[contains(normalize-space(.), 'lista')]"

    def open_page(self):
        self.navigate(self.URL)

    def close_banner(self):
        """tenta fechar o banner antes de navegar para login"""
        try:
            self.wait_for_overlay_to_disappear()
            self.click_element(By.XPATH, self.close_the_banner)
            log.info("banner fechado!")
            # espera o banner ser fechado depois de clicar
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, self.close_the_banner)))
        except Exception as e:
            log.info("não foi possível fechar o banner")

    def navigate_to_login_page(self):
        """clica no botão de login e retorna a instância LoginPage"""
        self.wait_for_overlay_to_disappear()
        self.click_element(By.XPATH, self.login_btn)
        return LoginPage(self.driver)

    def navigate_to_profile_page(self):
        """clica no botão com o email e retorna a instância ProfilePage"""
        self.wait_for_overlay_to_disappear()
        self.click_element(By.XPATH, self.profile_btn)
        return ProfilePage(self.driver)
    
    def find_the_logo(self):
        """tenta achar a logo na página"""
        try: 
            self.find_element(By.XPATH, self.logo_americanas)
            log.info('a logo foi encontrada!')
            return True

        except Exception as e:
            log.info("a logo não foi encontrada")
            return False

    def get_logged_user_email(self):
        """armazena o valor do email mostrado no header da página"""
        try:
            header_element = self.find_element(By.XPATH, self.header_email)
            header_text = header_element.text.strip()
            log.info(f"Texto encontrado no header: '{header_text}'")
            if "@" not in header_text:
                log.info(f"Header outer HTML: {header_element.get_attribute('outerHTML')}")
            return header_text

        except Exception as e:
            log.error(f'Não foi possível encontrar o texto: {e}')

    def search_product(self, product_name: str):
        """Procura por um produto e espera os resultados aparecerem."""
        try:
            log.info(f"Buscando produto: {product_name}")
            search_box = self.find_element(By.XPATH, self.search_bar)
            search_box.clear()
            search_box.send_keys(product_name + "\n")

            log.info("Aguardando resultados aparecerem...")
            self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[contains(@class, 'ProductCard_productInfo__')]")
                )
            )
            log.info("Resultados carregados com sucesso.")

        except Exception as e:
            log.error(f"Erro ao procurar produto '{product_name}': {e}", exc_info=True)
            raise
    
    def get_first_product_info(self):
        """Retorna o nome e o preço do primeiro produto nos resultados."""
        try:
            wait = WebDriverWait(self.driver, 15)
            log.info("Aguardando carregamento do primeiro produto...")

            first_card = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class,'ProductCard_productInfo__')]")
                )
            )

            name_el = first_card.find_element(By.XPATH, ".//h3[contains(@class,'ProductCard_productName__')]")
            price_el = first_card.find_element(By.XPATH, ".//p[contains(@class,'ProductCard_productPrice__')]")

            name = name_el.text.strip()
            price = price_el.text.strip()

            log.info(f"Produto encontrado: {name} — Preço: {price}")
            return {"name": name, "price": price, "element": first_card}

        except Exception as e:
            log.error(f"Erro ao capturar informações do primeiro produto: {e}", exc_info=True)
            raise

    def switch_to_list_view(self):
        """Trocando para visualização em lista."""
        try:
            log.info("Clicando no botão que troca para a visualização em lista...")
            self.click_element(By.XPATH, self.list_view_btn)
            log.info("Botão de visualização em lista clicado com sucesso!")

        except Exception as e:
            log.error("Ocorreu um erro ao trocar para a visualização em lista")
    
    def open_product(self, product_name: str):
        """Clica no produto para abrir detalhes."""
        try:
            log.info("Clicando no produto escolhido para validar detalhes.")
            self.click_element(By.XPATH, "//div[contains(@class,'ProductCard_productInfo__')]")
            log.info(f"Abrindo detalhes do produto: {product_name}")
            return ProductPage(self.driver)

        except Exception as e:
            log.error(f"Ocorreu um erro ao tentar abrir os detalhes do produto. {e}")

    def is_logged_in(self, timeout: int = 25):
        """Verifica se o usuário logado corresponde ao email salvo no JSON."""
        try:

            # Lê o e-mail salvo
            email_path = Path("data/email.json")
            with open(email_path, encoding="utf-8") as f:
                expected_email = json.load(f)["email"]

            # Espera o header atualizar após o login
            log.info("Aguardando o header do usuário aparecer após o login...")
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(
                    (By.XPATH, self.header_email), expected_email.split("@")[0]
                )
            )

            # Obtém o texto do header atualizado
            header_email = self.get_logged_user_email()
            log.info(f"Comparando email logado '{header_email}' com esperado '{expected_email}'")

            if expected_email.split("@")[0] in header_email:
                log.info("Usuário logado validado com sucesso!")
                return True
            else:
                log.error(f"O email exibido ('{header_email}') não corresponde ao esperado ('{expected_email}').")
                return False

        except Exception as e:
            log.error(f"Erro ao validar usuário logado: {e}", exc_info=True)
            return False




