from app import *
from backend.models.basic_model import *
from backend.basics.settings import *
from backend.models.settings import *


@app.route(f"{api}/info/subjects", methods=["GET", "POST"])
@cross_origin()
@jwt_required()
def info_subjects():
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity).first()
    if request.method == "GET":
        if user.role.type == "methodist":
            subjects = Subject.query.filter(or_(Subject.disabled == False, Subject.disabled == None)).order_by(
                Subject.id).all()
        elif user.role.type == "student":
            student = Student.query.filter(Student.user_id == user.id).first()
            groups = db.session.query(Group).join(Group.student).options(contains_eager(Group.student)).filter(
                Student.id == student.id).all()
            subject_list = []
            for gr in groups:
                if gr.subject_id not in subject_list:
                    subject_list.append(gr.subject_id)
            subjects = Subject.query.filter(Subject.id.in_(sub for sub in subject_list)).order_by(Subject.id).all()
        else:
            teacher = Teacher.query.filter(Teacher.user_id == user.id).first()
            groups = db.session.query(Group).join(Group.teacher).options(contains_eager(Group.teacher)).filter(
                Teacher.id == teacher.id).all()
            subject_list = []
            for gr in groups:
                if gr.subject_id not in subject_list:
                    subject_list.append(gr.subject_id)
            subjects = Subject.query.filter(Subject.id.in_(sub for sub in subject_list)).order_by(Subject.id).all()
        return jsonify({
            "subjects": iterate_models(subjects),
        })
    if request.method == "POST":
        info = request.form.get("info")
        json_file = json.loads(info)
        name = json_file['title']
        photo = request.files.get('file')
        desc = json_file['desc']

        if photo and check_file(photo.filename):
            get_img = add_file(photo, app, Images)
            add = Subject(name=name, desc=desc, img_id=get_img)
            add.add_commit()

        subjects = Subject.query.filter(or_(Subject.disabled == False, Subject.disabled == None)).order_by(
            Subject.id).all()
        subjects_server = Subject.query.order_by(Subject.id).all()
        send_subject_server("subject", platform_server, subjects_server)
        return create_msg(f"{name}", status=True, data=iterate_models(subjects))


@app.route(f'{api}/subject/<int:subject_id>')
def subject(subject_id):
    try:
        subject_view = Subject.query.filter(Subject.id == subject_id).first()
        return jsonify({
            "data": subject_view.convert_json(),
            "status": True
        })
    except:
        return jsonify({
            "status": False
        })


@app.route(f'{api}/edit_subject/<int:subject_id>', methods=['POST'])
@jwt_required()
def edit_subject(subject_id):
    subject_get = Subject.query.filter(Subject.id == subject_id).first()
    identity = get_jwt_identity()
    if request.method == "POST":
        info = request.form.get("info")
        json_file = json.loads(info)
        photo = request.files.get('file')
        name = json_file['title']
        desc = json_file['desc']
        try:
            if photo and check_file(photo.filename):
                get_img = add_file(photo, app, Images)
                check_img_remove(subject_get.img_id, Images)
                Subject.query.filter(Subject.id == subject_id).update({
                    "name": name,
                    "desc": desc,
                    "img_id": get_img

                })
            else:
                Subject.query.filter(Subject.id == subject_id).update({
                    "name": name,
                    "desc": desc
                })
            db.session.commit()
            subjects = Subject.query.filter(or_(Subject.disabled == False, Subject.disabled == None)).order_by(
                Subject.id).all()
            subjects_server = Subject.query.order_by(Subject.id).all()
            send_subject_server("subject", platform_server, subjects_server)
            return edit_msg(f"{name}", status=True, data=subject_get.convert_json())
        except:
            return edit_msg(f"{name}", status=False, data=subject_get.convert_json())


@app.route(f'{api}/del_subject/<int:subject_id>', methods=['DELETE'])
@jwt_required()
def del_subject(subject_id):
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity).first()
    sub_name = Subject.query.filter(Subject.id == subject_id).first()
    name = sub_name.name
    sub_name.disabled = True
    db.session.commit()
    if sub_name.img_id:
        check_img_remove(sub_name.img_id, Images)
    subjects_server = Subject.query.order_by(Subject.id).all()
    send_subject_server("subject", platform_server, subjects_server)
    return del_msg(item=name, status=True)
