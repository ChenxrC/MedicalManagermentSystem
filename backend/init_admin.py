from models import User, db
from app import app

def init_admin():
    with app.app_context():
        # 检查并创建默认管理员用户 default_admin
        default_admin = User.query.filter_by(username='default_admin').first()
        if not default_admin:
            default_admin = User(username='default_admin', email='default_admin@example.com', role='admin')
            default_admin.set_password('admin123')
            db.session.add(default_admin)
            db.session.commit()
            print('默认管理员用户 default_admin 创建成功')
        else:
            print('默认管理员用户 default_admin 已存在')
            
        # 检查并创建管理员用户 admin
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@example.com', role='admin')
            admin.set_password('123')
            db.session.add(admin)
            db.session.commit()
            print('管理员用户 admin 创建成功')
        else:
            print('管理员用户 admin 已存在')

if __name__ == '__main__':
    init_admin()