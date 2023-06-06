import allure
import pytest
import requests
from playwright.sync_api import sync_playwright
from env_settings.env_prod import Prod
from page_object.dashboard.dashboard_page import DashboardPage
from page_object.dashboard.landing_page import LandingPage
from page_object.dashboard.login_page import LoginPage
from schemas.base_schemas import LastEthBlockModel, ResultListModel
from utils.common import check_object_model


class TestDashboard:

    @pytest.fixture(scope="module")
    def browser(self):
        with sync_playwright() as playwright:
            # Запуск браузера с графическим интерфейсом headless=False / без графического интерфейса headless=True
            browser = playwright.chromium.launch(headless=True)
            yield browser
            browser.close()

    def test_login_api_e2e(self, browser):
        page = browser.new_page()
        page.goto(Prod.GETBLOCK_LANDING_PAGE)
        page.wait_for_url(url=Prod.GETBLOCK_LANDING_PAGE, wait_until="load")
        assert page.url == Prod.GETBLOCK_LANDING_PAGE
        page.click(LandingPage.ACCOUNT_BUTTON)
        page.wait_for_url(url=Prod.GETBLOCK_LOGIN_UI_PAGE, wait_until="load")
        assert page.url == Prod.GETBLOCK_LOGIN_UI_PAGE
        page.click(LoginPage.EMAIL_LOGIN_BUTTON)
        page.wait_for_url(url=Prod.GETBLOCK_SIGN_IN_EMAIL, wait_until="load")
        assert page.url == Prod.GETBLOCK_SIGN_IN_EMAIL
        page.type(LoginPage.EMAIL_INPUT_FIELD, text=Prod.MERCHANT_EMAIL, delay=100)
        page.type(LoginPage.PASSWORD_INPUT_FIELD, text=Prod.MERCHANT_PASSWORD, delay=100)
        page.click(LoginPage.CONTINUE_BUTTON)
        page.wait_for_url(url=Prod.GETBLOCK_DASHBOARD_UI_PAGE, wait_until="load")
        assert page.url == Prod.GETBLOCK_DASHBOARD_UI_PAGE
        # # Решение 1 не рабочее в браузере инкогнито доступ к clipboard отключен (локально работает)
        page.click(DashboardPage.KEY_BUTTON)
        # page.click(DashboardPage.COPY_BUTTON)
        # api_key_clipboard_value = page.evaluate("navigator.clipboard.readText()")
        # api_key = api_key_clipboard_value
        # # Решение 2 - рабочее- задать апи ключ в переменных
        # api_key = Prod.API_KEY
        # # Решение 3 - не рабочее - скопировать innertext по локатору (Текст в элементе protected)
        # api_key = page.inner_text(DashboardPage.API_KEY_VALUE)
        # Решение 4 - рабочее получить значение через JS page evaluate
        api_key = page.evaluate(Prod.API_KEY_JS)
        headers = {
            "x-api-key": f"{api_key}"
        }
        payload = {
            "jsonrpc": "2.0",
            "id": "healthcheck",
            "method": "getmininginfo",
            "params": []
        }

        response = requests.post(Prod.BITCOIN_TESTNET_URL, headers=headers, json=payload)
        with allure.step(f'{response=} equals {Prod.status_code_success=}'):
            assert response.status_code == Prod.status_code_success
        data = response.json()
        with allure.step(f'Check object model'):
            check_object_model(LastEthBlockModel, data)
        response_time = response.elapsed.total_seconds()
        data_result = data["result"]
        with allure.step(f'Check object model'):
            check_object_model(ResultListModel, data_result)
        with allure.step(f'{response_time=} less {Prod.max_response_time=}'):
            assert response_time <= Prod.max_response_time
        page.close()
