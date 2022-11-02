import json
import random
import secrets
from calendar import monthrange

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum
from django.shortcuts import render, redirect

from functions import *
from .models import JobPosition, Employee, Timetable, Pays, Paymenttypes, Positions, Fines, FinesDirectory, \
    ExpensesSource, Money, Expenses, Salary, PayinText, Statement, Files, Cards, Suppliers, \
    TovarRequests, Partners, Povarlogs, IikoArrivals, Blacklist, BeerArrival


def update_money(date, storage_id):  # need refactoring
    code = getCode(storage_id)
    pointOfSale = getPointOfSale(code)
    payOrders = 0
    nal = 0
    delivery = 0
    yandex = 0
    points = 0
    cashshifts_sum = 0
    d = 0

    jsonData = getIikoCashShifts2(date, date)
    dictData = json.loads(jsonData)
    for a in range(len(dictData)):
        if dictData[a]["pointOfSaleId"] == pointOfSale:
            if dictData[a]["id"] != 'a72c2adf-3fa6-4124-90f4-9aaa84d9f6f2':
                d = 1
                first_data = getSalesByDepartment(dictData[a]["id"])
                data = json.loads(first_data)
                payOrders = dictData[a]["payOrders"]

                for i in range(len(data["cashlessRecords"])):
                    row = Paymenttypes.objects.get(payment_id=data["cashlessRecords"][i]["info"]["paymentTypeId"])
                    if 'аличные' in row.name:
                        nal += int(data["cashlessRecords"][i]["info"]["sum"])
                    if row.name == 'Delivery Club':
                        delivery = int(delivery) + int(data["cashlessRecords"][i]["info"]["sum"])
                    if row.name == 'Яндекс ЕДА' or row.name == '-Яндекс ЕДА':
                        yandex += int(yandex) + int(data["cashlessRecords"][i]["info"]["sum"])
                    if row.name == 'Оплата баллами':
                        points += int(points) + int(data["cashlessRecords"][i]["info"]["sum"])
                    cashshifts_sum += data["cashlessRecords"][i]["info"]["sum"]
    if d == 1:
        all_expenses_nal = \
            Expenses.objects.filter(date_at=date, storage_id=storage_id, is_bn=0).aggregate(Sum('sum'))[
                'sum__sum']
        all_salary = Salary.objects.filter(date=date, storage_id=storage_id).aggregate(Sum('itogo'))['itogo__sum']
        payin = Pays.objects.filter(date_at=date, type=1, storage_id=storage_id).aggregate(Sum('sum'))[
            'sum__sum']
        payout = Pays.objects.filter(date_at=date, type=2, storage_id=storage_id).aggregate(Sum('sum'))[
            'sum__sum']
        if all_salary is None or all_salary == '' or all_salary == 'None':
            all_salary = 0
        else:
            all_salary = str(all_salary).split(',')[0]
        if payin is None or payin == '' or payin == 'None':
            payin = 0
        else:
            payin = int(str(payin).split('.')[0])
        if payout is None or payout == '' or payout == 'None':
            payout = 0
        else:
            payout = int(str(payout).split('.')[0])
        if all_expenses_nal is None or all_expenses_nal == '' or all_expenses_nal == 'None':
            all_expenses_nal = 0
        else:
            all_expenses_nal = int(str(all_expenses_nal).split('.')[0])

        for row in Expenses.objects.filter(date_at=date, storage_id=storage_id, is_bn=0):
            if row.expense == 'Внесение':
                payin += int(row.sum)
                all_expenses_nal -= int(row.sum)
            if row.expense == 'Изъятие':
                payout += int(row.sum)
                all_expenses_nal -= int(row.sum)

        cash = int(payOrders) - int(cashshifts_sum)
        rightCash = cash + int(nal)
        end_day = 0
        morning = 0

        if '.' in str(all_salary):
            all_salary = all_salary.split('.')[0]

        record = Money.objects.get(date_at=date, storage_id=storage_id)
        if record.sum_cash_end_day is not None:
            end_day = record.sum_cash_end_day
        if record.sum_cash_morning is not None or record.sum_cash_morning != 'None':
            morning = record.sum_cash_morning
        record.total_cash = rightCash
        record.total_bn = int(payOrders) - rightCash - (int(yandex) + int(delivery))
        record.total_day = int(payOrders)
        record.difference = \
            str(float(morning) + float(rightCash) - float(str(all_expenses_nal).split(',')[0]) - float(
                all_salary) + float(
                payin) - float(payout)).split('.')[0]
        record.difference2 = end_day - int(
            str(float(morning) + float(rightCash) - float(str(all_expenses_nal).split(',')[0]) - float(
                all_salary) + float(payin) - float(payout)).split('.')[0])
        record.total_market = int(yandex) + int(delivery)
        record.payin = int(str(payin).split('.')[0])
        record.payout = int(str(payout).split('.')[0])
        record.total_salary = int(all_salary)
        record.total_expenses = int(str(all_expenses_nal).split('.')[0])
        record.save()


# [ Pages ]

@login_required
def lk(request):
    return render(request, 'lk/lk.html')


@login_required
def money(request):
    return render(request, 'lk/lk_money.html', context={
        "rows": Money.objects.all(),
        "pays": Pays.objects.all(),
        "storages": Storages.objects.all()
    })


@login_required
def timetable(request):
    rows = Timetable.objects.all()
    return render(request, 'lk/lk_timetable.html', context={
        "rows": rows,
        "storages": Storages.objects.all(),
        "employees": Employee.objects.all()
    })


@login_required
def salary(request):
    return render(request, 'lk/lk_salary.html', context={
        "rows": Salary.objects.all(),
        "storages": Storages.objects.all(),
        "employees": Employee.objects.all()
    })


@login_required
def salary_new(request):
    if request.method == 'POST':
        row = Salary(
            employee_id=request.POST["employee"],
            storage_id=request.POST["storage_id"],
            type=request.POST["type"],
            sum=request.POST["oklad"],
            date=request.POST["date"],
            created_at=get_current_time(),
            sum_percent=request.POST["precent"],
            premium=request.POST["premium"],
            itogo=int(request.POST["oklad"]) + int(request.POST["precent"]) + int(request.POST["premium"])
        )
        row.save()
        update_money(request.POST["date"], request.POST["storage_id"])
        return redirect('/lk/salary')
    return render(request, 'lk/lk_salary_new.html', context={
        "storages": Storages.objects.all(),
        "employees": Employee.objects.all(),
    })


@login_required
def salary_edit(request):
    row = Salary.objects.get(id=request.GET.get('id'))
    if request.method == 'POST':

        row.employee_id = int(request.POST["employee_id"].split(' ')[0])
        row.storage_id = request.POST["storage_id"]
        row.type = request.POST["type"]
        row.sum = request.POST["oklad"]
        row.sum_percent = request.POST["precent"]
        row.premium = request.POST["premium"]
        if request.POST["month"] != 'a':
            row.sum_taxi = request.POST["month"] + ' ' + request.POST["days"]
        row.itogo = int(request.POST["oklad"]) + int(request.POST["precent"]) + int(request.POST["premium"])
        row.save()

        update_money(str(row.date), row.storage_id)

        return redirect('/lk/salary')
    return render(request, 'lk/lk_salary_edit.html', context={
        "row": row,
        "storages": Storages.objects.all(),
        "employees": Employee.objects.all(),
        "id": request.GET.get('id')
    })


@login_required
def timetable_edit(request):
    row = Timetable.objects.get(id=request.GET.get('id'))
    if request.method == 'POST':
        row.employee_id = int(request.POST["employee_id"].split(' ')[0])
        row.storage_id = request.POST["storage_id"]
        row.oklad = request.POST["oklad"]
        row.position = request.POST["position"]
        row.premium = request.POST["premium"]
        row.precent = request.POST["precent"]
        row.total = int(request.POST["oklad"]) + int(request.POST["precent"]) + int(request.POST["premium"])
        row.save()

        return redirect('/lk/timetable')
    return render(request, 'lk/lk_timetable_edit.html', context={
        "row": row,
        "storages": Storages.objects.all(),
        "positions": Positions.objects.all(),
        "employees": Employee.objects.all(),
        "id": request.GET.get('id')
    })


@login_required
def timetable_new(request):
    if request.method == 'POST':
        row = Timetable(
            employee_id=request.POST["employee"],
            storage_id=request.POST["storage_id"],
            date_at=request.POST["date"],
            created_at=get_current_time(),
            position=request.POST["position"],
            oklad=request.POST["oklad"],
            total=int(request.POST["oklad"]),
        )
        row.save()

        return redirect('/lk/timetable')
    return render(request, 'lk/lk_timetable_new.html', context={
        "storages": Storages.objects.all(),
        "employees": Employee.objects.all(),
    })


@login_required
def expenses(request):
    return render(request, 'lk/lk_expenses.html', context={
        "rows": Expenses.objects.all(),
        "storages": Storages.objects.all()
    })


@login_required
def pays(request):
    return render(request, 'lk/lk_pays.html', context={
        "rows": Pays.objects.all(),
        "storages": Storages.objects.all()
    })


@login_required
def employee(request):
    return render(request, 'lk/lk_employee.html', context={
        "rows": Employee.objects.all(),
        "storages": Storages.objects.all()
    })


@login_required
def employee_new(request):
    return render(request, 'lk/lk_employee_new.html', context={
        "storages": Storages.objects.all(),
        "positions": JobPosition.objects.all()
    })


@login_required
def employee_save(request):
    if request.method == 'POST':
        position = JobPosition.objects.get(id=request.POST["type"])
        if Employee.objects.filter(phone=request.POST["phone"]).count() == 0:
            employee = Employee(
                code=secrets.token_hex(16),
                fio=request.POST["fio"],
                address=request.POST["address"],
                storage_id=request.POST["cafe"],
                type=position.position,
                phone=request.POST["phone"],
                oklad=position.oklad,
                is_deleted='Активен'
            )
            employee.save()

        return redirect('/lk/employee')


@login_required
def employee_edit(request):
    if request.method == 'POST':
        employee = Employee.objects.get(id=request.GET.get('id'))
        position = JobPosition.objects.get(id=request.POST["type"])
        if employee.photo == 0:
            photo = request.FILES["photo"]

            fs = FileSystemStorage()
            fs.save(str(k) + '.png', photo)
            employee.photo = 1
        employee.fio = request.POST["fio"]
        employee.address = request.POST["address"]
        employee.birth_date = request.POST["birth_date"]
        employee.storage_id = request.POST["cafe"]
        employee.type = position.position
        employee.oklad = position.oklad
        employee.phone = request.POST["phone"]
        employee.save()

        return redirect('/lk/employee')
    return render(request, 'lk/lk_employee_edit.html', context={
        "id": request.GET.get('id'),
        "employee": Employee.objects.get(id=request.GET.get('id')),
        "storages": Storages.objects.all(),
        "positions": JobPosition.objects.all()
    })


@login_required
def delete(request, data, k):
    if data == 'salary':
        Salary.objects.get(id=request.GET.get('id')).delete()
    elif data == 'employee':
        record = Employee.objects.get(id=request.GET.get('id'))
        record.is_deleted = 'Уволен (' + get_current_time().strftime('%Y-%m-%d') + ')'
        record.save()
    elif data == 'pays':
        Pays.objects.get(id=request.GET.get('id')).delete()
    elif data == 'expenses':
        Expenses.objects.get(id=request.GET.get('id')).delete()
    elif data == 'money':
        Money.objects.get(id=request.GET.get('id')).delete()
    elif data == 'timetable':
        Timetable.objects.get(id=request.GET.get('id')).delete()
    return redirect('/lk/' + data)


@login_required
def expenses_edit(request):
    row = Expenses.objects.get(id=request.GET.get('id'))
    if request.method == 'POST':
        date = request.POST["date"]
        pay_type = request.POST["pay_type"]
        storage = request.POST["storage"]
        comment = request.POST["comment"]
        sum = request.POST["sum"]

        row.date_at = date
        row.is_bn = pay_type
        row.storage_id = storage
        row.comment = comment
        row.sum = sum
        row.save()
        update_money(str(row.date_at), row.storage_id)
        return redirect('/lk/expenses')
    return render(request, 'lk/lk_expenses_edit.html', context={
        "row": row,
        "storages": Storages.objects.all(),
        "id": request.GET.get('id')
    })


@login_required
def money_edit(request):
    row = Money.objects.get(id=request.GET.get('id'))
    if request.method == 'POST':
        sum_for_precent = 0 if row.sum_for_precent is None else int(row.sum_for_precent)
        row.sum_cash_morning = request.POST["morning"]
        row.sum_cash_end_day = request.POST["end_day"]
        row.difference2 = int(str(row.difference.split('.')[0])) - int(request.POST["end_day"])
        row.deposit = int(request.POST["deposit"])
        row.sum_for_precent = sum_for_precent + int(request.POST["deposit"])
        row.save()
        update_money(str(row.date_at), row.storage_id)
        return redirect('/lk/money')
    return render(request, 'lk/lk_money_edit.html', context={
        "row": row,
        "id": request.GET.get('id')
    })


@login_required
def expenses_new(request):
    if request.method == 'POST':
        date_at = request.POST["date"]
        storage_id = request.POST["storage"]
        pay_type = request.POST["pay_type"]
        expense = request.POST["expense"]
        comment = request.POST["comment"]
        sum = request.POST["sum"]

        is_bn = 0 if pay_type == 'Из кассы' else 1

        row = Expenses(
            date_at=date_at,
            storage_id=storage_id,
            is_bn=is_bn,
            expense=expense,
            comment=comment,
            sum=sum
        )
        row.save()
        update_money(date_at, storage_id)
        return redirect('/lk/expenses')
    return render(request, 'lk/lk_expenses_new.html', context={
        "storages": Storages.objects.all(),
        "expenses": ExpensesSource.objects.filter(type=3, is_active=1)
    })


@login_required
def update_end_day(request, date, storage_id):
    update_money(date, storage_id)
    return redirect('/lk/money')


@login_required
def salary_calculation(request):
    if request.method == 'POST':
        month = request.POST["month"]
        day = int(request.POST["day"])
        rows = ''
        days = monthrange(datetime.datetime.now().year, int(month))[1]
        if day == 1:
            rows = Timetable.objects.filter(date_at__contains='-' + month + '-')
        elif day == 2:
            rows = Timetable.objects.filter(date_at__contains='-' + month + '-', date_at__day__lte=15)
        elif day == 3:
            rows = Timetable.objects.filter(date_at__contains='-' + month + '-', date_at__day__gte=16,
                                            date_at__day__lte=days)
        return render(request, 'lk/lk_salary_calculation.html', context={
            "rows": rows,
            "storages": Storages.objects.all()
        })
    return render(request, 'lk/lk_salary_calculation.html')


@login_required
def salary_total_calculation(request):
    if request.method == "POST":
        storage_id = request.POST["storage_id"]
        month = request.POST["month"]
        day = int(request.POST["day"])
        rows = ''
        days = monthrange(datetime.datetime.now().year, int(month))[1]
        if day == 1:
            rows = Timetable.objects.filter(date_at__contains='-' + month + '-', storage_id=storage_id)
        elif day == 2:
            rows = Timetable.objects.filter(date_at__contains='-' + month + '-', date_at__day__lte=15,
                                            storage_id=storage_id)
        elif day == 3:
            rows = Timetable.objects.filter(date_at__contains='-' + month + '-', date_at__day__gte=16,
                                            date_at__day__lte=days, storage_id=storage_id)
        return render(request, 'lk/lk_salary_total_calculation.html', context={
            "rows": rows,
            "storages": Storages.objects.all()
        })
    return render(request, 'lk/lk_salary_total_calculation.html', context={
        "storages": Storages.objects.all()
    })


@login_required
def salary_employee_calculation(request):
    if request.method == "POST":
        employee = request.POST["employee_id"]
        month = request.POST["month"]
        month = month.split(' ')[0]
        employee_id = Employee.objects.get(fio=employee).id
        day = int(request.POST["day"])
        rows = ''
        records = ''
        days = monthrange(datetime.datetime.now().year, int(month))[1]
        d = ''
        m = 0
        usil = 0
        records_sum = 0
        rows_sum = 0
        if day == 1:
            d = 'Весь месяц'
            rows = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id)
            records = Salary.objects.filter(date__contains='-' + month + '-', employee_id=employee_id, type="Аванс")
            records_sum = \
                Salary.objects.filter(date__contains='-' + month + '-', employee_id=employee_id,
                                      type="Аванс").aggregate(
                    Sum('itogo'))['itogo__sum']
            rows_sum = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id).aggregate(
                Sum('total'))['total__sum']
            if 'Тех' in Employee.objects.get(id=employee_id).type:
                m = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id).count()
            else:
                m = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id,
                                             position__contains='основной').count()
                usil = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id,
                                                position__contains='усиление').count()
        elif day == 2:
            d = '1 - 15 число'
            rows = Timetable.objects.filter(date_at__contains='-' + month + '-', date_at__day__lte=15,
                                            employee_id=employee_id)
            records = Salary.objects.filter(date__contains='-' + month + '-', date__day__lte=15,
                                            employee_id=employee_id, type="Аванс")
            rows_sum = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id,
                                                date_at__day__lte=15).aggregate(Sum('total'))['total__sum']
            records_sum = \
                Salary.objects.filter(date__contains='-' + month + '-', date__day__lte=15, employee_id=employee_id,
                                      type="Аванс").aggregate(Sum('itogo'))['itogo__sum']
            if 'Тех' in Employee.objects.get(id=employee_id).type:
                m = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id,
                                             date_at__day__lte=15).count()
            else:
                m = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id,
                                             date_at__day__lte=15, position__contains='основной').count()
                usil = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id,
                                                date_at__day__lte=15, position__contains='усиление').count()
        elif day == 3:
            d = '16 - 31 число'
            rows = Timetable.objects.filter(date_at__contains='-' + month + '-', date_at__day__gte=16,
                                            date_at__day__lte=days, employee_id=employee_id)
            records = Salary.objects.filter(date__contains='-' + month + '-', date__day__gte=16, date__day__lte=days,
                                            employee_id=employee_id, type="Аванс")
            rows_sum = \
                Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id,
                                         date_at__day__gte=16,
                                         date_at__day__lte=days).aggregate(Sum('total'))['total__sum']
            records_sum = \
                Salary.objects.filter(date__contains='-' + month + '-', date__day__gte=16, date__day__lte=days,
                                      employee_id=employee_id, type="Аванс").aggregate(Sum('itogo'))['itogo__sum']
            if 'Тех' in Employee.objects.get(id=employee_id).type:
                m = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id,
                                             date_at__day__gte=16, date_at__day__lte=days).count()
            else:
                m = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id,
                                             date_at__day__gte=16, date_at__day__lte=days,
                                             position__contains='основной').count()
                usil = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id,
                                                date_at__day__gte=16, date_at__day__lte=days,
                                                position__contains='усиление').count()
        if records_sum is None:
            records_sum = 0
        return render(request, 'lk/lk_salary_employee_calculation.html', context={
            "rows": rows,
            "storages": Storages.objects.all(),
            "employees": Employee.objects.all(),
            "records": records,
            "days": d,
            "employee": employee,
            "month": request.POST["month"].split(' ')[1],
            "records_sum": int(records_sum),
            "rows_sum": int(rows_sum),
            "difference": int(rows_sum) - int(records_sum),
            "d": day,
            "m": month,
            "employee_id": employee_id,
            "main": m,
            "usil": usil
        })
    return render(request, 'lk/lk_salary_employee_calculation.html', context={
        "employees": Employee.objects.all()
    })


@login_required
def salary_employee_send(request):
    employee_id = request.GET["employee"]
    days = request.GET["days"]
    month = request.GET["month"]
    difference = request.GET["difference"]
    rows = request.GET["rows"]
    records = request.GET["records"]
    main = request.GET["main"]
    usil = request.GET["usil"]

    d = ''
    days = int(days)
    if days == 1:
        d = 'Весь месяц'
    elif days == 2:
        d = '1 - 15 число'
    elif days == 3:
        d = '16 - 31 число'

    text = f'Сотрудник: {Employee.objects.get(id=employee_id).fio}%0AМесяц: {month}%0AПериод: {d}%0AСумма к получению: {difference}%0A%0AНачислено: {rows}%0AПолучено: {records}%0AОсновные смены: {main}%0AСмены усиление: {usil}'
    send_webhook('-chat_id', text, 1)

    return redirect('/lk/salary/employee_calculation')


@login_required
def salary_calculation_update(request):
    barmen_count = 0
    month = request.GET.get('month')
    for record in Timetable.objects.filter(date_at__month=month):
        try:
            row = Money.objects.get(date_at=record.date_at, storage_id=record.storage_id)
            deposit = 0 if row.deposit is None else row.deposit
            payOrders = row.total_day
            sum_for_precent = payOrders - int(row.total_market) - deposit
            payOrders2 = payOrders - deposit

            barmen_count += int(Timetable.objects.filter(date_at=record.date_at,
                                                         storage_id=record.storage_id,
                                                         position='Бармен основной').count())
            barmen_count += int(Timetable.objects.filter(date_at=record.date_at,
                                                         storage_id=record.storage_id,
                                                         position='Бармен усиление').count())
            barmen_count += int(Timetable.objects.filter(date_at=record.date_at,
                                                         storage_id=record.storage_id,
                                                         position__contains='Бармен вызывной').count())

            if barmen_count > 1:
                precent = '2.5'
            else:
                precent = '3'

            if 'Повар' in record.position or 'Тех' in record.position or 'Бармен стажер' in record.position:
                precentt = 0
            else:
                precentt = int(sum_for_precent) * (float(precent) / 100)
                record.precent_num = precent

            if 'Бармен' not in record.position:
                if 60000 <= payOrders2 < 70000:
                    premium = 200
                elif 70000 <= payOrders2 < 100000:
                    premium = 500
                elif payOrders2 >= 100000:
                    premium = 1000
                else:
                    premium = 0
            else:
                if 'стажер' not in record.position:
                    if 60000 <= sum_for_precent < 70000:
                        premium = 200
                    elif 70000 <= sum_for_precent < 100000:
                        premium = 500
                    elif sum_for_precent >= 100000:
                        premium = 1000
                    else:
                        premium = 0
                else:
                    premium = 0

            record.precent = precentt
            record.premium = premium
            record.total = int(record.oklad) + int(record.precent) + int(record.premium)
            record.payorders = payOrders
            record.sumforprecent = sum_for_precent
            if 'стажер' in record.position:
                record.oklad = 500
            record.total = int(record.oklad) + int(record.precent) + int(record.premium)
            record.save()

            barmen_count = 0
        except Money.DoesNotExist:
            continue
    return redirect('/lk/timetable')


@login_required
def fine(request):
    return render(request, "lk/lk_fine.html", context={
        "storages": Storages.objects.all(),
        "employees": Employee.objects.all(),
        "fines": Fines.objects.all(),
        "finesDirectory": FinesDirectory.objects.all()
    })


@login_required
def fine_save(request):
    if request.method == 'POST':
        row = FinesDirectory(
            date_at=request.POST["date"],
            employee_id=request.POST["employee_id"].split(' ')[0],
            fine_id=request.POST["fine"]
        )
        row.save()
        return redirect('/lk/fine')
    return redirect('/lk/fine')


@login_required
def new_fine_save(request):
    if request.method == 'POST':
        row = Fines(
            text=request.POST["text"],
            sum=request.POST["sum"]
        )
        row.save()
        return redirect('/lk/fine')
    return redirect('/lk/fine')


@login_required
def mysql_prepare(request):
    # номера сотрудников
    """for record in Employee.objects.all():
        row = Employee.objects.get(id=record.id)
        phone = record.phone
        if phone is not None:
            array = phone.split('+')[1] if '+' in phone else phone
            phone = '7' + str(array[1:11]) if list(array)[0] != int(7) else phone
            row.phone = phone
            row.save()"""
    """for record in Povarlogs.objects.all():
        row = Povarlogs.objects.get(id=record.id)
        storage_name = ''
        try:
            row.yur_lico = Storages.objects.get(name=record.cafe).yur_lico
            row.save()
        except Storages.DoesNotExist:
            pass"""
    return redirect('/lk/employee')


@login_required
def blacklist(request):
    if request.method == 'POST':
        i = random.randint(0, 10000)
        row = Blacklist(
            date_at=request.POST["date"],
            storage_id=request.POST["storage_id"],
            photo=i
        )
        row.save()
        photo = request.FILES["photo"]

        fs = FileSystemStorage()
        fs.save(str(i) + 'black.png', photo)

        return redirect('/bar/blacklist?code=' + getCode(request.POST["storage_id"]))
    return render(request, 'lk/blacklist.html', context={
        "storages": Storages.objects.all(),
    })


@login_required
def employee_comeback(request):
    record = Employee.objects.get(id=request.GET.get('id'))
    if record.is_deleted != 'Активен':
        record.is_deleted = 'Активен'
    record.save()
    return redirect('/lk/employee')


@login_required
def pays_edit(request):
    record = Pays.objects.get(id=request.GET.get('id'))
    if request.method == 'POST':
        record.date_at = request.POST["date_at"]
        record.type = request.POST["type"]
        record.comment = request.POST["comment"]
        record.sum = request.POST["sum"]
        record.save()
    return render(request, 'lk/lk_pays_edit.html', context={
        "records": PayinText.objects.all(),
        "row": record,
        "id": request.GET.get('id')
    })


@login_required
def pays_new(request):
    if request.method == 'POST':
        record = Pays(
            date_at=request.POST["date_at"],
            created_at=get_current_time().strftime('Y-m-d H:M:S'),
            storage_id=request.POST["storage_id"],
            type=request.POST["type"],
            comment=request.POST["comment"],
            sum=request.POST["sum"],
        )
        record.save()
    return render(request, 'lk/lk_pays_new.html', context={
        "records": PayinText.objects.all(),
    })


@login_required
def bars(request):
    return render(request, 'lk/bars.html', context={
        "storages": Storages.objects.all()
    })


@login_required
def bank_parser(request):
    if request.method == "POST":
        file = request.FILES["file"]

        fs = FileSystemStorage()
        k = random.randint(0, 1000000)
        fs.save(str(k) + '.txt', file)
        b = []
        main = []
        f = open(f'url_to_file{str(k) + ".txt"}', encoding='windows-1251')
        a = f.readlines()
        l = [line.rstrip() for line in a]
        for x in l:
            b.append(x.split("="))
        # до секцидокумент
        for i in range(len(b)):
            if b[i][0] == 'СекцияДокумент':
                break
            else:
                main.append(b[i])

        key = 0
        doc = []
        q = {key: []}
        for k in range(len(main), len(b)):
            if b[k][0] == 'КонецДокумента':
                q[key] = doc
                doc = []
                key += 1
            elif b[k][0] == 'КонецФайла':
                break
            else:
                if 'СекцияДокумент' in b[k][0]:
                    doc.append(b[k][1])
                elif b[k][0] == 'Дата' or b[k][0] == 'Номер' or b[k][0] == 'НазначениеПлатежа' or b[k][0] == 'Сумма' or \
                        b[k][0] == 'Плательщик' or b[k][0] == 'Получатель' \
                        or b[k][0] == 'ПлательщикИНН' or b[k][0] == 'ПолучательИНН':
                    doc.append(b[k][1])

        for i in range(len(q)):
            card_id = -1
            for card in Cards.objects.all():
                card_id = card.id if card.num in q[i][4] else -1
            type = 1 if 'ордер' in q[i][0] else 2

            try:
                payer = Partners.objects.get(inn=q[i][5]).id if len(q[i][5]) > 0 else None
            except Partners.DoesNotExist:
                payer = None
            try:
                recipient = Partners.objects.get(inn=q[i][7]).id if len(q[i][7]) > 0 else None
            except Partners.DoesNotExist:
                recipient = None

            if payer is None:
                inn = q[i][5] if len(q[i][5]) > 0 else -1
                if Partners.objects.filter(inn=inn).count() == 0:
                    row = Partners(
                        storage_id=0,
                        name=q[i][4],
                        inn=inn,
                        type='',
                        status=0
                    )
                    row.save()
            if recipient is None:
                inn = q[i][7] if len(q[i][7]) > 0 else -1
                if Partners.objects.filter(inn=inn).count() == 0:
                    row = Partners(
                        storage_id=0,
                        name=q[i][6],
                        inn=inn,
                        type='',
                        status=0
                    )
                    row.save()

            date_at = q[i][2].split('.')[2] + '-' + q[i][2].split('.')[1] + '-' + q[i][2].split('.')[0] if len(
                q[i][2]) > 0 else ''
            if type == 1:
                try:
                    date = (q[i][8].split(' ')[11]).split('.')[2] + '-' + (q[i][8].split(' ')[11]).split('.')[1] + '-' + \
                           (q[i][8].split(' ')[11]).split('.')[0] if len(
                        (q[i][8].split(' ')[11]).split('.')) == 4 else ''
                except IndexError:
                    date = ''
            else:
                try:
                    date = (q[i][8].split(' ')[9]).split('.')[2] + '-' + (q[i][8].split(' ')[9]).split('.')[1] + '-' + \
                           (q[i][8].split(' ')[9]).split('.')[0] if len((q[i][8].split(' ')[9]).split('.')) == 4 else ''
                except IndexError:
                    date = ''
            if Statement.objects.filter(number=q[i][1], date_at=date_at).count() == 0:
                if 'енежное вознаграждение по реестру' in q[i][8]:
                    row = Statement(
                        date_at=date_at,
                        type=type,
                        number=q[i][1],
                        sum=q[i][3],
                        date=date,
                        payer_id=payer,
                        recipient_id=recipient,
                        payment=q[i][8],
                        card_id=card_id,
                        comment='Вывод ' + str(q[i][3])
                    )
                    row.save()
                else:
                    row = Statement(
                        date_at=date_at,
                        type=type,
                        number=q[i][1],
                        sum=q[i][3],
                        date=date,
                        payer_id=payer,
                        recipient_id=recipient,
                        payment=q[i][8],
                        card_id=card_id,
                    )
                    row.save()
                # 0 ордер поручение
                # 1 номер
                # 2 сумма
                # 3 дата
                # 4 плательщик
                # 5 плательщикИНН
                # 6 получатель
                # 7 получательИНН
                # 8 платеж РОП
        for row in Statement.objects.all():
            if row.card_id == -1:
                for card in Cards.objects.all():
                    if card.num in row.payment:
                        row.card_id = card.id
                        row.storage_id = card.storage_id
                        row.save()
    if request.GET.get('full') is not None:
        return render(request, 'lk/bank_menu.html', context={
            "rows": Statement.objects.all(),
            "cards": Cards.objects.all(),
            "files": Files.objects.filter(preparation=0),
            "full": 1,
            "partners": Partners.objects.all(),
            "records": Statement.objects.raw(
                'select 1 as id, statement.date, statement.storage_id, sum(statement.sum) as statmentSum, s.name as storageName, transDate, transSum, (transSum-sum(statement.sum)) as diffSum from statement left join storages s on s.id = statement.storage_id left join (select t.storage_id as transStorageId, t.date_at as transDate, sum(t.sum) as transSum from Expenses t where is_bn = 1 group by transStorageId, transDate order by transDate DESC limit 600) t on transStorageId = statement.storage_id and statement.date = transDate group by storage_id, date order by date DESC limit 600')
        })
    else:
        return render(request, 'lk/bank_menu2.html', context={
            "rows": Statement.objects.all(),
            "cards": Cards.objects.all(),
            "full": 0,
            "partners": Partners.objects.all(),
            "records": Statement.objects.raw(
                'select 1 as id, statement.date, statement.storage_id, sum(statement.sum) as statmentSum, s.name as storageName, transDate, transSum, (transSum-sum(statement.sum)) as diffSum from statement left join storages s on s.id = statement.storage_id left join (select t.storage_id as transStorageId, t.date_at as transDate, sum(t.sum) as transSum from Expenses t where is_bn = 1 group by transStorageId, transDate order by transDate DESC limit 600) t on transStorageId = statement.storage_id and statement.date = transDate group by storage_id, date order by date DESC limit 600')
        })


@login_required
def statement_cards(request):
    if request.method == 'POST':
        num = '*' + request.POST["num"] if int(request.POST["type"]) == 1 else request.POST["num"]
        card = Cards(
            num=num,
            cafe=request.POST["text"],
            type=request.POST["type"]
        )
        card.save()
        return redirect('/lk/statement/cards')
    undefined_cards = ''
    for record in Statement.objects.all():
        for card in Cards.objects.all():
            if record.type == 1 and record.card_id == -1:
                if len(record.payment.split(' ')) >= 10:
                    if card.num not in record.payment.split(' ')[9]:
                        if "/" in record.payment.split(' ')[9] or 'от' in record.payment.split(' ')[9]:
                            continue
                        else:
                            undefined_cards += record.payment.split(' ')[9] + '\n'
                        if record.payment.split(' ')[9] in undefined_cards:
                            continue
                    else:
                        continue
                else:
                    continue
    for row in Statement.objects.all():
        if row.card_id == -1:
            for card in Cards.objects.all():
                if card.num in row.payment:
                    row.card_id = card.id
                    row.save()
    return render(request, 'lk/cards.html', context={
        "cards": Cards.objects.all(),
        "undefined_cards": undefined_cards
    })


@login_required
def employee_with_salary(request):
    total = dict()
    prepaid = dict()
    received = dict()
    for employee in Employee.objects.filter(is_deleted='Активен'):
        if request.GET.get('month') is None:
            total_sum = 0 if \
                Timetable.objects.filter(date_at__contains='-' + get_current_time().strftime('%m') + '-',
                                         employee_id=employee.id).aggregate(
                    Sum('total'))[
                    'total__sum'] is None else \
                Timetable.objects.filter(date_at__contains='-' + get_current_time().strftime('%m') + '-',
                                         employee_id=employee.id).aggregate(
                    Sum('total'))[
                    'total__sum']
            prepaid_sum = 0 if \
                Salary.objects.filter(date__contains='-' + get_current_time().strftime('%m') + '-',
                                      employee_id=employee.id, type='Аванс').aggregate(Sum('itogo'))[
                    'itogo__sum'] is None else \
                round(Salary.objects.filter(date__contains='-' + get_current_time().strftime('%m') + '-',
                                            employee_id=employee.id, type='Аванс').aggregate(Sum('itogo'))[
                          'itogo__sum'])
            received_sum = total_sum - prepaid_sum
            total[employee.id] = total_sum
            prepaid[employee.id] = prepaid_sum
            received[employee.id] = received_sum
        else:
            total_sum = 0 if \
                Timetable.objects.filter(date_at__contains='-' + request.GET.get('month') + '-',
                                         employee_id=employee.id).aggregate(
                    Sum('total'))[
                    'total__sum'] is None else \
                Timetable.objects.filter(date_at__contains='-' + request.GET.get('month') + '-',
                                         employee_id=employee.id).aggregate(
                    Sum('total'))[
                    'total__sum']
            prepaid_sum = 0 if Salary.objects.filter(date__contains='-' + request.GET.get('month') + '-',
                                                     employee_id=employee.id, type='Аванс').aggregate(Sum('itogo'))[
                                   'itogo__sum'] is None else \
                round(Salary.objects.filter(date__contains='-' + request.GET.get('month') + '-',
                                            employee_id=employee.id, type='Аванс').aggregate(Sum('itogo'))[
                          'itogo__sum'])
            received_sum = total_sum - prepaid_sum
            total[employee.id] = total_sum
            prepaid[employee.id] = prepaid_sum
            received[employee.id] = received_sum

    return render(request, 'lk/employee_with_salary.html', context={
        "total": total,
        "prepaid": prepaid,
        "received": received,
        "employees": Employee.objects.filter(is_deleted='Активен'),
        "month": get_current_time().strftime('%m') if request.GET.get('month') is None else request.GET.get('month')
    })


def arrivals(request):
    return render(request, 'lk/arrivals.html', context={
        "rows": BeerArrival.objects.all(),
        "storages": Storages.objects.all(),
        "products": Products.objects.all(),
        "suppliers": Suppliers.objects.all(),
        "status": -1 if request.GET.get('status') is None else request.GET.get('status'),
    })


@login_required
def supplier_debt(request):
    if request.method == "POST":
        for record in BeerArrival.objects.filter(type=0):
            if request.POST.get(f'[{record.id}]') == str(record.sum):
                if record.type == 0:
                    supplier_id = record.supplier
                    date = request.POST["date"]
                    writer = 'ПриходПиваСайт'
                    sum = record.sum
                    worker = Suppliers.objects.get(supplier_id=supplier_id).name
                    type = 'Пиво/напитки'
                    fromtype = request.POST["fromtype"]
                    comment = '[' + str(record.date_at) + '] (' + request.POST[
                        "payer"] + ') Пиво долг (' + Suppliers.objects.get(
                        supplier_id=supplier_id).name + ' / ' + record.num + ')'
                    row = Povarlogs(
                        date=date,
                        writer=writer,
                        sum=sum,
                        worker=worker,
                        cafe=Storages.objects.get(id=record.storage_id).name,
                        type=type,
                        fromtype=fromtype,
                        comment=comment,
                        yur_lico=Storages.objects.get(id=record.storage_id).yur_lico
                    )
                    row.save()
                    record.type = 1
                    record.save()
    ip = None
    if request.GET.get('supplier_id') is None:
        suppliers = Suppliers.objects.filter(category='Пиво разливное')
        storage_name = 'Итого'
        records = []
        records2 = []
        rows = BeerArrival.objects.all()
        for supplier in suppliers:
            if request.GET.get('storage_id') is None:
                if request.GET.get('dateFrom') is None:
                    dictionary = dict()
                    dictionary["id"] = supplier.supplier_id
                    dictionary["total"] = 0 if \
                        BeerArrival.objects.filter(supplier=supplier.supplier_id).aggregate(Sum('sum'))[
                            'sum__sum'] is None else \
                        BeerArrival.objects.filter(supplier=supplier.supplier_id).aggregate(Sum('sum'))['sum__sum']
                    dictionary["paid"] = 0 if \
                        BeerArrival.objects.filter(supplier=supplier.supplier_id, type__gte=1).aggregate(Sum('sum'))[
                            'sum__sum'] is None else \
                        BeerArrival.objects.filter(supplier=supplier.supplier_id, type__gte=1).aggregate(Sum('sum'))[
                            'sum__sum']
                    dictionary["unpaid"] = dictionary["total"] - dictionary["paid"]
                    records.append(dictionary)
                    dictionary2 = dict()
                    dictionary2["id"] = supplier.supplier_id
                    dictionary2["total"] = 0 if \
                        IikoArrivals.objects.filter(supplier_id=supplier.id).aggregate(Sum('sum'))[
                            'sum__sum'] is None else \
                        IikoArrivals.objects.filter(supplier_id=supplier.id).aggregate(Sum('sum'))['sum__sum']
                    dictionary2["paid"] = 0 if \
                        IikoArrivals.objects.filter(supplier_id=supplier.id).aggregate(Sum('paid_sum'))[
                            'paid_sum__sum'] is None else \
                        IikoArrivals.objects.filter(supplier_id=supplier.id).aggregate(Sum('paid_sum'))[
                            'paid_sum__sum']
                    dictionary2["unpaid"] = dictionary2["total"] - dictionary2["paid"]
                    records2.append(dictionary2)
                else:
                    dictionary = dict()
                    dictionary["id"] = supplier.supplier_id
                    dictionary["total"] = 0 if \
                        BeerArrival.objects.filter(supplier=supplier.supplier_id, date_at__range=(
                            request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))[
                            'sum__sum'] is None else \
                        BeerArrival.objects.filter(supplier=supplier.supplier_id, date_at__range=(
                            request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))['sum__sum']
                    dictionary["paid"] = 0 if \
                        BeerArrival.objects.filter(supplier=supplier.supplier_id, type__gte=1, date_at__range=(
                            request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))[
                            'sum__sum'] is None else \
                        BeerArrival.objects.filter(supplier=supplier.supplier_id, type__gte=1, date_at__range=(
                            request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))['sum__sum']
                    dictionary["unpaid"] = dictionary["total"] - dictionary["paid"]
                    records.append(dictionary)
                    rows = BeerArrival.objects.filter(
                        date_at__range=(request.GET.get('dateFrom'), request.GET.get('dateTo')))
                    dictionary2 = dict()
                    dictionary2["id"] = supplier.supplier_id
                    dictionary2["total"] = 0 if \
                        IikoArrivals.objects.filter(supplier_id=supplier.id, date_at__range=(
                            request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))[
                            'sum__sum'] is None else \
                        IikoArrivals.objects.filter(supplier_id=supplier.id, date_at__range=(
                            request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))['sum__sum']
                    dictionary2["paid"] = 0 if \
                        IikoArrivals.objects.filter(supplier_id=supplier.id, date_at__range=(
                            request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('paid_sum'))[
                            'paid_sum__sum'] is None else \
                        IikoArrivals.objects.filter(supplier_id=supplier.id, date_at__range=(
                            request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('paid_sum'))[
                            'paid_sum__sum']
                    dictionary2["unpaid"] = dictionary2["total"] - dictionary2["paid"]
                    records2.append(dictionary2)
            else:
                if request.GET.get('storage_id') == 'luginin':
                    ip = 'угинин'
                    if request.GET.get('dateFrom') is None:
                        dictionary = dict()
                        dictionary["id"] = supplier.supplier_id
                        total = 0
                        paid = 0
                        for storage in Storages.objects.filter(yur_lico__contains='угинин'):
                            total += 0 if \
                                BeerArrival.objects.filter(supplier=supplier.supplier_id,
                                                           storage_id=storage.id).aggregate(Sum('sum'))[
                                    'sum__sum'] is None else \
                                BeerArrival.objects.filter(supplier=supplier.supplier_id,
                                                           storage_id=storage.id).aggregate(Sum('sum'))[
                                    'sum__sum']
                            paid += 0 if \
                                BeerArrival.objects.filter(supplier=supplier.supplier_id, type__gte=1,
                                                           storage_id=storage.id).aggregate(Sum('sum'))[
                                    'sum__sum'] is None else \
                                BeerArrival.objects.filter(supplier=supplier.supplier_id, type__gte=1,
                                                           storage_id=storage.id).aggregate(Sum('sum'))[
                                    'sum__sum']
                        dictionary["total"] = total
                        dictionary["paid"] = paid
                        dictionary["unpaid"] = dictionary["total"] - dictionary["paid"]
                        records.append(dictionary)
                        storage_name = 'ИП Лугинин А.А'
                        dictionary2 = dict()
                        dictionary2["id"] = supplier.supplier_id
                        total2 = 0
                        paid2 = 0
                        for storage in Storages.objects.filter(yur_lico__contains='угинин'):
                            total2 += 0 if \
                                IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                            storage_id=storage.id).aggregate(Sum('sum'))[
                                    'sum__sum'] is None else \
                                IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                            storage_id=storage.id).aggregate(Sum('sum'))[
                                    'sum__sum']
                            paid2 += 0 if \
                                IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                            storage_id=storage.id).aggregate(Sum('paid_sum'))[
                                    'paid_sum__sum'] is None else \
                                IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                            storage_id=storage.id).aggregate(Sum('paid_sum'))[
                                    'paid_sum__sum']
                        dictionary2["total"] = total2
                        dictionary2["paid"] = paid2
                        dictionary2["unpaid"] = dictionary2["total"] - dictionary2["paid"]
                        records2.append(dictionary2)
                    else:
                        dictionary = dict()
                        dictionary["id"] = supplier.supplier_id
                        total = 0
                        paid = 0
                        for storage in Storages.objects.filter(yur_lico__contains='угинин'):
                            total += 0 if \
                                BeerArrival.objects.filter(supplier=supplier.supplier_id,
                                                           storage_id=storage.id, date_at__range=(
                                        request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))[
                                    'sum__sum'] is None else \
                                BeerArrival.objects.filter(supplier=supplier.supplier_id,
                                                           storage_id=storage.id, date_at__range=(
                                        request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))[
                                    'sum__sum']
                            paid += 0 if \
                                BeerArrival.objects.filter(supplier=supplier.supplier_id, type__gte=1,
                                                           storage_id=storage.id, date_at__range=(
                                        request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))[
                                    'sum__sum'] is None else \
                                BeerArrival.objects.filter(supplier=supplier.supplier_id, type__gte=1,
                                                           storage_id=storage.id, date_at__range=(
                                        request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))[
                                    'sum__sum']
                        dictionary["total"] = total
                        dictionary["paid"] = paid
                        dictionary["unpaid"] = dictionary["total"] - dictionary["paid"]
                        records.append(dictionary)
                        rows = BeerArrival.objects.filter(
                            date_at__range=(request.GET.get('dateFrom'), request.GET.get('dateTo')))
                        storage_name = 'ИП Лугинин А.А'
                        dictionary2 = dict()
                        dictionary2["id"] = supplier.supplier_id
                        total2 = 0
                        paid2 = 0
                        for storage in Storages.objects.filter(yur_lico__contains='осквичев'):
                            total2 += 0 if \
                                IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                            storage_id=storage.id, date_at__range=(
                                        request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))[
                                    'sum__sum'] is None else \
                                IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                            storage_id=storage.id, date_at__range=(
                                        request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))[
                                    'sum__sum']
                            paid2 += 0 if \
                                IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                            storage_id=storage.id, date_at__range=(
                                        request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(
                                    Sum('paid_sum'))[
                                    'paid_sum__sum'] is None else \
                                IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                            storage_id=storage.id, date_at__range=(
                                        request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(
                                    Sum('paid_sum'))[
                                    'paid_sum__sum']
                        dictionary2["total"] = total2
                        dictionary2["paid"] = paid2
                        dictionary2["unpaid"] = dictionary2["total"] - dictionary2["paid"]
                        records2.append(dictionary2)
                elif request.GET.get('storage_id') == 'moskvichev':
                    ip = 'осквичев'
                    if request.GET.get('dateFrom') is None:
                        dictionary = dict()
                        dictionary["id"] = supplier.supplier_id
                        total = 0
                        paid = 0
                        for storage in Storages.objects.filter(yur_lico__contains='осквичев'):
                            total += 0 if \
                                BeerArrival.objects.filter(supplier=supplier.supplier_id,
                                                           storage_id=storage.id).aggregate(Sum('sum'))[
                                    'sum__sum'] is None else \
                                BeerArrival.objects.filter(supplier=supplier.supplier_id,
                                                           storage_id=storage.id).aggregate(Sum('sum'))[
                                    'sum__sum']
                            paid += 0 if \
                                BeerArrival.objects.filter(supplier=supplier.supplier_id, type__gte=1,
                                                           storage_id=storage.id).aggregate(Sum('sum'))[
                                    'sum__sum'] is None else \
                                BeerArrival.objects.filter(supplier=supplier.supplier_id, type__gte=1,
                                                           storage_id=storage.id).aggregate(Sum('sum'))[
                                    'sum__sum']
                        dictionary["total"] = total
                        dictionary["paid"] = paid
                        dictionary["unpaid"] = dictionary["total"] - dictionary["paid"]
                        records.append(dictionary)
                        storage_name = 'ИП Москвичев В.А'
                        dictionary2 = dict()
                        dictionary2["id"] = supplier.supplier_id
                        total2 = 0
                        paid2 = 0
                        for storage in Storages.objects.filter(yur_lico__contains='осквичев'):
                            total2 += 0 if \
                                IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                            storage_id=storage.id).aggregate(Sum('sum'))[
                                    'sum__sum'] is None else \
                                IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                            storage_id=storage.id).aggregate(Sum('sum'))[
                                    'sum__sum']
                            paid2 += 0 if \
                                IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                            storage_id=storage.id).aggregate(Sum('paid_sum'))[
                                    'paid_sum__sum'] is None else \
                                IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                            storage_id=storage.id).aggregate(Sum('paid_sum'))[
                                    'paid_sum__sum']
                        dictionary2["total"] = total2
                        dictionary2["paid"] = paid2
                        dictionary2["unpaid"] = dictionary2["total"] - dictionary2["paid"]
                        records2.append(dictionary2)
                    else:
                        dictionary = dict()
                        dictionary["id"] = supplier.supplier_id
                        total = 0
                        paid = 0
                        for storage in Storages.objects.filter(yur_lico__contains='осквичев'):
                            total += 0 if \
                                BeerArrival.objects.filter(supplier=supplier.supplier_id,
                                                           storage_id=storage.id, date_at__range=(
                                        request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))[
                                    'sum__sum'] is None else \
                                BeerArrival.objects.filter(supplier=supplier.supplier_id,
                                                           storage_id=storage.id, date_at__range=(
                                        request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))[
                                    'sum__sum']
                            paid += 0 if \
                                BeerArrival.objects.filter(supplier=supplier.supplier_id, type__gte=1,
                                                           storage_id=storage.id, date_at__range=(
                                        request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))[
                                    'sum__sum'] is None else \
                                BeerArrival.objects.filter(supplier=supplier.supplier_id, type__gte=1,
                                                           storage_id=storage.id, date_at__range=(
                                        request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))[
                                    'sum__sum']
                        dictionary["total"] = total
                        dictionary["paid"] = paid
                        dictionary["unpaid"] = dictionary["total"] - dictionary["paid"]
                        records.append(dictionary)
                        rows = BeerArrival.objects.filter(
                            date_at__range=(request.GET.get('dateFrom'), request.GET.get('dateTo')))
                        storage_name = 'ИП Москвичев В.А'
                        dictionary2 = dict()
                        dictionary2["id"] = supplier.supplier_id
                        total2 = 0
                        paid2 = 0
                        for storage in Storages.objects.filter(yur_lico__contains='осквичев'):
                            total2 += 0 if \
                                IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                            storage_id=storage.id, date_at__range=(
                                        request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))[
                                    'sum__sum'] is None else \
                                IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                            storage_id=storage.id, date_at__range=(
                                        request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))[
                                    'sum__sum']
                            paid2 += 0 if \
                                IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                            storage_id=storage.id, date_at__range=(
                                        request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(
                                    Sum('paid_sum'))[
                                    'paid_sum__sum'] is None else \
                                IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                            storage_id=storage.id, date_at__range=(
                                        request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(
                                    Sum('paid_sum'))[
                                    'paid_sum__sum']
                        dictionary2["total"] = total2
                        dictionary2["paid"] = paid2
                        dictionary2["unpaid"] = dictionary2["total"] - dictionary2["paid"]
                        records2.append(dictionary2)
                else:
                    if request.GET.get('dateFrom') is None:
                        dictionary = dict()
                        dictionary["id"] = supplier.supplier_id
                        dictionary["total"] = 0 if \
                            BeerArrival.objects.filter(supplier=supplier.supplier_id,
                                                       storage_id=request.GET.get('storage_id')).aggregate(Sum('sum'))[
                                'sum__sum'] is None else \
                            BeerArrival.objects.filter(supplier=supplier.supplier_id,
                                                       storage_id=request.GET.get('storage_id')).aggregate(Sum('sum'))[
                                'sum__sum']
                        dictionary["paid"] = 0 if \
                            BeerArrival.objects.filter(supplier=supplier.supplier_id, type__gte=1,
                                                       storage_id=request.GET.get('storage_id')).aggregate(Sum('sum'))[
                                'sum__sum'] is None else \
                            BeerArrival.objects.filter(supplier=supplier.supplier_id, type__gte=1,
                                                       storage_id=request.GET.get('storage_id')).aggregate(Sum('sum'))[
                                'sum__sum']
                        dictionary["unpaid"] = dictionary["total"] - dictionary["paid"]
                        records.append(dictionary)
                        rows = BeerArrival.objects.filter(storage_id=request.GET.get('storage_id'))
                        storage_name = Storages.objects.get(id=request.GET.get('storage_id')).name
                        dictionary2 = dict()
                        dictionary2["id"] = supplier.supplier_id
                        dictionary2["total"] = 0 if \
                            IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                        storage_id=request.GET.get('storage_id')).aggregate(Sum('sum'))[
                                'sum__sum'] is None else \
                            IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                        storage_id=request.GET.get('storage_id')).aggregate(Sum('sum'))[
                                'sum__sum']
                        dictionary2["paid"] = 0 if \
                            IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                        storage_id=request.GET.get('storage_id')).aggregate(
                                Sum('paid_sum'))[
                                'paid_sum__sum'] is None else \
                            IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                        storage_id=request.GET.get('storage_id')).aggregate(
                                Sum('paid_sum'))[
                                'paid_sum__sum']
                        dictionary2["unpaid"] = dictionary2["total"] - dictionary2["paid"]
                        records2.append(dictionary2)
                    else:
                        dictionary = dict()
                        dictionary["id"] = supplier.supplier_id
                        dictionary["total"] = 0 if \
                            BeerArrival.objects.filter(supplier=supplier.supplier_id, date_at__range=(
                                request.GET.get('dateFrom'), request.GET.get('dateTo')),
                                                       storage_id=request.GET.get('storage_id')).aggregate(Sum('sum'))[
                                'sum__sum'] is None else \
                            BeerArrival.objects.filter(supplier=supplier.supplier_id, date_at__range=(
                                request.GET.get('dateFrom'), request.GET.get('dateTo')),
                                                       storage_id=request.GET.get('storage_id')).aggregate(Sum('sum'))[
                                'sum__sum']
                        dictionary["paid"] = 0 if \
                            BeerArrival.objects.filter(supplier=supplier.supplier_id, type__gte=1, date_at__range=(
                                request.GET.get('dateFrom'), request.GET.get('dateTo')),
                                                       storage_id=request.GET.get('storage_id')).aggregate(Sum('sum'))[
                                'sum__sum'] is None else \
                            BeerArrival.objects.filter(supplier=supplier.supplier_id, type__gte=1, date_at__range=(
                                request.GET.get('dateFrom'), request.GET.get('dateTo')),
                                                       storage_id=request.GET.get('storage_id')).aggregate(Sum('sum'))[
                                'sum__sum']
                        dictionary["unpaid"] = dictionary["total"] - dictionary["paid"]
                        records.append(dictionary)
                        rows = BeerArrival.objects.filter(
                            date_at__range=(request.GET.get('dateFrom'), request.GET.get('dateTo')),
                            storage_id=request.GET.get('storage_id'))
                        storage_name = Storages.objects.get(id=request.GET.get('storage_id')).name
                        dictionary2 = dict()
                        dictionary2["id"] = supplier.supplier_id
                        dictionary2["total"] = 0 if \
                            IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                        storage_id=request.GET.get('storage_id'), date_at__range=(
                                    request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))[
                                'sum__sum'] is None else \
                            IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                        storage_id=request.GET.get('storage_id'), date_at__range=(
                                    request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(Sum('sum'))[
                                'sum__sum']
                        dictionary2["paid"] = 0 if \
                            IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                        storage_id=request.GET.get('storage_id'), date_at__range=(
                                    request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(
                                Sum('paid_sum'))[
                                'paid_sum__sum'] is None else \
                            IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                        storage_id=request.GET.get('storage_id'), date_at__range=(
                                    request.GET.get('dateFrom'), request.GET.get('dateTo'))).aggregate(
                                Sum('paid_sum'))[
                                'paid_sum__sum']
                        dictionary2["unpaid"] = dictionary2["total"] - dictionary2["paid"]
                        records2.append(dictionary2)
        return render(request, 'lk/supplier_debt.html', context={
            "rows": rows,
            "storages": Storages.objects.all(),
            "products": Products.objects.all(),
            "suppliers": Suppliers.objects.all(),
            "records": records,
            "records2": records2,
            "storage_name": storage_name,
            "storage_id": request.GET.get('storage_id'),
            "dateFrom": get_current_time().strftime('%Y-%m-%d') if request.GET.get(
                'dateFrom') is None else request.GET.get(
                'dateFrom'),
            "dateTo": get_current_time().strftime('%Y-%m-%d') if request.GET.get('dateTo') is None else request.GET.get(
                'dateTo'),
            "ip": ip,
            "date": get_current_time().strftime('%Y-%m-%d')
        })
    else:
        rows = []
        for row in Povarlogs.objects.filter(
                worker__contains=Suppliers.objects.get(id=request.GET.get('supplier_id')).name):
            status = 0
            for record in rows:
                for key, value in record.items():
                    if row.date in key:
                        status = 1
            if status == 0:
                dictionary = dict()
                dictionary[row.date] = \
                    Povarlogs.objects.filter(
                        worker__contains=Suppliers.objects.get(id=request.GET.get('supplier_id')).name,
                        date=row.date).aggregate(Sum('sum'))['sum__sum']
                rows.append(dictionary)
        return render(request, 'lk/supplier_debt_id.html', context={
            "records": rows,
            "rows": Povarlogs.objects.filter(
                worker__contains=Suppliers.objects.get(id=request.GET.get('supplier_id')).name)
        })


def beer_arrival_new(request):
    if request.method == 'POST':
        type = request.POST["type"]
        row = BeerArrival(
            date_at=request.POST["date_at"],
            num=request.POST["num"],
            storage_id=request.POST["storage_id"],
            supplier=Products.objects.get(id=request.POST["product"]).supplier_id,
            product=request.POST["product"],
            amount=request.POST["amount"],
            sum=request.POST["sum"],
            type=type
        )
        row.save()
        if type == 2:
            try:
                supplier = Suppliers.objects.get(
                    supplier_id=Products.objects.get(id=request.POST["product"]).supplier_id).name
            except Suppliers.DoesNotExist:
                supplier = 'Не назначен'
            row = Expenses(
                date_at=request.POST["date_at"],
                storage_id=request.POST["storage_id"],
                expense='Пиво/напитки',
                sum=request.POST["sum"],
                supplier_id=Products.objects.get(id=request.POST["product"]).supplier_id,
                product_id=request.POST["product"],
                num=request.POST["num"],
                is_bn=0,
                comment=supplier + ' // ' + request.POST["num"]
            )
            row.save()
        return redirect('/lk/arrivals')
    return render(request, 'lk/beer_arrival_new.html', context={
        "storages": Storages.objects.all(),
        "products": Products.objects.all()
    })


@login_required
def tovar_requests(request):
    return render(request, 'lk/tovar_requests.html', context={
        "rows": TovarRequests.objects.all(),
        "storages": Storages.objects.all()
    })


@login_required
def partners(request):
    return render(request, 'lk/partners.html', context={
        "rows": Partners.objects.all(),
        "storages": Storages.objects.all(),
        "suppliers": Suppliers.objects.all()
    })


@login_required
def partners_edit(request):
    if request.method == 'POST':
        row = Partners.objects.get(id=request.GET.get('id'))
        row.friendly_name = request.POST["friendly_name"]
        row.type = request.POST["type"]
        row.storage_id = request.POST.get('storage_id', '0')
        row.supplier_id = request.POST.get('supplier_id', '0')
        row.save()
        return redirect('/lk/partners')
    return render(request, 'lk/partners_edit.html', context={
        "row": Partners.objects.get(id=request.GET.get('id')),
        "storages": Storages.objects.all(),
        "types": ExpensesSource.objects.all(),
        "suppliers": Suppliers.objects.all()
    })


def arrivals_edit(request):
    if request.method == 'POST':
        row = BeerArrival.objects.get(id=request.GET.get('id'))
        row.date_at = request.POST["date_at"]
        row.num = request.POST["num"]
        row.storage_id = request.POST["storage_id"]
        row.supplier = request.POST["supplier"]
        row.product = request.POST["product"]
        row.amount = request.POST["amount"]
        row.sum = request.POST["sum"]
        row.type = request.POST["type"]
        row.save()
        return redirect('/lk/arrivals')
    return render(request, 'lk/arrivals_edit.html', context={
        "row": BeerArrival.objects.get(id=request.GET.get('id')),
        "suppliers": Suppliers.objects.all(),
        "products": Products.objects.all(),
        "storages": Storages.objects.all()
    })


def arrivals_copy(request):
    if request.method == 'POST':
        row = BeerArrival(
            date_at=request.POST["date_at"],
            num=request.POST["num"],
            storage_id=request.POST["storage_id"],
            supplier=request.POST["supplier"],
            product=request.POST["product"],
            amount=request.POST["amount"],
            sum=request.POST["sum"],
            type=request.POST["type"]
        )
        row.save()
        return redirect('/lk/arrivals')
    return render(request, 'lk/arrivals_copy.html', context={
        "row": BeerArrival.objects.get(id=request.GET.get('id')),
        "suppliers": Suppliers.objects.all(),
        "products": Products.objects.all(),
        "storages": Storages.objects.all()
    })


@login_required
def arrivals_delete(request):
    BeerArrival.objects.get(id=request.GET.get('id')).delete()
    return redirect('/lk/arrivals')


@login_required
def cards_edit(request):
    if request.method == "POST":
        row = Cards.objects.get(id=request.GET.get('id'))
        row.cafe = request.POST["cafe"]
        row.save()
        return redirect('/lk/statement/cards')
    return render(request, 'lk/cards_edit.html', context={
        "row": Cards.objects.get(id=request.GET.get('id')),
        "storages": Storages.objects.all()
    })


@login_required
def statement_edit(request):
    if request.method == 'POST':
        row = Statement.objects.get(id=request.GET.get('id'))
        row.comment = request.POST["comment"]
        row.save()
        return redirect('/lk/statement?full=1')
    return render(request, 'lk/statement_edit.html', context={
        "row": Statement.objects.get(id=request.GET.get('id')),
        "storages": Storages.objects.all()
    })


@login_required
def statement_cards_sum(request):
    dictionary = dict()
    if request.GET.get('month') is None:
        for card in Cards.objects.all():
            dictionary[card.cafe] = 0 if Statement.objects.filter(card_id=card.id).aggregate(Sum('sum'))[
                                             'sum__sum'] is None else round(
                Statement.objects.filter(card_id=card.id).aggregate(Sum('sum'))['sum__sum'])
    else:
        for card in Cards.objects.all():
            dictionary[card.cafe] = 0 if \
                Statement.objects.filter(card_id=card.id,
                                         date__contains='-' + request.GET.get('month') + '-').aggregate(
                    Sum('sum'))['sum__sum'] is None else round(Statement.objects.filter(card_id=card.id,
                                                                                        date__contains='-' + request.GET.get(
                                                                                            'month') + '-').aggregate(
                Sum('sum'))['sum__sum'])
    return render(request, 'lk/statement_sum_cards.html', context={
        "dict": dictionary,
        "month": 'Все записи' if request.GET.get('month') is None else request.GET.get('month')
    })


@login_required
def revise(request):
    rows = []
    for supplier in Suppliers.objects.all():
        dictionary = dict()
        if supplier.is_revise == 1:
            dictionary['id'] = supplier.id
            if request.GET.get('month') is None:
                dictionary['total'] = 0 if IikoArrivals.objects.filter(supplier_id=supplier.id).aggregate(Sum('sum'))[
                                               'sum__sum'] is None else \
                    IikoArrivals.objects.filter(supplier_id=supplier.id).aggregate(Sum('sum'))['sum__sum']
                try:
                    partner = Partners.objects.get(supplier_id=supplier.id)
                    dictionary['bank'] = 0 if Statement.objects.filter(recipient_id=partner.id).aggregate(Sum('sum'))[
                                                  'sum__sum'] is None else \
                        Statement.objects.filter(recipient_id=partner.id).aggregate(Sum('sum'))['sum__sum']
                except Partners.DoesNotExist:
                    dictionary['bank'] = 'Поставщик не привязан к контрагенту'
                dictionary['bar'] = 0
                dictionary['all'] = 0 if Povarlogs.objects.filter(worker=supplier.friendly_name).aggregate(Sum('sum'))[
                                             'sum__sum'] is None else \
                    Povarlogs.objects.filter(worker=supplier.friendly_name).aggregate(Sum('sum'))['sum__sum']
                dictionary['total_paied'] = dictionary['bank'] + dictionary['bar'] + dictionary[
                    'all'] if 'оставщик' not in str(dictionary['bank']) else dictionary['bar'] + dictionary['all']
                dictionary['difference'] = dictionary['total'] - dictionary['total_paied']
                rows.append(dictionary)
            else:
                dictionary['total'] = 0 if \
                    IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                date_at__month=request.GET.get('month')).aggregate(
                        Sum('sum'))[
                        'sum__sum'] is None else \
                    IikoArrivals.objects.filter(supplier_id=supplier.id,
                                                date_at__month=request.GET.get('month')).aggregate(Sum('sum'))[
                        'sum__sum']
                try:
                    partner = Partners.objects.get(supplier_id=supplier.id)
                    dictionary['bank'] = 0 if Statement.objects.filter(recipient_id=partner.id,
                                                                       date__contains='-' + request.GET.get(
                                                                           'month') + '-').aggregate(Sum('sum'))[
                                                  'sum__sum'] is None else \
                        Statement.objects.filter(recipient_id=partner.id,
                                                 date__contains='-' + request.GET.get('month') + '-').aggregate(
                            Sum('sum'))['sum__sum']
                except Partners.DoesNotExist:
                    dictionary['bank'] = 'Поставщик не привязан к контрагенту'
                dictionary['bar'] = 0
                dictionary['all'] = 0 if Povarlogs.objects.filter(worker=supplier.friendly_name,
                                                                  date__contains='-' + request.GET.get(
                                                                      'month') + '-').aggregate(Sum('sum'))[
                                             'sum__sum'] is None else \
                    Povarlogs.objects.filter(worker=supplier.friendly_name,
                                             date__contains='-' + request.GET.get('month') + '-').aggregate(Sum('sum'))[
                        'sum__sum']
                dictionary['total_paied'] = dictionary['bank'] + dictionary['bar'] + dictionary[
                    'all'] if 'оставщик' not in str(dictionary['bank']) else dictionary['bar'] + dictionary['all']
                dictionary['difference'] = dictionary['total'] - dictionary['total_paied']
                rows.append(dictionary)
    return render(request, 'lk/revise.html', context={
        "rows": rows,
        "suppliers": Suppliers.objects.all(),
    })


@login_required
def tovar_requests_edit(request):
    row = TovarRequests.objects.get(id=request.GET.get('id'))
    if request.method == "POST":
        if request.POST.get('status') is not None:
            row.status = 1
        else:
            row.status = 0
        row.save()
        return redirect('/lk/tovar_requests')
    return render(request, 'lk/tovar_requests_edit.html', context={
        "row": row
    })
