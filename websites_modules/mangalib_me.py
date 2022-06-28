import requests
import re
import json
from init_webdriver import init_webdriver


def execute():
    print("Mangalib module started")

    # Ask user for what to do
    print("What do you want to do?")
    print("[1] Find manga using search system of website")
    print("[2] Download manga by url")
    to_do = input("Choose a number[default=1]: ")

    match to_do:
        case "1":
            find()
        case "2":
            download_by_url()
        case _:
            find()


def download_by_url():

    # Ask user for manga url
    url = input("Please enter manga url:\n")

    url = re.search('mangalib.me/.*', url)

    if url:
        url = url.string
        if url.startswith("https://"):
            pass
        elif url.startswith("http://"):
            print(
                "Url passed but using http protocol. It will be automatically replaced by https")
            url = url.replace("http://", "https://")
        else:
            print("Url passed but no protocol specified. Https will be used")
            url = f"https://{url}"
    else:
        return print("Url is incorrect")

    print("Intializing webdriver. Please wait. This may take a while")

    webdriver = init_webdriver()

    webdriver.close()
    webdriver.quit()


def find():
    pass
