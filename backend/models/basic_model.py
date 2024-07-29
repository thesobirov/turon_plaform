from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import *
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, functions

db = SQLAlchemy()


def db_setup(app):
    app.config.from_object('backend.models.config')
    db.app = app
    db.init_app(app)
    Migrate(app, db)
    return db


class User(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "user"
    username = Column(String)
    name = Column(String)
    surname = Column(String)
    image = Column(String)
    password = Column(String)
    role = Column(String)
    parent_name = Column(String)
    birth_date = Column(DateTime)
    number = Column(String)
    email = Column(String)
    address = Column(String)
    age = Column(String)
    teacher = db.relationship("Teacher", backref="user", order_by="Teacher.id")
    student = db.relationship("Student", backref="user", order_by="Student.id")
    worker = db.relationship("Worker", backref="user", order_by="Worker.id")
    pdf_contract = relationship("PdfContract", backref="user", order_by="PdfContract.id")
    class_coins_by_month = relationship("ClassCoinsByMonth", backref="user", order_by="ClassCoinsByMonth.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class Teacher(db.Model):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    subject_id = Column(Integer, ForeignKey("subject.id"))
    salary_percentage = Column(Integer)
    salary_type = Column(Integer, ForeignKey("teacher_salary_type.id"))
    classes = relationship("Class", backref="teacher", secondary="teacher_class", order_by="Class.id")
    rooms = relationship("Room", backref="teacher", order_by="Room.id")
    flows = relationship("Flow", backref="teacher", order_by="Flow.id")
    daily_table = relationship("DailyTable", backref="teacher", order_by="DailyTable.id")
    teacher_salary_day = relationship("Teacher_salary_day", backref="teacher", order_by="Teacher_salary_day.id")
    teacher_attendance = db.relationship('TeacherAttendance', backref='teacher', order_by='TeacherAttendance.id')
    teacher_salaries = relationship("TeacherSalary", backref="teacher", order_by="TeacherSalary.id")
    lesson_plan = db.relationship('Lesson_plan_day', backref='teacher', order_by='Lesson_plan_day.id')
    deleted_teacher = relationship("DeletedTeacher", backref="teacher", order_by="DeletedTeacher.id")
    deleted_classes = relationship("DeletedClasses", backref="teacher",
                                   order_by="DeletedClasses.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class DeletedTeacher(db.Model):
    __tablename__ = "deleted_teacher"
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("teacher.id"))

    def add(self):
        db.session.add(self)
        db.session.commit()


class Worker(db.Model):
    __tablename__ = "worker"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    job_id = Column(Integer, ForeignKey("job.id"))
    worker_salary = relationship("WorkerSalary", backref="worker", order_by="WorkerSalary.id")
    salary = Column(String)

    def add(self):
        db.session.add(self)
        db.session.commit()


class Job(db.Model):
    __tablename__ = "job"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    workers = relationship("Worker", backref="job", order_by="Worker.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class WorkerSalary(db.Model):
    __tablename__ = "worker_salary"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("worker.id"))
    salary = Column(String)
    give_salary = Column(String)
    rest_salary = Column(String)
    month_id = Column(Integer, ForeignKey("month.id"))
    worker_salary_in_days = relationship("WorkerSalaryInDay", backref="worker_salary", order_by="WorkerSalaryInDay.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class WorkerSalaryInDay(db.Model):
    __tablename__ = "worker_salary_in_day"
    id = Column(Integer, primary_key=True)
    salary = Column(Integer)
    reason = Column(String)
    account_type_id = Column(Integer, ForeignKey("account_type.id"))
    year_id = Column(Integer, ForeignKey("years.id"))
    month_id = Column(Integer, ForeignKey("month.id"))
    day_id = Column(Integer, ForeignKey("day.id"))
    worker_salary_id = Column(Integer, ForeignKey("worker_salary.id"))
    deleted_worker_salary_inDay = relationship("DeletedWorkerSalaryInDay", backref="worker_salary_in_day",
                                               order_by="DeletedWorkerSalaryInDay.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class DeletedWorkerSalaryInDay(db.Model):
    __tablename__ = "deleted_worker_salary_inDay"
    id = Column(Integer, primary_key=True)
    worker_salary_in_day_id = Column(Integer, ForeignKey("worker_salary_in_day.id"))
    date = Column(DateTime)

    def add(self):
        db.session.add(self)
        db.session.commit()


class Student(db.Model):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    class_number = Column(Integer, ForeignKey("class_type.id"))
    language_type = Column(Integer, ForeignKey("language.id"))
    classes = relationship("Class", backref="student", secondary="student_class", order_by="Class.id")
    student_month_payments = relationship("StudentMonthPayments", backref="student", order_by="StudentMonthPayments.id")
    student_month_in_payments = relationship("StudentPaymentsInMonth", backref="student",
                                             order_by="StudentPaymentsInMonth.id")
    student_discount = relationship("StudentDiscount", backref="student", order_by="StudentDiscount.id")
    deleted_student = relationship("DeletedStudent", backref="student", order_by="DeletedStudent.id")
    deleted_student_for_classes = relationship("DeletedStudentForClasses", backref="student",
                                               order_by="DeletedStudentForClasses.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class DeletedStudent(db.Model):
    __tablename__ = "deleted_student"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("student.id"))


class TypeInfo(db.Model):
    __tablename__ = "type_info"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    infos = relationship('Info', backref="type_info", order_by="Info.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class Info(db.Model):
    __tablename__ = "info"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    img = Column(String)
    type_id = Column(Integer, ForeignKey('type_info.id'))
    date = Column(DateTime)
    vacations = relationship("Vacation", backref="info", order_by="Vacation.id")

    # workers = relationship("Worker", backref="info", order_by="Worker.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class Vacation(db.Model):
    __tablename__ = "vacation"
    id = Column(Integer, primary_key=True)
    info_id = Column(Integer, ForeignKey('info.id'))
    text = Column(String)
    requests = relationship("Requests", backref="vacation", order_by="Requests.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


# class Worker(db.Model):
#     __tablename__ = "worker"
#     id = Column(Integer, primary_key=True)
#     info_id = Column(Integer, ForeignKey('info.id'))
#     name = Column(String)
#     surname = Column(String)
#     img = Column(String)
#     text = Column(String)
#
#     def add(self):
#         db.session.add(self)
#         db.session.commit()


class Gallery(db.Model):
    __tablename__ = "gallery"
    id = Column(Integer, primary_key=True)
    img = Column(String)


class Partners(db.Model):
    __tablename__ = "partners"
    id = Column(Integer, primary_key=True)
    img = Column(String)


class Comments(db.Model):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    add_date = Column(DateTime)


class Requests(db.Model):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    phone = Column(String)
    vacation_id = Column(Integer, ForeignKey('vacation.id'))
    add_date = Column(DateTime)
    pdf_file = Column(String)

    def add(self):
        db.session.add(self)
        db.session.commit()


class Class(db.Model):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    class_number = Column(Integer)
    color = Column(String)
    price = Column(String)
    overall_coins = Column(Integer, default=0)
    language_type = Column(Integer, ForeignKey("language.id"))
    deleted_student_for_classes = relationship("DeletedStudentForClasses", backref="class",
                                               order_by="DeletedStudentForClasses.id")
    deleted_classes = relationship("DeletedClasses", backref="class",
                                   order_by="DeletedClasses.id")
    subjects = relationship("Subject", backref="class", secondary="class_subjects",
                            order_by="Subject.id")
    daily_table = relationship("DailyTable", backref="class_get", order_by="DailyTable.id")
    class_coins = relationship("ClassCoins", backref="class", order_by="ClassCoins.id")

    # teacher_classes_history = relationship("TeacherClassesHistory", backref="class",
    #                                        order_by="TeacherClassesHistory.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class ClassCoins(db.Model):
    __tablename__ = "class_coins"
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey("class.id"))
    year_id = Column(Integer, ForeignKey("years.id"))
    month_id = Column(Integer, ForeignKey("month.id"))
    coins = Column(Integer, default=0)
    given_coins = Column(Integer, default=0)
    rest_coins = Column(Integer, default=0)
    class_coins_by_month = relationship("ClassCoinsByMonth", backref="class_coins", order_by="ClassCoinsByMonth.id")


class ClassCoinsByMonth(db.Model):
    __tablename__ = "class_coins_by_month"
    id = Column(Integer, primary_key=True)
    class_coins_id = Column(Integer, ForeignKey("class_coins.id"))
    coins = Column(Integer)
    type = Column(Boolean)
    day_id = Column(Integer, ForeignKey("day.id"))
    reason = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))


db.Table('student_class',
         db.Column('class_id', db.Integer, db.ForeignKey('class.id')),
         db.Column('student_id', db.Integer, db.ForeignKey('student.id'))
         )

db.Table('teacher_class',
         db.Column('class_id', db.Integer, db.ForeignKey('class.id')),
         db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'))
         )


class Subject(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "subject"
    name = Column(String)
    teacher = relationship("Teacher", backref="subject", order_by="Teacher.id")
    flows = relationship("Flow", backref="subject", order_by="Flow.id")
    daily_table = relationship("DailyTable", backref="subject",
                               order_by="DailyTable.id")


db.Table('class_subjects',
         db.Column('class_id', db.Integer, db.ForeignKey('class.id')),
         db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'))
         )


class PdfContract(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "pdf_contract"
    user_id = Column(Integer, ForeignKey("user.id"))
    pdf = Column(String)


class AccountType(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "account_type"
    name = Column(String)
    student_month_payments = relationship("StudentMonthPayments", backref="account_type",
                                          order_by="StudentMonthPayments.id")
    student_payments_in_month = relationship("StudentPaymentsInMonth", backref="account_type",
                                             order_by="StudentPaymentsInMonth.id")
    overhead = relationship("Overhead", backref="account_type",
                            order_by="Overhead.id")
    stationary = relationship("Stationary", backref="account_type",
                              order_by="Stationary.id")
    catering_overhead = relationship("CateringOverhead", backref="account_type",
                                     order_by="CateringOverhead.id")
    capital_expenses = relationship("CapitalExpenses", backref="account_type",
                                    order_by="CapitalExpenses.id")
    marketing_overhead = relationship("MarketingOverhead", backref="account_type",
                                      order_by="MarketingOverhead.id")
    given_salaries_in_month = relationship("GivenSalariesInMonth", backref="account_type",
                                           order_by="GivenSalariesInMonth.id")
    worker_salary_days = db.relationship('WorkerSalaryInDay', backref='account_type',
                                         order_by='WorkerSalaryInDay.id')
    teacher_salary_day = relationship("Teacher_salary_day", backref="account_type",
                                      order_by="Teacher_salary_day.id")


class StudentMonthPayments(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "student_month_payments"
    student_id = Column(Integer, ForeignKey("student.id"))
    account_type_id = Column(Integer, ForeignKey("account_type.id"))
    class_price = Column(Integer)
    payed = Column(Integer)
    another = Column(Integer)
    month = Column(DateTime)
    real_price = Column(Integer)
    discount_percentage = Column(Integer)
    student_payments_in_month = relationship("StudentPaymentsInMonth", backref="student_month_payments",
                                             order_by="StudentPaymentsInMonth.id")


class LanguageType(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "language"
    name = Column(String)
    student = relationship("Student", backref="language",
                           order_by="Student.id")
    classes = relationship("Class", backref="language",
                           order_by="Class.id")


class StudentPaymentsInMonth(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "student_payments_in_month"
    student_month_payments_id = Column(Integer, ForeignKey("student_month_payments.id"))
    student_id = Column(Integer, ForeignKey("student.id"))
    account_type_id = Column(Integer, ForeignKey("account_type.id"))
    payed = Column(Integer)
    date = Column(DateTime)


class Overhead(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "over_head"
    name = Column(String)
    account_type_id = Column(Integer, ForeignKey("account_type.id"))
    payed = Column(Integer)
    date = Column(DateTime)
    deleted_over_head = relationship("DeleteDOverhead", backref="over_head",
                                     order_by="DeleteDOverhead.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class Stationary(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "stationary"
    name = Column(String)
    account_type_id = Column(Integer, ForeignKey("account_type.id"))
    payed = Column(Integer)
    date = Column(DateTime)
    deleted_stationary = relationship("DeleteDStationary", backref="stationary",
                                      order_by="DeleteDStationary.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class CateringOverhead(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "catering_overhead"
    name = Column(String)
    account_type_id = Column(Integer, ForeignKey("account_type.id"))
    payed = Column(Integer)
    date = Column(DateTime)
    deleted_catering_overhead = relationship("DeleteDCateringOverhead", backref="catering_overhead",
                                             order_by="DeleteDCateringOverhead.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class CapitalExpenses(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "capital_expenses"
    name = Column(String)
    account_type_id = Column(Integer, ForeignKey("account_type.id"))
    payed = Column(Integer)
    date = Column(DateTime)
    deleted_capital_expenses = relationship("DeleteDCapitalExpenses", backref="capital_expenses",
                                            order_by="DeleteDCapitalExpenses.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class MarketingOverhead(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "marketing_overhead"
    name = Column(String)
    account_type_id = Column(Integer, ForeignKey("account_type.id"))
    payed = Column(Integer)
    date = Column(DateTime)
    deleted_marketing_overhead = relationship("DeleteDMarketingOverhead", backref="marketing_overhead",
                                              order_by="DeleteDMarketingOverhead.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class DeleteDOverhead(db.Model):
    __tablename__ = "deleted_over_head"
    id = Column(Integer, primary_key=True)
    over_head_id = Column(Integer, ForeignKey("over_head.id"))
    date = Column(DateTime)

    def add(self):
        db.session.add(self)
        db.session.commit()


class DeleteDStationary(db.Model):
    __tablename__ = "deleted_stationary"
    id = Column(Integer, primary_key=True)
    stationary_id = Column(Integer, ForeignKey("stationary.id"))
    date = Column(DateTime)

    def add(self):
        db.session.add(self)
        db.session.commit()


class DeleteDCapitalExpenses(db.Model):
    __tablename__ = "deleted_capital_expenses"
    id = Column(Integer, primary_key=True)
    capital_expenses_id = Column(Integer, ForeignKey("capital_expenses.id"))
    date = Column(DateTime)

    def add(self):
        db.session.add(self)
        db.session.commit()


class DeleteDCateringOverhead(db.Model):
    __tablename__ = "deleted_catering_overhead"
    id = Column(Integer, primary_key=True)
    catering_overhead_id = Column(Integer, ForeignKey("catering_overhead.id"))
    date = Column(DateTime)

    def add(self):
        db.session.add(self)
        db.session.commit()


class DeleteDMarketingOverhead(db.Model):
    __tablename__ = "deleted_marketing_overhead"
    id = Column(Integer, primary_key=True)
    marketing_overhead_id = Column(Integer, ForeignKey("marketing_overhead.id"))
    date = Column(DateTime)

    def add(self):
        db.session.add(self)
        db.session.commit()


class ClassType(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "class_type"
    class_number = Column(Integer)
    price = Column(Integer)
    student = relationship("Student", backref="class_type",
                           order_by="Student.id")


class DiscountType(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "discount_type"
    name = Column(String)
    student_discount = relationship("StudentDiscount", backref="discount_type",
                                    order_by="StudentDiscount.id")


class StudentDiscount(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "student_discount"
    student_id = Column(Integer, ForeignKey("student.id"))
    discount_type_id = Column(Integer, ForeignKey("discount_type.id"))
    discount_percentage = Column(Integer)


class DeletedStudentForClasses(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "deleted_student_for_classes"
    student_id = Column(Integer, ForeignKey("student.id"))
    class_id = Column(Integer, ForeignKey("class.id"))
    reason = Column(String)


class DeletedClasses(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "deleted_classes"
    class_id = Column(Integer, ForeignKey("class.id"))
    teacher_id = Column(Integer, ForeignKey("teacher.id"))


class Room(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "room"
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    chair_count = Column(Integer)
    image = Column(String)
    daily_table = relationship("DailyTable", backref="room",
                               order_by="DailyTable.id")


class FlowTypes(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "flow_types"
    classes = Column(String)
    color = Column(String)
    start = Column(Integer)
    end = Column(Integer)


class Flow(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "flow"
    name = Column(String)
    subject_id = Column(Integer, ForeignKey("subject.id"))
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    students = relationship("Student", secondary="flow_students", backref="room",
                            order_by="Student.id")
    daily_table = relationship("DailyTable", backref="flow",
                               order_by="DailyTable.id", uselist=True)


db.Table("flow_students",
         Column("flow_id", Integer, ForeignKey("flow.id")),
         Column("student_id", Integer, ForeignKey("student.id"))
         )


class TimeList(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "time_list"
    lesson_count = Column(String)
    start = Column(String)
    end = Column(String)
    daily_time = relationship("DailyTable", backref="time_list",
                              order_by="DailyTable.id")
    lesson_days = relationship("Lesson_plan_day", backref="time_list",
                               order_by="Lesson_plan_day.id")


class TimeTableDay(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "time_table_day"
    name = Column(String)
    daily_table = relationship("DailyTable", backref="time_table_day",
                               secondary="time_table_day_lessons",
                               order_by="DailyTable.id", uselist=True)


class DailyTable(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "daily_table"
    lesson_time = Column(Integer, ForeignKey("time_list.id"))
    room_id = Column(Integer, ForeignKey("room.id"))
    class_id = Column(Integer, ForeignKey("class.id"))
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    flow_id = Column(Integer, ForeignKey("flow.id"))
    subject_id = Column(Integer, ForeignKey("subject.id"))
    day_id = Column(Integer)
    flow_lesson = Column(Boolean)


db.Table("time_table_day_lessons",
         Column("time_table_day_id", Integer, ForeignKey("time_table_day.id")),
         Column("daily_table_id", Integer, ForeignKey("daily_table.id"))
         )


class Years(db.Model):
    __tablename__ = 'years'
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    month = db.relationship('Month', backref='years', order_by='Month.id')
    day = db.relationship('Day', backref='years', order_by='Day.id')
    teacher_attendance = db.relationship('TeacherAttendance', backref='years', order_by='TeacherAttendance.id')
    given_salaries_in_month = db.relationship('GivenSalariesInMonth', backref='years',
                                              order_by='GivenSalariesInMonth.id')
    worker_salary_days = db.relationship('WorkerSalaryInDay', backref='years',
                                         order_by='WorkerSalaryInDay.id')
    class_coins = relationship("ClassCoins", backref="years", order_by="ClassCoins.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class TeacherSalaryType(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "teacher_salary_type"
    type_name = Column(String)
    salary = Column(Integer)
    teacher = relationship("Teacher", backref="teacher_salary_type", order_by="Teacher.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class Month(db.Model):
    __tablename__ = "month"
    id = Column(Integer, primary_key=True)
    month_number = Column(Integer)
    month_name = Column(String)
    years_id = Column(Integer, ForeignKey('years.id'))
    day = db.relationship('Day', backref='month', order_by='Day.id')
    teacher_salary = db.relationship('TeacherSalary', backref='month', order_by='TeacherSalary.id')
    worker_salary = db.relationship('WorkerSalary', backref='month', order_by='WorkerSalary.id')
    teacher_attendance = db.relationship('TeacherAttendance', backref='month', order_by='TeacherAttendance.id')
    given_salaries_in_month = db.relationship('GivenSalariesInMonth', backref='month',
                                              order_by='GivenSalariesInMonth.id')
    worker_salary_days = db.relationship('WorkerSalaryInDay', backref='month',
                                         order_by='WorkerSalaryInDay.id')

    class_coins = relationship("ClassCoins", backref="month", order_by="ClassCoins.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class Day(db.Model):
    __tablename__ = "day"
    id = Column(Integer, primary_key=True)
    day_number = Column(Integer)
    day_name = Column(String)
    month_id = Column(Integer, ForeignKey('month.id'))
    year_id = Column(Integer, ForeignKey('years.id'))
    teacher_attendance = db.relationship('TeacherAttendance', backref='day', order_by='TeacherAttendance.id')
    type_id = Column(Integer, ForeignKey('type_day.id'))
    given_salaries_in_month = db.relationship('GivenSalariesInMonth', backref='day',
                                              order_by='GivenSalariesInMonth.id')
    worker_salary_days = db.relationship('WorkerSalaryInDay', backref='day',
                                         order_by='WorkerSalaryInDay.id')
    teacher_salary_day = db.relationship('Teacher_salary_day', backref='day', order_by='Teacher_salary_day.id')
    lesson_plans = db.relationship('Lesson_plan_day', backref='day', order_by='Lesson_plan_day.id')
    class_coins_by_month = db.relationship('ClassCoinsByMonth', backref='day', order_by='ClassCoinsByMonth.id')

    def add(self):
        db.session.add(self)
        db.session.commit()

    # daily_lesson = db.relationship('DailyLesson', backref='days', order_by='DailyLesson.id')


class TeacherSalary(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "teacher_salary"
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    salary = Column(String)
    give_salary = Column(String)
    month_id = Column(Integer, ForeignKey("month.id"))
    rest_salary = Column(String)
    worked_days = Column(String)
    percentage = Column(Integer, default=50)
    given_salaries_in_month = db.relationship('GivenSalariesInMonth', backref='teacher_salary',
                                              order_by='GivenSalariesInMonth.id')
    teacher_salary_days = db.relationship('Teacher_salary_day', backref='teacher_salary',
                                          order_by='Teacher_salary_day.id')

    def add(self):
        db.session.add(self)
        db.session.commit()


class GivenSalariesInMonth(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "given_salaries_in_month"
    teacher_salary_id = Column(Integer, ForeignKey("teacher_salary.id"))
    given_salary = Column(String)
    year_id = Column(Integer, ForeignKey("years.id"))
    month_id = Column(Integer, ForeignKey("month.id"))
    day_id = Column(Integer, ForeignKey("day.id"))
    reason = Column(String)
    account_type_id = Column(Integer, ForeignKey("account_type.id"))
    deleted_given_salaries_in_month = db.relationship('DeletedGivenSalaryInMonth', backref='given_salaries_in_month',
                                                      order_by='DeletedGivenSalaryInMonth.id')

    def add(self):
        db.session.add(self)
        db.session.commit()


class DeletedGivenSalaryInMonth(db.Model):
    __tablename__ = "deleted_given_salaries_in_month"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    given_salary_in_month_id = Column(Integer, ForeignKey("given_salaries_in_month.id"))

    def add(self):
        db.session.add(self)
        db.session.commit()


class TeacherAttendance(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "teacher_attendance"
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    year_id = Column(Integer, ForeignKey("years.id"))
    month_id = Column(Integer, ForeignKey("month.id"))
    day_id = Column(Integer, ForeignKey("day.id"))
    status = Column(Boolean)

    def add(self):
        db.session.add(self)
        db.session.commit()


class TypeDay(db.Model):
    __tablename__ = "type_day"
    id = Column(Integer, primary_key=True)
    type = Column(String)
    color = Column(String)
    day = db.relationship('Day', backref='type_day', order_by='Day.id')

    def add(self):
        db.session.add(self)
        db.session.commit()


class Teacher_salary_day(db.Model):
    __tablename__ = "teacher_salary_day"
    id = Column(Integer, primary_key=True)
    salary = Column(Integer)
    reason = Column(String)
    account_type_id = Column(Integer, ForeignKey("account_type.id"))
    day_id = Column(Integer, ForeignKey("day.id"))
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    teacher_salary_id = Column(Integer, ForeignKey("teacher_salary.id"))
    deleted_teacher_salary_inDay = db.relationship('DeletedTeacherSalaryInDay', backref='teacher_salary_day',
                                                   order_by='DeletedTeacherSalaryInDay.id')

    def add(self):
        db.session.add(self)
        db.session.commit()


class DeletedTeacherSalaryInDay(db.Model):
    __tablename__ = "deleted_teacher_salary_inDay"
    id = Column(Integer, primary_key=True)
    teacher_salary_day_id = Column(Integer, ForeignKey("teacher_salary_day.id"))
    date = Column(DateTime)

    def add(self):
        db.session.add(self)
        db.session.commit()


class Lesson_plan_day(db.Model):
    __tablename__ = "lesson_plan_day"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    target = Column(String)
    main = Column(String)
    assessment = Column(String)
    homework = Column(String)
    day_id = Column(Integer, ForeignKey("day.id"))
    lesson_time_id = Column(Integer, ForeignKey("time_list.id"))
    teacher_id = Column(Integer, ForeignKey("teacher.id"))

    def add(self):
        db.session.add(self)
        db.session.commit()


class Premises(db.Model):
    __tablename__ = "premises"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    img = Column(String)


class Staffing(db.Model):
    __tablename__ = "staffing"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    img = Column(String)


class TeachAsses(db.Model):
    __tablename__ = "teach_asses"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    img = Column(String)


class CommunityAndHomePartnership(db.Model):
    __tablename__ = "CommunityAndHomePartnership"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    img = Column(String)


class GovernanceOwnershipLeadership(db.Model):
    __tablename__ = "governance_ownership_leadership"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    img = Column(String)


class Curriculum(db.Model):
    __tablename__ = "curriculum"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    img = Column(String)


class StudentsLearningAndWellBeing(db.Model):
    __tablename__ = "students_learning_and_well_being"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    img = Column(String)


class PurposeDirection(db.Model):
    __tablename__ = "purpose_direction"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    img = Column(String)


class Clients(db.Model):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    number = Column(String)
