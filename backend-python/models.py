from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """用户表"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(100), unique=True, nullable=False, comment='微信openid')
    unionid = db.Column(db.String(100), unique=True, nullable=True, comment='微信unionid')
    nickname = db.Column(db.String(50), nullable=True, comment='用户昵称')
    avatar = db.Column(db.String(255), nullable=True, comment='用户头像')
    phone = db.Column(db.String(20), nullable=True, comment='手机号')
    email = db.Column(db.String(100), nullable=True, comment='邮箱')
    status = db.Column(db.Enum('active', 'inactive', 'banned'), default='active', comment='用户状态')
    last_login_at = db.Column(db.DateTime, nullable=True, comment='最后登录时间')
    login_count = db.Column(db.Integer, default=0, comment='登录次数')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'openid': self.openid,
            'unionid': self.unionid,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'phone': self.phone,
            'email': self.email,
            'status': self.status,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'login_count': self.login_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 