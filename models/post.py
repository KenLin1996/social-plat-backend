# backend/models/post.py
from datetime import datetime, timezone
from backend import db  # 使用 app.py 裡的 db 實例


class Post(db.Model):
    __tablename__ = 'posts'  # 資料表名稱，會對應到資料庫中的 'posts' 表

    # 基本欄位
    id = db.Column(db.Integer, primary_key=True)    # 貼文 ID，主鍵
    image = db.Column(db.String(200), nullable=True)  # 儲存文章圖片的 URL
    content = db.Column(db.Text, nullable=False)  # 文章內容

    # 時間戳欄位
    created_at = db.Column(
        db.DateTime, default=datetime.now(timezone.utc))  # 創建時間
    updated_at = db.Column(db.DateTime, default=datetime.now(
        timezone.utc), onupdate=datetime.now(timezone.utc))  # 更新時間

    def __repr__(self):
        return f'<Post {self.id}>'

    @classmethod    # Python 語法，由類別調用的類別方法
    def create(cls, image, content):    # 參數 cls 表示類別本身（ Post），用來訪問類別屬性或建立類別實例。
        new_post = cls(image=image, content=content)

        # db.session 是 SQLAlchemy 提供的資料庫交易會話（Session）。用來管理與資料庫的互動，包含查詢、加入、更新、刪除資料等操作。

        db.session.add(new_post)    # 將新實例加入資料庫的交易會話，只是「準備」階段，尚未真正寫入資料庫。
        db.session.commit()  # 將所有未提交的變更（新增、更新、刪除）寫入資料庫
        return new_post

    # query 是 SQLAlchemy 提供的一個屬性，用來執行對資料庫的查詢操作。
    @classmethod
    def get_all(cls):
        return cls.query.all()

    # get() 方法僅能用於主鍵查詢，不能查詢其他欄位。如果找不到，返回 None。
    @classmethod
    def get_by_id(cls, post_id):
        return cls.query.get(post_id)
