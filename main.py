import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import datetime
from func import init_webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


def get_urls(driver, url):
    # url = 'https://docs.domonline.ru/category.php?id=9&name=obshchie-sobraniya'
    driver.get(url)
    driver.set_window_size(1920, 1080)
    names = []
    urls = []
    category_name = driver.find_element(By.CLASS_NAME, 'doc-inner-h1.wow.animate__fadeInUp').text
    el = driver.find_element(By.CLASS_NAME, 'doc_search-res-items.wow.animate__fadeInUp')
    for url in el.find_elements(By.TAG_NAME, 'a'):
        href = url.get_attribute('href')
        urls.append(href)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'doc_search-res-item-text')))
        name = url.find_element(By.CLASS_NAME, 'doc_search-res-item-text').text
        names.append(name)
    return zip(names, urls)


def name_category(url):
    driver.get(url)
    driver.set_window_size(1920, 1080)
    category_name = driver.find_element(By.CLASS_NAME, 'doc-inner-h1.wow.animate__fadeInUp').text
    return category_name


def save_link(book_link, book_name):
    the_book = requests.get(book_link, stream=True)
    with open(book_name, 'wb') as f:
        for chunk in the_book.iter_content(1024 * 1024 * 2):  # 2 MB chunks
            f.write(chunk)


def check(name):
    return name.replace('/', ' ')


def download(driver, category_urls):
    for category_url in category_urls:
        category_name = name_category(category_url)
        os.mkdir(category_name)

        for name, url in get_urls(driver, category_url):
            href = f"{url[:url.index('item')]}download/{url[url.find('&name=') + 6:]}.docx"

            save_link(href, f'{category_name}\{check(name)}.docx')
            print(href)
            """не стал переходить на каждую страницу, чтобы скаачать файл"""
            # driver.get(url)
            # driver.set_window_size(1920, 1080)
            # el = driver.find_element(By.CLASS_NAME, 'download-example-items')
            # tags = el.find_elements(By.TAG_NAME, 'a')
            # url_download = tags[1].get_attribute('href')


def category(driver, start):
    driver.get(start)
    driver.set_window_size(1920, 1080)
    category_links = []
    for i in range(1, 15):
        el = driver.find_element(By.CLASS_NAME, f'dz_doc-item.pdf-{i}')
        href = el.find_element(By.TAG_NAME, 'a').get_attribute('href')
        category_links.append(href)
    return category_links


def main(driver):
    startpage = 'https://docs.domonline.ru/category.php?id=9&name=obshchie-sobraniya'

    # pass
    # print(get_urls(driver))
    # driver.get(url)
    url_category = category(driver, startpage)

    download(driver, url_category)


if __name__ == '__main__':
    driver = init_webdriver()
    main(driver)
    # print(get_urls(driver))
    driver.quit()
