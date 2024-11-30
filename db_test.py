from app import app, db
import sys
import os

# 將 backend 資料夾加入 Python 模組搜尋路徑
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'backend')))


# 測試資料庫連接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Samson1219@127.0.0.1/myPracticeDatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    try:
        print("Testing database connection...")
        db.create_all()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error during database test: {e}")
