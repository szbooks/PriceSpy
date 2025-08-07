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

class Category(db.Model):
    """分类表"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, comment='分类名称')
    icon = db.Column(db.String(50), nullable=True, comment='分类图标')
    description = db.Column(db.Text, nullable=True, comment='分类描述')
    sort_order = db.Column(db.Integer, default=0, comment='排序')
    status = db.Column(db.Enum('active', 'inactive'), default='active', comment='状态')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联商品
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'description': self.description,
            'sort_order': self.sort_order,
            'status': self.status,
            'product_count': self.products.count(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Product(db.Model):
    """商品表"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, comment='商品名称')
    description = db.Column(db.Text, nullable=True, comment='商品描述')
    image = db.Column(db.String(255), nullable=True, comment='商品图片')
    price = db.Column(db.Numeric(10, 2), nullable=False, comment='当前价格')
    original_price = db.Column(db.Numeric(10, 2), nullable=True, comment='原价')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, comment='分类ID')
    brand = db.Column(db.String(100), nullable=True, comment='品牌')
    model = db.Column(db.String(100), nullable=True, comment='型号')
    url = db.Column(db.String(500), nullable=True, comment='商品链接')
    store = db.Column(db.String(100), nullable=True, comment='店铺名称')
    status = db.Column(db.Enum('active', 'inactive', 'discontinued'), default='active', comment='商品状态')
    last_price_update = db.Column(db.DateTime, nullable=True, comment='最后价格更新时间')
    price_change_count = db.Column(db.Integer, default=0, comment='价格变动次数')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联监测
    monitors = db.relationship('Monitor', backref='product', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'price': float(self.price),
            'original_price': float(self.original_price) if self.original_price else None,
            'category_id': self.category_id,
            'brand': self.brand,
            'model': self.model,
            'url': self.url,
            'store': self.store,
            'status': self.status,
            'last_price_update': self.last_price_update.isoformat() if self.last_price_update else None,
            'price_change_count': self.price_change_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Monitor(db.Model):
    """价格监测表"""
    __tablename__ = 'monitors'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户ID')
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, comment='商品ID')
    target_price = db.Column(db.Numeric(10, 2), nullable=False, comment='目标价格')
    current_price = db.Column(db.Numeric(10, 2), nullable=False, comment='当前价格')
    status = db.Column(db.Enum('monitoring', 'triggered', 'expired', 'cancelled'), default='monitoring', comment='监测状态')
    notification_enabled = db.Column(db.Boolean, default=True, comment='是否启用通知')
    check_interval = db.Column(db.Integer, default=3600, comment='检查间隔（秒）')
    last_check_at = db.Column(db.DateTime, nullable=True, comment='最后检查时间')
    triggered_at = db.Column(db.DateTime, nullable=True, comment='触发时间')
    expires_at = db.Column(db.DateTime, nullable=True, comment='过期时间')
    notes = db.Column(db.Text, nullable=True, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联用户
    user = db.relationship('User', backref='monitors')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'target_price': float(self.target_price),
            'current_price': float(self.current_price),
            'status': self.status,
            'notification_enabled': self.notification_enabled,
            'check_interval': self.check_interval,
            'last_check_at': self.last_check_at.isoformat() if self.last_check_at else None,
            'triggered_at': self.triggered_at.isoformat() if self.triggered_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 