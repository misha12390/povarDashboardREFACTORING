from django.db.models import Sum
from django.shortcuts import render, redirect
from .models import Employee, Timetable, Positions, Money, Expenses, ExpensesSource, Pays, PayinText, Salary, Storages, \
    Products, Inventory, Categories, AutoSalary, Paymenttypes
from functions import *
import datetime
import xml.etree.ElementTree as ET
import json


def index(request):
    code = request.GET.get("code")
    storage_id = getStorageId(code)
    date_at = getTime()

    try:
        sum_cash_morning = Money.objects.get(storage_id=storage_id, date_at=date_at).sum_cash_morning
    except Money.DoesNotExist:
        sum_cash_morning = None

    try:
        sum_cash_end_day = Money.objects.get(storage_id=storage_id, date_at=date_at).sum_cash_end_day
    except Money.DoesNotExist:
        sum_cash_end_day = None
    return render(request, 'bar/bar.html', context={
        "code": code,
        "cafe": getStorageName(code),
        "date": date_at,
        "storage_id": getStorageId(code),
        "employees": Employee.objects.all(),
        "positions": Positions.objects.all(),
        "sum_cash_morning": sum_cash_morning,
        "sum_cash_end_day": sum_cash_end_day,
        "rows": Timetable.objects.filter(storage_id=storage_id, date_at=date_at),
        "barmen": Timetable.objects.filter(storage_id=storage_id, date_at=date_at, position_id=1).count(),
        "teh": Timetable.objects.filter(storage_id=storage_id, date_at=date_at, position_id=9).count(),
    })


def timetable_save(request):
    code = None
    if request.method == 'POST':
        code = request.POST["code"]

        for position in Positions.objects.all():
            if position.id == 1 and Timetable.objects.filter(storage_id=getStorageId(code), date_at=getTime(),
                                                             position_id=1).count() > 0:
                continue
            elif position.id == 9 and Timetable.objects.filter(storage_id=getStorageId(code), date_at=getTime(),
                                                               position_id=9).count() > 0:
                continue
            elif '(' in position.position:
                if int(request.POST[f"position[{position.id}]"]) > 0:
                    oklad = 0
                    if 'армен вызывной (осн' in position.position:
                        oklad = Employee.objects.get(id=request.POST[f"position[{position.id}]"]).oklad
                    if 'армен вызывной (усил' in position.position:
                        oklad = Employee.objects.get(id=request.POST[f"position[{position.id}]"]).oklad - 400
                    if 'овар вызывной (осн' in position.position:
                        oklad = Employee.objects.get(id=request.POST[f"position[{position.id}]"]).oklad
                    if 'овар вызывной (усио' in position.position:
                        oklad = Employee.objects.get(id=request.POST[f"position[{position.id}]"]).oklad - 1200
                    row = Timetable(
                        created_at=get_current_time(),
                        date_at=getTime(),
                        storage_id=getStorageId(code),
                        employee_id=request.POST[f"position[{position.id}]"],
                        position_id=position.id,
                        oklad=oklad
                    )
                    row.save()
            else:
                if int(request.POST[f"position[{position.id}]"]) > 0:
                    row = Timetable(
                        created_at=get_current_time(),
                        date_at=getTime(),
                        storage_id=getStorageId(code),
                        employee_id=request.POST[f"position[{position.id}]"],
                        position_id=position.id,
                        oklad=Employee.objects.get(id=request.POST[f"position[{position.id}]"]).oklad
                    )
                    row.save()
        if Money.objects.filter(storage_id=getStorageId(code), date_at=getTime()).count() == 0:
            if int(request.POST["sum_cash_morning"]) >= 0:
                row = Money(
                    created_at=get_current_time(),
                    date_at=getTime(),
                    storage_id=getStorageId(code),
                    sum_cash_morning=request.POST["sum_cash_morning"]
                )
                row.save()
    return redirect('/bar?code=' + code)


def timetable_delete(request):
    try:
        row = Timetable.objects.get(id=request.GET.get('id'))
        if str(row.date_at) == getTime():
            row.delete()
    except Timetable.DoesNotExist:
        pass
    return redirect('/bar?code=' + request.GET["code"])


def month_salary(request):
    code = request.GET.get("code")

    return render(request, 'bar/month_salary.html', context={
        "code": code,
        "storage_id": getStorageId(code),
        "cafe": getStorageName(code),
        "date": getTime(),
        "employees": Employee.objects.all(),
        "timetable": Employee.objects.filter(storage_id=getStorageId(code), is_deleted='Активен'),
        "salaries": Salary.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=2),
    })


def month_salary_save(request):
    if request.method == 'POST':
        code = request.GET.get('code')
        count = Employee.objects.filter(storage_id=getStorageId(code), is_deleted='Активен')

        for a in count:
            if request.POST[f"[{a.id}][salary]"] != "":
                rows = Salary.objects.filter(employee_id=a.id,
                                             date_at=getTime(), type=2).count()
                if rows == 0:
                    obj = Salary(
                        employee_id=a.id,
                        storage_id=getStorageId(code),
                        type=2,
                        oklad=int(request.POST[f"[{a.id}][salary]"]),
                        date_at=getTime(),
                        created_at=get_current_time().strftime("%Y-%m-%d"),
                        percent=0,
                        premium=0,
                        month=request.POST["month"],
                        days=request.POST["days"]
                    )
                    obj.save()
                else:
                    row = Salary.objects.get(employee_id=a.id,
                                             date_at=getTime(), type=2)
                    row.created_at = get_current_time().strftime("%Y-%m-%d"),
                    row.oklad = int(request.POST[f"[{a.id}][salary]"])
                    row.month = request.POST["month"]
                    row.days = request.POST["days"]

                    row.save()
    return redirect('/bar/month_salary?code=' + request.GET.get('code'))


def salary(request):
    code = request.GET.get("code")

    return render(request, 'bar/salary.html', context={
        "code": code,
        "date": getTime(),
        "cafe": getStorageName(code),
        "salaries": Salary.objects.filter(storage_id=getStorageId(code), date_at=getTime()),
        "employees": Employee.objects.all(),
        "timetable": Timetable.objects.filter(storage_id=getStorageId(code), date_at=getTime())
    })


def salary_save(request):
    code = None
    if request.method == 'POST':
        code = request.POST["code"]

        count = Timetable.objects.filter(storage_id=getStorageId(code), date_at=getTime())

        for a in count:
            if request.POST[f"[{a.employee_id}][percent]"] == '':
                percent = 0
            else:
                percent = int(request.POST[f"[{a.employee_id}][percent]"])
            if request.POST[f"[{a.employee_id}][oklad]"] == '':
                oklad = 0
            else:
                oklad = int(request.POST[f"[{a.employee_id}][oklad]"])
            if request.POST[f"[{a.employee_id}][premium]"] == '':
                premium = 0
            else:
                premium = int(request.POST[f"[{a.employee_id}][premium]"])
            if request.POST[f"[{a.employee_id}][oklad]"] != "" or request.POST[f"[{a.employee_id}][percent]"] != "" or \
                    request.POST[f"[{a.employee_id}][premium]"] != "":
                rows = Salary.objects.filter(employee_id=a.employee_id,
                                             date_at=getTime(), type=1).count()
                if rows == 0:
                    obj = Salary(
                        employee_id=a.employee_id,
                        storage_id=getStorageId(code),
                        type=1,
                        oklad=oklad,
                        date_at=getTime(),
                        created_at=get_current_time().strftime("%Y-%m-%d"),
                        percent=percent,
                        premium=premium,
                    )
                    obj.save()
                else:
                    row = Salary.objects.get(employee_id=a.employee_id,
                                             date_at=getTime(), type=1)
                    row.created_at = get_current_time().strftime("%Y-%m-%d"),
                    if oklad != 0:
                        row.oklad = oklad
                    if percent != 0:
                        row.percent = percent
                    if premium != 0:
                        row.premium = premium

                    row.save()
    return redirect('/bar/salary?code=' + code)


def expenses(request):
    code = request.GET.get("code")

    return render(request, 'bar/expenses.html', context={
        "code": code,
        "date": getTime(),
        "cafe": getStorageName(code),
        "expenses": Expenses.objects.filter(storage_id=getStorageId(code), date_at=getTime()),
        "data": PayinText.objects.all(),
        "rows": ExpensesSource.objects.filter(is_active=1, type=3),
        "employees": Employee.objects.all(),
        "timetable": Timetable.objects.filter(
            date_at=getTime(), storage_id=getStorageId(code)),
        "pays": Pays.objects.filter(date_at=getTime(), storage_id=getStorageId(code))
    })


def expenses_save(request):
    if request.method == 'POST':
        code = request.POST["code"]
        pay_type = request.POST["pay_type"]

        if int(pay_type) >= 0:
            for record in ExpensesSource.objects.filter(is_active=1, type=3):
                if len(request.POST[f"{record.input_name}_sum"]) > 1:
                    row = Expenses(
                        storage_id=getStorageId(code),
                        created_at=get_current_time(),
                        date_at=getTime(),
                        name=record.text,
                        comment=request.POST[f"{record.input_name}_comment"],
                        sum=request.POST[f"{record.input_name}_sum"],
                        is_bn=pay_type
                    )
                    row.save()

        return redirect('/bar/expenses?code=' + code)


def expenses_delete(request):
    try:
        row = Expenses.objects.get(id=request.GET.get('id'))
        if str(row.date_at) == getTime():
            row.delete()
    except Expenses.DoesNotExist:
        pass
    return redirect('/bar/expenses?code=' + request.GET.get('code'))


def pays_save(request):
    if request.method == 'POST':
        code = request.POST["code"]

        payin_comment = request.POST["payin_comment"]
        payin_sum = request.POST["payin_sum"]

        payout_comment = request.POST["payout_comment"]
        payout_sum = request.POST["payout_sum"]

        if len(payout_sum) > 2:
            row = Pays(
                storage_id=getStorageId(code),
                created_at=get_current_time(),
                date_at=getTime(),
                type=2,
                comment=payout_comment,
                sum=payout_sum
            )
            row.save()
        if len(payin_sum) > 2:
            row = Pays(
                storage_id=getStorageId(code),
                created_at=get_current_time(),
                date_at=getTime(),
                type=1,
                comment=payin_comment,
                sum=payin_sum
            )
            row.save()
        return redirect('/bar/expenses?code=' + code)


def inventory(request):
    pass


def inventory_form(request, storageId):
    pass


def inventory_table(request):
    pass


def end_day(request):
    code = request.GET.get("code")
    pointOfSale = getPointOfSale(code)
    total_day = 0
    openDate = None
    closeDate = None
    sessionNumber = 0
    cash = 0
    cash_point = 0
    delivery = 0
    yandex = 0
    total_cashshifts = 0

    next_day = get_current_time() + datetime.timedelta(days=1)
    jsonData = getIikoCashShifts2((get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
                                  next_day.strftime('%Y-%m-%d'))
    dictData = json.loads(jsonData)
    for i in range(len(dictData)):
        if dictData[i]["pointOfSaleId"] == pointOfSale:
            first_data = getSalesByDepartment(dictData[i]["id"])
            data = json.loads(first_data)
            total_day = dictData[i]["payOrders"]
            openDate = dictData[i]["openDate"]
            closeDate = dictData[i]["closeDate"]
            sessionNumber = dictData[i]["sessionNumber"]

            for a in range(len(data["cashlessRecords"])):
                row = Paymenttypes.objects.get(payment_id=data["cashlessRecords"][a]["info"]["paymentTypeId"])
                if row.name == 'Наличные':
                    cash += int(data["cashlessRecords"][a]["info"]["sum"])
                if row.name == 'Наличные.':
                    cash_point += int(data["cashlessRecords"][a]["info"]["sum"])
                if row.name == 'Delivery Club':
                    delivery += int(data["cashlessRecords"][a]["info"]["sum"])
                if row.name == 'Яндекс ЕДА' or row.name == '-Яндекс ЕДА':
                    yandex += int(data["cashlessRecords"][a]["info"]["sum"])
                total_cashshifts += data["cashlessRecords"][a]["info"]["sum"]

    nal = int(total_day) - int(total_cashshifts)
    sumNal = int(cash) + nal + int(cash_point)
    sumBN = int(total_day) - sumNal - int(yandex) - int(delivery)

    if openDate is not None:
        openDate = openDate.split('T')[0] + ' ' + openDate.split('T')[1]

    sum_for_percent = total_day - int(yandex) - int(delivery)
    expensesNal = 0 if \
        Expenses.objects.filter(storage_id=getStorageId(code), date_at=getTime(), is_bn=0).aggregate(Sum('sum'))[
            'sum__sum'] is None else \
        Expenses.objects.filter(storage_id=getStorageId(code), date_at=getTime(), is_bn=0).aggregate(Sum('sum'))[
            'sum__sum']
    monthly_salary = 0 if \
        Salary.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=2).aggregate(Sum('oklad'))[
            'oklad__sum'] is None else \
        Salary.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=2).aggregate(Sum('oklad'))[
            'oklad__sum']
    total_salary = 0 if Salary.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=1).aggregate(
        total_sum=Sum('oklad') + Sum('percent') + Sum('premium'))['total_sum'] is None else \
        Salary.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=1).aggregate(
            total_sum=Sum('oklad') + Sum('percent') + Sum('premium'))['total_sum']
    payin = 0 if Pays.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=1).aggregate(Sum('sum'))[
                     'sum__sum'] is None else \
        Pays.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=1).aggregate(Sum('sum'))['sum__sum']
    payout = 0 if Pays.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=2).aggregate(Sum('sum'))[
                      'sum__sum'] is None else \
        Pays.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=2).aggregate(Sum('sum'))['sum__sum']

    try:
        row = Money.objects.get(storage_id=getStorageId(code), date_at=getTime())
        morning = row.sum_cash_morning
        difference = row.difference
        calculated = row.calculated
        end = None if row.sum_cash_end_day is None else row.sum_cash_end_day
    except Money.DoesNotExist:
        morning = 0
        calculated = 0
        difference = 0
        end = None

    return render(request, 'bar/end.html', context={
        "code": code,
        "cafe": getStorageName(code),
        "date": getTime(),
        "payOrders": total_day,
        "openDate": openDate,
        "closeDate": closeDate,
        "sessionId": sessionNumber,
        "cash": cash,
        "cash_point": cash_point,
        "delivery": delivery,
        "yandex": yandex,
        "sumNal": sumNal,
        "sumBN": sumBN,
        "nal": int(cash) + nal,
        "nal_point": cash_point,
        "sum_for_percent": sum_for_percent,
        "expensesNal": expensesNal,
        "monthly_salary": monthly_salary,
        "total_salary": total_salary,
        "payin": payin,
        "payout": payout,
        "morning": morning,
        "calculated": calculated,
        "difference": difference,
        "end": end
    })


def end_day_save(request):
    code = None
    if request.method == 'POST':
        code = request.POST["code"]
        total_cash = request.POST["sumNal"]
        total_bn = request.POST["sumBN"]
        total_day = request.POST["total_day"]
        yandex = request.POST["yandex"]
        delivery = request.POST["delivery"]
        cash = request.POST["cash"]

        record = Money.objects.get(storage_id=getStorageId(code), date_at=getTime())

        expensesNal = 0 if \
            Expenses.objects.filter(storage_id=getStorageId(code), date_at=getTime(), is_bn=0).aggregate(Sum('sum'))[
                'sum__sum'] is None else \
            Expenses.objects.filter(storage_id=getStorageId(code), date_at=getTime(), is_bn=0).aggregate(Sum('sum'))[
                'sum__sum']
        monthly_salary = 0 if \
            Salary.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=2).aggregate(Sum('oklad'))[
                'oklad__sum'] is None else \
            Salary.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=2).aggregate(Sum('oklad'))[
                'oklad__sum']
        total_salary = 0 if Salary.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=1).aggregate(
            total_sum=Sum('oklad') + Sum('percent') + Sum('premium'))['total_sum'] is None else \
            Salary.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=1).aggregate(
                total_sum=Sum('oklad') + Sum('percent') + Sum('premium'))['total_sum']
        payin = 0 if \
        Pays.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=1).aggregate(Sum('sum'))[
            'sum__sum'] is None else \
            Pays.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=1).aggregate(Sum('sum'))[
                'sum__sum']
        payout = 0 if \
        Pays.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=2).aggregate(Sum('sum'))[
            'sum__sum'] is None else \
            Pays.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=2).aggregate(Sum('sum'))[
                'sum__sum']

        calculated = int(record.sum_cash_morning) + int(total_cash) - int(expensesNal) - int(total_salary) - int(monthly_salary) + int(payin) - int(payout)

        difference = int(cash) - calculated

        record.sum_cash_end_day = cash
        record.total_day = total_day
        record.total_cash = total_cash
        record.total_bn = total_bn
        record.calculated = calculated
        record.difference = difference
        record.total_market = int(yandex) + int(delivery)
        record.total_salary = int(total_salary) + int(monthly_salary)
        record.total_expenses = int(expensesNal)
        record.payin = int(payin)
        record.payout = int(payout)
        record.save()
    return redirect('/bar/end?code=' + code)


def auto_salary(request):
    code = request.GET.get("code")
    percent_num = None
    storage_id = getStorageId(code)
    cafe = getStorageName(code)
    pointOfSale = getPointOfSale(code)
    payOrders = None
    delivery = 0
    yandex = 0
    next_day = (get_current_time() - datetime.timedelta(hours=2)) + datetime.timedelta(days=1)

    root = ET.fromstring(getIikoCashShifts((get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
                                           next_day.strftime('%Y-%m-%d')))

    for country in root.findall('CloseSessionItemDto'):
        if country.find('pointOfSale').text == pointOfSale:
            payOrders = country.find('payOrders').text

    if payOrders == '':
        total_market = 0
    else:
        total_market = int(payOrders.split('.')[0])

    jsonData = getIikoCashShifts2((get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
                                  next_day.strftime('%Y-%m-%d'))
    dictData = json.loads(jsonData)
    for i in range(len(dictData)):
        if dictData[i]["pointOfSaleId"] == pointOfSale:
            first_data = getSalesByDepartment(dictData[i]["id"])
            data = json.loads(first_data)

            for a in range(len(data["cashlessRecords"])):
                row = Paymenttypes.objects.get(payment_id=data["cashlessRecords"][i]["info"]["paymentTypeId"])
                if row.name == 'Delivery Club':
                    delivery += int(data["cashlessRecords"][a]["info"]["sum"])
                if row.name == 'Яндекс ЕДА' or row.name == '-Яндекс ЕДА':
                    yandex += int(data["cashlessRecords"][a]["info"]["sum"])

    sum_for_percent = int(total_market) - int(yandex) - int(delivery)

    AutoSalary.objects.all().delete()
    records = Timetable.objects.filter(date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
                                       storage_id=storage_id)
    if records.count() > 0:
        for record in records:

            barmen_count = 0
            barmen_count += int(Timetable.objects.filter(
                date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime("%Y-%m-%d"),
                storage_id=storage_id, position_id=1).count())
            barmen_count += int(Timetable.objects.filter(
                date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime("%Y-%m-%d"),
                storage_id=storage_id, position_id=2).count())
            barmen_count += int(Timetable.objects.filter(
                date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime("%Y-%m-%d"),
                storage_id=storage_id, position_id=11).count())
            barmen_count += int(Timetable.objects.filter(
                date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime("%Y-%m-%d"),
                storage_id=storage_id, position_id=12).count())

            position = Positions.objects.get(id=record.position_id)

            if barmen_count > 1:
                percent_num = '2.5'
            else:
                percent_num = '3'

            if 'Повар' in position.position or 'Тех' in position.position or 'Бармен стажер' in position.position:
                percent = 0
            else:
                percent = int(sum_for_percent) * (float(percent_num) / 100)

            if 'Бармен' not in position.position:
                if 60000 <= total_market < 70000:
                    premium = 200
                elif 70000 <= total_market < 100000:
                    premium = 500
                elif total_market >= 100000:
                    premium = 1000
                else:
                    premium = 0
            else:
                if 'стажер' not in position.position:
                    if 60000 <= sum_for_percent < 70000:
                        premium = 200
                    elif 70000 <= sum_for_percent < 100000:
                        premium = 500
                    elif sum_for_percent >= 100000:
                        premium = 1000
                    else:
                        premium = 0
                else:
                    premium = 0

            fine = 0

            if AutoSalary.objects.filter(storage_id=storage_id,
                                         date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime(
                                             "%Y-%m-%d"), id=record.employee_id).count() == 0:
                row = AutoSalary(
                    id=record.employee_id,
                    fio=Employee.objects.get(id=record.employee_id).fio,
                    date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime("%Y-%m-%d"),
                    storage_id=storage_id,
                    oklad=record.oklad,
                    percent=percent,
                    premium=premium,
                    fine=fine,
                    total=int(record.oklad) + int(percent) + int(premium) - int(fine)
                )
                row.save()
            else:
                row = AutoSalary.objects.get(storage_id=storage_id,
                                             date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime(
                                                 "%Y-%m-%d"), id=record.employee_id)
                row.id = record.employee_id
                row.fio = Employee.objects.get(id=record.employee_id).fio
                row.oklad = record.oklad
                row.percent = percent
                row.premium = premium
                row.fine = fine
                row.total = int(record.oklad) + int(percent) + int(premium) - int(fine)
                row.save()

    else:
        percent_num = 0

    return render(request, 'bar/auto_salary.html', context={
        "cafe": cafe,
        "storage_id": storage_id,
        "code": code,
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime('%d.%m.%Y'),
        "percent": percent_num,
        "sum_for_percent": sum_for_percent,
        "employees": Employee.objects.all(),
        "rows": AutoSalary.objects.filter(
            date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime("%Y-%m-%d"), storage_id=storage_id),
        "salary_sum":
            AutoSalary.objects.filter(date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime("%Y-%m-%d"),
                                      storage_id=storage_id).aggregate(Sum('total'))['total__sum'],
    })
