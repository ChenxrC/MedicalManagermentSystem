from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 初始化扩展
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    CORS(app)  # 允许跨域请求
    
    # 数据库配置
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///edu_management.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # JWT配置
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
    
    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    
    # JWT错误处理
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'message': 'Token has expired'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'message': 'Invalid token'}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'message': 'Missing token'}), 401
    
    # 注册蓝图
    from routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)