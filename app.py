# backend/app.py
# from backend.routes.user_route import user_bp
# from backend.routes.post_route import post_bp
from backend.models.user import User
from backend.models.post import Post
from backend.models.favorite import Favorite
from backend.models.like import Like
from backend.models.comment import Comment

from flask import Flask
from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
from backend import db  # 使用 backend/__init__.py 中的 db
from dotenv import load_dotenv
import os

from sqlalchemy.sql import text  # 導入 text 方法
from backend.config import Config

# 載入 .env 檔案
load_dotenv()

# 初始化應用程式
app = Flask(__name__)
app.config.from_object(Config)  # 載入配置檔

# 初始化資料庫
# db = SQLAlchemy(app)
db.init_app(app)  # 將 app 傳遞給 db 實例，完成初始化
migrate = Migrate(app, db)


# 載入 Routes
"""
app.register_blueprint(post_bp)  # 註冊貼文相關路由
app.register_blueprint(user_bp)  # 註冊認證相關路由（登入、註冊）
"""


# 創建資料庫表格（若資料庫尚未建立）
with app.app_context():
    db.create_all()


@app.route('/test-db')
def test_db():
    try:
        # 嘗試執行一個簡單的資料庫查詢
        db.session.execute(text('SELECT 1'))
        return "Database connection is successful!"
    except Exception as e:
        return f"Database connection failed: {e}"


if __name__ == '__main__':
    app.run(debug=True)
