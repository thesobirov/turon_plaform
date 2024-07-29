from backend.models.models import *


class PaymentTypes(db.Model):
    __tablename__ = "paymenttypes"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    student_payments = relationship('StudentPayments', backref="payment_type", order_by="StudentPayments.id")
    teacher_salaries = relationship('TeacherSalaries', backref="payment_type", order_by="TeacherSalaries.id")
    overhead_data = relationship('Overhead', backref="payment_type", order_by="Overhead.id")
    accounting = relationship("AccountingInfo", backref="payment_type", order_by="AccountingInfo.id")
    staff_salaries = relationship("StaffSalaries", backref="payment_type", order_by="StaffSalaries.id")
    capital = relationship("CapitalExpenditure", backref="payment_type", order_by="CapitalExpenditure.id")
    deleted_payments = relationship("DeletedStudentPayments", backref="payment_type")
    deleted_teacher_salaries = relationship("DeletedTeacherSalaries", backref="payment_type")
    deleted_capital = relationship("DeletedCapitalExpenditure", backref="payment_type")
    deleted_overhead = relationship("DeletedOverhead", backref="payment_type")
    deleted_staff_salaries = relationship("DeletedStaffSalaries", backref="payment_type")
    old_id = Column(Integer)


class StudentPayments(db.Model):
    __tablename__ = "studentpayments"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    calendar_day = Column(Integer, ForeignKey('calendarday.id'))
    calendar_month = Column(Integer, ForeignKey("calendarmonth.id"))
    calendar_year = Column(Integer, ForeignKey("calendaryear.id"))
    payment_sum = Column(Integer)
    payment_type_id = Column(Integer, ForeignKey('paymenttypes.id'))
    account_period_id = Column(Integer, ForeignKey('accountingperiod.id'))
    payment = Column(Boolean)
    by_who = Column(Integer, ForeignKey("users.id"))
    old_id = Column(Integer)


class StudentCharity(db.Model):
    __tablename__ = "studentcharity"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    discount = Column(Integer)
    group_id = Column(Integer, ForeignKey('groups.id'))
    calendar_day = Column(Integer, ForeignKey('calendarday.id'))
    calendar_month = Column(Integer, ForeignKey("calendarmonth.id"))
    calendar_year = Column(Integer, ForeignKey("calendaryear.id"))
    account_period_id = Column(Integer, ForeignKey('accountingperiod.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    old_id = Column(Integer)


class BookPayments(db.Model):
    __tablename__ = "book_payments"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    calendar_day = Column(Integer, ForeignKey('calendarday.id'))
    calendar_month = Column(Integer, ForeignKey("calendarmonth.id"))
    calendar_year = Column(Integer, ForeignKey("calendaryear.id"))
    payment_sum = Column(Integer)
    account_period_id = Column(Integer, ForeignKey('accountingperiod.id'))


class DeletedBookPayments(db.Model):
    __tablename__ = "deleted_book_payments"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    calendar_day = Column(Integer, ForeignKey('calendarday.id'))
    calendar_month = Column(Integer, ForeignKey("calendarmonth.id"))
    calendar_year = Column(Integer, ForeignKey("calendaryear.id"))
    payment_sum = Column(Integer)
    account_period_id = Column(Integer, ForeignKey('accountingperiod.id'))


class DeletedStudentPayments(db.Model):
    __tablename__ = "deletedstudentpayments"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    calendar_day = Column(Integer, ForeignKey('calendarday.id'))
    calendar_month = Column(Integer, ForeignKey("calendarmonth.id"))
    calendar_year = Column(Integer, ForeignKey("calendaryear.id"))
    payment_sum = Column(Integer)
    payment_type_id = Column(Integer, ForeignKey('paymenttypes.id'))
    account_period_id = Column(Integer, ForeignKey('accountingperiod.id'))
    payment = Column(Boolean)
    deleted_date = Column(DateTime)
    reason = Column(String)


class TeacherSalaries(db.Model):
    __tablename__ = "teachersalaries"
    id = Column(Integer, primary_key=True)
    payment_sum = Column(Integer)
    reason = Column(String)
    payment_type_id = Column(Integer, ForeignKey('paymenttypes.id'))
    salary_location_id = Column(Integer, ForeignKey("teachersalary.id"))
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    calendar_day = Column(Integer, ForeignKey('calendarday.id'))
    calendar_month = Column(Integer, ForeignKey("calendarmonth.id"))
    calendar_year = Column(Integer, ForeignKey("calendaryear.id"))
    account_period_id = Column(Integer, ForeignKey('accountingperiod.id'))
    by_who = Column(Integer, ForeignKey("users.id"))
    old_id = Column(Integer)


class DeletedTeacherSalaries(db.Model):
    __tablename__ = "deletedteachersalaries"
    id = Column(Integer, primary_key=True)
    payment_sum = Column(Integer)
    reason = Column(String)
    payment_type_id = Column(Integer, ForeignKey('paymenttypes.id'))
    group_id = Column(Integer, ForeignKey("groups.id"))
    salary_location_id = Column(Integer, ForeignKey("teachersalary.id"))
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    calendar_day = Column(Integer, ForeignKey('calendarday.id'))
    calendar_month = Column(Integer, ForeignKey("calendarmonth.id"))
    calendar_year = Column(Integer, ForeignKey("calendaryear.id"))
    account_period_id = Column(Integer, ForeignKey('accountingperiod.id'))
    deleted_date = Column(DateTime)
    reason_deleted = Column(String)


class StaffSalaries(db.Model):
    __tablename__ = "staffsalaries"
    id = Column(Integer, primary_key=True)
    payment_sum = Column(Integer)
    reason = Column(String)
    payment_type_id = Column(Integer, ForeignKey('paymenttypes.id'))
    salary_id = Column(Integer, ForeignKey('staffsalary.id'))
    staff_id = Column(Integer, ForeignKey('staff.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    calendar_day = Column(Integer, ForeignKey('calendarday.id'))
    calendar_month = Column(Integer, ForeignKey("calendarmonth.id"))
    calendar_year = Column(Integer, ForeignKey("calendaryear.id"))
    profession_id = Column(Integer, ForeignKey("professions.id"))
    account_period_id = Column(Integer, ForeignKey('accountingperiod.id'))
    by_who = Column(Integer, ForeignKey("users.id"))
    old_id = Column(Integer)


class DeletedStaffSalaries(db.Model):
    __tablename__ = "deletedstaffsalaries"
    id = Column(Integer, primary_key=True)
    payment_sum = Column(Integer)
    reason = Column(String)
    payment_type_id = Column(Integer, ForeignKey('paymenttypes.id'))
    salary_id = Column(Integer, ForeignKey('staffsalary.id'))
    staff_id = Column(Integer, ForeignKey('staff.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    calendar_day = Column(Integer, ForeignKey('calendarday.id'))
    calendar_month = Column(Integer, ForeignKey("calendarmonth.id"))
    calendar_year = Column(Integer, ForeignKey("calendaryear.id"))
    profession_id = Column(Integer, ForeignKey("professions.id"))
    account_period_id = Column(Integer, ForeignKey('accountingperiod.id'))
    deleted_date = Column(DateTime)
    reason_deleted = Column(String)


class Overhead(db.Model):
    __tablename__ = "overhead"
    id = Column(Integer, primary_key=True)
    item_sum = Column(Integer)
    item_name = Column(String)
    payment_type_id = Column(Integer, ForeignKey('paymenttypes.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    calendar_day = Column(Integer, ForeignKey('calendarday.id'))
    calendar_month = Column(Integer, ForeignKey("calendarmonth.id"))
    calendar_year = Column(Integer, ForeignKey("calendaryear.id"))
    account_period_id = Column(Integer, ForeignKey('accountingperiod.id'))
    by_who = Column(Integer, ForeignKey("users.id"))
    old_id = Column(Integer)


class DeletedOverhead(db.Model):
    __tablename__ = "deletedoverhead"
    id = Column(Integer, primary_key=True)
    item_sum = Column(Integer)
    item_name = Column(String)
    payment_type_id = Column(Integer, ForeignKey('paymenttypes.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    calendar_day = Column(Integer, ForeignKey('calendarday.id'))
    calendar_month = Column(Integer, ForeignKey("calendarmonth.id"))
    calendar_year = Column(Integer, ForeignKey("calendaryear.id"))
    account_period_id = Column(Integer, ForeignKey('accountingperiod.id'))
    deleted_date = Column(DateTime)
    reason = Column(String)


class CapitalExpenditure(db.Model):
    __tablename__ = "capital_expenditure"
    id = Column(Integer, primary_key=True)
    item_sum = Column(Integer)
    item_name = Column(String)
    payment_type_id = Column(Integer, ForeignKey('paymenttypes.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    calendar_day = Column(Integer, ForeignKey('calendarday.id'))
    calendar_month = Column(Integer, ForeignKey("calendarmonth.id"))
    calendar_year = Column(Integer, ForeignKey("calendaryear.id"))
    account_period_id = Column(Integer, ForeignKey('accountingperiod.id'))
    by_who = Column(Integer, ForeignKey("users.id"))
    old_id = Column(Integer)


class DeletedCapitalExpenditure(db.Model):
    __tablename__ = "deleted_capital"
    id = Column(Integer, primary_key=True)
    item_sum = Column(Integer)
    item_name = Column(String)
    payment_type_id = Column(Integer, ForeignKey('paymenttypes.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    calendar_day = Column(Integer, ForeignKey('calendarday.id'))
    calendar_month = Column(Integer, ForeignKey("calendarmonth.id"))
    calendar_year = Column(Integer, ForeignKey("calendaryear.id"))
    account_period_id = Column(Integer, ForeignKey('accountingperiod.id'))
    deleted_date = Column(DateTime)
    reason = Column(String)


class AccountingInfo(db.Model):
    __tablename__ = "accountinginfo"
    id = Column(Integer, primary_key=True)
    calendar_month = Column(Integer, ForeignKey("calendarmonth.id"))
    calendar_year = Column(Integer, ForeignKey("calendaryear.id"))
    payment_type_id = Column(Integer, ForeignKey('paymenttypes.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    all_payments = Column(Integer, default=0)
    all_teacher_salaries = Column(Integer, default=0)
    all_staff_salaries = Column(Integer, default=0)
    all_overhead = Column(Integer, default=0)
    all_capital = Column(Integer, default=0)
    all_charity = Column(Integer, default=0)
    current_cash = Column(Integer, default=0)
    old_cash = Column(Integer, default=0)
    account_period_id = Column(Integer, ForeignKey('accountingperiod.id'))

    def add(self):
        db.session.add(self)
        db.session.commit()


class OtherInfo(db.Model):
    __tablename__ = "other_info"
    id = Column(Integer, primary_key=True)
    all_discount = Column(Integer, default=0)
    debtors_red_num = Column(Integer, default=0)
    debtors_yel_num = Column(Integer, default=0)
    registered_students = Column(Integer, default=0)
    account_period_id = Column(Integer, ForeignKey('accountingperiod.id'))
    calendar_month = Column(Integer, ForeignKey("calendarmonth.id"))
    calendar_year = Column(Integer, ForeignKey("calendaryear.id"))
    location_id = Column(Integer, ForeignKey('locations.id'))

    def add(self):
        db.session.add(self)
        db.session.commit()


class TeacherSalary(db.Model):
    __tablename__ = "teachersalary"
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    total_salary = Column(Integer)
    remaining_salary = Column(Integer)
    location_id = Column(Integer, ForeignKey('locations.id'))
    calendar_month = Column(Integer, ForeignKey("calendarmonth.id"))
    calendar_year = Column(Integer, ForeignKey("calendaryear.id"))
    status = Column(Boolean, default=False)

    teacher_cash = relationship('TeacherSalaries', backref="salary", order_by="TeacherSalaries.id")
    deleted_teacher_salary = relationship("DeletedTeacherSalaries", backref="salary",
                                          order_by="DeletedTeacherSalaries.id")
    taken_money = Column(Integer)
    old_id = Column(Integer)


class StaffSalary(db.Model):
    __tablename__ = "staffsalary"
    id = Column(Integer, primary_key=True)
    staff_id = Column(Integer, ForeignKey('staff.id'))
    total_salary = Column(Integer)
    remaining_salary = Column(Integer)
    location_id = Column(Integer, ForeignKey('locations.id'))
    calendar_month = Column(Integer, ForeignKey("calendarmonth.id"))
    calendar_year = Column(Integer, ForeignKey("calendaryear.id"))
    status = Column(Boolean, default=False)
    taken_money = Column(Integer)
    staff_given_salary = relationship("StaffSalaries", backref="staff_salary", order_by="StaffSalaries.id")
    staff_deleted_salary = relationship("DeletedStaffSalaries", backref="staff_salary",
                                        order_by="DeletedStaffSalaries.id")
    old_id = Column(Integer)
