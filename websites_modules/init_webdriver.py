import undetected_chromedriver
import time
from selenium import webdriver


def init_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = undetected_chromedriver.Chrome(options)

    return driver
