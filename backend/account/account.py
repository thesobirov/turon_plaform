from app import *
from backend.settings.settings import *
from datetime import datetime
from flask_paginate import Pagination, get_page_args


def delete_payments():
    deleted_overheads = DeleteDOverhead.query.all()
    for deleted_overhead in deleted_overheads:
        dl_overhead = DeleteDOverhead.query.filter(DeleteDOverhead.id == deleted_overhead.id).first()
        db.session.delete(dl_overhead)
        db.session.commit()
    overheads = Overhead.query.all()
    for overhead in overheads:
        dl_overhead = Overhead.query.filter(Overhead.id == overhead.id).first()
        db.session.delete(dl_overhead)
        db.session.commit()
    student_payments_in_months = StudentPaymentsInMonth.query.all()
    for student_payments_in_month in student_payments_in_months:
        dl_overhead = StudentPaymentsInMonth.query.filter(
            StudentPaymentsInMonth.id == student_payments_in_month.id).first()
        db.session.delete(dl_overhead)
        db.session.commit()
    student_month_payments = StudentMonthPayments.query.all()
    for student_month_payment in student_month_payments:
        dl_overhead = StudentMonthPayments.query.filter(StudentMonthPayments.id == student_month_payment.id).first()
        db.session.delete(dl_overhead)
        db.session.commit()
    deleted_capital_expenses = DeleteDCapitalExpenses.query.all()
    for deleted_capital_expense in deleted_capital_expenses:
        dl_overhead = DeleteDCapitalExpenses.query.filter(DeleteDCapitalExpenses.id == deleted_capital_expense.id).first()
        db.session.delete(dl_overhead)
        db.session.commit()
    capital_expenses = CapitalExpenses.query.all()
    for capital_expense in capital_expenses:
        dl_overhead = CapitalExpenses.query.filter(CapitalExpenses.id == capital_expense.id).first()
        db.session.delete(dl_overhead)
        db.session.commit()
    deleted_catering_overheads = DeleteDCateringOverhead.query.all()
    for deleted_catering_overhead in deleted_catering_overheads:
        dl_overhead = DeleteDCateringOverhead.query.filter(DeleteDCateringOverhead.id == deleted_catering_overhead.id).first()
        db.session.delete(dl_overhead)
        db.session.commit()
    catering_overheads = CateringOverhead.query.all()
    for catering_overhead in catering_overheads:
        dl_overhead = CateringOverhead.query.filter(CateringOverhead.id == catering_overhead.id).first()
        db.session.delete(dl_overhead)
        db.session.commit()
    deleted_marketing_overheads = DeleteDMarketingOverhead.query.all()
    for deleted_marketing_overhead in deleted_marketing_overheads:
        dl_overhead = CateringOverhead.query.filter(DeleteDMarketingOverhead.id == deleted_marketing_overhead.id).first()
        db.session.delete(dl_overhead)
        db.session.commit()
    marketing_overheads = MarketingOverhead.query.all()
    for marketing_overhead in marketing_overheads:
        dl_overhead = MarketingOverhead.query.filter(MarketingOverhead.id == marketing_overhead.id).first()
        db.session.delete(dl_overhead)
        db.session.commit()
    deleted_stationaries = DeleteDStationary.query.all()
    for deleted_stationary in deleted_stationaries:
        dl_overhead = DeleteDStationary.query.filter(DeleteDStationary.id == deleted_stationary.id).first()
        db.session.delete(dl_overhead)
        db.session.commit()
    stationaries = Stationary.query.all()
    for stationary in stationaries:
        dl_overhead = Stationary.query.filter(Stationary.id == stationary.id).first()
        db.session.delete(dl_overhead)
        db.session.commit()

# @app.route('/collection', defaults={'type_request': "p"})
# @app.route('/collection/<type_request>/')
# def collection(type_request):
#     """
#     Front endga malumot yuboradigan app route
#     :return:
#     """
#     # delete_payments()
#     error = check_session()
#     # if error:
#     #     return redirect(url_for('home'))
#     user = User.query.filter(User.id == 1).first()
#     about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
#     about_id = 0
#     about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
#     news = TypeInfo.query.filter(TypeInfo.id == 2).first()
#     jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
#     about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
#     cost_o_all = Overhead.query.filter(Overhead.deleted_over_head == None).order_by(Overhead.id).all()
#     cost_c_all = CateringOverhead.query.filter(CateringOverhead.deleted_catering_overhead == None).order_by(
#         CateringOverhead.id).all()
#     cost_m_all = MarketingOverhead.query.filter(MarketingOverhead.deleted_marketing_overhead == None).order_by(
#         MarketingOverhead.id).all()
#     student_pay_all = StudentPaymentsInMonth.query.order_by(StudentPaymentsInMonth.id).all()
#     teacher_sal_all = GivenSalariesInMonth.query.order_by(GivenSalariesInMonth.id).all()
#     worker_sal_all = WorkerSalaryInDay.query.filter(WorkerSalaryInDay.deleted_worker_salary_inDay == None).order_by(
#         WorkerSalaryInDay.id).all()
#
#     balance_sp = 0
#     balance_ts = 0
#     balance_ws = 0
#     balance_co = 0
#
#     balance_p = 0
#     balance_t = 0
#     balance_w = 0
#     balance_o = 0
#     balance_c = 0
#     balance_m = 0
#
#     for payment in student_pay_all:
#         balance_p += int(payment.payed)
#     for payment in teacher_sal_all:
#
#         # print(payment)
#         balance_ts += int(payment.given_salary)
#     for payment in worker_sal_all:
#         balance_ws += int(payment.salary)
#     for payment in cost_all:
#         balance_co += int(payment.payed)
#
#     balance = balance_sp - balance_ts - balance_ws - balance_co
#     if type_request == 'sp' or type_request == '':
#
#         balance_t += int(payment.given_salary)
#     for payment in worker_sal_all:
#         balance_w += int(payment.salary)
#     for payment in cost_o_all:
#         balance_o += int(payment.payed)
#     for payment in cost_c_all:
#         balance_c += int(payment.payed)
#     for payment in cost_m_all:
#         balance_m += int(payment.payed)
#     balance = balance_p - balance_t - balance_w - balance_o - balance_c - balance_m
#     if type_request == 'p' or type_request == '':
#
#         payments = student_pay_all
#     elif type_request == 't':
#         payments = teacher_sal_all
#     elif type_request == 'w':
#         payments = worker_sal_all
#     elif type_request == 'o':
#         payments = cost_o_all
#     elif type_request == 'c':
#         payments = cost_c_all
#     elif type_request == 'm':
#         payments = cost_m_all
#     else:
#         payments = []
#         balance = 0
#     return render_template('account/account.html', balance_p=balance_p, balance_t=balance_t,
#                            balance_w=balance_w, balance_o=balance_o,
#                            balance_c=balance_c, balance_m=balance_m,
#                            type_request=type_request, payments=payments,
#                            user=user, about_us=about_us,
#                            about_id=about_id, news=news,
#                            jobs=jobs, about=about, balance=balance)


# mani variantim
# @app.route('/collection', defaults={'type_request': "p"})
# @app.route('/collection/<type_request>/')
# def collection(type_request):
#     """
#     Front endga malumot yuboradigan app route
#     :return:
#     """
#     # delete_payments()
#     error = check_session()
#     # if error:
#     #     return redirect(url_for('home'))
#     user = User.query.filter(User.id == 1).first()
#     about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
#     about_id = 0
#     about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
#     news = TypeInfo.query.filter(TypeInfo.id == 2).first()
#     jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
#     about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
#     cost_o_all = Overhead.query.filter(Overhead.deleted_over_head == None).order_by(Overhead.id).all()
#     cost_c_all = CateringOverhead.query.filter(CateringOverhead.deleted_catering_overhead == None).order_by(
#         CateringOverhead.id).all()
#     cost_m_all = MarketingOverhead.query.filter(MarketingOverhead.deleted_marketing_overhead == None).order_by(
#         MarketingOverhead.id).all()
#     student_pay_all = StudentPaymentsInMonth.query.order_by(StudentPaymentsInMonth.id).all()
#     teacher_sal_all = GivenSalariesInMonth.query.order_by(GivenSalariesInMonth.id).all()
#     worker_sal_all = WorkerSalaryInDay.query.filter(WorkerSalaryInDay.deleted_worker_salary_inDay == None).order_by(
#         WorkerSalaryInDay.id).all()
#
#     balance_sp = 0
#     balance_ts = 0
#     balance_ws = 0
#     balance_co = 0
#
#     balance_p = 0
#     balance_t = 0
#     balance_w = 0
#     balance_o = 0
#     balance_c = 0
#     balance_m = 0
#
#     for payment in student_pay_all:
#         balance_p += int(payment.payed)
#     for payment in teacher_sal_all:
#
#         # print(payment)
#         balance_ts += int(payment.given_salary)
#     for payment in worker_sal_all:
#         balance_ws += int(payment.salary)
#     for payment in cost_all:
#         balance_co += int(payment.payed)
#
#     balance = balance_sp - balance_ts - balance_ws - balance_co
#     if type_request == 'sp' or type_request == '':
#
#         balance_t += int(payment.given_salary)
#     for payment in worker_sal_all:
#         balance_w += int(payment.salary)
#     for payment in cost_o_all:
#         balance_o += int(payment.payed)
#     for payment in cost_c_all:
#         balance_c += int(payment.payed)
#     for payment in cost_m_all:
#         balance_m += int(payment.payed)
#     balance = balance_p - balance_t - balance_w - balance_o - balance_c - balance_m
#     if type_request == 'p' or type_request == '':
#
#         payments = student_pay_all
#     elif type_request == 't':
#         payments = teacher_sal_all
#     elif type_request == 'w':
#         payments = worker_sal_all
#     elif type_request == 'o':
#         payments = cost_o_all
#     elif type_request == 'c':
#         payments = cost_c_all
#     elif type_request == 'm':
#         payments = cost_m_all
#     else:
#         payments = []
#         balance = 0
#     return render_template('account/account.html', balance_p=balance_p, balance_t=balance_t,
#                            balance_w=balance_w, balance_o=balance_o,
#                            balance_c=balance_c, balance_m=balance_m,
#                            type_request=type_request, payments=payments,
#                            user=user, about_us=about_us,
#                            about_id=about_id, news=news,
#                            jobs=jobs, about=about, balance=balance)


def delete_function():
    deleted_given_salary_in_months = DeletedGivenSalaryInMonth.query.all()
    for dl_given_salary in deleted_given_salary_in_months:
        filter_info = DeletedGivenSalaryInMonth.query.filter(DeletedGivenSalaryInMonth.id == dl_given_salary.id).first()
        db.session.delete(filter_info)
        db.session.commit()
    given_salary_in_months = GivenSalariesInMonth.query.all()
    for dl_given_salary in given_salary_in_months:
        filter_info = GivenSalariesInMonth.query.filter(GivenSalariesInMonth.id == dl_given_salary.id).first()
        db.session.delete(filter_info)
        db.session.commit()


@app.route('/collection', defaults={'type_request': "p"})
@app.route('/collection/<type_request>/')
def collection(type_request):
    """
    Front endga malumot yuboradigan app route
    :return:
    """
    # delete_payments()
    # delete_function()
    # delete_payments()
    # error = check_session()
    # if error:
    #     return redirect(url_for('home'))
    user = User.query.filter(User.id == 1).first()
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    cost_o_all = Overhead.query.filter(Overhead.deleted_over_head == None).order_by(Overhead.id).all()
    cost_s_all = Stationary.query.filter(Stationary.deleted_stationary == None).order_by(Stationary.id).all()
    cost_c_all = CateringOverhead.query.filter(CateringOverhead.deleted_catering_overhead == None).order_by(
        CateringOverhead.id).all()
    cost_m_all = MarketingOverhead.query.filter(MarketingOverhead.deleted_marketing_overhead == None).order_by(
        MarketingOverhead.id).all()
    cost_e_all = CapitalExpenses.query.filter(CapitalExpenses.deleted_capital_expenses == None).order_by(
        CapitalExpenses.id).all()
    student_pay_all = StudentPaymentsInMonth.query.order_by(StudentPaymentsInMonth.id).all()
    student_pay_all_by_month = db.session.query(StudentPaymentsInMonth).join(
        StudentPaymentsInMonth.student_month_payments).options(
        contains_eager(StudentPaymentsInMonth.student_month_payments)).order_by(StudentMonthPayments.month).all()
    teacher_sal_all = GivenSalariesInMonth.query.filter(
        GivenSalariesInMonth.deleted_given_salaries_in_month == None).order_by(GivenSalariesInMonth.id).all()
    worker_sal_all = WorkerSalaryInDay.query.filter(WorkerSalaryInDay.deleted_worker_salary_inDay == None).order_by(
        WorkerSalaryInDay.id).all()
    balance_p = 0
    balance_t = 0
    balance_w = 0
    balance_o = 0
    balance_c = 0
    balance_s = 0
    balance_m = 0
    balance_e = 0
    for payment in student_pay_all:
        balance_p += int(payment.payed)
    for payment in teacher_sal_all:
        balance_t += int(payment.given_salary)
    for payment in worker_sal_all:
        balance_w += int(payment.salary)
    for payment in cost_o_all:
        balance_o += int(payment.payed)
    for payment in cost_c_all:
        balance_c += int(payment.payed)
    for payment in cost_m_all:
        balance_m += int(payment.payed)
    for payment in cost_s_all:
        balance_s += int(payment.payed)
    for payment in cost_e_all:
        balance_e += int(payment.payed)
    balance = balance_p - balance_t - balance_w - balance_o - balance_c - balance_m - balance_s - balance_e
    if type_request == 'p' or type_request == '':
        payments = student_pay_all
    elif type_request == 't':
        payments = teacher_sal_all
    elif type_request == 'w':
        payments = worker_sal_all
    elif type_request == 'o':
        payments = cost_o_all
    elif type_request == 'c':
        payments = cost_c_all
    elif type_request == 'm':
        payments = cost_m_all
    elif type_request == 's':
        payments = cost_s_all

    elif type_request == 'by':
        payments = student_pay_all_by_month

    elif type_request == 'e':
        payments = cost_e_all

    else:
        payments = []
        balance = 0
    if type_request == 't':
        for page in payments:
            print(page.teacher_salary.teacher.user.name)
    return render_template('account/account.html', balance_p=balance_p, balance_t=balance_t,
                           balance_w=balance_w, balance_o=balance_o, balance_s=balance_s, balance_e=balance_e,
                           balance_c=balance_c, balance_m=balance_m,
                           type_request=type_request, payments=payments,
                           user=user, about_us=about_us,
                           about_id=about_id, news=news,
                           jobs=jobs, about=about, balance=balance)


@app.route('/search', methods=["POST"])
def search():
    """
    Kunlar bo'yicha qidiarigan app route
    :return:
    """
    input_one = request.get_json()["input_one"]
    input_two = request.get_json()["input_two"]
    type_request = request.get_json()["type_request"]
    button = request.get_json()["button"]
    if button == 'Bank':
        button_number = 1
    elif button == 'Click':
        button_number = 2
    elif button == 'Cash':
        button_number = 3
    else:
        button_number = 0
    payment_all = StudentPaymentsInMonth.query.order_by(StudentPaymentsInMonth.id).all()
    cost_o_all = Overhead.query.filter(Overhead.deleted_over_head == None).order_by(Overhead.id).all()
    cost_c_all = CateringOverhead.query.filter(CateringOverhead.deleted_catering_overhead == None).order_by(
        CateringOverhead.id).all()
    cost_s_all = Stationary.query.filter(Stationary.deleted_stationary == None).order_by(
        Stationary.id).all()
    cost_e_all = CapitalExpenses.query.filter(CapitalExpenses.deleted_capital_expenses == None).order_by(
        CapitalExpenses.id).all()
    cost_m_all = MarketingOverhead.query.filter(MarketingOverhead.deleted_marketing_overhead == None).order_by(
        MarketingOverhead.id).all()
    worker_salary_all = WorkerSalaryInDay.query.filter(WorkerSalaryInDay.deleted_worker_salary_inDay == None).order_by(
        WorkerSalaryInDay.id).all()
    teacher_salary_all = GivenSalariesInMonth.query.filter(
        GivenSalariesInMonth.deleted_given_salaries_in_month == None).order_by(GivenSalariesInMonth.id).all()
    list_pay = []
    balance = 0
    if button_number != 0 and input_one and input_two:
        if type_request == 'p' or type_request == '':
            for payment in payment_all:
                if payment.account_type_id == button_number and input_one[0:4] <= payment.date.strftime(
                        "%Y") and input_one[5:7] <= payment.date.strftime(
                    "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[
                                                                                 0:4] >= payment.date.strftime(
                    "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[
                                                                                8:10] >= payment.date.strftime(
                    "%d"):
                    info = {
                        "id": payment.student_id,
                        "name": payment.student.user.name,
                        "surname": payment.student.user.surname,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        if type_request == 'by':
            print("by 1")
            for payment in payment_all:
                print(payment.student_month_payments.month)
                if payment.account_type_id == button_number and input_one[
                                                                0:4] <= payment.student_month_payments.month.strftime(
                    "%Y") and input_one[5:7] <= payment.student_month_payments.month.strftime(
                    "%m") and input_one[8:10] <= payment.student_month_payments.month.strftime("%d") and input_two[
                                                                                                         0:4] >= payment.student_month_payments.month.strftime(
                    "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[
                                                                                8:10] >= payment.student_month_payments.month.strftime(
                    "%d"):
                    info = {
                        "id": payment.student_id,
                        "name": payment.student.user.name,
                        "surname": payment.student.user.surname,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d"),
                        "payment_by_month": payment.student_month_payments.month.strftime("%Y-%m")
                    }
                    print(info)
                    balance += int(payment.payed)
                    list_pay.append(info)

        elif type_request == 'w':
            for payment in worker_salary_all:
                if payment.account_type_id == button_number and int(input_one[0:4]) <= payment.years.year and int(
                        input_one[5:7]) <= payment.month.month_number and int(input_one[
                                                                              8:10]) <= payment.day.day_number and int(
                    input_two[
                    0:4]) >= payment.years.year and int(input_two[
                                                        5:7]) >= payment.month.month_number and int(input_two[
                                                                                                    8:10]) >= payment.day.day_number:
                    info = {
                        "name": payment.worker_salary.worker.user.name,
                        "surname": payment.worker_salary.worker.user.surname,
                        "payed": payment.salary,
                        "account_type_name": payment.account_type.name,
                        "date": f' {payment.years.year} -{payment.month.month_number}-{payment.day.day_number}'
                    }
                    balance += int(payment.salary)
                    list_pay.append(info)
        elif type_request == 't':
            for payment in teacher_salary_all:
                if payment.account_type_id == button_number and int(input_one[0:4]) <= payment.years.year and int(
                        input_one[5:7]) <= payment.month.month_number and int(input_one[
                                                                              8:10]) <= payment.day.day_number and int(
                    input_two[
                    0:4]) >= payment.years.year and int(input_two[
                                                        5:7]) >= payment.month.month_number and int(input_two[
                                                                                                    8:10]) >= payment.day.day_number:
                    info = {
                        "name": payment.teacher_salary.teacher.user.name,
                        "surname": payment.teacher_salary.teacher.user.surname,
                        "payed": payment.given_salary,
                        "account_type_name": payment.account_type.name,
                        "date": f' {payment.years.year} -{payment.month.month_number}-{payment.day.day_number}'
                    }
                    balance += int(payment.given_salary)
                    list_pay.append(info)
        elif type_request == 'o':
            for payment in cost_o_all:
                if payment.account_type_id == button_number and input_one[0:4] <= payment.date.strftime(
                        "%Y") and input_one[5:7] <= payment.date.strftime(
                    "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[
                                                                                 0:4] >= payment.date.strftime(
                    "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[
                                                                                8:10] >= payment.date.strftime(
                    "%d"):
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        elif type_request == 'c':
            for payment in cost_c_all:
                if payment.account_type_id == button_number and input_one[0:4] <= payment.date.strftime(
                        "%Y") and input_one[5:7] <= payment.date.strftime(
                    "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[
                                                                                 0:4] >= payment.date.strftime(
                    "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[
                                                                                8:10] >= payment.date.strftime(
                    "%d"):
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        elif type_request == 'm':
            for payment in cost_m_all:
                if payment.account_type_id == button_number and input_one[0:4] <= payment.date.strftime(
                        "%Y") and input_one[5:7] <= payment.date.strftime(
                    "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[
                                                                                 0:4] >= payment.date.strftime(
                    "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[
                                                                                8:10] >= payment.date.strftime(
                    "%d"):
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        elif type_request == 's':
            for payment in cost_s_all:
                if payment.account_type_id == button_number and input_one[0:4] <= payment.date.strftime(
                        "%Y") and input_one[5:7] <= payment.date.strftime(
                    "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[
                                                                                 0:4] >= payment.date.strftime(
                    "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[
                                                                                8:10] >= payment.date.strftime(
                    "%d"):
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        elif type_request == 'e':
            for payment in cost_e_all:
                if payment.account_type_id == button_number and input_one[0:4] <= payment.date.strftime(
                        "%Y") and input_one[5:7] <= payment.date.strftime(
                    "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[
                                                                                 0:4] >= payment.date.strftime(
                    "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[
                                                                                8:10] >= payment.date.strftime(
                    "%d"):
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
    elif button_number == 0 and input_one != '' and input_two != '':
        if type_request == 'p' or type_request == '':
            for payment in payment_all:
                if input_one[0:4] <= payment.date.strftime("%Y") and input_one[5:7] <= payment.date.strftime(
                        "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[
                                                                                     0:4] >= payment.date.strftime(
                    "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[
                                                                                8:10] >= payment.date.strftime(
                    "%d"):
                    info = {
                        "id": payment.student_id,
                        "name": payment.student.user.name,
                        "surname": payment.student.user.surname,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        if type_request == 'by':
            print("by")

            for payment in payment_all:
                print(payment.student_month_payments.month)
                if input_one[0:4] <=payment.student_month_payments.month.strftime("%Y") and input_one[5:7] <= payment.student_month_payments.month.strftime(
                        "%m") and input_one[8:10] <= payment.student_month_payments.month.strftime("%d") and input_two[
                                                                                     0:4] >= payment.student_month_payments.month.strftime(
                    "%Y") and input_two[5:7] >= payment.student_month_payments.month.strftime("%m") and input_two[
                                                                                8:10] >= payment.student_month_payments.month.strftime(
                    "%d"):
                    info = {
                        "id": payment.student_id,
                        "name": payment.student.user.name,
                        "surname": payment.student.user.surname,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d"),
                        "payment_by_month": payment.student_month_payments.month.strftime("%Y-%m")
                    }
                    print(info)
                    balance += int(payment.payed)
                    list_pay.append(info)
        elif type_request == 'w':
            for payment in worker_salary_all:
                if int(input_one[0:4]) <= payment.years.year and int(
                        input_one[5:7]) <= payment.month.month_number and int(input_one[
                                                                              8:10]) <= payment.day.day_number and int(
                    input_two[
                    0:4]) >= payment.years.year and int(input_two[
                                                        5:7]) >= payment.month.month_number and int(input_two[
                                                                                                    8:10]) >= payment.day.day_number:
                    info = {
                        "name": payment.worker_salary.worker.user.name,
                        "surname": payment.worker_salary.worker.user.surname,
                        "payed": payment.salary,
                        "account_type_name": payment.account_type.name,
                        "date": f' {payment.years.year} -{payment.month.month_number}-{payment.day.day_number}'
                    }
                    balance += int(payment.salary)
                    list_pay.append(info)
        elif type_request == 't':
            for payment in teacher_salary_all:
                if int(input_one[0:4]) <= payment.years.year and int(
                        input_one[5:7]) <= payment.month.month_number and int(input_one[
                                                                              8:10]) <= payment.day.day_number and int(
                    input_two[
                    0:4]) >= payment.years.year and int(input_two[
                                                        5:7]) >= payment.month.month_number and int(input_two[
                                                                                                    8:10]) >= payment.day.day_number:
                    info = {
                        "name": payment.teacher_salary.teacher.user.name,
                        "surname": payment.teacher_salary.teacher.user.surname,
                        "payed": payment.given_salary,
                        "account_type_name": payment.account_type.name,
                        "date": f' {payment.years.year} -{payment.month.month_number}-{payment.day.day_number}'
                    }
                    balance += int(payment.given_salary)
                    list_pay.append(info)
        elif type_request == 'o':
            for payment in cost_o_all:
                if input_one[0:4] <= payment.date.strftime("%Y") and input_one[5:7] <= payment.date.strftime(
                        "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[
                                                                                     0:4] >= payment.date.strftime(
                    "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[
                                                                                8:10] >= payment.date.strftime(
                    "%d"):
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        elif type_request == 'c':
            for payment in cost_c_all:
                if input_one[0:4] <= payment.date.strftime("%Y") and input_one[5:7] <= payment.date.strftime(
                        "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[
                                                                                     0:4] >= payment.date.strftime(
                    "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[
                                                                                8:10] >= payment.date.strftime(
                    "%d"):
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        elif type_request == 'm':
            for payment in cost_m_all:
                if input_one[0:4] <= payment.date.strftime("%Y") and input_one[5:7] <= payment.date.strftime(
                        "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[
                                                                                     0:4] >= payment.date.strftime(
                    "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[
                                                                                8:10] >= payment.date.strftime(
                    "%d"):
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        elif type_request == 's':
            for payment in cost_s_all:
                if input_one[0:4] <= payment.date.strftime("%Y") and input_one[5:7] <= payment.date.strftime(
                        "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[
                                                                                     0:4] >= payment.date.strftime(
                    "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[
                                                                                8:10] >= payment.date.strftime(
                    "%d"):
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        elif type_request == 'e':
            for payment in cost_e_all:
                if input_one[0:4] <= payment.date.strftime("%Y") and input_one[5:7] <= payment.date.strftime(
                        "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[
                                                                                     0:4] >= payment.date.strftime(
                    "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[
                                                                                8:10] >= payment.date.strftime(
                    "%d"):
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
    elif button_number != 0 and input_one == None and input_two == None:
        if type_request == 'p' or type_request == '':
            for payment in payment_all:
                if payment.account_type_id == button_number:
                    info = {
                        "id": payment.student_id,
                        "name": payment.student.user.name,
                        "surname": payment.student.user.surname,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        if type_request == 'by':
            for payment in payment_all:
                if payment.account_type_id == button_number:
                    info = {
                        "id": payment.student_id,
                        "name": payment.student.user.name,
                        "surname": payment.student.user.surname,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d"),
                        "payment_by_month": payment.student_month_payments.month.strftime("%Y-%m")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        elif type_request == 'w':
            for payment in worker_salary_all:
                if payment.account_type_id == button_number:
                    info = {
                        "name": payment.worker_salary.worker.user.name,
                        "surname": payment.worker_salary.worker.user.surname,
                        "payed": payment.salary,
                        "account_type_name": payment.account_type.name,
                        "date": f' {payment.years.year} -{payment.month.month_number}-{payment.day.day_number}'
                    }
                    balance += int(payment.salary)
                    list_pay.append(info)
        elif type_request == 't':
            for payment in teacher_salary_all:
                if payment.account_type_id == button_number:
                    info = {
                        "name": payment.teacher_salary.teacher.user.name,
                        "surname": payment.teacher_salary.teacher.user.surname,
                        "payed": payment.given_salary,
                        "account_type_name": payment.account_type.name,
                        "date": f' {payment.years.year} -{payment.month.month_number}-{payment.day.day_number}'
                    }
                    balance += int(payment.given_salary)
                    list_pay.append(info)
        elif type_request == 'o':
            for payment in cost_o_all:
                if payment.account_type_id == button_number:
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        elif type_request == 'c':
            for payment in cost_c_all:
                if payment.account_type_id == button_number:
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        elif type_request == 'm':
            for payment in cost_m_all:
                if payment.account_type_id == button_number:
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        elif type_request == 's':
            for payment in cost_s_all:
                if payment.account_type_id == button_number:
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        elif type_request == 'e':
            for payment in cost_e_all:
                if payment.account_type_id == button_number:
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
    return jsonify({
        'payments': list_pay,
        'balance': balance
    })
