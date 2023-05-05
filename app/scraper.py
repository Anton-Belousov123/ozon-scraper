import time

import undetected_chromedriver as uc
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dataclasses import dataclass
from webdriver_manager.chrome import ChromeDriverManager


@dataclass()
class Item:
    article: int
    url: str
    name: str
    photo: str
    price: float


class Scraper:
    def scrape_item(self, text: str):
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        browser = uc.Chrome(ChromeDriverManager().install(), use_subprocess=True, options=options)
        browser.maximize_window()
        browser.get(f"https://www.ozon.ru/search/?from_global=true&text={text}")
        time.sleep(2)
        page_source = browser.page_source
        soup = BeautifulSoup(browser.page_source, features="html.parser")
        browser.close()
        objects = self._parse_code_to_object(soup)
        response = []
        for obj in objects:
            code = obj.photo.split('/')[-1].split('.')[0]
            codes = page_source.split(code)[-1].split(']')[0].split('multimedia-')[1::]
            images = [obj.photo.replace('/wc250', '')]
            for code in codes:
                symbol, code = code.split('&quot')[0].split('\\u002F')
                images.append('https://ir.ozone.ru/s3/multimedia-' + symbol + '/' + code)
            obj.photo = str(images)
            response.append(obj)
        return response
    def _parse_code_to_object(self, soup):
        response = []
        items = (
            soup.find("div", {"class": "widget-search-result-container"})
            .find("div")
            .find_all("div")
        )
        for item in items:
            try:
                description_block = str(item)
                try:
                    price = description_block.split("₽")[0].split(">")[-1]
                    price = float(
                        "".join(price.replace("thinsp;", "").replace(",", ".").split())
                    )
                except:
                    continue
                descr = (
                    description_block.split("</span></span></a>")[0]
                    .split("<span>")[-1]
                    .strip()
                )
                ozon_item_link_el = item.findNext("a")
                if not ozon_item_link_el:
                    continue
                ozon_item_link = "https://www.ozon.ru" + ozon_item_link_el.get("href")
                ozon_id = ozon_item_link.split("/?")[0].split("-")[-1]
                if ozon_id == 'https://www.ozon.ruhttps://job.ozon.ru/' or ozon_item_link_el.find("img") is None:
                    continue
                img = ozon_item_link_el.find("img").get("src")
                response.append(Item(
                    article=int(ozon_id),
                    url=ozon_item_link,
                    name=descr,
                    photo=img,
                    price=float(price)
                ))
            except:
                pass
        return response
