from flask import Blueprint, request, jsonify
from extensions import jwt_required, get_jwt_identity
from models import User, db
from routes import get_user_permissions

user_management_bp = Blueprint('user_management', __name__)

@user_management_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 检查用户是否为管理员或具有查看用户权限
    current_user = User.query.get(current_user_id)
    permissions = get_user_permissions(current_user.role)
    if 'view_users' not in permissions:
        return jsonify({'message': '您没有查看用户列表的权限'}), 403
    
    # 获取用户列表，包含权限信息
    users = User.query.all()
    users_data = []
    for user in users:
        user_permissions = get_user_permissions(user.role)
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'permissions': user_permissions
        })
    
    return jsonify({'users': users_data}), 200

@user_management_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 检查用户是否为管理员或具有创建用户权限
    current_user = User.query.get(current_user_id)
    permissions = get_user_permissions(current_user.role)
    if 'create_users' not in permissions:
        return jsonify({'message': '您没有创建用户的权限'}), 403
    
    # 获取请求数据
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    
    # 检查用户名和邮箱是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'message': '用户名已存在'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'message': '邮箱已存在'}), 400
    
    # 创建新用户
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    
    # 保存到数据库
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': '用户创建成功',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 201

@user_management_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 检查用户是否为管理员或具有更新用户权限
    current_user = User.query.get(current_user_id)
    permissions = get_user_permissions(current_user.role)
    if 'update_users' not in permissions:
        return jsonify({'message': '您没有更新用户信息的权限'}), 403
    
    # 查找要更新的用户
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    
    # 获取请求数据
    data = request.get_json()
    
    # 更新用户信息
    if 'username' in data:
        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'message': '用户名已存在'}), 400
        user.username = data['username']
    
    if 'email' in data:
        # 检查邮箱是否已存在
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'message': '邮箱已存在'}), 400
        user.email = data['email']
    
    if 'role' in data:
        # 只有管理员可以更改角色（分配权限）
        if current_user.role != 'admin':
            return jsonify({'message': '只有管理员可以更改用户角色'}), 403
        user.role = data['role']
    
    # 保存到数据库
    db.session.commit()
    
    # 获取更新后的用户权限
    user_permissions = get_user_permissions(user.role)
    
    return jsonify({
        'message': '用户信息更新成功',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'permissions': user_permissions
        }
    }), 200

@user_management_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 检查用户是否为管理员或具有删除用户权限
    current_user = User.query.get(current_user_id)
    permissions = get_user_permissions(current_user.role)
    if 'delete_users' not in permissions:
        return jsonify({'message': '您没有删除用户的权限'}), 403
    
    # 查找要删除的用户
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    
    # 删除用户
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': '用户删除成功'}), 200

@user_management_bp.route('/users/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 查找当前用户
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    
    # 获取请求数据
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    # 验证旧密码
    if not user.check_password(old_password):
        return jsonify({'message': '旧密码错误'}), 400
    
    # 设置新密码
    user.set_password(new_password)
    
    # 保存到数据库
    db.session.commit()
    
    return jsonify({'message': '密码修改成功'}), 200