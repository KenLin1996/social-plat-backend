# backend/config.py
from dotenv import load_dotenv
import os
import pymysql
pymysql.install_as_MySQLdb()


# 載入 .env 配置檔案
load_dotenv()

# 載入 .env 配置檔案，指定 backend 資料夾中的 .env
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


class Config:
    # 設定 Flask 應用程式的密鑰
    # 若 .env 中無 SECRET_KEY，則使用隨機生成的密鑰
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))

    # 設定 MySQL 資料庫連接字串，並從環境變數讀取
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    # 禁用 SQLAlchemy 的物件修改追蹤功能，提升性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False
