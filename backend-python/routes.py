from flask import Blueprint, request, jsonify
from models import db, User
from datetime import datetime

# 创建蓝图
auth_bp = Blueprint('auth', __name__)

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