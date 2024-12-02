# backend/models/like.py
from datetime import datetime, timezone
from backend import db


class Like(db.Model):
    __tablename__ = "likes"

    # 基本欄位
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    # 關聯：每個 Like 都會指向一個 User 和一個 Post
    user = db.relationship('User', backref=db.backref('likes', lazy=True))
    post = db.relationship('Post', backref=db.backref('likes', lazy=True))

    # 時間戳欄位：每個點讚的時間
    created_at = db.Column(
        db.DateTime, default=datetime.now(timezone.utc))  # 創建時間

    def __repr__(self):
        return f"<Like user_id={self.user_id} post_id={self.post_id}>"

    @classmethod
    def create(cls, user_id, post_id):
        new_like = cls(user_id=user_id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()
        return new_like

    @classmethod
    def get_by_user_and_post(cls, user_id, post_id):
        return cls.query.filter_by(user_id=user_id, post_id=post_id).first()

    @classmethod
    def delete_like(cls, user_id, post_id):
        result = cls.query.filter_by(user_id=user_id, post_id=post_id).delete()
        if result:
            db.session.commit()
            return True
        return False
