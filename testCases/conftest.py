import pytest
from selenium.webdriver import common
from selenium.webdriver.chrome.service import Service
from selenium import common
from selenium import webdriver


@pytest.fixture
def setup():
    try:
        ser = Service(".\\chromedriver.exe")
        op = webdriver.ChromeOptions()
        op.add_experimental_option('excludeSwitches', ['enable-logging'])
        op.add_argument('--ignore-certificate-errors-spki-list')
        op.add_argument('--ignore-ssl-errors')
        op.add_argument('ignore-certificate-errors')
        op.add_argument('force-device-scale-factor=0.95')
        op.add_argument('high-dpi-support=0.95')
        driver = webdriver.Chrome(service=ser, options=op)
        driver.maximize_window()
    except common.exceptions.WebDriverException:
        print("Chrome Driver Error")
    else:
        return driver



