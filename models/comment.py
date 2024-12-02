# backend/models/comment.py
from datetime import datetime, timezone
from backend import db


class Comment(db.Model):
    __tablename__ = 'comments'

    # 基本欄位
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)    # 留言內容
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)  # 發表留言的用戶
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), nullable=False)  # 留言所屬的貼文

    # 關聯：每個 Comment 都指向一個 User 和一個 Post
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))

    # 時間戳欄位：每個留言的創建時間
    created_at = db.Column(
        db.DateTime, default=datetime.now(timezone.utc))  # 留言創建時間
    updated_at = db.Column(db.DateTime, default=datetime.now(
        timezone.utc), onupdate=datetime.now)  # 留言更新時間

    def __repr__(self):
        return f"<Comment user_id={self.user_id} post_id={self.post_id} content={self.content[:20]}>"

    # 創建留言
    @classmethod
    def create(cls, user_id, post_id, content):
        new_comment = cls(user_id=user_id, post_id=post_id, content=content)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment

    # 根據貼文 ID 獲取所有留言
    @classmethod
    def get_comments_for_post(cls, post_id):
        return cls.query.filter_by(post_id=post_id).all()

    # 根據留言 ID 獲取單條留言
    @classmethod
    def get_comment_by_id(cls, comment_id):
        return cls.query.get(comment_id)

    # 修改留言
    @classmethod
    def update_comment(cls, comment_id, new_content):
        comment = cls.get_comment_by_id(comment_id)
        if comment:
            comment.content = new_content
            db.session.commit()
            return comment
        return None

    # 刪除留言
    @classmethod
    def delete_comment(cls, comment_id):
        comment = cls.get_comment_by_id(comment_id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return True
        return False
