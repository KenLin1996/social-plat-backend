# backend/models/user.py
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from backend import db


class User(db.Model):
    __tablename__ = 'users'

    # 基本欄位
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # 使用者暱稱
    email = db.Column(db.String(100), unique=True, nullable=False)  # 電子郵件
    password_hash = db.Column(db.String(128), nullable=False)  # 加密密碼
    mobile_phone = db.Column(db.String(15), unique=True)  # 支援國際電話號碼
    website = db.Column(db.String(200))  # 網站連結
    avatar = db.Column(
        db.String(200), default="default_avatar.png")  # 頭像，提供預設值
    profile_intro = db.Column(db.Text)  # 用戶自我介紹

    # 時間戳欄位
    created_at = db.Column(
        db.DateTime, default=datetime.now(timezone.utc))  # 帳戶創建時間
    updated_at = db.Column(db.DateTime, default=datetime.now(
        timezone.utc), onupdate=datetime.now(timezone.utc))  # 帳戶更新時間

    def __repr__(self):
        return f'<User {self.username}>'

    # 密碼相關方法
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 類別方法
    @classmethod
    def create(cls, username, email, password):
        new_user = cls(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    # 建立查詢條件的方法，通過將查詢條件作為參數傳遞來過濾資料表中的記錄。
    # #根據條件過濾資料，並返回一個查詢對象（query object），但不會馬上執行查詢。
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
