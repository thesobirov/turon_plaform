from app import *
from backend.models.models import *
from backend.functions.functions import *


@app.route(f'{api}/login2', methods=['POST', 'GET'])
def login2():
    refreshdatas()

    calendar_year = CalendarYear.query.filter(CalendarYear.date == new_year()).first()

    calendar_month = CalendarMonth.query.filter(CalendarMonth.date == new_month(),
                                                CalendarMonth.year_id == calendar_year.id).first()
    calendar_day = CalendarDay.query.filter(CalendarDay.date == new_today(),
                                            CalendarDay.month_id == calendar_month.id).first()
    if request.method == "POST":

        json_request = request.get_json()
        username = json_request['username']
        password = json_request['password']
        username_sign = Users.query.filter_by(username=username).first()

        if username_sign and check_password_hash(username_sign.password, password):
            access_token = create_access_token(identity=username)
            # if username_sign.username == "metod":
            #     get_role = Roles.query.filter(Roles.type_role == "methodist").first()
            #     username_sign.role_id = get_role.id
            #     db.session.commit()
            # print(username_sign.role_info.type_role)
            if username_sign.username == "teststudent" or username_sign.username == "testteacher" or username_sign.username == "metod":
                return jsonify({
                    'class': True,
                    "access_token": access_token,
                })
            role = Roles.query.filter(Roles.id == username_sign.role_id).first()
            refresh_age(username_sign.id)
            return jsonify({
                "data": {
                    "username": username_sign.username,
                    "surname": username_sign.surname.title(),
                    "name": username_sign.name.title(),
                    "id": username_sign.id,
                    "access_token": access_token,
                    "role": role.role,
                    "refresh_token": create_refresh_token(identity=username),
                    "location_id": username_sign.location_id
                },
                "success": True
            })

        else:
            return jsonify({
                "success": False,
                "msg": "Username yoki parol noturg'i"
            })


@app.route(f'{api}/attendance_classroom/<int:group_id>')
@jwt_required()
def attendance_classroom(group_id):
    refreshdatas()
    calendar_year = CalendarYear.query.filter(CalendarYear.date == new_year()).first()

    calendar_month = CalendarMonth.query.filter(CalendarMonth.date == new_month(),
                                                CalendarMonth.year_id == calendar_year.id).first()
    calendar_day = CalendarDay.query.filter(CalendarDay.date == new_today(),
                                            CalendarDay.month_id == calendar_month.id).first()

    today = datetime.today()

    hour = datetime.strftime(today, "%Y/%m/%d/%H/%M")
    hour2 = datetime.strptime(hour, "%Y/%m/%d/%H/%M")

    students = db.session.query(Students).join(Students.group).options(contains_eager(Students.group)).filter(
        Groups.id == group_id).filter(or_(Students.ball_time <= hour2, Students.ball_time == None)).order_by('id').all()
    student_list = []
    for student in students:
        color = ""
        if student.debtor == 0:
            color = "green"
        elif student.debtor == 1:
            color = "yellow"
        elif student.debtor == 2:
            color = "red"
        elif student.debtor == 3:
            color = "navy"
        elif student.debtor == 4:
            color = "black"

        info = {
            "id": student.user.id,
            "name": student.user.name.title(),
            "surname": student.user.surname.title(),
            "money": student.user.balance,
            "active": False,
            "checked": False,
            "profile_photo": student.user.photo_profile,

            "typeChecked": "",
            "date": {},
            "scores": {},
            "money_type": color
        }
        student_list.append(info)
    group = Groups.query.filter(Groups.id == group_id).first()
    attendance_info = []
    for student in group.student:
        if group.subject.ball_number > 2:
            score = [
                {
                    "name": "Homework",
                    "activeBall": 0
                },
                {
                    "name": "activity",
                    "activeBall": 0
                },
                {
                    "name": "dictionary",
                    "activeBall": 0
                },
            ]
        else:
            score = [
                {
                    "name": "Homework",
                    "activeBall": 0
                },
                {
                    "name": "activity",
                    "activeBall": 0
                },
            ]
        att = {
            "id": student.user.id,
            "name": student.user.name,
            "surname": student.user.name,
            "balance": student.user.balance,
            "score": score,
            "type": ""
        }
        attendance_info.append(att)

    gr_functions = Group_Functions(group_id=group_id)
    gr_functions.update_list_balance()
    return jsonify({
        "date": old_current_dates(group_id),
        "users": attendance_info
    })


@app.route(f'{api}/make_attendance_classroom', methods=['POST'])
@jwt_required()
def make_attendance_classroom():
    refreshdatas()
    calendar_year = CalendarYear.query.filter(CalendarYear.date == new_year()).first()

    calendar_month = CalendarMonth.query.filter(CalendarMonth.date == new_month(),
                                                CalendarMonth.year_id == calendar_year.id).first()
    calendar_day = CalendarDay.query.filter(CalendarDay.date == new_today(),
                                            CalendarDay.month_id == calendar_month.id).first()

    month = str(datetime.now().month)
    current_year = datetime.now().year
    old_year = datetime.now().year - 1
    data = request.get_json()['data']
    day = data['day']
    get_month = data['month']

    if len(month) == 1:
        month = "0" + str(month)

    students = data['users']
    group_id = int(data['group_id'])
    group = Groups.query.filter(Groups.id == group_id).first()
    teacher = Teachers.query.filter(Teachers.id == group.teacher_id).first()
    errors = []
    for st in students:
        student = Students.query.filter(Students.user_id == st['id']).first()
        homework = 0
        dictionary = 0
        active = 0
        if student.debtor != 4:
            scores = st['score']
            for score in scores:
                if score['name'] == "Homework":
                    homework = score['activeBall']
                if score['name'] == "activity":
                    active = score['activeBall']
                if score['name'] == "dictionary":
                    dictionary = score['activeBall']

        type_attendance = st['type']

        if type_attendance == "yes":
            type_status = True
        else:
            type_status = False

        discount = StudentCharity.query.filter(StudentCharity.group_id == group_id,
                                               StudentCharity.student_id == student.id).first()
        if get_month == "12" and month == "01":
            current_year = old_year
        if not get_month:
            get_month = month

        date_day = str(current_year) + "-" + str(get_month) + "-" + str(day)
        date_month = str(current_year) + "-" + str(get_month)
        date_year = str(current_year)
        date_day = datetime.strptime(date_day, "%Y-%m-%d")
        date_month = datetime.strptime(date_month, "%Y-%m")
        date_year = datetime.strptime(date_year, "%Y")
        calendar_day = CalendarDay.query.filter(CalendarDay.date == date_day).first()
        calendar_month = CalendarMonth.query.filter(CalendarMonth.date == date_month).first()
        calendar_year = CalendarYear.query.filter(CalendarYear.date == date_year).first()
        if not calendar_year:
            calendar_year = CalendarYear(date=date_year)
            db.session.add(calendar_year)
            db.session.commit()
        if not calendar_month:
            calendar_month = CalendarMonth(date=date_month, year_id=calendar_year.id)
            db.session.add(calendar_month)
            db.session.commit()
        if not calendar_day:
            calendar_day = CalendarDay(date=date_day, month_id=calendar_month.id)
            db.session.add(calendar_day)
            db.session.commit()
        balance_with_discount = 0
        discount_per_day = 0
        discount_status = False
        if discount:
            balance_with_discount = round(
                (group.price / group.attendance_days) - (discount.discount / group.attendance_days))
            discount_per_day = round(discount.discount / group.attendance_days)
            discount_status = True
        today = datetime.today()
        hour = datetime.strftime(today, "%Y/%m/%d/%H/%M")
        hour2 = datetime.strptime(hour, "%Y/%m/%d/%H/%M")
        balance_per_day = round(group.price / group.attendance_days)
        salary_per_day = round(group.teacher_salary / group.attendance_days)
        ball_time = hour2 + timedelta(minutes=0)
        Students.query.filter(Students.id == student.id).update({"ball_time": ball_time})
        subject = Subjects.query.filter(Subjects.id == group.subject_id).first()
        attendance = Attendance.query.filter(Attendance.student_id == student.id,
                                             Attendance.calendar_year == calendar_year.id,
                                             Attendance.location_id == group.location_id,
                                             Attendance.calendar_month == calendar_month.id,
                                             Attendance.teacher_id == group.teacher_id,
                                             Attendance.group_id == group.id, Attendance.subject_id == subject.id,
                                             Attendance.course_id == group.course_type_id).first()

        if not attendance:
            attendance = Attendance(student_id=student.id, calendar_year=calendar_year.id,
                                    location_id=group.location_id,
                                    calendar_month=calendar_month.id, teacher_id=teacher.id, group_id=group_id,
                                    course_id=group.course_type_id, subject_id=subject.id)
            db.session.add(attendance)
            db.session.commit()

        exist_attendance = db.session.query(AttendanceDays).join(AttendanceDays.attendance).options(
            contains_eager(AttendanceDays.attendance)).filter(AttendanceDays.student_id == student.id,
                                                              AttendanceDays.calendar_day == calendar_day.id,
                                                              AttendanceDays.group_id == group_id,
                                                              Attendance.calendar_month == calendar_month.id,
                                                              Attendance.calendar_year == calendar_year.id).first()
        if exist_attendance:
            info = {
                "active": True,
                "message": f"{student.user.name} {student.user.surname} bu kunda davomat qilingan",
                "status": "danger"

            }
            errors.append(info)
            continue
        len_attendance = AttendanceDays.query.filter(AttendanceDays.student_id == student.id,
                                                     AttendanceDays.group_id == group_id,
                                                     AttendanceDays.location_id == group.location_id,
                                                     AttendanceDays.attendance_id == attendance.id,
                                                     ).count()

        if len_attendance >= group.attendance_days:
            info = {
                "active": True,
                "message": f"{student.user.name} {student.user.surname} bu oyda 13 kun dan ko'p davomat qilindi",
                "status": "danger"
            }
            errors.append(info)
            continue
        if not type_status:
            attendance_add = AttendanceDays(teacher_id=teacher.id, student_id=student.id,
                                            calendar_day=calendar_day.id, attendance_id=attendance.id,
                                            reason="",
                                            status=0, balance_per_day=balance_per_day,
                                            balance_with_discount=balance_with_discount,
                                            salary_per_day=salary_per_day, group_id=group_id,
                                            location_id=group.location_id,
                                            discount_per_day=discount_per_day,
                                            discount=discount_status)
            db.session.add(attendance_add)
            db.session.commit()
        elif homework == 0 and dictionary == 0 and active == 0:
            attendance_add = AttendanceDays(teacher_id=teacher.id, student_id=student.id,
                                            calendar_day=calendar_day.id, attendance_id=attendance.id,
                                            status=1, balance_per_day=balance_per_day,
                                            balance_with_discount=balance_with_discount,
                                            salary_per_day=salary_per_day, group_id=group_id,
                                            location_id=group.location_id, discount=discount_status,
                                            discount_per_day=discount_per_day)
            db.session.add(attendance_add)
            db.session.commit()
        else:
            average_ball = round((homework + dictionary + active) / subject.ball_number)
            attendance_add = AttendanceDays(student_id=student.id, attendance_id=attendance.id,
                                            dictionary=dictionary,
                                            calendar_day=calendar_day.id,
                                            status=2, balance_per_day=balance_per_day, homework=homework,
                                            average_ball=average_ball, activeness=active, group_id=group_id,
                                            location_id=group.location_id, teacher_id=teacher.id,
                                            balance_with_discount=balance_with_discount,
                                            salary_per_day=salary_per_day, discount=discount_status,
                                            discount_per_day=discount_per_day)
            db.session.add(attendance_add)
            db.session.commit()

        st_functions = Student_Functions(student_id=student.id)
        st_functions.update_debt()
        st_functions.update_extra_payment()
        st_functions.update_balance()
        # user = Users.query.filter(Users.user_id == student_id).first()
        # if user.balance >= student_get.combined_debt:
        #     black_balance = AttendanceDays(student_id=student_get.id, attendance_id=attendance.id,
        #                                    days_id=attendance_add.id,
        #                                     calendar_day=calendar_day.id,
        #                                     status=2, balance_per_day=balance_per_day,
        #                                      group_id=group_id,
        #                                     location_id=group.location_id, teacher_id=teacher.id,
        #                                     balance_with_discount=balance_with_discount,
        #                                     salary_per_day=salary_per_day, discount=discount_status,
        #                                     discount_per_day=discount_per_day)
        #     db.session.add(attendance_add)
        #     db.session.commit()

        salary_debt(student_id=student.id, group_id=group_id, attendance_id=attendance_add.id,
                    status_attendance=False, type_attendance="add")

        update_salary(teacher_id=teacher.user_id)
    if errors:
        status = "danger"
    else:
        status = "success"
    return jsonify({
        "message": "O'quvchilar davomat qilindi",
        "status": status,
        "errors": errors
    })
