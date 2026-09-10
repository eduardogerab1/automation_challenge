from mobile_automation.mobile_pages.app_home_page import HomePage
from mobile_automation.mobile_pages.base_page_mobile import BaseMethods
from utils.logger import log
from rapidfuzz import fuzz
import pytest

@pytest.mark.mobile
def test_search_product_from_api(driver, wishlist_data):
    home_page = HomePage(driver)
    home_page.close_permission_notifications()
    home_page.close_the_banner()

    falhas = []  # <--- REGISTRA OS ERROS

    for product in wishlist_data:
        product_name = product["Product"]
        api_price = str(product["Price"])

        try:
            log.info(f"Buscando produto da API: {product_name}")
            home_page.load_results(product_name)

            product_info = home_page.get_product_info(product_name)

            # ==== Validação do título ====
            expected_name = BaseMethods.normalize(product_name)
            actual_name = BaseMethods.normalize(product_info["name"])
            similarity = fuzz.token_set_ratio(expected_name, actual_name)

            assert similarity > 75, (
                f"Título diferente: esperado '{expected_name}', obtido '{actual_name}', "
                f"similaridade: {similarity}%"
            )

            # ==== Validação do preço ====
            api_price_float = float(api_price.replace(".", "").replace(",", "."))
            price_str = str(product_info["price"]).replace("R$", "").replace("\u00A0", "").strip()

            if "," in price_str:
                price_str = price_str.replace(".", "").replace(",", ".")
            else:
                price_str = price_str.replace(",", "")

            app_price_float = float(price_str)

            assert abs(api_price_float - app_price_float) <= 0.05, (
                f"Preço diferente: esperado {api_price_float}, obtido {app_price_float}"
            )
            log.info(f"Produto validado com sucesso em grid: {product_name}")

            # Muda para lista
            home_page.switch_to_list_view()

            # Pega o primeiro produto dos resultados
            product_info = home_page.get_product_info(product_name)

            expected_name = BaseMethods.normalize(product_name)
            actual_name = BaseMethods.normalize(product_info["name"])
            similarity = fuzz.token_set_ratio(expected_name, actual_name)

            assert similarity > 75, (
                f"Título diferente: esperado '{expected_name}', obtido '{actual_name}', "
                f"similaridade: {similarity}%"
            )

            api_price_float = float(api_price.replace(".", "").replace(",", "."))
            price_str = str(product_info["price"]).replace("R$", "").replace("\u00A0", "").strip()

            if "," in price_str:
                price_str = price_str.replace(".", "").replace(",", ".")
            else:
                price_str = price_str.replace(",", "")
            app_price_float = float(price_str)

            assert abs(api_price_float - app_price_float) <= 0.05, (
                f"Preço diferente: esperado {api_price_float}, obtido {app_price_float}"
            )
            log.info(f"Produto validado com sucesso em lista: {product_name}")

            # Abre os detalhes do produto
            product_page = home_page.open_product(product_name)

            title = product_page.get_product_name()
            price = product_page.get_product_price()

            expected_name = BaseMethods.normalize(product_name)
            actual_name = BaseMethods.normalize(title)
            similarity = fuzz.token_set_ratio(expected_name, actual_name)

            assert similarity > 75, (
                f"Título incorreto na página de produto: esperado '{expected_name}', obtido '{actual_name}', "
                f"similaridade: {similarity}%"
            )

            assert api_price.replace(" ", "") in price.replace(" ", ""), (
                f"Preço incorreto: esperado '{api_price}', obtido '{price}'"
            )

            home_page.back_to_last_screen()

        except Exception as e:
            falhas.append(f"{product_name} -> {str(e)}")   # REGISTRA O ERRO
            log.error(f"Falha ao validar produto {product_name}, seguindo para o próximo.", exc_info=False)
            continue  # <--- CONTINUA O LOOP

    # SÓ FALHA NO FINAL
    assert not falhas, (
        "\nALGUNS PRODUTOS FALHARAM NA VALIDAÇÃO:\n" +
        "\n".join(falhas)
    )
