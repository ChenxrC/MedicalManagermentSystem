from flask import Blueprint, request, jsonify
current_user = None

# 导入模型和扩展
from models import User, Course, Document, Question, Exam, ExamResult
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

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
    role = data.get('role', 'student')  # 默认角色为学生
    
    # 检查用户名和邮箱是否已存在
    # 使用应用上下文进行数据库查询
    from app import create_app
    app = create_app()
    with app.app_context():
        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'Email already exists'}), 400
        
        # 创建新用户
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        
        # 保存到数据库
        db.session.add(user)
        db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@api_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # 使用应用上下文进行数据库查询
    from app import create_app
    app = create_app()
    with app.app_context():
        # 查找用户
        user = User.query.filter_by(username=username).first()
        
        # 验证用户和密码
        if not user or not user.check_password(password):
            return jsonify({'message': 'Invalid username or password'}), 401
        
        # 创建访问令牌
        access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'User logged in successfully',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 200

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
            'answer': question.answer,
            'type': question.type,
            'created_at': question.created_at
        })
    return jsonify({'questions': questions_data}), 200

@api_bp.route('/questions', methods=['POST'])
@jwt_required()
def create_question():
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 检查用户是否为教师或管理员
    user = User.query.get(current_user_id)
    if user.role not in ['teacher', 'admin']:
        return jsonify({'message': '只有教师和管理员可以创建题目'}), 403
    
    # 获取请求数据
    data = request.get_json()
    content = data.get('content')
    options = data.get('options')
    answer = data.get('answer')
    q_type = data.get('type')
    
    # 创建新题目
    question = Question(content=content, options=options, answer=answer, type=q_type)
    
    # 保存到数据库
    db.session.add(question)
    db.session.commit()
    
    return jsonify({
        'message': 'Question created successfully',
        'question': {
            'id': question.id,
            'content': question.content,
            'options': question.options,
            'answer': question.answer,
            'type': question.type,
            'created_at': question.created_at
        }
    }), 201

@api_bp.route('/exams', methods=['GET'])
def get_exams():
    # 获取试卷列表
    exams = Exam.query.all()
    exams_data = []
    for exam in exams:
        exams_data.append({
            'id': exam.id,
            'title': exam.title,
            'course_id': exam.course_id,
            'questions': exam.questions,
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
        return jsonify({'message': '只有教师和管理员可以创建试卷'}), 403
    
    # 获取请求数据
    data = request.get_json()
    title = data.get('title')
    course_id = data.get('course_id')
    questions = data.get('questions', [])
    
    # 检查课程是否存在
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': '课程不存在'}), 404
    
    # 创建新试卷
    exam = Exam(title=title, course_id=course_id, questions=questions)
    
    # 保存到数据库
    db.session.add(exam)
    db.session.commit()
    
    return jsonify({
        'message': 'Exam created successfully',
        'exam': {
            'id': exam.id,
            'title': exam.title,
            'course_id': exam.course_id,
            'questions': exam.questions,
            'created_at': exam.created_at
        }
    }), 201

@api_bp.route('/exams/<int:exam_id>/submit', methods=['POST'])
@jwt_required()
def submit_exam(exam_id):
    # 获取当前用户ID
    current_user_id = get_jwt_identity()
    
    # 检查用户是否为学生
    user = User.query.get(current_user_id)
    if user.role != 'student':
        return jsonify({'message': '只有学生可以提交考试'}), 403
    
    # 获取考试
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({'message': '考试不存在'}), 404
    
    # 获取请求数据
    data = request.get_json()
    answers = data.get('answers', [])
    
    # 计算分数（简化实现）
    score = 0
    total_questions = len(exam.questions)
    
    # 创建考试结果
    exam_result = ExamResult(
        exam_id=exam_id,
        student_id=current_user_id,
        score=score,
        answers=answers
    )
    
    # 保存到数据库
    db.session.add(exam_result)
    db.session.commit()
    
    return jsonify({
        'message': 'Exam submitted successfully',
        'result': {
            'id': exam_result.id,
            'exam_id': exam_result.exam_id,
            'student_id': exam_result.student_id,
            'score': exam_result.score,
            'answers': exam_result.answers,
            'submitted_at': exam_result.submitted_at
        }
    }), 201