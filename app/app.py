import time

from app.database import Database
from app.scraper import Scraper


def start_app():
    database = Database()
    scraper = Scraper()
    while True:
        dbobj = database.get_code()
        if not dbobj:
            time.sleep(60)
            continue
        try:
            item = scraper.scrape_item(dbobj.s_name)
        except Exception:
            item = []
        print(item)
        database.update_item(item, dbobj)
