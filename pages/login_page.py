from pages.base_page import BasePage
from utils import config


class LoginPage(BasePage):


    def login(self, username, password):
        try:
            self.fill(config.get_login_elements('username'), username)
            self.fill(config.get_login_elements('password'), password)
            self.click(config.get_login_elements('login_btn'))
            return True
        except Exception as e:
            return False

    def logout(self):
        try:
            self.click(config.get_web_elements('menu_icon_open'))
            self.click(config.get_web_elements('login_logo'))
            return True
        except Exception as e:
            return False


    def get_error(self):
        return self.get_text(config.get_login_elements('error_msg'))

    def get_attributes(self, *args):
        return self.page.locator(args[0]).get_attribute(args[1])



