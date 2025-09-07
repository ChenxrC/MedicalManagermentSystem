from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 创建扩展实例
app = Flask(__name__)
CORS(app)  # 允许跨域请求

from extensions import db, jwt

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///edu_management.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT配置
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
print(f"JWT_SECRET_KEY loaded: {app.config['JWT_SECRET_KEY']}")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 900  # 15分钟

# 初始化扩展
db.init_app(app)
jwt.init_app(app)

# 创建数据库表
with app.app_context():
    from models import User, Course, Document, Question, Exam, ExamResult
    db.create_all()

# JWT错误处理
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'Token has expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'message': 'Invalid token', 'error_details': str(error)}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'message': 'Missing token'}), 401

# 注册蓝图
from routes import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

# 注册用户管理蓝图
from user_management import user_management_bp
app.register_blueprint(user_management_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=5001)