from pages.base_page import BasePage
from utils import config


class InventoryPage(BasePage):

    def logout(self):
        try:
            self.click(config.get_web_elements('menu_icon_open'))
            self.click(config.get_web_elements('login_logo'))
            return True
        except Exception as e:
            return False

    def clear_cart(self):
        try:
            self.click(config.get_web_elements('menu_icon_open'))
            self.click(config.get_web_elements('reset_cart'))
            self.click(config.get_web_elements('menu_icon_close'))
            return True
        except Exception as e:
            return False

    def home_page(self):
        try:
            self.click(config.get_web_elements('menu_icon_open'))
            self.click(config.get_web_elements('all_items'))
            self.click(config.get_web_elements('menu_icon_close'))
            return True
        except Exception as e:
            return False

    def get_cart_items(self):
        cart_badge = self.page.locator(config.get_inventory_elements('cart_count'))
        count = 0
        if cart_badge.count() > 0:
            count = int(cart_badge.text_content())

        return count
