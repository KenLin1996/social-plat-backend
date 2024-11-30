# backend/app.py
# from backend.routes.user_routes import user_bp
# from backend.routes.post_routes import post_bp
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os

# 初始化應用程式
app = Flask(__name__)
app.config.from_object(Config)  # 載入配置檔

# 初始化資料庫
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 載入 Routes
"""
app.register_blueprint(post_bp)  # 註冊貼文相關路由
app.register_blueprint(user_bp)  # 註冊認證相關路由（登入、註冊）
"""


# 創建資料庫表格（若資料庫尚未建立）
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
