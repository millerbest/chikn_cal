from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager


# Later put into config file
EGG_URL = "https://dexscreener.com/avalanche/0xb2ff0817ad078c92c3afb82326592e06c92581b8"


def get_egg_price() -> float:
    """Get the egg price using selenium, somehow it does not work with streamlit server"""
    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(EGG_URL)
        driver.implicitly_wait(5)
        price = driver.find_element(
            by="xpath",
            value="/html/body/div[1]/div/main/div/div/div[2]/div/div/div[1]/div[1]/ul/li[1]/div/span[2]/div",
        ).text
        return float(price.split("$")[1])
    except WebDriverException:
        return 5.0
