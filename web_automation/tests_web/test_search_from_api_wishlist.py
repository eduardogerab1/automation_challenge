from web_automation.pages_web.home_page import HomePage
from utils.logger import log
from web_automation.pages_web.base_page_web import normalize_text
from rapidfuzz import fuzz
import pytest

@pytest.mark.web
def test_search_product_from_api(driver, wishlist_data):
    home_page = HomePage(driver)
    home_page.open_page()
    home_page.close_banner()

    for product in wishlist_data:
        product_name = product["Product"]
        api_price = product["Price"]

        log.info(f"Buscando produto da API: {product_name}")
        home_page.search_product(product_name)

        # GRID VIEW
        product_info = home_page.get_first_product_info()

        expected_name = normalize_text(product_name)
        actual_name = normalize_text(product_info["name"])

        similarity = fuzz.token_set_ratio(expected_name, actual_name)
        assert similarity > 75, (
            f"Título diferente no grid: esperado '{expected_name}', obtido '{actual_name}', "
            f"similaridade: {similarity}%"
        )

        assert api_price.replace(" ", "") in product_info["price"].replace(" ", ""), (
            f"Preço diferente no grid: esperado '{api_price}', obtido '{product_info['price']}'"
        )

        log.info(f"Produto validado com sucesso em grid: {product_name}")

        # LIST VIEW
        home_page.switch_to_list_view()
        product_info2 = home_page.get_first_product_info()

        expected_name = normalize_text(product_name)
        actual_name = normalize_text(product_info2["name"])

        similarity = fuzz.token_set_ratio(expected_name, actual_name)
        assert similarity > 75, (
            f"Título diferente na lista: esperado '{expected_name}', obtido '{actual_name}', "
            f"similaridade: {similarity}%"
        )

        assert api_price.replace(" ", "") in product_info2["price"].replace(" ", ""), (
            f"Preço diferente na lista: esperado '{api_price}', obtido '{product_info2['price']}'"
        )

        # PRODUCT PAGE DETAILS
        product_page = home_page.open_product(product_name)

        title = normalize_text(product_page.get_product_name())
        expected = normalize_text(product_name)

        similarity = fuzz.token_set_ratio(expected, title)
        assert similarity > 75, (
            f"Título incorreto na página do produto: esperado '{expected}', obtido '{title}', "
            f"similaridade: {similarity}%"
        )

        price = product_page.get_product_price()
        assert api_price.replace(" ", "") in price.replace(" ", ""), (
            f"Preço incorreto na página do produto: esperado '{api_price}', obtido '{price}'"
        )
