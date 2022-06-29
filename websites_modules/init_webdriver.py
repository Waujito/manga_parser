import undetected_chromedriver
import time
from selenium import webdriver
from pathlib import Path


def init_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Start chrome in silent mode

    # If driver file exists run chrome from driver
    # Else download driver
    if Path(Path(__file__).parent.resolve(), 'chromedriver.exe').exists():
        driver = undetected_chromedriver.Chrome(options=options, driver_executable_path=Path(
            Path(__file__).parent.resolve(), 'chromedriver.exe').__str__())
    else:
        driver = undetected_chromedriver.Chrome(options=options)

    return driver
