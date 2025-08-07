#!/usr/bin/env python3
"""
数据库初始化脚本
"""

from app import app, db
from models import User, Product, Monitor, Category
from datetime import datetime

def init_database():
    """初始化数据库"""
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("数据库表创建完成")

        # 检查是否已有数据
        if Category.query.count() == 0:
            # 创建默认分类
            categories = [
                Category(
                    name='数码产品',
                    icon='📱',
                    description='手机、电脑、平板等数码产品',
                    sort_order=1
                ),
                Category(
                    name='服装鞋帽',
                    icon='👕',
                    description='衣服、鞋子、帽子等服饰',
                    sort_order=2
                ),
                Category(
                    name='家居用品',
                    icon='🏠',
                    description='家具、家电、生活用品',
                    sort_order=3
                ),
                Category(
                    name='食品饮料',
                    icon='🍎',
                    description='零食、饮料、生鲜等',
                    sort_order=4
                )
            ]
            
            for category in categories:
                db.session.add(category)
            
            db.session.commit()
            print("默认分类创建完成")

        if Product.query.count() == 0:
            # 创建示例商品
            products = [
                Product(
                    name='iPhone 15 Pro',
                    description='最新款iPhone，搭载A17 Pro芯片',
                    price=7999.00,
                    original_price=8999.00,
                    category_id=1,
                    brand='Apple',
                    model='iPhone 15 Pro',
                    url='https://example.com/product/1',
                    store='Apple官方旗舰店',
                    last_price_update=datetime.utcnow()
                ),
                Product(
                    name='MacBook Air M2',
                    description='轻薄便携的MacBook Air，搭载M2芯片',
                    price=8999.00,
                    original_price=9999.00,
                    category_id=1,
                    brand='Apple',
                    model='MacBook Air M2',
                    url='https://example.com/product/2',
                    store='Apple官方旗舰店',
                    last_price_update=datetime.utcnow()
                ),
                Product(
                    name='Nike Air Max 270',
                    description='舒适透气的运动鞋',
                    price=899.00,
                    original_price=1099.00,
                    category_id=2,
                    brand='Nike',
                    model='Air Max 270',
                    url='https://example.com/product/3',
                    store='Nike官方旗舰店',
                    last_price_update=datetime.utcnow()
                )
            ]
            
            for product in products:
                db.session.add(product)
            
            db.session.commit()
            print("示例商品创建完成")

        print("数据库初始化完成！")

if __name__ == '__main__':
    init_database() 