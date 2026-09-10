from mobile_automation.mobile_pages.app_home_page import HomePage
from mobile_automation.mobile_pages.product_page import ProductPage
from mobile_automation.mobile_pages.base_page_mobile import BaseMethods
from rapidfuzz import fuzz
import pytest
import re
from utils.logger import log

@pytest.mark.mobile
def test_product_purchase_flow(driver, wishlist_data):
    FUZZY_THRESHOLD = 70 
    home_page = HomePage(driver)
    product_page = ProductPage(driver)

    home_page.close_permission_notifications()
    home_page.close_the_banner()

    falhas = []

    for product in wishlist_data:
        product_name = product["Product"]
        log.info(f"\n==== Validando produto da API: {product_name} ====")

        try:
            product_price = product["Price"]
            valid_zipcode = product["Zipcode"]
            delivery_estimate = product["delivery_estimate"]
            shipping_fee = product["shipping_fee"]

            # 1. Buscar produto
            home_page.search_product(product_name)

            # 2. Validar nome do produto
            current_name = product_page.get_product_name()
            similarity = fuzz.token_set_ratio(product_name.lower(), current_name.lower())

            assert similarity > FUZZY_THRESHOLD, (
                f"Nome divergente!\n"
                f"Esperado: {product_name}\nObtido: {current_name}"
            )

            # 3. Validar preço
            price_in_cart = product_page.get_product_price()

            expected_price = re.sub(r"[^\d,]", "", product_price)
            price_in_cart = re.sub(r"[^\d,]", "", price_in_cart)

            expected_price_float = float(expected_price.replace(".", "").replace(",", "."))
            price_in_cart_float = float(price_in_cart.replace(".", "").replace(",", "."))

            assert abs(expected_price_float - price_in_cart_float) < 0.01, (
                f"Preço divergente!\n"
                f"Esperado: {expected_price_float:.2f}\nObtido: {price_in_cart_float:.2f}"
            )

            # 4. Validação de CEP
            assert product_page.invalid_zip_code(), "Mensagem de CEP inválido não exibida."
            delivery_info = product_page.valid_zipcode_from_api(valid_zipcode)

            delivery_info_normalized = BaseMethods.normalize(delivery_info)
            expected_estimate = BaseMethods.normalize(delivery_estimate)
            expected_fee = BaseMethods.normalize(shipping_fee)

            assert expected_estimate in delivery_info_normalized, "Prazo divergente no app"
            assert expected_fee in delivery_info_normalized, "Frete divergente no app"

            # 5. Checar popup de compra
            popup_content = product_page.check_product_in_the_pop_up(product_name)
            assert popup_content, "Popup não retornou conteúdo válido!"

            # 6. Quantidade
            assert product_page.increase_quantity() == "2"
            assert product_page.decrease_quantity() == "1"
            assert product_page.is_minus_button_disabled(), "Botão '-' deveria estar desativado"

            # 7. Ir ao carrinho
            cart_page = product_page.add_product_to_cart(product_name)
            assert cart_page, "Falha ao navegar para o carrinho"

            # validação nome no carrinho
            name_in_cart = cart_page.get_product_name_in_cart()
            similarity = fuzz.token_set_ratio(product_name.lower(), name_in_cart.lower())
            assert similarity > FUZZY_THRESHOLD, "Nome divergente no carrinho"

            # validação preço total
            qty_in_cart = int(cart_page.check_quantity_in_cart())
            converted_price = float(product_price.replace(".", "").replace(",", "."))
            expected_total_price = converted_price * qty_in_cart
            price_in_cart = cart_page.get_product_price_in_cart()
            assert expected_total_price == price_in_cart, "Preço total divergente no carrinho"

            # validação CEP no carrinho
            assert cart_page.invalid_zip_code(), "Mensagem de CEP inválido no carrinho não exibida"
            delivery_info = cart_page.valid_zipcode_from_api(valid_zipcode)
            delivery_info_normalized = BaseMethods.normalize(delivery_info)
            assert expected_estimate in delivery_info_normalized
            assert expected_fee in delivery_info_normalized

            # finalizar compra
            finish_purchase = cart_page.finish_purchase()
            assert finish_purchase.check_page_msg() == "Informe seu e-mail para continuar"

            finish_purchase.go_back_to_cart()
            confirm_clear_msg = cart_page.clear_cart()
            assert confirm_clear_msg == "sua cesta está vazia"

            product_page.go_back_to_home()

            log.info(f"Produto validado com sucesso: {product_name}")

        except AssertionError as e:
            log.error(f"Falha no produto '{product_name}': {e}")
            falhas.append((product_name, str(e)))
            product_page.go_back_to_home()
            continue  # segue para o próximo produto

    # === Validação final após o loop ===
    if falhas:
        mensagens = "\n".join([f"- {nome}: {erro}" for nome, erro in falhas])
        pytest.fail(f"\nForam encontrados problemas nos seguintes produtos:\n{mensagens}")
