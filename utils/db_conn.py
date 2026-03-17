import pymysql
import logging
from utils.data_loader import *

logger = logging.getLogger("APITest")


class Database:
    def __init__(self, db_type="mysql"):
        cfg = config[db_type]  # 直接从JSON取对应数据库配置
        self.conn = pymysql.connect(
            host=cfg["host"],
            port=cfg["port"],
            user=cfg["username"],
            password=cfg["password"],
            database=cfg["database"],
            charset=cfg.get("charset", "utf8mb4"),
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()
        logger.info(f"{db_type} 数据库连接成功")

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        affected = self.cursor.execute(sql, params or ())
        self.conn.commit()
        return affected

    def close(self):
        self.cursor.close()
        self.conn.close()
        logger.info("数据库连接已关闭")


# 使用示例
if __name__ == "__main__":
    db = Database("mysql")
    data = db.query("SELECT * FROM redis_data_test2 order by id LIMIT 5 ")
    print(data)
    db.close()
