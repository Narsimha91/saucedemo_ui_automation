from pages.login_page import LoginPage
from utils import config
import allure
import pytest


def login(page, username, password, expected):

    assert LoginPage(page).login(username, password)
    if "inventory.html" in expected:
        assert expected in page.url
        assert LoginPage(page).logout()
        assert config.get('base_url') in page.url
    else:
        assert expected in LoginPage(page).get_text(config.get_login_elements('error_msg'))


@allure.feature("Login Page Validation")
@allure.story("Login page input validation")
@pytest.mark.parametrize("username, password, expected", config.USERS)
@pytest.mark.login_test
@pytest.mark.regression
@pytest.mark.functional_e2e
def test_login_all_users(username, password, expected, page):
    with allure.step(f"Login Page Validation with user: {username}"):
        login(page, username, password, expected)


@allure.feature("Login Page Validation")
@allure.story("Login with all Users")
@pytest.mark.parametrize("username, password, expected", config.LOGIN_SCENARIOS)
@pytest.mark.login_test
@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.functional_e2e
def test_login_validations(username, password, expected, page):
    login(page, username, password, expected)


@allure.feature("Login Page Validation")
@allure.story("Login with default User")
@pytest.mark.login_test
@pytest.mark.smoke
@pytest.mark.functional_e2e
@pytest.mark.parametrize("username, password, expected", [
    ("standard_user", "secret_sauce", "inventory.html")
])
def test_login_user(username, password, expected, page):
    login(page, username, password, expected)

