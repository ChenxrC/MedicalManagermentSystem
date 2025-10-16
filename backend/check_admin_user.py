from app import app
from models import User, db

with app.app_context():
    # 查询所有用户
    all_users = User.query.all()
    print(f"Total users: {len(all_users)}")
    
    # 打印每个用户的信息
    for user in all_users:
        print(f"\nUser ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")
        print(f"Password hash: {user.password_hash}")
    
    # 特别检查admin用户
    admin_user = User.query.filter_by(username='admin').first()
    if admin_user:
        print(f"\nAdmin user exists with username: {admin_user.username}")
    else:
        print("\nAdmin user does not exist!")
        
    # 检查是否有default_admin用户
    default_admin = User.query.filter_by(username='default_admin').first()
    if default_admin:
        print(f"default_admin user exists with role: {default_admin.role}")
    else:
        print("default_admin user does not exist!")