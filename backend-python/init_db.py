#!/usr/bin/env python3
"""
数据库初始化脚本
"""

from app import app, db
from models import User

def init_database():
    """初始化数据库"""
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("数据库表创建完成")

        print("数据库初始化完成！")

if __name__ == '__main__':
    init_database() 