import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import re
import json
import urllib.parse
import time

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    }

def get_source_html(url):
    driver = webdriver.Chrome(executable_path="C:\PythonCode\spb_zoon_ru__medical\chromedriver.exe")
    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(3)

        while True:
            find_more_element = driver.find_element(By.CLASS_NAME, "catalog-button-showMore")

            if driver.find_elements(By.CLASS_NAME, "hasmore-text"):
                with open("C:\PythonCode\spb_zoon_ru__medical\source_page.html", "w") as file:
                    file.write(driver.page_source)
                break

            else:
                ActionChains(driver).move_to_element(find_more_element).perform()
                time.sleep(3)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def get_items_url(file_path):
    with open(file_path) as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    items_urls = soup.find_all(class_="minicard-item js-results-item")

    urls = []
    for item in items_urls:
        item_url = item.find("div", class_="minicard-item__container").find(class_="minicard-item__title").find("a").get("href")
        urls.append(item_url)

    with open("C:\PythonCode\spb_zoon_ru__medical\items_urls.txt", "w") as file:
        for url in urls:
            file.write(f"{url}\n")

    print("[INFO] Urls collected successfully!")


def get_data(file_path):
    with open(file_path) as file:

        url_read_file = file.readlines()
        url_list = []
        for url in url_read_file:
            url = url.strip()
            url_list.append(url)

        # url_list = [url.strip() for url in file.readlines()]

    count = 0
    url_count = len(url_list)

    rezult_list = []
    for url in url_list:
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        try:
            # item_name = soup.find("span", {"itemprop":"name"}).text.strip()
            item_name = soup.find("span", {"itemprop": "name"}).text.replace(" ", " ").strip()
        except Exception as _ex:
            item_name = None

        item_phone = []
        try:
            phone_number = soup.find("div", class_="service-phones-list").find_all("a", {"rel":"nofollow"})
            for item in phone_number:
                item_phones = item.get("href").split(":")[-1].strip()
                item_phone.append(item_phones)
        except Exception as _ex:
            item_phone = None

        try:
            # item_address = soup.find("address", class_="iblock").text.strip()
            item_address = soup.find("address", class_="iblock").text.replace(" ", " ").strip()
        except Exception as _ex:
            item_address = None

        try:
            item_site = soup.find(text=re.compile("Сайт|Официальный сайт")).find_next().text.strip()
        except Exception as _ex:
            item_site = None

        item_social_network = []
        try:
            sn_list = soup.find(text=re.compile("Страница в соцсетях")).find_next().find_all("a")
            for item in sn_list:
                sn_url = item.get("href")
                sn_unquote = urllib.parse.unquote(sn_url).split("?to=")[1].split("&")[0]
                item_social_network.append(sn_unquote)
        except Exception as _ex:
            item_social_network = None

        rezult_list.append(
            {
                "item_name": item_name,
                "item_phone": item_phone,
                "item_address": item_address,
                "item_site": item_site,
                "item_social_network": item_social_network
            }
        )

        count+=1
        print(f"[+ INFO] {count}/{url_count}")

        # time.sleep(random.randrange(3, 5))

    with open("C:\PythonCode\spb_zoon_ru__medical\qwerty.json", "w") as file:
        json.dump(rezult_list, file, indent=4, ensure_ascii=False)
        # print(item_name, item_phone, item_address, item_site, item_social_network)


def main():
    get_source_html(url="https://spb.zoon.ru/medical/type/detskaya_poliklinika/")
    get_items_url(file_path="C:\PythonCode\spb_zoon_ru__medical\source_page.html")
    get_data("C:\PythonCode\spb_zoon_ru__medical\items_urls.txt")

if __name__ == "__main__":
    main()
