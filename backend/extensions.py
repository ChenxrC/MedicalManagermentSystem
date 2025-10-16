from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# 创建扩展实例
db = SQLAlchemy()
jwt = JWTManager()