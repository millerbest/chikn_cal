from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Later put into config file
CHROME_DRIVER = r"./drivers/chromedriver.exe"
EGG_URL = "https://dexscreener.com/avalanche/0xb2ff0817ad078c92c3afb82326592e06c92581b8"


def get_egg_price() -> float:
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER, options=options)
    driver.get(EGG_URL)
    driver.implicitly_wait(5)
    price = driver.find_element(
        by="xpath",
        value="/html/body/div[1]/div/main/div/div/div[2]/div/div/div[1]/div[1]/ul/li[1]/div/span[2]/div",
    ).text
    return float(price.split("$")[1])
