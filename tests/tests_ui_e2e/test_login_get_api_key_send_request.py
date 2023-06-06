import allure
import pytest
import requests
from playwright.sync_api import sync_playwright
from pytest_playwright.pytest_playwright import browser_type, page
from env_settings.env_prod import GETBLOCK_LANDING_PAGE, MERCHANT_EMAIL, MERCHANT_PASSWORD, GETBLOCK_LOGIN_UI_PAGE, \
    GETBLOCK_DASHBOARD_UI_PAGE, status_code_success, max_response_time, BITCOIN_TESTNET_URL, GETBLOCK_SIGN_IN_EMAIL, \
    API_KEY
from page_object.dashboard.dashboard_page import KEY_BUTTON, API_KEY_VALUE, COPY_BUTTON
from page_object.dashboard.landing_page import ACCOUNT_BUTTON
from page_object.dashboard.login_page import EMAIL_LOGIN_BUTTON, EMAIL_INPUT_FIELD, PASSWORD_INPUT_FIELD, \
    CONTINUE_BUTTON
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
        page.goto(GETBLOCK_LANDING_PAGE)
        page.wait_for_url(url=GETBLOCK_LANDING_PAGE, wait_until="load")
        assert page.url == GETBLOCK_LANDING_PAGE
        page.click(ACCOUNT_BUTTON)
        page.wait_for_url(url=GETBLOCK_LOGIN_UI_PAGE,wait_until="load")
        assert page.url == GETBLOCK_LOGIN_UI_PAGE
        page.click(EMAIL_LOGIN_BUTTON)
        page.wait_for_url(url=GETBLOCK_SIGN_IN_EMAIL,wait_until="load")
        assert page.url == GETBLOCK_SIGN_IN_EMAIL
        page.type(EMAIL_INPUT_FIELD, text=MERCHANT_EMAIL, delay=100)
        page.type(PASSWORD_INPUT_FIELD, text=MERCHANT_PASSWORD, delay=100)
        page.click(CONTINUE_BUTTON)
        page.wait_for_url(url=GETBLOCK_DASHBOARD_UI_PAGE, wait_until="load")
        assert page.url == GETBLOCK_DASHBOARD_UI_PAGE
        # # Решение 1 не рабочее в браузере инкогнито доступ к clipboard
        page.click(KEY_BUTTON)
        page.click(COPY_BUTTON)
        # api_key_clipboard_value = page.evaluate("navigator.clipboard.readText()")
        # api_key = api_key_clipboard_value
        # # Решение 2 - рабочее- захардкодить апи ключ
        api_key = API_KEY
        # # Решение 3 - не рабочее - скопировать innertext по локатору (Текст в элементе protected)
        # api_key = page.inner_text(API_KEY_VALUE)
        # Решение 4 - не рабочее получить значение через JS $0.value
        # element = page.query_selector(API_KEY_VALUE)
        # api_key = element.evaluate('(api_key) => $0.value')
        headers = {
            "x-api-key": f"{api_key}"
        }
        payload = {
            "jsonrpc": "2.0",
            "id": "healthcheck",
            "method": "getmininginfo",
            "params": []
        }

        response = requests.post(BITCOIN_TESTNET_URL, headers=headers,json=payload)
        with allure.step(f'{response=} equals {status_code_success=}'):
            assert response.status_code == status_code_success
        data = response.json()
        with allure.step(f'Check object model'):
            check_object_model(LastEthBlockModel, data)
        response_time = response.elapsed.total_seconds()
        data_result = data["result"]
        with allure.step(f'Check object model'):
            check_object_model(ResultListModel, data_result)
        with allure.step(f'{response_time=} less {max_response_time=}'):
            assert response_time <= max_response_time
        page.close()


