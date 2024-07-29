from backend.models.basic_model import *
from app import *
from backend.models.settings import *
from backend.basics.settings import *
from pprint import pprint
import json
from sqlalchemy import desc as teskari


@app.route(f'{api}/filter_exercise/<subject_id>/<level_id>')
@jwt_required()
def filter_exercise(subject_id, level_id):
    exercises = Exercise.query.filter(Exercise.subject_id == subject_id, Exercise.level_id == level_id).order_by(
        Exercise.id).all()

    return jsonify({
        "data": iterate_models(exercises)
    })


@app.route(f'{api}/lessons/<int:level_id>', methods=["GET", 'POST'])
@jwt_required()
def lessons(level_id):
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity).first()

    if request.method == "POST":
        info = request.form.get("info")
        get_json = json.loads(info)
        pprint(get_json)
        selected_subject = get_json['subjectId']
        name = get_json['name']
        components = get_json['components']
        order = 1
        lesson_get = Lesson.query.filter(Lesson.level_id == level_id, Lesson.subject_id == selected_subject).order_by(
            Lesson.order).all()
        if lesson_get:
            order = len(lesson_get) + 1
        lesson_add = Lesson(subject_id=selected_subject, level_id=level_id, name=name, order=order)
        lesson_add.add_commit()
        for component in components:
            exercise_id = None
            video_url = ''
            desc = ''
            clone = ''
            if component['type'] == "exc":
                exercise_id = component['id']
            elif component['type'] == "video":
                video_url = component['videoLink']
                clone = component
            elif component['type'] == "text" or component['type'] == "snippet":
                desc = component['text']
                clone = component
            lesson_img = request.files.get(f'component-{component["index"]}-img')
            get_img = None
            if lesson_img:
                get_img = add_file(lesson_img, app, Images)
            lesson_block = LessonBlock(lesson_id=lesson_add.id, exercise_id=exercise_id, video_url=video_url, desc=desc,
                                       img_id=get_img, clone=clone, type_block=component['type'])
            lesson_block.add_commit()
        return create_msg(name, True)

    lessons = Lesson.query.filter(Lesson.level_id == level_id, Lesson.disabled != True).order_by(Lesson.order).all()
    if user.student:
        student = Student.query.filter(Student.user_id == user.id).first()
        for lesson in lessons:
            student_lesson = StudentLesson.query.filter(StudentLesson.lesson_id == lesson.id,
                                                        StudentLesson.student_id == student.id,
                                                        StudentLesson.level_id == level_id).first()
            if not student_lesson:
                student_lesson = StudentLesson(lesson_id=lesson.id, student_id=student.id, level_id=level_id)
                student_lesson.add_commit()

        student_lessons = db.session.query(StudentLesson).join(StudentLesson.lesson).options(
            contains_eager(StudentLesson.lesson)).filter(Lesson.disabled != True,
                                                         StudentLesson.student_id == student.id).order_by(
            StudentLesson.id).all()
        return jsonify({
            "length": len(lessons),
            "data": iterate_models(student_lessons)
        })
    return jsonify({
        "data": iterate_models(lessons),
        "length": len(lessons)
    })


@app.route(f'{api}/info_lesson/<level_id>/<order>', methods=['POST', 'GET', 'DELETE'])
@jwt_required()
def info_lesson(level_id, order):
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity).first()
    lesson = Lesson.query.filter(Lesson.level_id == level_id, Lesson.order == order).first()
    next = Lesson.query.filter(Lesson.level_id == level_id, Lesson.order > lesson.order).filter(
        or_(Lesson.disabled == False, Lesson.disabled == None)).order_by(Lesson.id).first()

    prev = Lesson.query.filter(Lesson.level_id == level_id, Lesson.order < order).filter(
        or_(Lesson.disabled == False, Lesson.disabled == None)).order_by(teskari(Lesson.id)).first()

    if next and next.order:
        next_order = next.order
    else:
        next_order = 1
    if prev and prev.order:
        prev_order = prev.order
    else:

        prev_order = 1
    lessons = Lesson.query.filter(Lesson.level_id == lesson.level_id, Lesson.disabled != True).order_by(
        Lesson.order).all()
    lesson_id = lesson.id
    if request.method == "GET":
        if user.student:
            student = Student.query.filter(Student.user_id == user.id).first()
            student_lesson = StudentLesson.query.filter(StudentLesson.lesson_id == lesson_id,
                                                        StudentLesson.student_id == student.id).first()

            return jsonify({
                "data": student_lesson.convert_json(entire=True),
                "length": len(lessons),
                'lesson_id': student_lesson.id,
                "next": next_order,
                "prev": prev_order
                # "student_exercises": iterate_models(student_exercises, entire=True)
            })
        return jsonify({
            "data": lesson.convert_json(entire=True),
            "length": len(lessons)
        })
    elif request.method == "POST":
        info = request.form.get("info")
        get_json = json.loads(info)
        name = get_json['name']

        lesson.name = name
        db.session.commit()
        components = get_json['components']

        for component in components:
            exercise_id = None
            video_url = ''
            desc = ''
            clone = ''
            if component['type'] == "exc":
                exercise_id = component['id']
            elif component['type'] == "video":
                video_url = component['videoLink']
                clone = component
            elif component['type'] == "text":
                desc = component['text']
                clone = component
            lesson_img = None
            if "index" in component:
                lesson_img = request.files.get(f'component-{component["index"]}-img')
            get_img = None
            if lesson_img:
                get_img = add_file(lesson_img, app, Images)
            if 'block_id' in component:
                lesson_block = LessonBlock.query.filter(LessonBlock.id == component['block_id']).first()
                if lesson_block.img_id:
                    check_img_remove(lesson_block.img_id, Images)
                lesson_block.img_id = get_img
                lesson_block.exercise_id = exercise_id
                lesson_block.video_url = video_url
                lesson_block.desc = desc
                lesson_block.clone = clone
                lesson_block.type_block = component['type']
                db.session.commit()
            else:
                lesson_block = LessonBlock(lesson_id=lesson_id, exercise_id=exercise_id, video_url=video_url,
                                           desc=desc,
                                           img_id=get_img, clone=component, type_block=component['type'])
                lesson_block.add_commit()
        return edit_msg(lesson.name, status=True)

    else:
        lesson.disabled = True
        db.session.commit()
        return del_msg(lesson.name, True)


@app.route(f'{api}/del_lesson_block/<int:block_id>', methods=['DELETE'])
@jwt_required()
def del_lesson_block(block_id):
    lesson_block = LessonBlock.query.filter(LessonBlock.id == block_id).first()
    if lesson_block.img_id:
        check_img_remove(lesson_block.img_id, Images)
    lesson_block.delete_commit()
    return del_msg(item="block", status=True)


@app.route(f'{api}/set_order', methods=['POST'])
@jwt_required()
def set_order():
    lessons_list = request.get_json()['lessons']
    lesson_get = Lesson.query.filter(Lesson.id == lessons_list[0]['id']).first()
    for lesson in lessons_list:
        Lesson.query.filter(Lesson.id == lesson['id']).update({"order": lesson['order']})
        db.session.commit()
    lessons = Lesson.query.filter(Lesson.level_id == lesson_get.level_id, Lesson.disabled != True).order_by(
        Lesson.order).all()
    return jsonify({
        "data": iterate_models(lessons),
        "length": len(lessons)
    })
