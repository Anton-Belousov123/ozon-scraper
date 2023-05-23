from app.scraper import Item
from secrets import secret
import psycopg2
import dataclasses


@dataclasses.dataclass
class DBObj:
    s_article: str
    s_name: str
    s_url: str
    s_photo: str
    s_price: float
    t_name: str
    t_url: str
    t_photo: str
    t_price: float
    t_type: str
    stage: str
    t_article: int


class Database:
    def __init__(self):
        pass

    def delete_item(self, dbobj: DBObj):
        self.conn = psycopg2.connect(
            host=secret.DATABASE_HOST,
            database=secret.DATABASE_NAME,
            user=secret.DATABASE_LOGIN,
            password=secret.DATABASE_PASSWORD,
        )
        self.cur = self.conn.cursor()
        self.cur.execute('UPDATE oleg SET stage=%s WHERE s_article=%s;', ('Ozon error', dbobj.s_article))
        self.conn.commit()
        self.conn.close()

    def get_code(self, table_name):
        self.conn = psycopg2.connect(
            host=secret.DATABASE_HOST,
            database=secret.DATABASE_NAME,
            user=secret.DATABASE_LOGIN,
            password=secret.DATABASE_PASSWORD,
        )
        self.cur = self.conn.cursor()
        self.cur.execute(f"SELECT * FROM {table_name} WHERE stage=%s", ("Source parsed",))
        record = self.cur.fetchone()
        if not record:
            return None
        return DBObj(
            record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8],
            record[9], record[10], record[11])
        self.conn.close()
    def update_item(self, items: list[Item], dbobj: DBObj, table_name):
        self.conn = psycopg2.connect(
            host=secret.DATABASE_HOST,
            database=secret.DATABASE_NAME,
            user=secret.DATABASE_LOGIN,
            password=secret.DATABASE_PASSWORD,
        )
        self.cur = self.conn.cursor()
        self.cur.execute(f'DELETE FROM {table_name} WHERE s_article=%s;', (dbobj.s_article,))
        for item in items:
            self.cur.execute(
                f"INSERT INTO {table_name} (s_article, s_name, s_url, s_photo, s_price, t_name, t_url, t_photo, t_price, t_type, stage, t_article) "
                f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (dbobj.s_article, dbobj.s_name, dbobj.s_url, dbobj.s_photo, dbobj.s_price, item.name, item.url,
                 item.photo, item.price, 'ozon', 'Target parsed', item.article)
            )
        self.conn.commit()
        self.conn.close()