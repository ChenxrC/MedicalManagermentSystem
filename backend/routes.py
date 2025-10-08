from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# 导入模型和扩展
from models import User, Course, Document, Question, Exam, ExamResult, db
from extensions import jwt

# 导入datetime模块用于日期处理
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'Education Management System API is running'})

@api_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = 'student'  # 禁止注册管理员账户，强制设为学生
    
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
    
    return jsonify({'message': '用户注册成功'}), 201

@api_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # 查找用户
    user = User.query.filter_by(username=username).first()
    
    # 验证用户和密码
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    # 创建访问令牌
    access_token = create_access_token(identity=str(user.id))
    
    # 根据用户角色定义权限
    permissions = get_user_permissions(user.role)
    
    return jsonify({
        'message': 'User logged in successfully',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'permissions': permissions
        }
    }), 200

@api_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 查找当前用户
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # 获取用户权限
    permissions = get_user_permissions(user.role)
    
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'permissions': permissions
        }
    }), 200

@api_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 查找当前用户
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'message': 'User not found'}), 404
    
    # 只有管理员可以查看所有用户
    if current_user.role != 'admin':
        return jsonify({'message': '只有管理员可以查看用户列表'}), 403
    
    # 获取用户列表
    users = User.query.all()
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'permissions': get_user_permissions(user.role)
        })
    
    return jsonify({'users': users_data}), 200

@api_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 查找当前用户
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'message': 'User not found'}), 404
    
    # 只有管理员可以创建用户
    if current_user.role != 'admin':
        return jsonify({'message': '只有管理员可以创建用户'}), 403
    
    # 获取请求数据
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'student')  # 默认为学生角色
    
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

@api_bp.route('/users/<int:user_id>', methods=['PATCH'])
@jwt_required()
def update_user(user_id):
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 查找当前用户
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'message': 'User not found'}), 404
    
    # 只有管理员可以更新用户
    if current_user.role != 'admin':
        return jsonify({'message': '只有管理员可以更新用户'}), 403
    
    # 查找要更新的用户
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': '要更新的用户不存在'}), 404
    
    # 获取请求数据
    data = request.get_json()
    
    # 更新用户信息
    if 'username' in data:
        # 检查新用户名是否已存在
        if User.query.filter(User.id != user_id, User.username == data['username']).first():
            return jsonify({'message': '用户名已存在'}), 400
        user.username = data['username']
    
    if 'email' in data:
        # 检查新邮箱是否已存在
        if User.query.filter(User.id != user_id, User.email == data['email']).first():
            return jsonify({'message': '邮箱已存在'}), 400
        user.email = data['email']
    
    if 'role' in data:
        user.role = data['role']
    
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    
    # 保存到数据库
    db.session.commit()
    
    return jsonify({
        'message': '用户更新成功',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 200

@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 查找当前用户
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'message': 'User not found'}), 404
    
    # 只有管理员可以删除用户
    if current_user.role != 'admin':
        return jsonify({'message': '只有管理员可以删除用户'}), 403
    
    # 禁止删除自己
    if current_user_id == user_id:
        return jsonify({'message': '不能删除当前登录用户'}), 400
    
    # 查找要删除的用户
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': '要删除的用户不存在'}), 404
    
    # 从数据库中删除用户
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': '用户删除成功'}), 200

def get_user_permissions(role):
    """根据用户角色返回对应的权限列表"""
    # 定义不同角色的权限
    permissions_map = {
        'admin': [
            'view_users', 'create_users', 'update_users', 'delete_users',
            'view_courses', 'create_courses', 'update_courses', 'delete_courses',
            'view_documents', 'create_documents', 'update_documents', 'delete_documents',
            'view_exams', 'create_exams', 'update_exams', 'delete_exams',
            'view_results', 'manage_system'
        ],
        'teacher': [
            'view_courses', 'create_courses', 'update_courses', 'delete_courses',
            'view_documents', 'create_documents', 'update_documents', 'delete_documents',
            'view_exams', 'create_exams', 'update_exams', 'delete_exams',
            'view_results'
        ],
        'student': [
            'view_courses',
            'view_documents',
            'take_exams',
            'view_own_results'
        ]
    }
    
    # 返回对应角色的权限，如果角色不存在则返回空列表
    return permissions_map.get(role, [])

@api_bp.route('/courses', methods=['GET'])
def get_courses():
    # 获取课程列表
    courses = Course.query.all()
    courses_data = []
    for course in courses:
        courses_data.append({
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'teacher_id': course.teacher_id,
            'created_at': course.created_at
        })
    return jsonify({'courses': courses_data}), 200

@api_bp.route('/courses', methods=['POST'])
@jwt_required()
def create_course():
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 检查用户是否为教师或管理员
    user = User.query.get(current_user_id)
    if user.role not in ['teacher', 'admin']:
        return jsonify({'message': '只有教师和管理员可以创建课程'}), 403
    
    # 获取请求数据
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    
    # 创建新课程
    course = Course(title=title, description=description, teacher_id=current_user_id)
    
    # 保存到数据库
    db.session.add(course)
    db.session.commit()
    
    return jsonify({
        'message': 'Course created successfully',
        'course': {
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'teacher_id': course.teacher_id,
            'created_at': course.created_at
        }
    }), 201

@api_bp.route('/exam-results', methods=['GET'])
@jwt_required()
def get_exam_results():
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 获取用户考试结果
    exam_results = ExamResult.query.filter_by(student_id=current_user_id).all()
    results_data = []
    for result in exam_results:
        results_data.append({
            'id': result.id,
            'exam_id': result.exam_id,
            'student_id': result.student_id,
            'score': result.score,
            'answers': result.answers,
            'submitted_at': result.submitted_at
        })
    
    return jsonify({'exam_results': results_data}), 200

@api_bp.route('/documents', methods=['GET'])
def get_documents():
    # 获取文档列表
    documents = Document.query.all()
    documents_data = []
    for document in documents:
        documents_data.append({
            'id': document.id,
            'title': document.title,
            'content': document.content,
            'course_id': document.course_id,
            'created_at': document.created_at
        })
    return jsonify({'documents': documents_data}), 200

@api_bp.route('/documents/published', methods=['GET'])
def get_published_documents():
    # 获取已发布的文档列表（目前所有文档都视为已发布）
    documents = Document.query.all()
    documents_data = []
    for document in documents:
        documents_data.append({
            'id': document.id,
            'title': document.title,
            'course_id': document.course_id,
            'created_at': document.created_at
        })
    return jsonify({'documents': documents_data}), 200

@api_bp.route('/documents', methods=['POST'])
@jwt_required()
def upload_document():
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 检查用户是否为教师或管理员
    user = User.query.get(current_user_id)
    if user.role not in ['teacher', 'admin']:
        return jsonify({'message': '只有教师和管理员可以上传文档'}), 403
    
    # 获取请求数据
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    course_id = data.get('course_id')
    
    # 检查课程是否存在
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': '课程不存在'}), 404
    
    # 创建新文档
    document = Document(title=title, content=content, course_id=course_id)
    
    # 保存到数据库
    db.session.add(document)
    db.session.commit()
    
    return jsonify({
        'message': 'Document uploaded successfully',
        'document': {
            'id': document.id,
            'title': document.title,
            'content': document.content,
            'course_id': document.course_id,
            'created_at': document.created_at
        }
    }), 201

@api_bp.route('/questions', methods=['GET'])
def get_questions():
    # 获取题目列表
    questions = Question.query.all()
    questions_data = []
    for question in questions:
        questions_data.append({
            'id': question.id,
            'content': question.content,
            'options': question.options,
            'correct_answer': question.answer,  # 修正字段名，模型中是answer
            'type': question.type  # 添加type字段
        })
    return jsonify({'questions': questions_data}), 200

@api_bp.route('/exams', methods=['GET'])
def get_exams():
    # 获取考试列表
    exams = Exam.query.all()
    exams_data = []
    for exam in exams:
        exams_data.append({
            'id': exam.id,
            'title': exam.title,
            'course_id': exam.course_id,
            'created_at': exam.created_at
        })
    return jsonify({'exams': exams_data}), 200

@api_bp.route('/exams', methods=['POST'])
@jwt_required()
def create_exam():
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 检查用户是否为教师或管理员
    user = User.query.get(current_user_id)
    if user.role not in ['teacher', 'admin']:
        return jsonify({'message': '只有教师和管理员可以创建考试'}), 403
    
    # 获取请求数据
    data = request.get_json()
    title = data.get('title')
    course_id = data.get('course_id')
    
    # 检查课程是否存在
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': '课程不存在'}), 404
    
    # 创建新考试
    exam = Exam(title=title, course_id=course_id)
    
    # 保存到数据库
    db.session.add(exam)
    db.session.commit()
    
    return jsonify({
        'message': 'Exam created successfully',
        'exam': {
            'id': exam.id,
            'title': exam.title,
            'course_id': exam.course_id,
            'created_at': exam.created_at
        }
    }), 201

@api_bp.route('/exam-results', methods=['POST'])
@jwt_required()
def submit_exam():
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 获取请求数据
    data = request.get_json()
    exam_id = data.get('exam_id')
    answers = data.get('answers')
    
    # 检查考试是否存在
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'message': '考试不存在'}), 404
    
    # 计算分数
    score = 0
    for answer in answers:
        question = Question.query.get(answer['question_id'])
        if question and question.correct_answer == answer['answer']:
            score += 1
    
    # 创建考试结果
    exam_result = ExamResult(exam_id=exam_id, student_id=current_user_id, score=score, answers=answers)
    
    # 保存到数据库
    db.session.add(exam_result)
    db.session.commit()
    
    return jsonify({
        'message': 'Exam submitted successfully',
        'exam_result': {
            'id': exam_result.id,
            'exam_id': exam_result.exam_id,
            'student_id': exam_result.student_id,
            'score': exam_result.score,
            'answers': exam_result.answers,
            'submitted_at': exam_result.submitted_at
        }
    }), 201

# 考试分配相关API
@api_bp.route('/exam-assignments', methods=['GET'])
@jwt_required()
def get_exam_assignments():
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 查找当前用户
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'message': 'User not found'}), 404
    
    # 根据用户角色获取不同的考试分配列表
    if current_user.role == 'admin':
        # 管理员可以查看所有考试分配
        assignments = db.session.query(
            ExamResult.id,
            Exam.title.label('exam_title'),
            User.username.label('student_username'),
            ExamResult.submitted_at.label('submitted_at')
        ).join(
            Exam, ExamResult.exam_id == Exam.id
        ).join(
            User, ExamResult.student_id == User.id
        ).all()
    elif current_user.role == 'teacher':
        # 教师可以查看自己创建的课程的考试分配
        assignments = db.session.query(
            ExamResult.id,
            Exam.title.label('exam_title'),
            User.username.label('student_username'),
            ExamResult.submitted_at.label('submitted_at')
        ).join(
            Exam, ExamResult.exam_id == Exam.id
        ).join(
            User, ExamResult.student_id == User.id
        ).join(
            Course, Exam.course_id == Course.id
        ).filter(
            Course.teacher_id == current_user_id
        ).all()
    else:
        # 学生只能查看自己的考试分配
        assignments = db.session.query(
            ExamResult.id,
            Exam.title.label('exam_title'),
            ExamResult.submitted_at.label('submitted_at')
        ).join(
            Exam, ExamResult.exam_id == Exam.id
        ).filter(
            ExamResult.student_id == current_user_id
        ).all()
    
    # 格式化考试分配数据
    assignments_data = []
    for assignment in assignments:
        data = {
            'id': assignment.id,
            'exam': {'title': assignment.exam_title},
            'status': 'completed' if assignment.submitted_at else 'assigned'
        }
        
        # 如果有提交时间，添加提交时间字段
        if hasattr(assignment, 'submitted_at') and assignment.submitted_at:
            data['submitted_at'] = assignment.submitted_at.isoformat()
        
        # 如果是管理员或教师，添加学生信息
        if current_user.role in ['admin', 'teacher']:
            data['student'] = {
                'username': assignment.student_username
            }
        
        assignments_data.append(data)
    
    return jsonify({'results': assignments_data, 'count': len(assignments_data)}), 200

@api_bp.route('/exam-assignments', methods=['POST'])
@jwt_required()
def create_exam_assignment():
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 查找当前用户
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'message': 'User not found'}), 404
    
    # 只有管理员和教师可以创建考试分配
    if current_user.role not in ['admin', 'teacher']:
        return jsonify({'message': '只有管理员和教师可以分配考试'}), 403
    
    # 获取请求数据
    data = request.get_json()
    exam_id = data.get('exam_id')
    student_id = data.get('student_id')
    
    # 检查考试是否存在
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'message': '考试不存在'}), 404
    
    # 检查学生是否存在
    student = User.query.get(student_id)
    if not student or student.role != 'student':
        return jsonify({'message': '学员不存在'}), 404
    
    # 检查是否已分配过该考试
    existing_assignment = ExamResult.query.filter_by(
        exam_id=exam_id,
        student_id=student_id
    ).first()
    if existing_assignment:
        return jsonify({'message': '该学员已经分配过此考试'}), 400
    
    # 创建考试分配（实际上是创建一个空的考试结果记录）
    exam_result = ExamResult(
        exam_id=exam_id,
        student_id=student_id,
        score=0,  # 初始分数为0
        answers=[]  # 初始答案为空列表
    )
    
    # 保存到数据库
    db.session.add(exam_result)
    db.session.commit()
    
    return jsonify({
        'message': '考试分配成功',
        'assignment': {
            'id': exam_result.id,
            'exam_id': exam_result.exam_id,
            'student_id': exam_result.student_id,
            'assigned_at': exam_result.created_at.isoformat()
        }
    }), 201

@api_bp.route('/exam-assignments/<int:assignment_id>', methods=['DELETE'])
@jwt_required()
def delete_exam_assignment(assignment_id):
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 查找当前用户
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'message': 'User not found'}), 404
    
    # 只有管理员和教师可以删除考试分配
    if current_user.role not in ['admin', 'teacher']:
        return jsonify({'message': '只有管理员和教师可以删除考试分配'}), 403
    
    # 查找考试分配
    assignment = ExamResult.query.get(assignment_id)
    if not assignment:
        return jsonify({'message': '考试分配不存在'}), 404
    
    # 如果是教师，检查是否有权限删除
    if current_user.role == 'teacher':
        # 检查考试所属的课程是否由该教师创建
        exam = Exam.query.get(assignment.exam_id)
        if not exam:
            return jsonify({'message': '考试不存在'}), 404
        
        course = Course.query.get(exam.course_id)
        if not course or course.teacher_id != current_user_id:
            return jsonify({'message': '您没有权限删除此考试分配'}), 403
    
    # 从数据库中删除考试分配
    db.session.delete(assignment)
    db.session.commit()
    
    return jsonify({'message': '考试分配删除成功'}), 200