from app import *
from backend.functions.functions import *
from backend.models.models import *
from flask_jwt_extended import *


@app.route(f'{api}/teacher_salary/<int:user_id>/<int:location_id>')
@jwt_required()
def teacher_salary(user_id, location_id):
    staff_salary_update()
    refreshdatas()
    calendar_year = CalendarYear.query.filter(CalendarYear.date == new_year()).first()

    calendar_month = CalendarMonth.query.filter(CalendarMonth.date == new_month(),
                                                CalendarMonth.year_id == calendar_year.id).first()
    calendar_day = CalendarDay.query.filter(CalendarDay.date == new_today(),
                                            CalendarDay.month_id == calendar_month.id).first()
    teacher = Teachers.query.filter(Teachers.user_id == user_id).first()
    staff = Staff.query.filter(Staff.user_id == user_id).first()

    if teacher:
        teacher_salaries = TeacherSalary.query.filter(TeacherSalary.teacher_id == teacher.id,
                                                      TeacherSalary.location_id == location_id).order_by(
            desc(TeacherSalary.id)).all()
        teacher_salary_list = []
        for salary in teacher_salaries:
            if salary.remaining_salary:
                residue = salary.remaining_salary
            elif salary.status:
                residue = 0
            else:
                residue = salary.total_salary
            info = {
                "id": salary.id,
                "salary": salary.total_salary,
                "residue": residue,
                "taken_salary": salary.taken_money,
                "date": salary.month.date.strftime("%Y-%m")
            }
            teacher_salary_list.append(info)
        return jsonify({
            "data": teacher_salary_list
        })
    else:
        staff_salaries = StaffSalary.query.filter(StaffSalary.staff_id == staff.id,
                                                  StaffSalary.location_id == location_id).order_by(
            desc(StaffSalary.id)).all()
        teacher_salary_list = []

        for salary in staff_salaries:
            if salary.remaining_salary:
                residue = salary.remaining_salary
            elif salary.status:
                residue = 0
            else:
                residue = salary.total_salary
            info = {
                "id": salary.id,
                "salary": salary.total_salary,
                "residue": residue,
                "taken_salary": salary.taken_money,
                "date": salary.month.date.strftime("%Y-%m")
            }
            teacher_salary_list.append(info)

        return jsonify({
            "data": teacher_salary_list
        })


@app.route(f'{api}/teacher_salary_inside/<int:salary_id>/<int:user_id>')
@jwt_required()
def teacher_salary_inside(salary_id, user_id):
    staff_salary_update()
    refreshdatas()
    calendar_year = CalendarYear.query.filter(CalendarYear.date == new_year()).first()

    calendar_month = CalendarMonth.query.filter(CalendarMonth.date == new_month(),
                                                CalendarMonth.year_id == calendar_year.id).first()
    calendar_day = CalendarDay.query.filter(CalendarDay.date == new_today(),
                                            CalendarDay.month_id == calendar_month.id).first()
    teacher = Teachers.query.filter(Teachers.user_id == user_id).first()
    staff = Staff.query.filter(Staff.user_id == user_id).first()
    result = 0
    if teacher:
        salary = TeacherSalary.query.filter(TeacherSalary.id == salary_id).first()

        teacher_salaries = TeacherSalaries.query.filter(TeacherSalaries.salary_location_id == salary_id).order_by(
            TeacherSalaries.id).all()
        list_salaries = []
        all_salaries = 0
        for sal in teacher_salaries:
            all_salaries += sal.payment_sum
            info = {
                "id": sal.id,
                "salary": sal.payment_sum,
                "reason": sal.reason,
                "payment_type": sal.payment_type.name,
                "date": sal.day.date.strftime("%Y-%m-%d")
            }
            list_salaries.append(info)

        result = salary.total_salary - all_salaries
        TeacherSalary.query.filter(TeacherSalary.id == salary_id).update({
            "remaining_salary": result,
            "taken_money": all_salaries
        })
        db.session.commit()


    else:
        salary = StaffSalary.query.filter(StaffSalary.id == salary_id).first()

        staff_salaries = StaffSalaries.query.filter(StaffSalaries.salary_id == salary_id).order_by(
            StaffSalaries.id).all()
        list_salaries = []
        for sal in staff_salaries:
            info = {
                "id": sal.id,
                "salary": sal.payment_sum,
                "reason": sal.reason,
                "payment_type": sal.payment_type.name,
                "date": sal.day.date.strftime("%Y-%m-%d")
            }
            list_salaries.append(info)
    if salary.remaining_salary:
        exist_money = salary.remaining_salary
    else:
        exist_money = salary.total_salary
    return jsonify({
        "data": {
            "salary": salary.total_salary,
            "residue": salary.remaining_salary,
            "taken_salary": salary.taken_money,
            "exist_salary": exist_money,
            "month": salary.month.date.strftime("%Y-%m"),
            "data": list_salaries,
            "error_salary": result
        }
    })


@app.route(f'{api}/teacher_salary_deleted_inside/<int:salary_id>/<int:user_id>')
@jwt_required()
def teacher_salary_deleted_inside(salary_id, user_id):
    refreshdatas()
    calendar_year = CalendarYear.query.filter(CalendarYear.date == new_year()).first()

    calendar_month = CalendarMonth.query.filter(CalendarMonth.date == new_month(),
                                                CalendarMonth.year_id == calendar_year.id).first()
    calendar_day = CalendarDay.query.filter(CalendarDay.date == new_today(),
                                            CalendarDay.month_id == calendar_month.id).first()
    teacher = Teachers.query.filter(Teachers.user_id == user_id).first()
    staff = Staff.query.filter(Staff.user_id == user_id).first()
    if teacher:
        salary = TeacherSalary.query.filter(TeacherSalary.id == salary_id).first()

        teacher_salarie = DeletedTeacherSalaries.query.filter(
            DeletedTeacherSalaries.salary_location_id == salary_id).order_by(
            DeletedTeacherSalaries.id).all()
        list_salaries = []
        for sal in teacher_salarie:
            info = {
                "id": sal.id,
                "salary": sal.payment_sum,
                "reason": sal.reason_deleted,
                "payment_type": sal.payment_type.name,
                "date": sal.day.date.strftime("%Y-%m-%d")
            }
            list_salaries.append(info)
    else:
        salary = StaffSalary.query.filter(StaffSalary.id == salary_id).first()

        staff_salaries = DeletedStaffSalaries.query.filter(DeletedStaffSalaries.salary_id == salary_id).order_by(
            DeletedStaffSalaries.id).all()
        list_salaries = []
        for sal in staff_salaries:
            info = {
                "id": sal.id,
                "salary": sal.payment_sum,
                "reason": sal.reason_deleted,
                "payment_type": sal.payment_type.name,
                "date": sal.day.date.strftime("%Y-%m-%d")
            }
            list_salaries.append(info)
    return jsonify({
        "data": {
            "salary": salary.total_salary,
            "residue": salary.remaining_salary,
            "taken_salary": salary.taken_money,
            "month": salary.month.date.strftime("%Y-%m"),
            "data": list_salaries
        }
    })


@app.route(f'{api}/salary_give_teacher/<int:salary_id>/<int:user_id>', methods=['POST'])
@jwt_required()
def salary_give_teacher(salary_id, user_id):
    refreshdatas()
    calendar_year = CalendarYear.query.filter(CalendarYear.date == new_year()).first()
    calendar_month = CalendarMonth.query.filter(CalendarMonth.date == new_month(),
                                                CalendarMonth.year_id == calendar_year.id).first()
    calendar_day = CalendarDay.query.filter(CalendarDay.date == new_today(),
                                            CalendarDay.month_id == calendar_month.id).first()
    teacher = Teachers.query.filter(Teachers.user_id == user_id).first()
    staff = Staff.query.filter(Staff.user_id == user_id).first()
    teacher_salary = int(request.get_json().get('payment'))
    reason = request.get_json().get('reason')
    payment_type = int(request.get_json().get('typePayment'))
    payment_type_id = PaymentTypes.query.filter(PaymentTypes.id == payment_type).first()
    accounting_period = db.session.query(AccountingPeriod).join(AccountingPeriod.month).options(
        contains_eager(AccountingPeriod.month)).order_by(desc(CalendarMonth.id)).first()
    if teacher:
        teacher_cash = TeacherSalary.query.filter(TeacherSalary.id == salary_id).first()
        if teacher_cash.remaining_salary:
            total_salary = teacher_cash.remaining_salary
        else:
            total_salary = teacher_cash.total_salary
        if teacher_salary > total_salary:
            return jsonify({
                "success": False,
                "msg": "Kiritilgan summa miqdori umumiy oylik miqdoridan kop"
            })
        else:
            add = TeacherSalaries(payment_sum=teacher_salary, reason=reason, payment_type_id=payment_type_id.id,
                                  teacher_id=teacher_cash.teacher_id, location_id=teacher_cash.location_id,
                                  calendar_month=calendar_month.id, calendar_day=calendar_day.id,
                                  calendar_year=calendar_year.id, account_period_id=accounting_period.id,
                                  salary_location_id=teacher_cash.id)
            db.session.add(add)
            db.session.commit()

            if not teacher_cash.remaining_salary:
                result = -teacher_cash.total_salary + teacher_salary
            else:
                result = -teacher_cash.remaining_salary + teacher_salary
            if teacher_cash.taken_money:
                taken_money = teacher_cash.taken_money + teacher_salary
            else:
                taken_money = teacher_salary

            if result < 0:
                remaining_salary = abs(result)
                TeacherSalary.query.filter(TeacherSalary.id == salary_id).update(
                    {'remaining_salary': remaining_salary, 'taken_money': taken_money})
                db.session.commit()
            else:
                TeacherSalary.query.filter(TeacherSalary.id == salary_id).update(
                    {'remaining_salary': 0, "taken_money": teacher_cash.total_salary, 'status': True})
                db.session.commit()
            update_salary(teacher_id=user_id)
    else:
        staff_cash = StaffSalary.query.filter(StaffSalary.id == salary_id).first()
        if staff_cash.remaining_salary:
            total_salary = staff_cash.remaining_salary
        else:
            total_salary = staff_cash.total_salary
        if teacher_salary > total_salary:
            return jsonify({
                "success": False,
                "msg": "Kiritilgan summa miqdori umumiy oylik miqdoridan kop"
            })
        else:
            add = StaffSalaries(payment_sum=teacher_salary, reason=reason, payment_type_id=payment_type_id.id,
                                staff_id=staff_cash.staff_id, location_id=staff_cash.location_id,
                                calendar_month=calendar_month.id, calendar_day=calendar_day.id,
                                calendar_year=calendar_year.id, account_period_id=accounting_period.id,
                                salary_id=staff_cash.id, profession_id=staff.profession_id)
            db.session.add(add)
            db.session.commit()
            if not staff_cash.remaining_salary:
                result = -staff_cash.total_salary + teacher_salary
            else:
                result = -staff_cash.remaining_salary + teacher_salary
            if staff_cash.taken_money:
                taken_money = staff_cash.taken_money + teacher_salary
            else:
                taken_money = teacher_salary

            if result < 0:
                remaining_salary = abs(result)
                StaffSalary.query.filter(StaffSalary.id == salary_id).update(
                    {'remaining_salary': remaining_salary, 'taken_money': taken_money})
                db.session.commit()
            else:
                StaffSalary.query.filter(StaffSalary.id == salary_id).update(
                    {'remaining_salary': 0, "taken_money": staff_cash.total_salary, 'status': True})
                db.session.commit()

    return jsonify({
        "success": True,
        "msg": "Oylik berildi"
    })


@app.route(f'{api}/delete_salary_teacher/<int:salary_id>/<int:user_id>', methods=['POST'])
@jwt_required()
def delete_salary_teacher(salary_id, user_id):
    reason = request.get_json()['otherReason']
    teacher = Teachers.query.filter(Teachers.user_id == user_id).first()
    staff = Staff.query.filter(Staff.user_id == user_id).first()
    refreshdatas()
    calendar_year = CalendarYear.query.filter(CalendarYear.date == new_year()).first()

    calendar_month = CalendarMonth.query.filter(CalendarMonth.date == new_month(),
                                                CalendarMonth.year_id == calendar_year.id).first()
    calendar_day = CalendarDay.query.filter(CalendarDay.date == new_today(),
                                            CalendarDay.month_id == calendar_month.id).first()
    if teacher:

        teacher_salary = TeacherSalaries.query.filter(TeacherSalaries.id == salary_id).first()
        teacher = Teachers.query.filter(Teachers.id == teacher_salary.teacher_id).first()
        teacher_cash = TeacherSalary.query.filter(TeacherSalary.id == teacher_salary.salary_location_id,
                                                  TeacherSalary.teacher_id == teacher.id,
                                                  TeacherSalary.location_id == teacher_salary.location_id,
                                                  TeacherSalary.taken_money != None).first()
        result = teacher_cash.taken_money - teacher_salary.payment_sum

        remaining_salary = teacher_cash.total_salary - result
        if remaining_salary == teacher_cash.total_salary:
            remaining_salary = 0

        TeacherSalary.query.filter(TeacherSalary.id == teacher_cash.id).update(
            {"taken_money": result, "remaining_salary": remaining_salary, "status": False})
        db.session.commit()

        deleted_salary = DeletedTeacherSalaries(payment_sum=teacher_salary.payment_sum, reason=teacher_salary.reason,
                                                payment_type_id=teacher_salary.payment_type_id,
                                                teacher_id=teacher_cash.teacher_id, reason_deleted=reason,
                                                location_id=teacher_cash.location_id,
                                                calendar_month=teacher_salary.calendar_month,
                                                calendar_day=teacher_salary.calendar_day,
                                                calendar_year=teacher_salary.calendar_year,
                                                account_period_id=teacher_salary.account_period_id,
                                                salary_location_id=teacher_salary.salary_location_id,
                                                deleted_date=calendar_day.date)
        db.session.add(deleted_salary)
        db.session.commit()
        db.session.delete(teacher_salary)
        db.session.commit()
        update_salary(teacher_id=teacher.user_id)
    else:
        staff_salary = StaffSalaries.query.filter(StaffSalaries.id == salary_id).first()
        staff_cash = StaffSalary.query.filter(StaffSalary.id == staff_salary.salary_id,
                                              StaffSalary.staff_id == staff.id,
                                              StaffSalary.location_id == staff_salary.location_id,
                                              StaffSalary.taken_money != None).first()
        result = staff_cash.taken_money - staff_salary.payment_sum

        remaining_salary = staff_cash.total_salary - result
        if remaining_salary == staff_cash.total_salary:
            remaining_salary = 0

        StaffSalary.query.filter(StaffSalary.id == staff_cash.id).update(
            {"taken_money": result, "remaining_salary": remaining_salary, "status": False})
        db.session.commit()
        deleted_salary = DeletedStaffSalaries(payment_sum=staff_salary.payment_sum, reason=staff_salary.reason,
                                              payment_type_id=staff_salary.payment_type_id,
                                              staff_id=staff_salary.staff_id, reason_deleted=reason,
                                              location_id=staff_salary.location_id,
                                              calendar_month=staff_salary.calendar_month,
                                              calendar_day=staff_salary.calendar_day,
                                              calendar_year=staff_salary.calendar_year,
                                              account_period_id=staff_salary.account_period_id,
                                              salary_id=staff_cash.id,
                                              deleted_date=calendar_day.date,
                                              profession_id=staff_salary.profession_id)
        db.session.add(deleted_salary)
        db.session.commit()
        db.session.delete(staff_salary)
        db.session.commit()

    return jsonify({
        "success": True,
        "msg": "Oylik o'chirildi"
    })


@app.route(f'{api}/change_teacher_salary/<int:salary_id>/<type_id>/<int:user_id>')
@jwt_required()
def change_teacher_salary(salary_id, type_id, user_id):
    refreshdatas()
    calendar_year = CalendarYear.query.filter(CalendarYear.date == new_year()).first()

    calendar_month = CalendarMonth.query.filter(CalendarMonth.date == new_month(),
                                                CalendarMonth.year_id == calendar_year.id).first()
    calendar_day = CalendarDay.query.filter(CalendarDay.date == new_today(),
                                            CalendarDay.month_id == calendar_month.id).first()
    teacher = Teachers.query.filter(Teachers.user_id == user_id).first()
    staff = Staff.query.filter(Staff.user_id == user_id).first()
    payment_type = PaymentTypes.query.filter(PaymentTypes.name == type_id).first()
    if teacher:
        TeacherSalaries.query.filter(TeacherSalaries.id == salary_id).update({
            "payment_type_id": payment_type.id
        })
        db.session.commit()

    elif staff:
        StaffSalaries.query.filter(StaffSalaries.id == salary_id).update({
            "payment_type_id": payment_type.id
        })
        db.session.commit()

    else:

        StudentPayments.query.filter(StudentPayments.id == salary_id).update({
            "payment_type_id": payment_type.id
        })
        db.session.commit()

    return jsonify({
        "success": True,
        "msg": "Oylik qiymat turi o'zgartirildi"
    })


@app.route(f'{api}/set_salary/<int:user_id>', methods=['POST'])
@jwt_required()
def set_salary(user_id):
    refreshdatas()
    calendar_year = CalendarYear.query.filter(CalendarYear.date == new_year()).first()

    calendar_month = CalendarMonth.query.filter(CalendarMonth.date == new_month(),
                                                CalendarMonth.year_id == calendar_year.id).first()
    calendar_day = CalendarDay.query.filter(CalendarDay.date == new_today(),
                                            CalendarDay.month_id == calendar_month.id).first()
    salary = int(request.get_json()['salary'])
    Staff.query.filter(Staff.user_id == user_id).update({
        "salary": salary
    })
    db.session.commit()
    return jsonify({
        "success": True,
        "msg": "Oylik belgilandi"
    })


@app.route(f'{api}/employees/<int:location_id>')
@jwt_required()
def employees(location_id):
    refreshdatas()
    calendar_year = CalendarYear.query.filter(CalendarYear.date == new_year()).first()

    calendar_month = CalendarMonth.query.filter(CalendarMonth.date == new_month(),
                                                CalendarMonth.year_id == calendar_year.id).first()
    calendar_day = CalendarDay.query.filter(CalendarDay.date == new_today(),
                                            CalendarDay.month_id == calendar_month.id).first()
    staff_salary_update()
    list_staff = []
    staffs = db.session.query(Staff).join(Staff.user).options(contains_eager(Staff.user)).filter(
        Users.location_id == location_id).order_by(Users.id).all()
    for staff in staffs:
        info = {
            "id": staff.user.id,
            "name": staff.user.name.title(),
            "surname": staff.user.surname.title(),
            "username": staff.user.username,
            "language": staff.user.language.name,
            "age": staff.user.age,
            "reg_date": staff.user.day.date.strftime("%Y-%m-%d"),
            "job": staff.profession.name,
            "role": staff.user.role_info.role
        }
        list_staff.append(info)
    return jsonify({
        "data": list_staff
    })
