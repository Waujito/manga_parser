import string
from websites_modules.init_webdriver import init_webdriver
import requests
from bs4 import BeautifulSoup
from os import mkdir
from pathlib import Path
from urllib.parse import urlparse

from selenium.webdriver.common.by import By
from selenium import webdriver


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

    print("Parsing url...")
    url = urlparse(url)

    if url.netloc == "mangalib.me" or url.netloc == "www.mangalib.me":
        if url.scheme == "https":
            pass
        elif url.scheme == "http":
            print(
                "Url passed but using http protocol. It will be automatically replaced by https")
            url = url._replace(scheme="https")
        else:
            print("Url passed but no protocol specified. Https will be used")
            url._replace(scheme="https")
    else:
        return print("Url is incorrect")

    url_path = [x for x in url.path.split('/') if x]

    if url_path.__len__() == 1:
        q = input(
            f"Is {url.path} path to manga that you would to download?[Y/n] ")
        if q == "y" or q == "Y" or q == "" or q == " ":
            print("Intializing webdriver. Please wait. This may take a while...")
            webdriver = init_webdriver()
            print("Webdriver successfully initialized. Loading page...")

            get_manga_info(*url_path, webdriver=webdriver)

        else:
            return print("Invalid uri")
    elif url_path.__len__() == 3:
        q = input(
            f"Is {url.path} path to tom and chapter that you would to download?[Y/n] ")
        if q == "y" or q == "Y" or q == "" or q == " ":
            print("Intializing webdriver. Please wait. This may take a while...")
            webdriver = init_webdriver()
            print("Webdriver successfully initialized. Downloading...")

            url_path[1] = int(url_path[1].removeprefix('v'))
            url_path[2] = int(url_path[2].removeprefix('c'))

            download_chapter(*url_path, webdriver=webdriver)

        else:
            return print("Invalid uri")
    else:
        return print("Invalid uri")

    webdriver.close()
    webdriver.quit()


def find():
    pass


def download_chapter(manga_name: string, tom_num: int, chapter_num: int, webdriver: webdriver.Chrome):
    url = f"https://mangalib.me/{manga_name}/v{tom_num}/c{chapter_num}"
    webdriver.get(url)

    # Check driver url and manga url
    if urlparse(url).path != urlparse(webdriver.current_url).path:

        print(url)
        print(webdriver.current_url)

        with open('page_data.html', 'w', encoding='utf-8') as f:
            f.write(webdriver.page_source)

        webdriver.close()
        webdriver.quit()
        raise Exception(
            "Something went wrong. Page url does not equals webdriver url. Seems like redirect. Page data has been saved to page_data.html")

    # By default mangalib loads only 2 first manga pages
    # So we cannot simply parse it
    # Loading one page and then accessing new one like viewers

    # Getting all pages
    pages = webdriver.find_elements(
        By.XPATH, "//select[@id='reader-pages']/option")

    if not pages:
        with open('page_data.html', 'w', encoding='utf-8') as f:
            f.write(webdriver.page_source)

        webdriver.close()
        webdriver.quit()
        raise Exception(
            "Something went wrong. Cannot find manga pages. Page data has been saved to page_data.html")

    # Creating destination dirs

    dist_path = Path(__file__).parent.parent.joinpath('dist_manga')
    if not dist_path.exists():
        mkdir(dist_path)

    manga_path = Path(dist_path, manga_name)
    if not manga_path.exists():
        mkdir(manga_path)

    tom_path = Path(manga_path, f"tom {tom_num}")
    if not tom_path.exists():
        mkdir(tom_path)

    chapter_path = Path(tom_path, f"chapter {chapter_num}")
    if not chapter_path.exists():
        mkdir(chapter_path)

    for page in pages:
        page.click()

        page_num = page.get_attribute('value')

        manga_img = webdriver.find_element(
            By.XPATH,
            f"//div[@class='reader']/div[@class='reader-view']/div[@class='reader-view__container']/div[@data-p='{page_num}']/img"
        ).get_attribute('src')

        print(f"Downloading {manga_img}...")

        resp = requests.get(manga_img)

        if manga_img.endswith('.png'):
            filename = f"{page_num}.png"
        elif manga_img.endswith('.jpg'):
            filename = f"{page_num}.jpg"
        elif manga_img.endswith('.jpeg'):
            filename = f"{page_num}.jepg"
        else:
            raise Exception(f"Undefined file extension: {manga_img}")

        with open(Path(chapter_path, filename), 'wb') as f:
            f.write(resp.content)


def download_tom(manga_name, tom_num, webdriver):
    pass


def get_manga_info(manga_name, webdriver):
    pass
