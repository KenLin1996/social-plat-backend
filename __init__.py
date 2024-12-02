# backend/__init__.py

from flask_sqlalchemy import SQLAlchemy

# 初始化 db 實例
db = SQLAlchemy()

# 將 db 初始化放在這裡，方便其他模組使用它
