from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import unicodedata
from utils.logger import log

def normalize_text(text):
        """Normaliza texto removendo acentos e diferenças de encoding."""
        if not text:
            return ""
        # Garante que o texto está em unicode decodificando Latin-1 se necessário
        if isinstance(text, bytes):
            text = text.decode("utf-8", "ignore")
        else:
            try:
                text = text.encode("latin-1").decode("utf-8")
            except UnicodeEncodeError:
                pass  # já está em utf-8
            except UnicodeDecodeError:
                text = text.encode("utf-8", "ignore").decode("utf-8")

        # Normaliza acentos e remove caracteres combinantes
        text = unicodedata.normalize("NFKD", text)
        text = "".join(ch for ch in text if not unicodedata.combining(ch))

        return text.lower().strip()

class BaseMethods:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
    
    def navigate(self, url):
        log.info('estabelecendo driver...')
        self.driver.get(url)

    def find_element(self, by, locator):
        log.info(f'tentando encontrar elemento com o locator: {locator}')
        try:
            return self.wait.until(EC.visibility_of_element_located((by, locator)))
        except Exception as e:
            log.error(f'não foi possível encontrar o elemento com o locator: {locator}', exc_info=True)
            raise
    
    def find_element_present(self, by, locator):
        """Retorna o elemento assim que ele estiver presente no DOM (não necessariamente visível)."""
        log.info(f"Tentando encontrar elemento presente no DOM: {locator}")
        try:
            return self.wait.until(EC.presence_of_element_located((by, locator)))
        except Exception:
            log.error(f"Elemento não encontrado no DOM: {locator}", exc_info=True)
            raise

    def find_elements(self, by, locator):
        return self.wait.until(EC.presence_of_all_elements_located((by, locator)))

    def wait_for_element_to_be_clickable(self, by, locator, timeout=15):
        log.info(f"Aguardando elemento ficar clicável: {locator}")
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, locator))
            )
        except Exception as e:
            log.error(f"Elemento não ficou clicável a tempo: {locator}", exc_info=True)
            raise

    def wait_for_element_visible(self, by, locator, timeout=15):
        log.info(f"Aguardando visibilidade do elemento: {locator}")
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, locator))
            )
        except Exception as e:
            log.error(f"Elemento não ficou visível a tempo: {locator}", exc_info=True)
            raise

    def click_element(self, by, locator):
        log.info(f'clicando no elemento que tem o locator {locator}')
        try:
            self.wait_for_element_to_be_clickable(by, locator).click()
            log.info(f'o elemento foi clicado com sucesso!')
        except Exception as e:
            log.error(f'não foi possível clicar no elemento com o locator: {locator}', exc_info=True)
            raise
    
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

    def open_new_tab(self, url=None):
        """Abre uma nova aba e, opcionalmente, navega até uma URL"""
        log.info("Abrindo nova aba")
        main_window = self.driver.current_window_handle
        handles_before = self.driver.window_handles

        # Abre nova aba via JavaScript
        self.driver.execute_script("window.open('');")

        # Aguarda até que uma nova aba apareça
        try:
            WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > len(handles_before))
            all_windows = self.driver.window_handles
            new_window = [w for w in all_windows if w != main_window][-1]
            self.driver.switch_to.window(new_window)
            log.info(f"Nova aba aberta com sucesso ({new_window})")
        except Exception as e:
            log.error("Falha ao abrir nova aba", exc_info=True)
            raise

        # Se uma URL for passada, navega até ela
        if url:
            log.info(f"Navegando para {url} na nova aba")
            self.navigate(url)

    def switch_to_tab(self, tab_index=None, main_window=None):
        """Alterna para uma aba específica pelo índice ou para a nova aba aberta

        Args:
            tab_index (int, optional): Índice da aba (0 = primeira). Ignorado se main_window for passado.
            main_window (str, optional): Handle da aba principal; se informado, muda para a nova aba criada depois dela.
        """
        try:
            if main_window:
                log.info("Aguardando nova aba para alternar")
                WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
                all_windows = self.driver.window_handles
                new_window = [w for w in all_windows if w != main_window][-1]
                self.driver.switch_to.window(new_window)
                log.info(f"Alternado para nova aba: {self.driver.current_url}")
            elif tab_index is not None:
                log.info(f"Alternando para aba de índice {tab_index}")
                self.driver.switch_to.window(self.driver.window_handles[tab_index])
            else:
                raise ValueError("Você deve informar tab_index ou main_window")
        except Exception:
            log.error("Falha ao alternar de aba", exc_info=True)
            raise
    
    def wait_for_overlay_to_disappear(self, overlay_selector="//div[contains(@class, 'SearchInput_overlay')]", timeout=10):
        """Aguarda até que o overlay de carregamento desapareça da tela."""
        try:
            log.info(f"Aguardando overlay desaparecer: {overlay_selector}")
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located((By.XPATH, overlay_selector))
            )
            log.info("Overlay desapareceu, pode clicar com segurança.")
        except TimeoutException:
            log.warning("O overlay não desapareceu dentro do tempo limite, tentando clicar mesmo assim.")
    