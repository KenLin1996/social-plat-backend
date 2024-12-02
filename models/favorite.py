# backend/models/favorite.py
from datetime import datetime, timezone
from backend import db


class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    # 關聯：每個 Favorite 都會指向一個 User 和一個 Post
    user = db.relationship('User', backref=db.backref('favorites', lazy=True))
    post = db.relationship('Post', backref=db.backref('favorites', lazy=True))

    # 時間戳欄位：每個收藏的時間
    created_at = db.Column(
        db.DateTime, default=datetime.now(timezone.utc))  # 創建時間

    def __repr__(self):
        return f"<Favorite user_id={self.user_id} post_id={self.post_id}>"

    # 類別方法：創建 Favorite
    @classmethod
    def create(cls, user_id, post_id):
        new_favorite = cls(user_id=user_id, post_id=post_id)
        db.session.add(new_favorite)
        db.session.commit()
        return new_favorite

    # 類別方法：根據 user_id 和 post_id 查找指定的 Favorite
    @classmethod
    def get_by_user_and_post(cls, user_id, post_id):
        return cls.query.filter_by(user_id=user_id, post_id=post_id).first()

    # 類別方法：取得某個用戶的所有收藏（Favorites）
    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    # 類別方法：取得某篇貼文的所有收藏（Favorites）
    @classmethod
    def get_all_by_post(cls, post_id):
        return cls.query.filter_by(post_id=post_id).all()
