import random
import allure
import pytest
from utils import config
from pages.inventory_page import InventoryPage


@allure.feature("Product purchase Page Validation")
@allure.story("Single or multiple product purchase validation")
@pytest.mark.add_to_cart
@pytest.mark.product_test
@pytest.mark.functional_e2e
def test_add_to_cart(request, page, login_fixture):
    assert login_fixture

    buy_count = int(request.config.getoption("--buy"))

    assert buy_count <= 6, "Products out of range (Max 6 items)"

    all_product = page.locator(config.get_inventory_elements('inventory_item'))

    assert all_product.count() > 0, "No products displayed"

    add_to_cart_items = []

    for index in range(all_product.count()):
        with allure.step(f"Add product to card"):
            product = all_product.nth(index)

            product_name = product.locator(config.get_product_elements('product_name')).text_content()

            add_to_cart_items.append(product_name)

            product.locator(config.get_product_elements('add_to_cart')).click()

            cart_items_count =  InventoryPage(page).get_cart_items()
            assert cart_items_count == index + 1
            if buy_count == index + 1:
                break
            else:
                continue

    page.locator(config.get_web_elements('cart')).click()
    assert "cart.html" in page.url

    allure.attach(
        page.screenshot(),
        name=f"Item Added to Cart",
        attachment_type=allure.attachment_type.PNG
    )

    cart_items = page.locator(".cart_item")

    add_to_cart_verity = []
    for cart_index in range(cart_items.count()):
        with allure.step(f"Validate cart product {cart_index + 1}"):
            each_product = cart_items.nth(cart_index)

            cart_product_name = each_product.locator(config.get_product_elements("product_name")).text_content()
            cart_product_price = each_product.locator(config.get_product_elements("product_price")).text_content()

            print(cart_product_name, cart_product_price)

            if cart_product_name in add_to_cart_items:
                add_to_cart_verity.append(cart_product_name)

    assert add_to_cart_verity == add_to_cart_items

    page.locator(config.get_web_elements('checkout_btn')).click()
    assert "checkout-step-one.html" in page.url

    InventoryPage(page).fill(config.get_checkout_elements('firstname'), config.get("username"))
    InventoryPage(page).fill(config.get_checkout_elements('lastname'), config.get("lastname"))
    InventoryPage(page).fill(config.get_checkout_elements('pincode'), config.get("pincode"))
    #
    page.locator(config.get_web_elements('continue_btn')).click()
    assert "checkout-step-two.html" in page.url

    allure.attach(
        page.screenshot(),
        name=f"Item Checkout",
        attachment_type=allure.attachment_type.PNG
    )

    cart_items = page.locator("[data-test='inventory-item']")
    total_price = 0.0

    for i in range(cart_items.count()):
        each_product = cart_items.nth(i)

        total_price += float(each_product.locator(config.get_product_elements("product_price")).text_content().replace("$", '').strip())

    sub_total = float(page.locator(config.get_checkout_elements("subtotal")).text_content().split("$")[-1].strip())

    assert sub_total == total_price
    tax = float(page.locator(config.get_checkout_elements("tax")).text_content().split("$")[-1].strip())
    total_with_tax = float(page.locator(config.get_checkout_elements("final_price")).text_content().split("$")[-1].strip())

    assert total_with_tax == sub_total + tax

    page.locator(config.get_web_elements('finish_btn')).click()

    assert "checkout-complete.html" in page.url
    assert "Thank you for your order!" == page.locator(config.get_checkout_elements("order_complete_text")).text_content()

    allure.attach(
        page.screenshot(),
        name=f"Item purchase complete",
        attachment_type=allure.attachment_type.PNG
    )

    page.locator(config.get_web_elements("finish_back_btn")).click()
    assert "inventory.html" in page.url

    cart_items = InventoryPage(page).get_cart_items()
    assert cart_items == 0

    InventoryPage(page).logout()
    assert "saucedemo.com" in page.url


@allure.feature("Product selection Validation")
@allure.story("Clear products selected validation")
@pytest.mark.product_clear
@pytest.mark.product_test
@pytest.mark.functional_e2e
def test_clear_items(page, login_fixture):
    assert login_fixture

    all_product = page.locator(config.get_inventory_elements('inventory_item'))

    assert all_product.count() > 0, "No products displayed"

    add_to_cart_items = []
    for index in range(all_product.count()):
        with allure.step(f"Add product to card"):
            product = all_product.nth(index)

            product_name = product.locator(config.get_product_elements('product_name')).text_content()
            add_to_cart_items.append(product_name)
            product.locator(config.get_product_elements('add_to_cart')).click()
            cart_items_count =  InventoryPage(page).get_cart_items()
            assert cart_items_count == index + 1

    assert len(add_to_cart_items) == InventoryPage(page).get_cart_items()

    InventoryPage(page).clear_cart()

    assert not InventoryPage(page).get_cart_items()

    InventoryPage(page).logout()
    assert "saucedemo.com" in page.url


@allure.feature("Product selection Validation")
@allure.story("Remove items from cart validation")
@pytest.mark.remove_from_cart
@pytest.mark.product_test
@pytest.mark.functional_e2e
def test_remove_from_cart(page, login_fixture):
    assert login_fixture

    all_product = page.locator(config.get_inventory_elements('inventory_item'))

    assert all_product.count() > 0, "No products displayed"
    add_to_cart_items = []
    count = 0
    for index in random.choices([1,2,3,4,5,6], k=2):
        product = all_product.nth(index)
        count += 1

        product_name = product.locator(config.get_product_elements('product_name')).text_content()
        add_to_cart_items.append(product_name)
        product.locator(config.get_product_elements('add_to_cart')).click()
        cart_items_count =  InventoryPage(page).get_cart_items()
        assert cart_items_count == count


    assert len(add_to_cart_items) == InventoryPage(page).get_cart_items()

    page.locator(config.get_web_elements('cart')).click()
    assert "cart.html" in page.url

    cart_items = page.locator(".cart_item")
    add_to_cart_verity = []
    count = 0
    for cart_index in range(cart_items.count()):
        with allure.step(f"Validate cart product {cart_index + 1}"):
            each_product = cart_items.nth(cart_index - count)
            count += 1
            product = each_product.locator(config.get_product_elements('product_name')).text_content().lower().replace(" ", "-")

            page.locator(f'[data-test="remove-{product}"]').click()

    assert not InventoryPage(page).get_cart_items()

    InventoryPage(page).logout()
    assert "saucedemo.com" in page.url


@allure.feature("Product page selection Validation")
@allure.story("Cancel purchase validation")
@pytest.mark.cancel_buy
@pytest.mark.product_test
@pytest.mark.functional_e2e
def test_cancel_checkout(page, login_fixture):
    assert login_fixture, "Loin Failed"

    all_product = page.locator(config.get_inventory_elements('inventory_item'))

    assert all_product.count() > 0, "No products displayed"
    add_to_cart_items = []
    count = 0
    for index in random.choices([1,2,3,4,5,6], k=2):
        product = all_product.nth(index)
        count += 1

        product_name = product.locator(config.get_product_elements('product_name')).text_content()
        add_to_cart_items.append(product_name)
        product.locator(config.get_product_elements('add_to_cart')).click()
        cart_items_count =  InventoryPage(page).get_cart_items()
        assert cart_items_count == count


    assert len(add_to_cart_items) == InventoryPage(page).get_cart_items()

    page.locator(config.get_web_elements('cart')).click()
    assert "cart.html" in page.url

    page.locator(config.get_web_elements('checkout_btn')).click()
    assert "checkout-step-one.html" in page.url

    page.locator(config.get_web_elements('cancel_btn')).click()
    assert "cart.html" in page.url

    page.locator(config.get_web_elements('checkout_btn')).click()
    assert "checkout-step-one.html" in page.url

    InventoryPage(page).fill(config.get_checkout_elements('firstname'), config.get("username"))
    InventoryPage(page).fill(config.get_checkout_elements('lastname'), config.get("lastname"))
    InventoryPage(page).fill(config.get_checkout_elements('pincode'), config.get("pincode"))

    page.locator(config.get_web_elements('continue_btn')).click()
    assert "checkout-step-two.html" in page.url

    page.locator(config.get_web_elements('cancel_btn')).click()
    assert "inventory.html" in page.url

    assert len(add_to_cart_items) == InventoryPage(page).get_cart_items()

    InventoryPage(page).logout()
    assert "saucedemo.com" in page.url



@allure.story("Product purchase via product page validation")
@allure.story("Cancel purchase validation")
@pytest.mark.product_page_buy
@pytest.mark.product_test
@pytest.mark.functional_e2e
def test_product_page_checkout(page, login_fixture):
    assert login_fixture

    all_product = page.locator(config.get_inventory_elements('inventory_item'))

    assert all_product.count() > 0, "No products displayed"
    add_to_cart_items = []

    for index in random.choices([1,2,3,4,5,6], k=1):

        product = all_product.nth(index)
        product_name = product.locator(config.get_product_elements('product_name')).text_content()
        add_to_cart_items.append(product_name)

        product.locator(config.get_product_elements('product_name')).click()
        cart_items_count =  InventoryPage(page).get_cart_items()
        assert not cart_items_count

    page.locator(config.get_product_elements('add_to_cart')).click()
    assert  InventoryPage(page).get_cart_items() == 1

    page.locator(config.get_web_elements('cart')).click()
    assert "cart.html" in page.url

    cart_items = page.locator(".cart_item")

    add_to_cart_verity = []

    for cart_index in range(cart_items.count()):
        with allure.step(f"Validate cart product {cart_index + 1}"):
            each_product = cart_items.nth(cart_index)

            cart_product_name = each_product.locator(config.get_product_elements("product_name")).text_content()
            cart_product_price = each_product.locator(config.get_product_elements("product_price")).text_content()

            print(cart_product_name, cart_product_price)

            if cart_product_name in add_to_cart_items:
                add_to_cart_verity.append(cart_product_name)

    assert add_to_cart_verity == add_to_cart_items

    page.locator(config.get_web_elements('checkout_btn')).click()
    assert "checkout-step-one.html" in page.url

    InventoryPage(page).fill(config.get_checkout_elements('firstname'), config.get("username"))
    InventoryPage(page).fill(config.get_checkout_elements('lastname'), config.get("lastname"))
    InventoryPage(page).fill(config.get_checkout_elements('pincode'), config.get("pincode"))
    #
    page.locator(config.get_web_elements('continue_btn')).click()
    assert "checkout-step-two.html" in page.url

    allure.attach(
        page.screenshot(),
        name=f"Item Checkout",
        attachment_type=allure.attachment_type.PNG
    )

    cart_items = page.locator("[data-test='inventory-item']")
    total_price = 0.0

    for i in range(cart_items.count()):
        each_product = cart_items.nth(i)

        total_price += float(each_product.locator(config.get_product_elements("product_price")).text_content().replace("$", '').strip())

    sub_total = float(page.locator(config.get_checkout_elements("subtotal")).text_content().split("$")[-1].strip())

    assert sub_total == total_price
    tax = float(page.locator(config.get_checkout_elements("tax")).text_content().split("$")[-1].strip())
    total_with_tax = float(page.locator(config.get_checkout_elements("final_price")).text_content().split("$")[-1].strip())

    assert total_with_tax == sub_total + tax

    page.locator(config.get_web_elements('finish_btn')).click()

    assert "checkout-complete.html" in page.url
    assert "Thank you for your order!" == page.locator(config.get_checkout_elements("order_complete_text")).text_content()

    allure.attach(
        page.screenshot(),
        name=f"Item purchase complete",
        attachment_type=allure.attachment_type.PNG
    )

    page.locator(config.get_web_elements("finish_back_btn")).click()
    assert "inventory.html" in page.url

    cart_items = InventoryPage(page).get_cart_items()
    assert cart_items == 0

    InventoryPage(page).logout()
    assert "saucedemo.com" in page.url



@allure.feature("Product selection Validation")
@allure.story("Go to Home page validation")
@pytest.mark.go_to_home
@pytest.mark.product_test
@pytest.mark.functional_e2e
def test_clear_items(page, login_fixture):
    assert login_fixture

    all_product = page.locator(config.get_inventory_elements('inventory_item'))

    assert all_product.count() > 0, "No products displayed"

    add_to_cart_items = []
    count = 0
    for index in random.choices([1,2,3,4,5,6], k=1):
        with allure.step(f"Add product to card"):
            product = all_product.nth(index)

            product_name = product.locator(config.get_product_elements('product_name')).text_content()
            add_to_cart_items.append(product_name)
            product.locator(config.get_product_elements('add_to_cart')).click()
            cart_items_count =  InventoryPage(page).get_cart_items()
            count += 1
            assert cart_items_count == count

    assert len(add_to_cart_items) == InventoryPage(page).get_cart_items()

    page.locator(config.get_web_elements('cart')).click()
    assert "cart.html" in page.url

    InventoryPage(page).home_page()
    assert "inventory.html" in page.url


    page.locator(config.get_web_elements('cart')).click()
    assert "cart.html" in page.url

    page.locator(config.get_web_elements('checkout_btn')).click()
    assert "checkout-step-one.html" in page.url

    InventoryPage(page).home_page()
    assert "inventory.html" in page.url

    InventoryPage(page).logout()
    assert "saucedemo.com" in page.url
