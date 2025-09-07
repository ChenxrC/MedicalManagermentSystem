@echo off
echo 启动Django后端服务器...
cd backend
python manage.py migrate
python manage.py runserver
pause
