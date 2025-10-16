from models import Course, Question, Exam, ExamResult, User, db
from app import app
import json
from datetime import datetime, timedelta


def init_test_data():
    with app.app_context():
        # 1. 创建测试课程
        print("正在创建测试课程...")
        
        # 查找teacher1用户作为课程教师
        teacher = User.query.filter_by(username='teacher1').first()
        if not teacher:
            # 如果没有teacher1用户，创建一个
            teacher = User(username='teacher1', email='teacher1@example.com', role='teacher')
            teacher.set_password('123')
            db.session.add(teacher)
            db.session.commit()
            print('教师用户 teacher1 创建成功')
        
        # 创建5门课程
        courses = []
        course_titles = [
            "医学基础理论",
            "内科学",
            "外科学",
            "儿科学",
            "妇产科学"
        ]
        
        for title in course_titles:
            if not Course.query.filter_by(title=title).first():
                course = Course(
                    title=title,
                    description=f"{title}是医学教育中的重要课程",
                    teacher_id=teacher.id
                )
                db.session.add(course)
                courses.append(course)
        
        db.session.commit()
        print(f"成功创建{len(courses)}门课程")
        
        # 2. 创建测试题目
        print("正在创建测试题目...")
        
        # 创建一些单选题
        questions = []
        question_data = [
            {
                "content": "以下哪种药物是抗生素？",
                "options": {"A": "阿司匹林", "B": "青霉素", "C": "布洛芬", "D": "对乙酰氨基酚"},
                "answer": "B",
                "type": "single_choice"
            },
            {
                "content": "正常人体体温范围是？",
                "options": {"A": "35-36°C", "B": "36-37.2°C", "C": "37-38°C", "D": "38-39°C"},
                "answer": "B",
                "type": "single_choice"
            },
            {
                "content": "心脏位于人体的哪个部位？",
                "options": {"A": "胸腔左侧", "B": "胸腔右侧", "C": "腹腔", "D": "头部"},
                "answer": "A",
                "type": "single_choice"
            },
            {
                "content": "以下哪些属于人体必需营养素？",
                "options": {"A": "蛋白质", "B": "碳水化合物", "C": "脂肪", "D": "以上都是"},
                "answer": "D",
                "type": "single_choice"
            },
            {
                "content": "高血压的诊断标准是收缩压≥140mmHg和（或）舒张压≥90mmHg。",
                "options": {"A": "正确", "B": "错误"},
                "answer": "A",
                "type": "true_false"
            }
        ]
        
        for data in question_data:
            question = Question(
                content=data["content"],
                options=json.dumps(data["options"]),
                answer=data["answer"],
                type=data["type"]
            )
            db.session.add(question)
            questions.append(question)
        
        db.session.commit()
        print(f"成功创建{len(questions)}道题目")
        
        # 3. 创建测试考试
        print("正在创建测试考试...")
        
        # 获取所有课程
        all_courses = Course.query.all()
        if not all_courses:
            print("没有可用的课程，无法创建考试")
            return
        
        # 为每门课程创建一个考试
        exams = []
        for i, course in enumerate(all_courses):
            exam_title = f"{course.title}期末考试"
            if not Exam.query.filter_by(title=exam_title).first():
                # 为每个考试选择2-3道题目
                exam_questions = questions[i*2:(i+1)*2] if (i+1)*2 <= len(questions) else questions[-2:]
                question_ids = [q.id for q in exam_questions]
                
                exam = Exam(
                    title=exam_title,
                    course_id=course.id,
                    questions=json.dumps(question_ids)
                )
                db.session.add(exam)
                exams.append(exam)
        
        db.session.commit()
        print(f"成功创建{len(exams)}个考试")
        
        # 4. 创建测试学生用户
        print("正在创建测试学生用户...")
        
        students = []
        for i in range(5):
            username = f"student{i+1}"
            if not User.query.filter_by(username=username).first():
                student = User(
                    username=username,
                    email=f"{username}@example.com",
                    role="student"
                )
                student.set_password("123")
                db.session.add(student)
                students.append(student)
        
        db.session.commit()
        print(f"成功创建{len(students)}个学生用户")
        
        # 5. 创建考试分配
        print("正在创建考试分配...")
        
        # 获取所有学生和考试
        all_students = User.query.filter_by(role="student").all()
        all_exams = Exam.query.all()
        
        if not all_students or not all_exams:
            print("没有可用的学生或考试，无法创建考试分配")
            return
        
        # 为每个学生分配2个考试
        assignments = []
        for student in all_students:
            # 为每个学生选择2个不同的考试
            student_exams = all_exams[:2] if len(all_exams) >= 2 else all_exams
            
            for exam in student_exams:
                # 检查是否已存在该分配
                existing = ExamResult.query.filter_by(exam_id=exam.id, student_id=student.id).first()
                if not existing:
                    assignment = ExamResult(
                        exam_id=exam.id,
                        student_id=student.id,
                        score=0.0,  # 临时使用0作为未完成考试的默认分数
                        answers=None
                    )
                    db.session.add(assignment)
                    assignments.append(assignment)
        
        db.session.commit()
        print(f"成功创建{len(assignments)}个考试分配")
        
        # 6. 添加一些已完成的考试结果
        print("正在添加一些已完成的考试结果...")
        
        # 为前两个学生的第一个考试添加成绩
        completed_assignments = ExamResult.query.limit(2).all()
        for i, assignment in enumerate(completed_assignments):
            assignment.score = 80.0 + i * 10
            assignment.answers = json.dumps({"1": "B", "2": "A"})
            assignment.submitted_at = datetime.now() - timedelta(days=i)
        
        db.session.commit()
        print(f"成功更新{len(completed_assignments)}个考试结果为已完成状态")
        
        print("\n测试数据初始化完成！")
        print(f"\n系统现在包含：")
        print(f"- {Course.query.count()}门课程")
        print(f"- {Question.query.count()}道题目")
        print(f"- {Exam.query.count()}个考试")
        print(f"- {User.query.filter_by(role='student').count()}个学生用户")
        print(f"- {ExamResult.query.count()}个考试分配（其中{ExamResult.query.filter(ExamResult.submitted_at.isnot(None)).count()}个已完成）")
        print(f"\n管理员用户：admin / 123")
        print(f"教师用户：teacher1 / 123")
        print(f"学生用户：student1-student5 / 123")


if __name__ == '__main__':
    init_test_data()