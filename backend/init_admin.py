from app import create_app
from models import User, db

def init_admin():
    app = create_app()
    with app.app_context():
        # 检查是否已存在管理员用户
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print('管理员用户已存在')
            return
        
        # 创建管理员用户
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('123')
        
        # 保存到数据库
        db.session.add(admin)
        db.session.commit()
        
        print('管理员用户创建成功')

if __name__ == '__main__':
    init_admin()