
import shutil, os, time
import pytest, allure
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from utils import config as configuration
from utils.logger import get_logger

def pytest_configure(config):
    try:
        shutil.rmtree("allure-results")
    except:
        pass

    screenshot_dir = "screenshots"
    if os.path.exists(screenshot_dir):
        shutil.rmtree(screenshot_dir)
    os.makedirs(screenshot_dir, exist_ok=True)

@pytest.fixture(autouse=True)
def execution_time(test_logger, request):
    start = time.perf_counter()
    yield
    test_logger.info("Execution time of %s is: %.2f seconds"
                     , request.node.name, time.perf_counter() - start)

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit", "chrome", "edge"],
        help="Browser to run tests against",
    )
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Browser to run tests on: chrome, firefox, edge"
    )
    parser.addoption(
        "--buy",
        action="store",
        default="1",
        help="Specify Purchase count",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Only take screenshot if the test failed during execution
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            allure.attach(
                page.screenshot(),
                name=f"{item.name}_failure",
                attachment_type=allure.attachment_type.PNG
            )



@pytest.fixture
def login_fixture(page):
    return LoginPage(page).login("standard_user", "secret_sauce")


@pytest.fixture(scope="session")
def browser(request):
    browser_name = request.config.getoption("--browser")

    with sync_playwright() as p:
        if browser_name == "chromium":
            browser = p.chromium.launch(headless=False,
                slow_mo=configuration.SLOW_MO)

        elif browser_name == "firefox":
            browser = p.firefox.launch(headless=False, args=["--start-maximized"])

        elif browser_name == "webkit":
            browser = p.webkit.launch(headless=False)

        elif browser_name == "chrome":
            browser = p.chromium.launch(
                channel="chrome",
                headless=False,
                args=["--start-maximized"],
                slow_mo=1000
            )

        elif browser_name == "edge":
            browser = p.chromium.launch(
                channel="msedge",
                headless=False
            )

        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.saucedemo.com")

    yield page

    context.close()


def pytest_sessionstart(session):
    if session.config.getoption("--env").lower() == "prod":
        pytest.exit(
            "Execution stopped: Tests are not allowed on the Production environment.",
            returncode=1
        )

# Test Fixtures
@pytest.fixture(scope="session")
def test_logger():
    return get_logger("api_automation")