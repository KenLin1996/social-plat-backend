# backend/models/post.py
from datetime import datetime, timezone
from backend import db
# from backend.models.user import User
from backend.models.like import Like
from backend.models.favorite import Favorite
from backend.models.comment import Comment


class Post(db.Model):
    __tablename__ = 'posts'  # 資料表名稱，會對應到資料庫中的 'posts' 表

    # 基本欄位
    id = db.Column(db.Integer, primary_key=True)    # 貼文 ID，主鍵
    image = db.Column(db.String(200), nullable=True)  # 儲存文章圖片的 URL
    content = db.Column(db.Text, nullable=False)  # 文章內容

    # 外鍵欄位，指向 User 表格
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # 關聯：每篇文章的作者
    author = db.relationship('User', backref='posts', lazy='joined')

    # 關聯：每篇貼文可以被多個使用者按讚和收藏
    likes = db.relationship('Like', backref='post', lazy=True)
    favorites = db.relationship('Favorite', backref='post', lazy=True)

    # 關聯：每篇文章可以有多個留言
    comments = db.relationship('Comment', backref='post', lazy=True)

    # 時間戳欄位
    created_at = db.Column(
        db.DateTime, default=datetime.now(timezone.utc))  # 創建時間
    updated_at = db.Column(db.DateTime, default=datetime.now(
        timezone.utc), onupdate=datetime.now(timezone.utc))  # 更新時間

    def __repr__(self):
        return f'<Post {self.id}>'

    @classmethod    # Python 語法，由類別調用的類別方法
    # 創建文章
    def create(cls, user_id, image, content):    # 參數 cls 表示類別本身（ Post），用來訪問類別屬性或建立類別實例。
        new_post = cls(user_id=user_id, image=image, content=content)

        # db.session 是 SQLAlchemy 提供的資料庫交易會話（Session）。用來管理與資料庫的互動，包含查詢、加入、更新、刪除資料等操作。

        db.session.add(new_post)    # 將新實例加入資料庫的交易會話，只是「準備」階段，尚未真正寫入資料庫。
        db.session.commit()  # 將所有未提交的變更（新增、更新、刪除）寫入資料庫
        return new_post

    # query 是 SQLAlchemy 提供的一個屬性，用來執行對資料庫的查詢操作。
    @classmethod
    # 取得所有文章
    def get_all(cls):
        return cls.query.all()

    # get() 方法僅能用於主鍵查詢，不能查詢其他欄位。如果找不到，返回 None。
    @classmethod
    # 根據 ID 查找文章
    def get_by_id(cls, post_id):
        return cls.query.get(post_id)

    @classmethod
    # 更新文章內容
    def update_content(cls, post_id, user_id, new_content):
        """
        僅允許修改文章內容，並限制只有作者能修改。
        :param post_id: 文章 ID
        :param user_id: 操作者的用戶 ID
        :param new_content: 新的文章內容
        :return: 更新後的文章物件，或錯誤訊息字典
        """
        post = cls.query.get(post_id)
        if not post:
            return {"error": "文章不存在"}

        # 檢查是否為文章的作者
        if post.user_id != user_id:
            return {"error": "您無權修改此文章"}

        # 更新文章內容
        post.content = new_content
        post.updated_at = datetime.now(timezone.utc)
        db.session.commit()

        return post

    @classmethod
    # 刪除文章
    def delete_post(cls, post_id, user_id):
        """
        僅允許作者刪除文章。
        :param post_id: 文章 ID
        :param user_id: 操作者的用戶 ID
        :return: 成功訊息或錯誤字典
        """
        post = cls.query.get(post_id)
        if not post:
            return {"error": "文章不存在"}

        if post.user_id != user_id:
            return {"error": "您無權刪除此文章"}

        db.session.delete(post)
        db.session.commit()
        return {"message": "文章已成功刪除"}
