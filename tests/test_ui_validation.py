from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils import config
import allure
import pytest


@allure.feature("Login Page UI Validation")
@allure.story("Login Page all UI elements validation")
@pytest.mark.ui_validation
@pytest.mark.sanity
@pytest.mark.functional_e2e
@pytest.mark.login_test
def test_login_ui(page):
    failures = []
    login_page = LoginPage(page)

    with allure.step("Login UI verification"):
       checks = [
           ("Username Input", login_page.is_visible(config.get_login_elements('username'))),
           ("Username Placeholder",
            login_page.get_attributes(config.get_login_elements('username'), "placeholder") == "Username"),

           ("Password Input", login_page.is_visible(config.get_login_elements('password'))),
           ("Password Placeholder",
            login_page.get_attributes(config.get_login_elements('password'), "placeholder") == "Password"),

           ("Login Button Visible", login_page.is_visible(config.get_login_elements('password'))),
           ("Login Button Text",
            login_page.get_attributes(config.get_login_elements('login_btn'), "value") == "Login"),

           ("Website Logo Visible", login_page.is_visible(config.get_web_elements('app_logo'))),
           ("Website Logo Text",
            login_page.get_text(config.get_web_elements('app_logo')) == "Swag Labs"),

       ]

       for name, result in checks:
           if not result:
               failures.append(f"- {name} failed")

    assert not failures, "UI Validation Failed:\n" + "\n".join(failures)


def header_details(page, inventory_page):
    failures = []


    with allure.step("Header UI verification"):
        checks = [
            ("Page Logo", inventory_page.get_text(config.get_web_elements('app_logo')) == "Swag Labs"),
            ("Side Menu Icon", inventory_page.is_visible(config.get_web_elements('menu_icon_open'))),
            ("Cart Icon", inventory_page.is_visible(config.get_web_elements('cart'))),

        ]
        for name, result in checks:
            if not result:
                failures.append(f"- {name} Failed")
    return not failures, "UI Validation Failed:\n" + "\n".join(failures)


def footer_details(page, inventory_page):
    failures = []

    with allure.step("Header UI verification"):
        checks = [
            ("Terms-Policy Text", "Sauce Labs" in inventory_page.get_text(config.get_footer_elements('copyrights'))),
            ("Twitter Icon", inventory_page.is_visible(config.get_footer_elements('twitter'))),
            ("Facebook Icon", inventory_page.is_visible(config.get_footer_elements('facebook'))),
            ("Linkedin Icon", inventory_page.is_visible(config.get_footer_elements('linkedin'))),
        ]
        for name, result in checks:
            if not result:
                failures.append(f"- {name} Failed")
    return not failures, "UI Validation Failed:\n" + "\n".join(failures)



def product_details( page, inventory_page):

    all_product = page.locator(config.get_inventory_elements('inventory_item'))

    assert all_product.count() > 0, "No products displayed"

    with allure.step(f"All Products are displayed"):
        assert all_product.count() == 6, "Missing some products"

    failures = []

    with allure.step("Products UI verification"):
        for index in range(all_product.count()):
            with allure.step(f"Validate product card {index + 1}"):
                product = all_product.nth(index)
                checks = [
                    ("Item Image", product.locator(config.get_product_elements('product_img'))),
                    ("Item Name", product.locator(config.get_product_elements('product_name'))),
                    ("Item Description", product.locator(config.get_product_elements('product_desc'))),
                    ("Item Price", product.locator(config.get_product_elements('product_price'))),
                    ("Item Add to Cart Button", product.locator(config.get_product_elements('add_to_cart'))),
                ]

                for name, locator in checks:
                    if not locator.is_visible():
                        failures.append(f"Product {index + 1}: {name} Failed")
    assert not failures, "UI Validation Failed:\n" + "\n".join(failures)


def sort_by(page, option):

    page.locator(config.get_inventory_elements('product_sort')).select_option(option)
    dropdown= page.locator(config.get_inventory_elements('product_sort'))

    selected_text = dropdown.locator("option:checked").text_content()
    return selected_text == option


def get_product_names(page):
    return page.locator(".inventory_item_name").all_text_contents()


def get_product_prices(page):
    prices = page.locator('.inventory_item_price').all_text_contents()
    return [float(price.replace("$", "")) for price in prices]


def sorted_order_verification(page, option):

    names = get_product_names(page)
    prices = get_product_prices(page)

    if option == config.A_TO_Z:
        assert names == sorted(names)
    elif option == config.Z_TO_A:
        assert names == sorted(names, reverse=True)
    elif option == config.PRICE_HIGH_TO_LOW:
        assert prices == sorted(prices)
    elif option == config.PRICE_LOW_TO_HIGH:
        assert prices == sorted(prices, reverse=True)

    return True


@allure.feature("Inventory Page UI Validation")
@allure.story("Header and Footer elements validation")
@pytest.mark.ui_validation
@pytest.mark.sanity
@pytest.mark.functional_e2e
def test_header_footer_ui_check(page, login_fixture):

    assert login_fixture
    inventory_page = InventoryPage(page)

    for each_url in config.get("all_urls"):
        page.goto(each_url)
        assert each_url in page.url


        with allure.step(f"Header and Footer validation for url {each_url}"):
            assert header_details(page, inventory_page)
            assert footer_details(page, inventory_page)


@allure.feature("Inventory Page UI Validation")
@allure.story("Main page UI elements validation")
@pytest.mark.ui_validation
@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.functional_e2e
def test_product_page_ui_check(page, login_fixture):
    assert login_fixture
    inventory_page = InventoryPage(page)

    with allure.step(f"Header and Footer validation"):
        assert header_details(page, inventory_page)
        assert footer_details(page, inventory_page)

    for option in config.SORT_BY:
        sort_by(page, option)
        sorted_order_verification(page, option)

    product_details(page, inventory_page)



@allure.feature("Checkout Page UI Validation")
@allure.story("Main page UI elements validation")
@pytest.mark.ui_validation
@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.functional_e2e
@pytest.mark.product_test
@pytest.mark.parametrize("firstname, lastname, pincode, expected", config.CHECKOUT_INFO)
def test_checkout_page_ui_check(firstname, lastname, pincode, expected, page, login_fixture):
    assert login_fixture

    page.goto("https://www.saucedemo.com/checkout-step-one.html")
    assert "checkout-step-one.html" in page.url
    assert InventoryPage(page).get_attributes(config.get_checkout_elements('firstname'), "placeholder") == "First Name"
    assert InventoryPage(page).get_attributes(config.get_checkout_elements('lastname'), "placeholder") == "Last Name"
    assert InventoryPage(page).get_attributes(config.get_checkout_elements('pincode'), "placeholder") == "Zip/Postal Code"

    InventoryPage(page).fill(config.get_checkout_elements('firstname'), firstname)
    InventoryPage(page).fill(config.get_checkout_elements('lastname'), lastname)
    InventoryPage(page).fill(config.get_checkout_elements('pincode'), pincode)

    page.locator(config.get_web_elements('continue_btn')).click()


    # //h3[@data-test='error']

    if expected == "checkout-step-two.html":
        assert expected == "checkout-step-two.html"
    else:
        assert expected in InventoryPage(page).get_text("//h3[@data-test='error']")








