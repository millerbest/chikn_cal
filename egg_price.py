from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager


# Later put into config file
EGG_URL = "https://dexscreener.com/avalanche/0x3052a75dfd7a9d9b0f81e510e01d3fe80a9e7ec7"


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


if __name__ == "__main__":
    print(get_egg_price())
