from backend.models.basic_model import *
from app import *
from backend.models.basic_model import *


@app.route(f'{api}/finish/lesson/<int:lesson_id>')
@jwt_required()
def finish_lesson(lesson_id):
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity).first()
    student = Student.query.filter(Student.user_id == user.id).first()
    StudentLesson.query.filter(StudentLesson.id == lesson_id).update({
        "finished": True
    })
    db.session.commit()
    lesson = StudentLesson.query.filter(StudentLesson.id == lesson_id,
                                        StudentLesson.student_id == student.id).first()
    student_lessons_true = StudentLesson.query.filter(StudentLesson.level_id == lesson.level_id,
                                                      StudentLesson.finished == True,
                                                      StudentLesson.student_id == student.id).count()
    student_lessons = StudentLesson.query.filter(StudentLesson.level_id == lesson.level_id,
                                                 StudentLesson.student_id == student.id).count()
    student_level = StudentLevel.query.filter(StudentLevel.level_id == lesson.level_id,
                                              StudentLevel.student_id == student.id).first()

    if student_lessons_true == student_lessons:
        student_level.finished = True
        db.session.commit()
    return jsonify({
        "status": 'success'
    })


@app.route(f'{api}/complete_exercise', methods=['POST'])
@jwt_required()
def complete_exercise():
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity).first()
    answers = request.get_json()['block']
    lesson_id = request.get_json()['lessonId']
    exercise_id = request.get_json()['excId']
    student = Student.query.filter(Student.user_id == user.id).first()
    student_lesson = StudentLesson.query.filter(StudentLesson.lesson_id == lesson_id,
                                                StudentLesson.student_id == student.id).first()
    for answer in answers:
        block = ExerciseBlock.query.filter(ExerciseBlock.id == answer['block_id']).first()
        exercise = Exercise.query.filter(Exercise.id == block.exercise_id).first()
        exist_block = StudentExerciseBlock.query.filter(StudentExerciseBlock.lesson_id == lesson_id,
                                                        StudentExerciseBlock.student_id == student.id,
                                                        StudentExerciseBlock.block_id == block.id,
                                                        StudentExerciseBlock.exercise_id == exercise.id).first()
        if not exist_block:
            student_exe_block = StudentExerciseBlock(student_id=student.id, block_id=block.id, exercise_id=exercise.id,
                                                     clone=answer['answers'], lesson_id=lesson_id)
            student_exe_block.add_commit()

        if answer['innerType'] == "text" and answer['type'] == "question" or answer['innerType'] == "image" and answer[
            'type'] == "question" or answer['innerType'] == "imageInText" and answer['type'] == "question":
            exercise_answer = ExerciseAnswers.query.filter(ExerciseAnswers.block_id == answer['block_id'],
                                                           ExerciseAnswers.status == True).first()
            for ans in answer['answers']:

                if ans['checked'] == True:
                    status = False
                    if exercise_answer.order == ans['index']:
                        status = True
                    else:
                        exercise_answer = ExerciseAnswers.query.filter(ExerciseAnswers.block_id == answer['block_id'],
                                                                       ExerciseAnswers.order == ans['index']).first()
                    exist_exercise = StudentExercise.query.filter(StudentExercise.student_id == student.id,
                                                                  StudentExercise.lesson_id == lesson_id,
                                                                  StudentExercise.exercise_id == exercise.id,
                                                                  StudentExercise.answer_id == exercise_answer.id).first()
                    if not exist_exercise:
                        student_exercise = StudentExercise(student_id=student.id, lesson_id=lesson_id,
                                                           exercise_id=exercise.id, subject_id=exercise.subject_id,
                                                           type_id=exercise.type_id, level_id=exercise.level_id,
                                                           boolean=status, block_id=block.id,
                                                           answer_id=exercise_answer.id, value=ans['checked'])
                        student_exercise.add_commit()
                    else:
                        return jsonify({
                            'msg': 'seryoz'
                        })
            update_ratings(student, lesson_id)

        elif answer["innerType"] == "innerInputs" and answer['type'] == "text":

            for ans in answer['answers']:
                exercise_answer = ExerciseAnswers.query.filter(ExerciseAnswers.block_id == answer['block_id'],
                                                               ExerciseAnswers.order == ans['id']).first()
                if exercise_answer.desc == ans['value']:
                    exercise_status = True
                else:
                    exercise_status = False
                exist_exercise = StudentExercise.query.filter(StudentExercise.student_id == student.id,
                                                              StudentExercise.lesson_id == lesson_id,
                                                              StudentExercise.exercise_id == exercise.id,
                                                              StudentExercise.answer_id == exercise_answer.id).first()
                if not exist_exercise:
                    student_exercise = StudentExercise(student_id=student.id, lesson_id=lesson_id,
                                                       exercise_id=exercise.id, subject_id=exercise.subject_id,
                                                       type_id=exercise.type_id, level_id=exercise.level_id,
                                                       boolean=exercise_status, block_id=block.id,
                                                       answer_id=exercise_answer.id, value=ans['value'])
                    student_exercise.add_commit()
                else:
                    return jsonify({
                        'msg': 'seryoz'
                    })

        elif answer["innerType"] == "matchWords" and answer['type'] == "text":
            for ans in answer['answers']:
                exercise_answer = ExerciseAnswers.query.filter(ExerciseAnswers.block_id == answer['block_id'],
                                                               ExerciseAnswers.order == ans['id']).first()
                if exercise_answer.desc == ans['value']:
                    exercise_status = True
                else:
                    exercise_status = False
                exist_exercise = StudentExercise.query.filter(StudentExercise.student_id == student.id,
                                                              StudentExercise.lesson_id == lesson_id,
                                                              StudentExercise.exercise_id == exercise.id,
                                                              StudentExercise.answer_id == exercise_answer.id).first()
                if not exist_exercise:
                    student_exercise = StudentExercise(student_id=student.id, lesson_id=lesson_id, value=ans['value'],
                                                       exercise_id=exercise.id, subject_id=exercise.subject_id,
                                                       type_id=exercise.type_id, level_id=exercise.level_id,
                                                       boolean=exercise_status, block_id=block.id,
                                                       answer_id=exercise_answer.id)
                    student_exercise.add_commit()
                else:
                    return jsonify({
                        'msg': 'seryoz'
                    })

    update_ratings(student, lesson_id)
    exercise_block = StudentExerciseBlock.query.filter(StudentExerciseBlock.lesson_id == lesson_id,
                                                       StudentExerciseBlock.student_id == student.id,
                                                       StudentExerciseBlock.exercise_id == exercise_id).order_by(
        StudentExerciseBlock.id).all()

    return jsonify({
        "success": True,
        "block": iterate_models(exercise_block)
    })


def update_ratings(student, lesson_id):
    student_exercises_true = StudentExercise.query.filter(StudentExercise.student_id == student.id,
                                                          StudentExercise.boolean == True,
                                                          StudentExercise.lesson_id == lesson_id).count()
    student_exercises = StudentExercise.query.filter(StudentExercise.student_id == student.id,
                                                     StudentExercise.lesson_id == lesson_id).count()
    if student_exercises_true:
        percentage = round((student_exercises_true / student_exercises) * 100)
        StudentLesson.query.filter(StudentLesson.lesson_id == lesson_id, StudentLesson.student_id == student.id).update(
            {
                "percentage": percentage
            })
        db.session.commit()
    else:
        StudentLesson.query.filter(StudentLesson.lesson_id == lesson_id, StudentLesson.student_id == student.id).update(
            {
                "percentage": 0
            })
        db.session.commit()
    lesson = StudentLesson.query.filter(StudentLesson.lesson_id == lesson_id,
                                        StudentLesson.student_id == student.id).first()
    student_lessons = StudentLesson.query.filter(StudentLesson.level_id == lesson.level_id,
                                                 StudentLesson.student_id == student.id
                                                 ).count()
    student_lessons_finished = StudentLesson.query.filter(StudentLesson.level_id == lesson.level_id,
                                                          StudentLesson.percentage == 100).count()

    level_percentage = round((student_lessons_finished / student_lessons) * 100)
    student_level = StudentLevel.query.filter(StudentLevel.level_id == lesson.level_id,
                                              StudentLevel.student_id == student.id).first()
    student_level.percentage = level_percentage
    db.session.commit()
