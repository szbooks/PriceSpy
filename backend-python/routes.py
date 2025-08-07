from flask import Blueprint, request, jsonify
from models import db, User, Product, Monitor, Category
from datetime import datetime
import requests

# 创建蓝图
auth_bp = Blueprint('auth', __name__)
products_bp = Blueprint('products', __name__)
monitors_bp = Blueprint('monitors', __name__)
users_bp = Blueprint('users', __name__)
categories_bp = Blueprint('categories', __name__)

# 认证相关路由
@auth_bp.route('/login', methods=['POST'])
def login():
    """微信小程序登录"""
    try:
        data = request.get_json()
        code = data.get('code')
        
        if not code:
            return jsonify({'error': '缺少code参数'}), 400

        # TODO: 调用微信API获取openid
        # 这里使用模拟数据
        openid = f'mock-openid-{datetime.now().timestamp()}'
        
        # 查找或创建用户
        user = User.query.filter_by(openid=openid).first()
        if not user:
            user = User(
                openid=openid,
                nickname='用户',
                status='active'
            )
            db.session.add(user)
            db.session.commit()
        
        # 更新登录信息
        user.last_login_at = datetime.utcnow()
        user.login_count += 1
        db.session.commit()

        return jsonify({
            'success': True,
            'message': '登录成功',
            'data': {
                'token': f'mock-token-{datetime.now().timestamp()}',
                'openid': openid,
                'user_id': user.id
            }
        })
    except Exception as e:
        return jsonify({'error': f'登录失败: {str(e)}'}), 500

@auth_bp.route('/verify', methods=['GET'])
def verify_token():
    """验证token"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': '缺少token'}), 401

        # TODO: 验证token
        return jsonify({
            'success': True,
            'message': 'token有效'
        })
    except Exception as e:
        return jsonify({'error': f'token验证失败: {str(e)}'}), 401

# 商品相关路由
@products_bp.route('/', methods=['GET'])
def get_products():
    """获取商品列表"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        category = request.args.get('category', type=int)
        keyword = request.args.get('keyword', '')

        query = Product.query

        if category:
            query = query.filter_by(category_id=category)
        
        if keyword:
            query = query.filter(Product.name.contains(keyword))

        products = query.paginate(
            page=page, 
            per_page=limit, 
            error_out=False
        )

        return jsonify({
            'success': True,
            'data': {
                'products': [product.to_dict() for product in products.items],
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': products.total,
                    'pages': products.pages
                }
            }
        })
    except Exception as e:
        return jsonify({'error': f'获取商品列表失败: {str(e)}'}), 500

@products_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    """获取商品详情"""
    try:
        product = Product.query.get_or_404(id)
        return jsonify({
            'success': True,
            'data': product.to_dict()
        })
    except Exception as e:
        return jsonify({'error': f'获取商品详情失败: {str(e)}'}), 500

@products_bp.route('/search', methods=['GET'])
def search_products():
    """搜索商品"""
    try:
        keyword = request.args.get('keyword', '')
        category = request.args.get('category', type=int)
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)

        if not keyword:
            return jsonify({'error': '缺少搜索关键词'}), 400

        query = Product.query.filter(Product.name.contains(keyword))

        if category:
            query = query.filter_by(category_id=category)

        products = query.paginate(
            page=page, 
            per_page=limit, 
            error_out=False
        )

        return jsonify({
            'success': True,
            'data': {
                'products': [product.to_dict() for product in products.items],
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': products.total,
                    'pages': products.pages
                }
            }
        })
    except Exception as e:
        return jsonify({'error': f'搜索商品失败: {str(e)}'}), 500

# 监测相关路由
@monitors_bp.route('/', methods=['GET'])
def get_monitors():
    """获取用户的监测列表"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'error': '缺少用户ID'}), 400

        monitors = Monitor.query.filter_by(user_id=user_id).all()
        
        # 获取商品信息
        monitor_list = []
        for monitor in monitors:
            monitor_data = monitor.to_dict()
            product = Product.query.get(monitor.product_id)
            if product:
                monitor_data['product_name'] = product.name
                monitor_data['product_image'] = product.image
            monitor_list.append(monitor_data)

        return jsonify({
            'success': True,
            'data': monitor_list
        })
    except Exception as e:
        return jsonify({'error': f'获取监测列表失败: {str(e)}'}), 500

@monitors_bp.route('/', methods=['POST'])
def create_monitor():
    """创建监测"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        target_price = data.get('target_price')

        if not all([user_id, product_id, target_price]):
            return jsonify({'error': '缺少必要参数'}), 400

        # 获取商品当前价格
        product = Product.query.get_or_404(product_id)
        current_price = float(product.price)

        monitor = Monitor(
            user_id=user_id,
            product_id=product_id,
            target_price=target_price,
            current_price=current_price
        )

        db.session.add(monitor)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': '监测创建成功',
            'data': monitor.to_dict()
        })
    except Exception as e:
        return jsonify({'error': f'创建监测失败: {str(e)}'}), 500

@monitors_bp.route('/<int:id>', methods=['PUT'])
def update_monitor(id):
    """更新监测"""
    try:
        monitor = Monitor.query.get_or_404(id)
        data = request.get_json()

        if 'target_price' in data:
            monitor.target_price = data['target_price']
        if 'notification_enabled' in data:
            monitor.notification_enabled = data['notification_enabled']

        db.session.commit()

        return jsonify({
            'success': True,
            'message': '监测更新成功'
        })
    except Exception as e:
        return jsonify({'error': f'更新监测失败: {str(e)}'}), 500

@monitors_bp.route('/<int:id>', methods=['DELETE'])
def delete_monitor(id):
    """删除监测"""
    try:
        monitor = Monitor.query.get_or_404(id)
        db.session.delete(monitor)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': '监测删除成功'
        })
    except Exception as e:
        return jsonify({'error': f'删除监测失败: {str(e)}'}), 500

# 用户相关路由
@users_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    """获取用户信息"""
    try:
        user = User.query.get_or_404(id)
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
    except Exception as e:
        return jsonify({'error': f'获取用户信息失败: {str(e)}'}), 500

@users_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    """更新用户信息"""
    try:
        user = User.query.get_or_404(id)
        data = request.get_json()

        if 'nickname' in data:
            user.nickname = data['nickname']
        if 'phone' in data:
            user.phone = data['phone']
        if 'email' in data:
            user.email = data['email']

        db.session.commit()

        return jsonify({
            'success': True,
            'message': '用户信息更新成功'
        })
    except Exception as e:
        return jsonify({'error': f'更新用户信息失败: {str(e)}'}), 500

# 分类相关路由
@categories_bp.route('/', methods=['GET'])
def get_categories():
    """获取分类列表"""
    try:
        categories = Category.query.filter_by(status='active').order_by(Category.sort_order).all()
        return jsonify({
            'success': True,
            'data': [category.to_dict() for category in categories]
        })
    except Exception as e:
        return jsonify({'error': f'获取分类列表失败: {str(e)}'}), 500

@categories_bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    """获取分类详情"""
    try:
        category = Category.query.get_or_404(id)
        return jsonify({
            'success': True,
            'data': category.to_dict()
        })
    except Exception as e:
        return jsonify({'error': f'获取分类详情失败: {str(e)}'}), 500 