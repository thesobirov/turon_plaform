from app import *
from backend.models.basic_model import *
from backend.basics.settings import *


@app.route(f'{api}/get_groups')
@cross_origin()
@jwt_required()
def get_groups():
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity).first()
    student = Student.query.filter(Student.user_id == user.id).first()
    teacher = Teacher.query.filter(Teacher.user_id == user.id).first()
    if student:
        groups = db.session.query(Group).join(Group.student).options(contains_eager(Group.student)).filter(
            Student.id == student.id).all()
    else:
        groups = db.session.query(Group).join(Group.teacher).options(contains_eager(Group.teacher)).filter(
            Teacher.id == teacher.id).all()

    return iterate_models(groups)


@app.route(f'{api}/group_profile/<int:group_id>')
@jwt_required()
def group_profile(group_id):
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity).first()

    student = Student.query.filter(Student.user_id == user.id).first()
    teacher = Teacher.query.filter(Teacher.user_id == user.id).first()
    subject_level = []
    if student:
        subject_level = db.session.query(StudentLevel).join(StudentLevel.subject_level).options(
            contains_eager(StudentLevel.subject_level)).filter(StudentLevel.student_id == student.id,
                                                               StudentLevel.group_id == group_id).order_by(
            SubjectLevel.id).all()
        subject_level = iterate_models(subject_level)
    group = Group.query.filter(Group.id == group_id).first()
    levels = SubjectLevel.query.filter(SubjectLevel.subject_id == group.subject_id).filter(
        or_(SubjectLevel.disabled == False, SubjectLevel.disabled == None)).order_by(SubjectLevel.id).all()

    return jsonify({
        "data": group.convert_json(),
        "subject_levels": iterate_models(levels),
        "curriculum": subject_level
    })


@app.route(f'{api}/check_level/<group_id>/<level_id>', methods=['POST', 'GET'])
def check_level(group_id, level_id):
    subject_level = SubjectLevel.query.filter(SubjectLevel.id == level_id).first()
    if request.method == "POST":
        student_list = request.get_json()['users']
        for st in student_list:
            student = Student.query.filter(Student.user_id == st['id']).first()
            exist = StudentLevel.query.filter(StudentLevel.level_id == subject_level.id,
                                              StudentLevel.student_id == student.id,
                                              StudentLevel.group_id == group_id,
                                              StudentLevel.subject_id == subject_level.subject_id).first()
            if st['level']:
                if not exist:
                    exist = StudentLevel(student_id=student.id, level_id=subject_level.id, group_id=group_id,
                                         subject_id=subject_level.subject_id)
                    exist.add_commit()
            else:
                if exist:
                    db.session.delete(exist)
                    db.session.commit()
        return jsonify({
            "msg": f"O'zgartirildi",
            "status": 'success'
        })
    students = db.session.query(Student).join(Student.groups).options(contains_eager(Student.groups)).filter(
        Group.id == group_id).order_by(Student.id).all()

    student_list = []
    for student in students:
        exist_level = False
        exist = StudentLevel.query.filter(StudentLevel.level_id == subject_level.id,
                                          StudentLevel.student_id == student.id,
                                          StudentLevel.group_id == group_id).first()
        if exist:
            exist_level = True
        info = student.convert_json()
        info['level'] = exist_level
        student_list.append(info)
    return jsonify({
        "students": student_list
    })
