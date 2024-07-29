from backend.models.basic_model import *


class Subject(db.Model):
    __tablename__ = "subject"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    img_id = Column(Integer, ForeignKey('images.id'))
    desc = Column(String)
    levels = relationship("SubjectLevel", backref="subject", order_by="SubjectLevel.id")
    answer = relationship('ExerciseAnswers', backref="subject", order_by="ExerciseAnswers.id")
    lesson = relationship('Lesson', backref="subject", order_by="Lesson.id")
    exercise = relationship('Exercise', backref="subject", order_by="Exercise.id")
    student_question = relationship("StudentQuestion", lazy="select", order_by="StudentQuestion.id")
    question_answers = relationship("QuestionAnswers", lazy="select", order_by="QuestionAnswers.id")
    answer_comment = relationship("QuestionAnswerComment", lazy="select", order_by="QuestionAnswerComment.id")
    donelessons = relationship('StudentExercise', backref="subject", order_by="StudentExercise.id")
    studentsubject = relationship('StudentSubject', backref="subject", order_by="StudentSubject.id")
    certificate = relationship('Certificate', backref="subject", order_by="Certificate.id")
    groups = relationship("Group", backref="subject", order_by="Group.id")
    disabled = Column(Boolean, default=False)

    def convert_json(self, entire=False):
        if self.groups or self.lesson or self.levels or self.exercise:
            deleted = False
        else:
            deleted = True
        if not entire:
            info = {
                "id": self.id,
                "name": self.name,
                "img": None,
                "desc": self.desc,
                "disabled": self.disabled,
                "status_deleted": deleted
            }
            if self.img and self.img.url:
                info['img'] = self.img.url
            return info
        info = {
            "id": self.id,
            "name": self.name,
            "img": None,
            "desc": self.desc,
            "disabled": self.disabled,
            "status_deleted": deleted,
            "levels": []
        }
        if self.img and self.img.url:
            info['img'] = self.img.url
        for level in self.levels:
            level_info = {
                "id": level.id,
                "name": level.name,
                "disabled": level.disabled
            }
            info['level'].append(level_info)
        return info

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class LevelCategory(db.Model):
    __tablename__ = "level_category"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ot = Column(Float)
    do = Column(Float)
    # students = relationship("Student", backref="level", order_by="Student.id", lazy="select")


class SubjectLevel(db.Model):
    __tablename__ = "subject_level"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)
    subject_id = Column(Integer, ForeignKey("subject.id"))
    disabled = Column(Boolean, default=False)
    lesson = relationship('Lesson', backref="subject_level", order_by="Lesson.id")
    student_lesson = relationship("StudentLesson", backref="subject_level", order_by="StudentLesson.id")
    exercise = relationship('Exercise', backref="subject_level", order_by="Exercise.id")
    donelessons = relationship("StudentExercise", backref="subject_level", order_by="StudentExercise.id")
    student_level = relationship('StudentLevel', backref="subject_level", order_by="StudentLevel.id")
    certificate = relationship('Certificate', backref="subject_level", order_by="Certificate.id")
    groups = relationship('Group', backref="subject_level", order_by="Group.id")

    def convert_json(self, entire=False):
        return {
            "id": self.id,
            "name": self.name,
            "subject": {
                "id": self.subject_id,
                "name": self.subject.name,
                "disabled": self.subject.disabled
            },
            "desc": self.desc,
            "disabled": self.disabled
        }

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class Lesson(db.Model):
    __tablename__ = "lesson"
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subject.id"))
    level_id = Column(Integer, ForeignKey("subject_level.id"))
    name = Column(String)
    exercises = relationship("Exercise", secondary="lesson_exercise", backref="lesson", order_by="Exercise.id")
    blocks = relationship("LessonBlock", backref="lesson", order_by="LessonBlock.id")
    student_lesson = relationship("StudentLesson", backref="lesson", order_by="StudentLesson.id")
    disabled = Column(Boolean, default=False)
    order = Column(Integer)

    def convert_json(self, entire=False):
        if entire:
            info = {
                "id": self.id,
                "name": self.name,
                "subject_id": self.subject.id,
                "subject_name": self.subject.name,
                "level_id": self.subject_level.id,
                "level_name": self.subject_level.name,
                "blocks": [],
                "order": self.order,
            }
            for block in self.blocks:
                block_info = {
                    "id": block.id,
                    "video_url": block.video_url,
                    "img": None,
                    "desc": block.desc,
                    "clone": block.clone,
                    "exercise_id": block.exercise_id,
                    "type": block.type_block,
                    "exercise_block": []
                }
                if block.img_id:
                    block_info['img'] = block.img.url
                if block.exercise_id:
                    exercise = Exercise.query.filter(Exercise.id == block.exercise_id).first()

                    for block_exercise in exercise.block:
                        ex_block = {
                            "id": block_exercise.id,
                            "answers": [],
                            'innerType': block_exercise.inner_type,
                            "clone": block_exercise.clone,
                            "type": block_exercise.component.name,
                            "img": "",
                            "audio_url": block_exercise.audio_url,
                            "desc": block_exercise.desc,
                            "words_img": []

                        }
                        block_images = ExerciseBlockImages.query.filter(
                            ExerciseBlockImages.block_id == block_exercise.id).order_by(ExerciseBlockImages.id).all()
                        for img in block_images:
                            info_img = {
                                "id": img.img.id,
                                "img": img.img.url,
                                "order": img.order,
                                "type": img.type_image
                            }
                            ex_block['words_img'].append(info_img)
                        if block_exercise.img:
                            ex_block['img'] = block_exercise.img.url
                        answers = ExerciseAnswers.query.filter(ExerciseAnswers.block_id == block_exercise.id,
                                                               ExerciseAnswers.exercise_id == block.exercise_id,
                                                               ).order_by(
                            ExerciseAnswers.id).all()
                        for exe in answers:
                            answer_info = {
                                "id": exe.id,
                                "desc": exe.desc,
                                "order": exe.order,
                                "img": None,
                                "block_id": exe.block_id,
                                "type_img": exe.type_img
                            }
                            ex_block['answers'].append(answer_info)
                        block_info['exercise_block'].append(ex_block)
                info['blocks'].append(block_info)
            return info
        else:

            return {
                "id": self.id,
                "name": self.name,
                "subject_id": self.subject.id,
                "subject_name": self.subject.name,
                "level_id": self.subject_level.name,
                "order": self.order

            }

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class LessonBlock(db.Model):
    __tablename__ = "lesson_block"
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lesson.id'))
    exercise_id = Column(Integer, ForeignKey('exercise.id'))
    video_url = Column(String)
    img_id = Column(Integer, ForeignKey('images.id'))
    desc = Column(String)
    clone = Column(JSON)
    type_block = Column(String)

    def add_commit(self):
        db.session.add(self)
        db.session.commit()

    def delete_commit(self):
        db.session.delete(self)
        db.session.commit()


class ExerciseTypes(db.Model):
    __tablename__ = "exercise_types"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    exercises = relationship("Exercise", backref="exercise_types", order_by="Exercise.id")
    donelessons = relationship("StudentExercise", backref="exercise_types", order_by="StudentExercise.id")
    disabled = Column(Boolean, default=False)

    def convert_json(self, entire=False):
        return {
            "id": self.id,
            "del_status": False,
            "name": self.name,
        }

    def convert_json_check(self):
        return {
            "id": self.id,
            "del_status": True,
            "name": self.name
        }

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class Component(db.Model):
    __tablename__ = "component"
    id = Column(Integer, primary_key=True)
    type_component = Column(String)
    name = Column(String)
    exercise_blocks = relationship("ExerciseBlock", backref="component", order_by="ExerciseBlock.id")

    def convert_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "desc": self.desc
        }

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class Exercise(db.Model):
    __tablename__ = "exercise"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    subject_id = Column(Integer, ForeignKey("subject.id"))
    type_id = Column(Integer, ForeignKey('exercise_types.id'))
    level_id = Column(Integer, ForeignKey("subject_level.id"))
    block = relationship("ExerciseBlock", backref="exercise", lazy="select", order_by="ExerciseBlock.id")
    exercise_answers = relationship("ExerciseAnswers", backref="exercise", order_by="ExerciseAnswers.id")
    donelessons = relationship("StudentExercise", backref="exercise", order_by="StudentExercise.id")

    def add_commit(self):
        db.session.add(self)
        db.session.commit()

    def convert_json(self, entire=False):
        if entire:
            info = {
                "id": self.id,
                "name": self.name,
                "subject": {
                    "id": self.subject.id,
                    "name": self.subject.name
                },
                "type": {
                    "id": self.exercise_types.id,
                    "name": self.exercise_types.name

                },
                "level": {
                    "id": self.subject_level.id,
                    "name": self.subject_level.name
                },
                "block": [],
            }

            for block in self.block:
                info_block = {
                    "id": block.id,
                    "desc": block.desc,
                    "clone": block.clone,
                    "type": block.component.name,
                    "img": None,
                    "audio": block.audio_url,
                    "answers": [],
                    "innerType": block.inner_type,
                    "words_img": []

                }
                block_images = ExerciseBlockImages.query.filter(
                    ExerciseBlockImages.block_id == block.id).order_by(ExerciseBlockImages.id).all()
                for img in block_images:
                    info_img = {
                        "id": img.img.id,
                        "img": img.img.url,
                        "order": img.order,
                        "type": img.type_image
                    }
                    info_block['words_img'].append(info_img)
                if block.img:
                    info_block['img'] = block.img.url
                info['block'].append(info_block)
                for answers in block.exercise_answers:
                    info_answer = {
                        "id": answers.id,
                        "desc": answers.desc,
                        "order": answers.order,
                        "img": None,
                        "block_id": answers.block_id,
                        "type_img": answers.type_img
                    }
                    if answers.img:
                        info_answer['img'] = answers.img.url
                    info_block['answers'].append(info_answer)
            return info
        return {
            "id": self.id,
            "name": self.name,
            "subject": {
                "id": self.subject.id,
                "name": self.subject.name
            },
            "type": {
                "id": self.exercise_types.id,
                "name": self.exercise_types.name

            },
            "level": {
                "id": self.subject_level.id,
                "name": self.subject_level.name
            },
            "block": [],

        }

    def delete_commit(self):
        db.session.delete(self)
        db.session.commit()


class ExerciseBlock(db.Model):
    __tablename__ = "exercise_block"
    id = Column(Integer, primary_key=True)
    desc = Column(String)
    exercise_id = Column(Integer, ForeignKey('exercise.id'))
    clone = Column(JSON())
    component_id = Column(Integer, ForeignKey('component.id'))
    img_id = Column(Integer, ForeignKey('images.id'))
    audio_url = Column(String)
    exercise_answers = relationship("ExerciseAnswers", backref="exercise_block", order_by="ExerciseAnswers.id")
    student_exercises = relationship("StudentExercise", backref="exercise_block", order_by="StudentExercise.id")
    student_block = relationship("StudentExerciseBlock", backref="exercise_block", order_by="StudentExerciseBlock.id")
    inner_type = Column(String)

    def add_commit(self):
        db.session.add(self)
        db.session.commit()

    def delete_commit(self):
        db.session.delete(self)
        db.session.commit()


db.Table('lesson_exercise',
         db.Column('lesson_id', db.Integer, db.ForeignKey('lesson.id')),
         db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id'))
         )


class ExerciseAnswers(db.Model):
    __tablename__ = "exercise_answers"
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('exercise_types.id'))
    exercise_id = Column(Integer, ForeignKey('exercise.id'))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    level_id = Column(Integer, ForeignKey("subject_level.id"))
    desc = Column(String)
    order = Column(Integer)
    img_id = Column(Integer, ForeignKey('images.id'))
    status = Column(Boolean, default=False)
    block_id = Column(Integer, ForeignKey('exercise_block.id'))
    type_img = Column(String)
    student_exercise = relationship("StudentExercise", backref="exercise_answer", order_by="StudentExercise.id")

    def convert_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img.url,
            "desc": self.desc
        }

    def add_commit(self):
        db.session.add(self)
        db.session.commit()

    def delete_commit(self):
        db.session.delete(self)
        db.session.commit()


class StudentExercise(db.Model):
    __tablename__ = "student_exercise"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("student.id"))
    lesson_id = Column(Integer, ForeignKey("lesson.id"))
    level_id = Column(Integer, ForeignKey("subject_level.id"))
    type_id = Column(Integer, ForeignKey("exercise_types.id"))
    subject_id = Column(Integer, ForeignKey("subject.id"))
    exercise_id = Column(Integer, ForeignKey("exercise.id"))
    boolean = Column(Boolean)
    block_id = Column(Integer, ForeignKey('exercise_block.id'))
    answer_id = Column(Integer, ForeignKey('exercise_answers.id'))
    value = Column(JSON())

    def convert_json(self, entire=False):
        if entire:
            exercise = {
                "block": {
                    "id": self.block_id,
                    "answers": []
                }
            }
            for answer in self.exercise_block.exercise_answers:
                block_info = {
                    "id": answer.id,
                    "answer": answer.status
                }
                exercise['block']['answers'].append(block_info)
            return exercise

    def add_commit(self):
        db.session.add(self)
        db.session.commit()

    def delete_commit(self):
        db.session.delete(self)
        db.session.commit()


class ExerciseBlockImages(db.Model):
    __tablename__ = "exercise_block_images"
    id = Column(Integer, primary_key=True)
    img_id = Column(Integer, ForeignKey('images.id'))
    block_id = Column(Integer, ForeignKey('exercise_block.id'))
    order = Column(Integer)
    type_image = Column(String)

    def add_commit(self):
        db.session.add(self)
        db.session.commit()

    def delete_commit(self):
        db.session.delete(self)
        db.session.commit()


class StudentLesson(db.Model):
    __tablename__ = "student_lesson"
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lesson.id"))
    student_id = Column(Integer, ForeignKey("student.id"))
    percentage = Column(Float, default=0)
    finished = Column(Boolean, default=False)
    level_id = Column(Integer, ForeignKey("subject_level.id"))

    def convert_json(self, entire=False):
        if entire:
            info = {
                "id": self.lesson.id,
                "name": self.lesson.name,
                "lesson_id": self.id,
                "subject_id": self.lesson.subject.id,
                "subject_name": self.lesson.subject.name,
                "level_id": self.lesson.subject_level.id,
                "level_name": self.subject_level.name,
                "blocks": [],
                "order": self.lesson.order,
                "percentage": self.percentage,
                "checked": self.finished
            }

            for block in self.lesson.blocks:

                block_info = {
                    "id": block.id,
                    "video_url": block.video_url,
                    "img": None,
                    "desc": block.desc,
                    "clone": block.clone,
                    "exercise_id": block.exercise_id,
                    "type": block.type_block,
                    "exercise_block": []
                }
                if block.img_id:
                    block_info['img'] = block.img.url
                if block.exercise_id:
                    exercise = Exercise.query.filter(Exercise.id == block.exercise_id).first()

                    for block_exercise in exercise.block:
                        ex_block = {
                            "id": block_exercise.id,
                            "answers": [],
                            'innerType': block_exercise.inner_type,
                            "clone": block_exercise.clone,
                            "type": block_exercise.component.name,
                            "img": "",
                            "audio_url": block_exercise.audio_url,
                            "desc": block_exercise.desc,
                            "words_img": [],
                            'isAnswered': False

                        }
                        block_images = ExerciseBlockImages.query.filter(
                            ExerciseBlockImages.block_id == block_exercise.id).order_by(ExerciseBlockImages.id).all()
                        for img in block_images:
                            info_img = {
                                "id": img.img.id,
                                "img": img.img.url,
                                "order": img.order,
                                "type": img.type_image
                            }
                            ex_block['words_img'].append(info_img)
                        if block_exercise.img:
                            ex_block['img'] = block_exercise.img.url

                        exercise_answers = ExerciseAnswers.query.filter(
                            ExerciseAnswers.exercise_id == block.exercise_id,
                            ExerciseAnswers.block_id == block_exercise.id).order_by(ExerciseAnswers.id).all()
                        student_exercise = StudentExercise.query.filter(
                            StudentExercise.block_id == block_exercise.id,
                            StudentExercise.exercise_id == block.exercise_id,
                            StudentExercise.student_id == self.student_id).order_by(
                            StudentExercise.id).all()
                        if student_exercise:
                            for exe in student_exercise:
                                info_answer = {
                                    "id": exe.id,
                                    "desc": exe.exercise_answer.desc,
                                    "order": exe.exercise_answer.order,
                                    "img": None,
                                    "block_id": exe.exercise_answer.block_id,
                                    "type_img": exe.exercise_answer.type_img,
                                    'status': exe.boolean,
                                    'value': exe.value,

                                }
                                if exe.exercise_answer.img:
                                    info_answer['img'] = exe.exercise_answer.img.url
                                ex_block['isAnswered'] = True
                                ex_block['answers'].append(info_answer)
                        else:
                            for exe in exercise_answers:
                                info_answer = {
                                    "id": exe.id,
                                    "desc": exe.desc,
                                    "order": exe.order,
                                    "img": None,
                                    "block_id": exe.block_id,
                                    "type_img": exe.type_img,
                                }
                                if exe.img:
                                    info_answer['img'] = exe.img.url
                                ex_block['answers'].append(info_answer)
                        block_info['exercise_block'].append(ex_block)
                info['blocks'].append(block_info)

            return info
        return {
            "id": self.lesson.id,
            "lesson_id": self.id,
            "name": self.lesson.name,
            "subject_id": self.lesson.subject.id,
            "subject_name": self.lesson.subject.name,
            "level_id": self.subject_level.name,
            "order": self.lesson.order,
            "percentage": self.percentage,
            "checked": self.finished

        }

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class StudentExerciseBlock(db.Model):
    __tablename__ = "student_exercise_block"
    id = Column(Integer, primary_key=True)
    exercise_id = Column(Integer, ForeignKey('exercise.id'))
    block_id = Column(Integer, ForeignKey('exercise_block.id'))
    clone = Column(JSON())
    student_id = Column(Integer, ForeignKey('student.id'))
    lesson_id = Column(Integer, ForeignKey("lesson.id"))

    def convert_json(self, entire=False):
        ex_block = {
            "id": self.exercise_block.id,
            "answers": [],
            'innerType': self.exercise_block.inner_type,
            "clone": self.exercise_block.clone,
            "type": self.exercise_block.component.name,
            "img": "",
            "audio_url": self.exercise_block.audio_url,
            "desc": self.exercise_block.desc,
            "words_img": [],
            'isAnswered': False

        }
        block_images = ExerciseBlockImages.query.filter(
            ExerciseBlockImages.block_id == self.exercise_block.id).order_by(ExerciseBlockImages.id).all()
        for img in block_images:
            info_img = {
                "id": img.img.id,
                "img": img.img.url,
                "order": img.order,
                "type": img.type_image
            }
            ex_block['words_img'].append(info_img)
        if self.exercise_block.img:
            ex_block['img'] = self.exercise_block.img.url

        student_exercise = StudentExercise.query.filter(
            StudentExercise.block_id == self.exercise_block.id,
            StudentExercise.exercise_id == self.exercise_block.exercise_id,
            StudentExercise.student_id == self.student_id).order_by(
            StudentExercise.id).all()

        for exe in student_exercise:
            info_answer = {
                "id": exe.id,
                "desc": exe.exercise_answer.desc,
                "order": exe.exercise_answer.order,
                "img": None,
                "block_id": exe.exercise_answer.block_id,
                "type_img": exe.exercise_answer.type_img,
                'status': exe.boolean,
                'value': exe.value,

            }
            if exe.exercise_answer.img:
                info_answer['img'] = exe.exercise_answer.img.url
            ex_block['isAnswered'] = True
            ex_block['answers'].append(info_answer)
        return ex_block

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class StudentLevel(db.Model):
    __tablename__ = "student_level"
    id = Column(Integer, primary_key=True)
    level_id = Column(Integer, ForeignKey("subject_level.id"))
    student_id = Column(Integer, ForeignKey("student.id"))
    percentage = Column(Float, default=0)
    group_id = Column(Integer, ForeignKey('group.id'))
    finished = Column(Boolean, default=False)
    subject_id = Column(Integer, ForeignKey('subject.id'))

    def convert_json(self, entire=False):
        return {
            "id": self.subject_level.id,
            "percentage": self.percentage,
            "checked": self.finished,
            "level_id": self.id,
            "name": self.subject_level.name,
            "subject": {
                "id": self.subject_level.subject_id,
                "name": self.subject_level.subject.name,
                "disabled": self.subject_level.subject.disabled
            },
            "desc": self.subject_level.desc,
            "disabled": self.subject_level.disabled
        }

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class StudentSubject(db.Model):
    __tablename__ = "student_subject"
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subject.id"))
    student_id = Column(Integer, ForeignKey("student.id"))
    percentage = Column(Integer, default=0)
    finished = Column(Boolean, default=False)

    def convert_json(self, entire=False):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "desc": self.desc
        }

    def add_commit(self):
        db.session.add(self)
        db.session.commit()
