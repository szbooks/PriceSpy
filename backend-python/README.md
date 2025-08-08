# PriceSpy 小程序后台API服务

基于 Flask + MySQL 的微信小程序后台API服务，为小程序端提供数据接口。

## 技术栈

- **框架**: Flask 2.3.3
- **数据库**: MySQL + PyMySQL
- **ORM**: SQLAlchemy
- **数据库迁移**: Flask-Migrate
- **跨域**: Flask-CORS

## 项目结构

```
backend-python/
├── app.py              # 主应用文件
├── models.py           # 数据模型
├── routes.py           # API路由
├── init_db.py          # 数据库初始化脚本
├── requirements.txt    # Python依赖
├── config.env.example  # 环境变量示例
└── README.md          # 说明文档
```

## 快速开始

### 1. 环境准备

- Python 3.8+
- MySQL 8.0+

### 2. 安装依赖

```bash
cd backend-python
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp config.env.example .env
# 编辑 .env 文件，配置数据库连接等信息
```

### 4. 创建数据库

```sql
CREATE DATABASE pricespy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 初始化数据库

```bash
python init_db.py
```

### 6. 启动服务

```bash
python app.py
```

服务将在 http://localhost:5000 启动

## API 接口

### 认证相关
- `POST /api/auth/login` - 微信小程序登录
- `GET /api/auth/verify` - 验证token

## 数据库模型

### User (用户表)
- id: 主键
- openid: 微信openid
- unionid: 微信unionid
- nickname: 用户昵称
- avatar: 用户头像
- phone: 手机号
- email: 邮箱
- status: 用户状态
- last_login_at: 最后登录时间
- login_count: 登录次数


## 开发说明

1. **数据库连接**: 确保MySQL服务运行，并创建了pricespy数据库
2. **环境变量**: 根据实际情况修改.env文件中的配置
3. **微信API**: 需要配置真实的微信小程序AppID和Secret
4. **生产部署**: 建议使用Gunicorn等WSGI服务器

## 注意事项

- 当前使用模拟的微信登录，生产环境需要集成真实的微信API
- 数据库连接字符串格式: `mysql+pymysql://用户名:密码@主机:端口/数据库名`
- 建议在生产环境中使用环境变量管理敏感信息
- 此服务专门为微信小程序提供API接口，不包含管理后台功能 