from flask import Blueprint, request, jsonify
from extensions import create_access_token, jwt_required, get_jwt_identity

# 导入模型和扩展
from models import User, Course, Document, Question, Exam, ExamResult, db
from extensions import jwt

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
            'correct_answer': question.correct_answer,
            'exam_id': question.exam_id
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