from django.shortcuts import render, redirect
from bar.models import \
    ExpensesSource, PayinText, Categories, Products, Inventory, Storages, Paymenttypes, Employee, Timetable, Money, \
    Expenses, Pays, \
    Salary, AutoSalary, Calendar, Blacklist, TovarRequests, Suppliers, BeerArrival, Povarlogs
from django.db.models import Sum
import xml.etree.ElementTree as ET
import json
from calendar import monthrange
from functions import *
import requests


def send_webhk(chat_id, message, id):
    send_text = ''
    if id == 1:  # crm
        send_text = 'https://api.telegram.org/botBOT_API/sendMessage?chat_id=' + chat_id + '&text=' + message
    elif id == 2:  # ?
        send_text = 'https://api.telegram.org/botBOT_API/sendMessage?chat_id=' + chat_id + '&text=' + message
    elif id == 3:  # test
        send_text = 'https://api.telegram.org/botBOT_API/sendMessage?chat_id=' + chat_id + '&text=' + message
    response = requests.get(send_text)
    return response.json()


# [ Functions ]

def update_money(pk, storage_id):
    row = -1
    if pk == 1:
        salary = Salary.objects.filter(date=getTime(),
                                       storage_id=storage_id).aggregate(Sum('itogo'))['itogo__sum']
        row = Money.objects.get(date_at=getTime(),
                                storage_id=storage_id)
        row.total_salary = salary
    elif pk == 2:
        expenses = \
            Expenses.objects.filter(date_at=getTime(),
                                    storage_id=storage_id).aggregate(Sum('sum'))['sum__sum']
        row = Money.objects.get(date_at=getTime(),
                                storage_id=storage_id)
        row.total_expenses = expenses
    total_cash = 0 if row.total_cash is None else row.total_cash
    total_expenses = 0 if row.total_expenses is None else row.total_expenses
    total_salary = 0 if row.total_salary is None else row.total_salary
    payin = 0 if row.payin is None else row.payin
    payout = 0 if row.payout is None else row.payout
    end_day = 0 if row.sum_cash_end_day is None else row.sum_cash_end_day
    row.difference = row.sum_cash_morning + total_cash - total_expenses - total_salary + payin - payout
    row.save()
    row.difference2 = end_day - int(row.difference)
    row.save()


# [ Pages ]
def bar(request):
    if request.method == 'POST':
        storage_id = request.POST["cafe"]
        codee = request.POST["code"]
        cafe = request.POST["cafee"]
        if Timetable.objects.filter(date_at=getTime(),
                                    storage_id=storage_id, position='Бармен основной').count() == 0:
            barmen = request.POST["barmen"]
        else:
            barmen = 0
        barmen_plus = request.POST["barmen_plus"]
        barmen_call = request.POST["barmen_call"]
        barmen_stazh = request.POST["barmen_stazh"]

        povar = request.POST["povar"]
        povar_plus = request.POST["povar_plus"]
        povar_call = request.POST["povar_call"]
        povar_stazh = request.POST["povar_stazh"]

        call = request.POST["call"]
        call2 = request.POST["call2"]

        sum_cash_morning = 0
        sum_cash_end_day = 0

        dateFromm = get_current_time() - datetime.timedelta(days=1)
        dateFrom = dateFromm.strftime('%Y-%m-%d')

        if Money.objects.filter(date_at=getTime(),
                                storage_id=storage_id).count() == 0:
            cash = request.POST["cash"]
            ak = Money(
                storage_id=storage_id,
                created_at=get_current_time().strftime("%Y-%m-%d %H:%M:%S"),
                date_at=getTime(),
                sum_cash_morning=cash,
            )
            ak.save()
            row = Money.objects.get(date_at=dateFrom, storage_id=storage_id)

            if row.sum_cash_end_day is None:
                sum_cash_end_day = 0
            else:
                sum_cash_end_day = row.sum_cash_end_day
            data = 'Заведение: ' + cafe + '%0A%0AКасса утро ' + get_current_time().strftime(
                '%Y-%m-%d %H:%M:%S') + ': ' + \
                   str(cash) + '%0AКасса вечер ' + dateFrom + ': ' + str(sum_cash_end_day) + \
                   '%0A%0AРазница: ' + str(int(cash) - int(sum_cash_end_day))
            send_webhk('chat_id', data, 1)
        else:
            cash = ''

        if Money.objects.filter(date_at=dateFrom, storage_id=storage_id).count() > 0:
            row = Money.objects.get(date_at=dateFrom, storage_id=storage_id)
            row2 = Money.objects.get(date_at=getTime(),
                                     storage_id=storage_id)

            if row2.sum_cash_morning is None:
                sum_cash_morning = 0
            else:
                sum_cash_morning = row2.sum_cash_morning

            if row.sum_cash_end_day is None:
                sum_cash_end_day = 0
            else:
                sum_cash_end_day = row.sum_cash_end_day

        if Timetable.objects.filter(date_at=getTime(),
                                    storage_id=storage_id, position='Тех. служащий').count() == 0:
            teh = request.POST["teh"]
        else:
            teh = 0
        teh_call = request.POST["teh_call"]

        if Money.objects.filter(date_at=getTime(),
                                storage_id=storage_id).count() > 0:
            if int(barmen) > 0:
                obj = Employee.objects.get(id=barmen)
                if Timetable.objects.filter(
                        date_at=getTime(),
                        storage_id=storage_id, employee_id=obj.id).count() == 0:
                    a = Timetable(
                        employee_id=obj.id,
                        storage_id=storage_id,
                        created_at=get_current_time().strftime("%Y-%m-%d %H:%M:%S"),
                        date_at=getTime(),
                        position='Бармен основной',
                        position_base_id=0,
                        oklad=obj.oklad
                    )
                    a.save()
            if int(barmen_call) > 0:
                obj = Employee.objects.get(id=barmen_call)
                if Timetable.objects.filter(
                        date_at=getTime(),
                        storage_id=storage_id, employee_id=obj.id).count() == 0:
                    oklad_barmen = obj.oklad
                    s = 'Бармен вызывной '
                    if int(call) == 2:
                        oklad_barmen = int(obj.oklad) - 400
                        s += '(усиление)'
                    elif int(call) == 1:
                        s += '(основной)'
                    a = Timetable(
                        employee_id=obj.id,
                        storage_id=storage_id,
                        created_at=get_current_time().strftime("%Y-%m-%d %H:%M:%S"),
                        date_at=getTime(),
                        position=s,
                        position_base_id=0,
                        oklad=oklad_barmen
                    )
                    a.save()
            if int(barmen_plus) > 0:
                obj = Employee.objects.get(id=barmen_plus)
                if Timetable.objects.filter(
                        date_at=getTime(),
                        storage_id=storage_id, employee_id=obj.id).count() == 0:
                    a = Timetable(
                        employee_id=obj.id,
                        storage_id=storage_id,
                        created_at=get_current_time().strftime("%Y-%m-%d %H:%M:%S"),
                        date_at=getTime(),
                        position='Бармен усиление',
                        position_base_id=0,
                        oklad=int(obj.oklad) - 400
                    )
                    a.save()
            if int(barmen_stazh) > 0:
                obj = Employee.objects.get(id=barmen_stazh)
                if Timetable.objects.filter(
                        date_at=getTime(),
                        storage_id=storage_id, employee_id=obj.id).count() == 0:
                    a = Timetable(
                        employee_id=obj.id,
                        storage_id=storage_id,
                        created_at=get_current_time().strftime("%Y-%m-%d %H:%M:%S"),
                        date_at=getTime(),
                        position='Бармен стажер',
                        position_base_id=0,
                        oklad='500'
                    )
                    a.save()
            if int(povar) > 0:
                obj = Employee.objects.get(id=povar)
                if Timetable.objects.filter(
                        date_at=getTime(),
                        storage_id=storage_id, employee_id=obj.id).count() == 0:
                    a = Timetable(
                        employee_id=obj.id,
                        storage_id=storage_id,
                        created_at=get_current_time().strftime("%Y-%m-%d %H:%M:%S"),
                        date_at=getTime(),
                        position='Повар основной',
                        position_base_id=0,
                        oklad=obj.oklad
                    )
                    a.save()
            if int(povar_plus) > 0:
                obj = Employee.objects.get(id=povar_plus)
                oklad = obj.oklad - 1300 if obj.type == 'Су-Шеф' else obj.oklad - 1100
                if obj.type == 'Бренд-Шеф':
                    oklad = 0
                if Timetable.objects.filter(
                        date_at=getTime(),
                        storage_id=storage_id, employee_id=obj.id).count() == 0:
                    a = Timetable(
                        employee_id=obj.id,
                        storage_id=storage_id,
                        created_at=get_current_time().strftime("%Y-%m-%d %H:%M:%S"),
                        date_at=getTime(),
                        position='Повар усиление',
                        position_base_id=0,
                        oklad=oklad
                    )
                    a.save()
            if int(povar_stazh) > 0:
                obj = Employee.objects.get(id=povar_stazh)
                if Timetable.objects.filter(
                        date_at=getTime(),
                        storage_id=storage_id, employee_id=obj.id).count() == 0:
                    a = Timetable(
                        employee_id=obj.id,
                        storage_id=storage_id,
                        created_at=get_current_time().strftime("%Y-%m-%d %H:%M:%S"),
                        date_at=getTime(),
                        position='Повар стажер',
                        position_base_id=0,
                        oklad=obj.oklad
                    )
                    a.save()
            if int(povar_call) > 0:
                obj = Employee.objects.get(id=povar_call)
                if Timetable.objects.filter(
                        date_at=getTime(),
                        storage_id=storage_id, employee_id=obj.id).count() == 0:
                    oklad_barmen = obj.oklad
                    s = 'Повар вызывной '
                    if int(call2) == 2:
                        s += '(усиление)'
                        oklad_barmen = obj.oklad - 1300 if obj.type == 'Су-Шеф' else obj.oklad - 1100
                        if obj.type == 'Бренд-Шеф':
                            oklad_barmen = 0
                    elif int(call2) == 1:
                        s += '(основной)'
                    a = Timetable(
                        employee_id=obj.id,
                        storage_id=storage_id,
                        created_at=get_current_time().strftime("%Y-%m-%d %H:%M:%S"),
                        date_at=getTime(),
                        position=s,
                        position_base_id=0,
                        oklad=oklad_barmen
                    )
                    a.save()
            if int(teh) > 0:
                obj = Employee.objects.get(id=teh)
                if Timetable.objects.filter(
                        date_at=getTime(),
                        storage_id=storage_id, employee_id=obj.id).count() == 0:
                    a = Timetable(
                        employee_id=obj.id,
                        storage_id=storage_id,
                        created_at=get_current_time().strftime("%Y-%m-%d %H:%M:%S"),
                        date_at=getTime(),
                        position='Тех. служащий',
                        position_base_id=0,
                        oklad=obj.oklad
                    )
                    a.save()
            if int(teh_call) > 0:
                obj = Employee.objects.get(id=teh_call)
                if Timetable.objects.filter(
                        date_at=getTime(),
                        storage_id=storage_id, employee_id=obj.id).count() == 0:
                    a = Timetable(
                        employee_id=obj.id,
                        storage_id=storage_id,
                        created_at=get_current_time().strftime("%Y-%m-%d %H:%M:%S"),
                        date_at=getTime(),
                        position='Тех. служащий вызывной',
                        position_base_id=0,
                        oklad=obj.oklad
                    )
                    a.save()
        return redirect('/bar?code=' + codee)
    code = request.GET["code"]
    cafe = getStorageName(code)
    storage_id = getStorageId(code)

    if Money.objects.filter(date_at=getTime(),
                            storage_id=storage_id).count() == 0:
        cash_morning = 0
    else:
        al = Money.objects.get(date_at=getTime(),
                               storage_id=storage_id)
        cash_morning = al.sum_cash_morning
    return render(request, "bar/bar.html", context={
        "code": code,
        "cafe": cafe,
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime("%d.%m.%Y"),
        "storage_id": storage_id,
        "employees": Employee.objects.all(),
        "timetable": Timetable.objects.filter(
            date_at=getTime()),
        "barmen": Timetable.objects.filter(
            date_at=getTime(), storage_id=storage_id,
            position='Бармен основной').count(),
        "teh": Timetable.objects.filter(date_at=getTime(),
                                        storage_id=storage_id, position='Тех. служащий').count(),
        "money": Money.objects.filter(date_at=getTime(),
                                      storage_id=storage_id).count(),
        "cash_morning": cash_morning,
        "barmen_call": Timetable.objects.filter(
            date_at=getTime(), storage_id=storage_id,
            position='Бармен вызывной (основной)').count()
    })


def bar_expenses(request):
    code = request.GET["code"]
    storage_id = getStorageId(code)
    cafe = getStorageName(code)

    return render(request, 'bar/bar_expenses.html', context={
        "cafe": cafe,
        "code": code,
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime("%d.%m.%Y"),
        "storage_id": storage_id,
        "data": PayinText.objects.all(),
        "rows": ExpensesSource.objects.filter(is_active=1, type=3),
        "employees": Employee.objects.all(),
        "timetable": Timetable.objects.filter(
            date_at=getTime(), storage_id=storage_id),
        "expenses_sum":
            Expenses.objects.filter(date_at=getTime(),
                                    storage_id=storage_id).aggregate(Sum('sum'))['sum__sum'],
        "all_expenses_card":
            Expenses.objects.filter(date_at=getTime(),
                                    storage_id=storage_id, is_bn=1).aggregate(Sum('sum'))['sum__sum'],
        "all_expenses_nal":
            Expenses.objects.filter(date_at=getTime(),
                                    storage_id=storage_id, is_bn=0).aggregate(Sum('sum'))['sum__sum'],
        "expenses": Expenses.objects.filter(
            date_at=getTime(), storage_id=storage_id),
        "pays": Pays.objects.filter(date_at=getTime(),
                                    storage_id=storage_id),
        "all_pays": Pays.objects.filter(date_at=getTime(),
                                        storage_id=storage_id).aggregate(Sum('sum'))['sum__sum']
    })


def bar_expenses_save(request):
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
                        expense=record.text,
                        comment=request.POST[f"{record.input_name}_comment"],
                        sum=request.POST[f"{record.input_name}_sum"],
                        is_bn=pay_type
                    )
                    row.save()

        return redirect('/bar/expenses?code=' + code)


def bar_pays_save(request):
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


def bar_salary(request):
    code = request.GET["code"]
    storage_id = getStorageId(code)

    return render(request, 'bar/bar_salary.html', context={
        "code": code,
        "cafe": getStorageName(code),
        "storage_id": storage_id,
        "employees": Employee.objects.all(),
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime("%d.%m.%Y"),
        "salary_sum":
            Salary.objects.filter(date=getTime(),
                                  storage_id=storage_id, type='Аванс').aggregate(Sum('itogo'))['itogo__sum'],
        "timetable": Timetable.objects.filter(storage_id=storage_id,
                                              date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime(
                                                  "%Y-%m-%d")),
        "salaries": Salary.objects.filter(storage_id=storage_id,
                                          date=getTime(),
                                          type='Аванс'),
        "warning": None if request.GET.get('warning') is None else request.GET.get('warning')

    })


def bar_salary_save(request):
    code = None
    warning = None
    if request.method == 'POST':
        storage_id = request.POST["cafe"]
        code = request.POST["code"]

        count = Timetable.objects.filter(storage_id=storage_id,
                                         date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime(
                                             "%Y-%m-%d"))

        for a in count:
            if request.POST[f"[{a.employee_id}][precent]"] == '':
                precent = 0
            else:
                precent = int(request.POST[f"[{a.employee_id}][precent]"])
            if request.POST[f"[{a.employee_id}][oklad]"] == '':
                oklad = 0
            else:
                oklad = int(request.POST[f"[{a.employee_id}][oklad]"])
            if request.POST[f"[{a.employee_id}][premium]"] == '':
                premium = 0
            else:
                premium = int(request.POST[f"[{a.employee_id}][premium]"])
            if request.POST[f"[{a.employee_id}][oklad]"] != "" or request.POST[f"[{a.employee_id}][precent]"] != "" or \
                    request.POST[f"[{a.employee_id}][premium]"] != "":
                rows = Salary.objects.filter(employee_id=a.employee_id,
                                             date=(get_current_time() - datetime.timedelta(hours=2)).strftime(
                                                 "%Y-%m-%d"), type='Аванс').count()
                if rows == 0:
                    obj = Salary(
                        employee_id=a.employee_id,
                        storage_id=storage_id,
                        type='Аванс',
                        sum=oklad,
                        date=getTime(),
                        created_at=get_current_time().strftime("%Y-%m-%d %H:%M:%S"),
                        sum_percent=precent,
                        premium=premium,
                        itogo=precent + oklad + premium
                    )
                    obj.save()
                else:
                    row = Salary.objects.get(employee_id=a.employee_id,
                                             date=(get_current_time() - datetime.timedelta(hours=2)).strftime(
                                                 "%Y-%m-%d"), type='Аванс')
                    if row.storage_id != getStorageId(code):
                        warning = 1
                    row.created_at = get_current_time().strftime("%Y-%m-%d %H:%M:%S")
                    if oklad != 0:
                        row.sum = oklad
                    else:
                        oklad = row.sum
                    if precent != 0:
                        row.sum_percent = precent
                    else:
                        precent = row.sum_percent
                    if premium != 0:
                        row.premium = premium
                    else:
                        premium = row.premium
                    row.itogo = int(precent) + int(oklad) + int(premium)

                    row.save()
        update_money(1, storage_id)
        if warning is not None:
            return redirect('/bar/salary?code=' + code + '&warning=' + str(warning))
        else:
            return redirect('/bar/salary?code=' + code)


def bar_invent(request):
    code = request.GET["code"]
    storage_id = getStorageId(code)

    row = Storages.objects.get(id=storage_id)
    storageId = row.storage_id

    barmen = 'Нет'
    if Timetable.objects.filter(date_at=getTime(),
                                position='Бармен основной', storage_id=storage_id).count() > 0:
        record = Timetable.objects.get(date_at=getTime(),
                                       position='Бармен основной', storage_id=storage_id)
        barmen = Employee.objects.get(id=record.employee_id).fio

    return render(request, 'bar/bar_invent.html', context={
        "bar_products": Products.objects.filter(product_category='Бар'),
        "code": code,
        "cafe": getStorageName(code),
        "storage_id": storage_id,
        "storageId": storageId,
        "barmen": barmen,
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime('%d.%m.%Y')
    })


def bar_invent_form(request, storageId):
    code = None
    page_code = None
    name = None
    data = None
    if request.method == 'POST':
        root = ET.fromstring(getIikoStorages())
        page_code = request.POST["page_code"]
        barmen = request.POST["barmen"]

        for _ in root.findall('corporateItemDto'):
            cat = Categories.objects.filter(is_remains=1)
            Inventory.objects.all().delete()
            for ca in cat:
                if ca.name == 'Бар':
                    xml = checkInventory(storageId, ca.name)
                    root = ET.fromstring(xml)
                    stor = Storages.objects.get(storage_id=storageId)
                    storage = stor.name
                    data = 'Заведение: ' + storage + '%0AОсновной бармен: ' + barmen + '%0A'
                    for cc in root.findall('items/item'):
                        for c in cc.findall('product'):
                            name = c.find('name').text
                            code = c.find('code').text
                        expectedAmount = cc.find('expectedAmount').text

                        amount = f'{int(round(float(expectedAmount)))}'
                        if request.POST[f"{code}"] == '':
                            a = 0
                        else:
                            a = request.POST[f"{code}"]
                        difference = int(a) - int(round(float(expectedAmount)))
                        # worker.name
                        data += '%0A' + name + ': ' + amount + ' | ' + request.POST[f"{code}"] + ' (разница: ' + str(
                            difference) + ')'

                        inventory = Inventory(
                            name=name,
                            amount=int(round(float(expectedAmount))),
                            fact=request.POST[f"{code}"],
                            difference=difference
                        )
                        inventory.save()
        send_webhk('chat_id', data, 1)

    return redirect('/bar/invent/table?code=' + page_code)


def bar_invent_table(request):
    code = request.GET["code"]
    storage_id = getStorageId(code)

    barmen = 'Нет'
    if Timetable.objects.filter(date_at=getTime(),
                                position='Бармен основной',
                                storage_id=storage_id).count() > 0:
        record = Timetable.objects.get(date_at=getTime(),
                                       position='Бармен основной',
                                       storage_id=storage_id)
        barmen = Employee.objects.get(id=record.employee_id).fio

    return render(request, 'bar/bar_invent_table.html', context={
        "items": Inventory.objects.all(),
        "code": code,
        "barmen": barmen,
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime('%d.%m.%Y')
    })


def bar_invent_second(request):
    code = request.GET["code"]
    storage_id = getStorageId(code)

    row = Storages.objects.get(id=storage_id)
    storageId = row.storage_id

    barmen = 'Нет'
    if Timetable.objects.filter(date_at=getTime(),
                                position='Бармен основной', storage_id=storage_id).count() > 0:
        record = Timetable.objects.get(date_at=getTime(),
                                       position='Бармен основной', storage_id=storage_id)
        barmen = Employee.objects.get(id=record.employee_id).fio

    return render(request, 'bar/bar_invent_second.html', context={
        "bar_products": Products.objects.filter(product_category='Посуда'),
        "code": code,
        "cafe": getStorageName(code),
        "storage_id": storage_id,
        "storageId": storageId,
        "barmen": barmen,
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime('%d.%m.%Y')
    })


def bar_invent_form_second(request, storageId):
    code = None
    page_code = None
    name = None
    data = None
    if request.method == 'POST':
        root = ET.fromstring(getIikoStorages())
        page_code = request.POST["page_code"]
        barmen = request.POST["barmen"]

        for _ in root.findall('corporateItemDto'):
            cat = Categories.objects.all()
            Inventory.objects.all().delete()
            for ca in cat:
                if ca.name == 'Посуда':
                    xml = checkInventory(storageId, ca.name)
                    root = ET.fromstring(xml)
                    stor = Storages.objects.get(storage_id=storageId)
                    storage = stor.name
                    data = 'Заведение: ' + storage + '%0AОсновной бармен: ' + barmen + '%0A'
                    for cc in root.findall('items/item'):
                        for c in cc.findall('product'):
                            name = c.find('name').text
                            code = c.find('code').text
                        expectedAmount = cc.find('expectedAmount').text

                        amount = f'{int(round(float(expectedAmount)))}'
                        if request.POST[f"{code}"] == '':
                            a = 0
                        else:
                            a = request.POST[f"{code}"]
                        difference = int(a) - int(round(float(expectedAmount)))
                        # worker.name
                        data += '%0A' + name + ': ' + amount + ' | ' + request.POST[f"{code}"] + ' (разница: ' + str(
                            difference) + ')'

                        inventory = Inventory(
                            name=name,
                            amount=int(round(float(expectedAmount))),
                            fact=request.POST[f"{code}"],
                            difference=difference
                        )
                        inventory.save()
        send_webhk('chat_id', data, 1)

    return redirect('/bar/invent/second/table?code=' + page_code)


def bar_invent_table_second(request):
    code = request.GET["code"]
    storage_id = getStorageId(code)

    barmen = 'Нет'
    if Timetable.objects.filter(date_at=getTime(),
                                position='Бармен основной',
                                storage_id=storage_id).count() > 0:
        record = Timetable.objects.get(date_at=getTime(),
                                       position='Бармен основной',
                                       storage_id=storage_id)
        barmen = Employee.objects.get(id=record.employee_id).fio

    return render(request, 'bar/bar_invent_table.html', context={
        "items": Inventory.objects.all(),
        "code": code,
        "barmen": barmen,
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime('%d.%m.%Y')
    })


def bar_end(request):
    code = request.GET["code"]
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
        Salary.objects.filter(storage_id=getStorageId(code), date=getTime(), type='Зарплата').aggregate(Sum('sum'))[
            'sum__sum'] is None else \
        Salary.objects.filter(storage_id=getStorageId(code), date=getTime(), type='Зарплата').aggregate(Sum('sum'))[
            'sum__sum']
    total_salary = 0 if Salary.objects.filter(storage_id=getStorageId(code), date=getTime(), type='Аванс').aggregate(
        total_sum=Sum('sum') + Sum('sum_percent') + Sum('premium'))['total_sum'] is None else \
        Salary.objects.filter(storage_id=getStorageId(code), date=getTime(), type='Аванс').aggregate(
            total_sum=Sum('sum') + Sum('sum_percent') + Sum('premium'))['total_sum']
    payin = 0 if Pays.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=1).aggregate(Sum('sum'))[
                     'sum__sum'] is None else \
        Pays.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=1).aggregate(Sum('sum'))['sum__sum']
    payout = 0 if Pays.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=2).aggregate(Sum('sum'))[
                      'sum__sum'] is None else \
        Pays.objects.filter(storage_id=getStorageId(code), date_at=getTime(), type=2).aggregate(Sum('sum'))['sum__sum']

    try:
        row = Money.objects.get(storage_id=getStorageId(code), date_at=getTime())
        morning = row.sum_cash_morning
        difference = row.difference2
        calculated = row.difference
        end = None if row.sum_cash_end_day is None else row.sum_cash_end_day
    except Money.DoesNotExist:
        morning = 0
        calculated = 0
        difference = 0
        end = None

    return render(request, 'bar/bar_end.html', context={
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


def bar_end_save(request):
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
            Salary.objects.filter(storage_id=getStorageId(code), date=getTime(), type='Зарплата').aggregate(Sum('sum'))[
                'sum__sum'] is None else \
            Salary.objects.filter(storage_id=getStorageId(code), date=getTime(), type='Зарплата').aggregate(Sum('sum'))[
                'sum__sum']
        total_salary = 0 if \
            Salary.objects.filter(storage_id=getStorageId(code), date=getTime(), type='Аванс').aggregate(
                total_sum=Sum('sum') + Sum('sum_percent') + Sum('premium'))['total_sum'] is None else \
            Salary.objects.filter(storage_id=getStorageId(code), date=getTime(), type='Аванс').aggregate(
                total_sum=Sum('sum') + Sum('sum_percent') + Sum('premium'))['total_sum']
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

        calculated = int(record.sum_cash_morning) + int(total_cash) - int(expensesNal) - int(total_salary) - int(
            monthly_salary) + int(payin) - int(payout)

        difference = int(cash) - calculated

        record.sum_cash_end_day = cash
        record.total_day = total_day
        record.total_cash = total_cash
        record.total_bn = total_bn
        record.difference = calculated
        record.difference2 = difference
        record.total_market = int(yandex) + int(delivery)
        record.total_salary = int(total_salary) + int(monthly_salary)
        record.total_expenses = int(expensesNal)
        record.payin = int(payin)
        record.payout = int(payout)
        record.save()
        storage = Storages.objects.get(id=getStorageId(code))
        date_at = (get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d')

        data = f'Заведение: {storage.name}%0AДата: {date_at}%0AОбщая выручка: {record.total_day}%0A%0AКасса утро: {record.sum_cash_morning}%0AНал: {record.total_cash}%0AБезнал: {record.total_bn}%0AРасходы нал: {expensesNal}%0AЗП аванс: {total_salary}%0AЗП расчет: {monthly_salary}%0AВнесения: {payin}%0AИзъятия: {payout}%0AЯндекс: {yandex}%0AДеливери: {delivery}%0A%0AОстаток в кассе: {record.sum_cash_end_day} (расчетный: {record.difference}, расхождение: {record.difference2})'

        send_webhk('chat_id', data, 1)

        data = '(@VovaMoskvichev)%0A%0AДата: ' + (get_current_time() - datetime.timedelta(hours=2)).strftime(
            '%Y-%m-%d') + '%0AЗаведение: ' + storage.name + '%0A%0A'
        for row in TovarRequests.objects.filter(
                date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'), storage_id=storage.id,
                product_category__contains='Пиво разливное'):
            data += f'{row.product_name}%0A'

        res = send_webhk('-chat_id', data, 1)
        send_webhk('-chat_id', str(res), 1)

        yandex = 0
        delivery = 0
        payOrders = 0
        barmen_count = 0
        jsonData = getIikoCashShifts2((get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
                                      (get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'))
        dictData = json.loads(jsonData)
        for i in range(len(dictData)):
            if dictData[i]["pointOfSaleId"] == storage.pointofsale:
                first_data = getSalesByDepartment(dictData[i]["id"])
                data = json.loads(first_data)
                payOrders = dictData[i]["payOrders"]

                for i in range(len(data["cashlessRecords"])):
                    row = Paymenttypes.objects.get(payment_id=data["cashlessRecords"][i]["info"]["paymentTypeId"])
                    if 'Delivery' in row.name:
                        delivery += int(data["cashlessRecords"][i]["info"]["sum"])
                    if 'Яндекс' in row.name:
                        yandex += int(data["cashlessRecords"][i]["info"]["sum"])
        sum_for_precent = payOrders - int(yandex) - int(delivery)
        records = Timetable.objects.filter(storage_id=storage.id,
                                           date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime(
                                               '%Y-%m-%d'))
        barmen_count += int(
            Timetable.objects.filter(date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
                                     storage_id=storage.id, position='Бармен основной').count())
        barmen_count += int(
            Timetable.objects.filter(date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
                                     storage_id=storage.id, position='Бармен усиление').count())
        barmen_count += int(
            Timetable.objects.filter(date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
                                     storage_id=storage.id, position__contains='Бармен вызывной').count())

        if barmen_count > 1:
            precent = '2.5'
        else:
            precent = '3'
        for record in records:
            if 'Повар' in record.position or 'Тех' in record.position or 'Бармен стажер' in record.position:
                precentt = 0
            else:
                precentt = int(sum_for_precent) * (float(precent) / 100)
                record.precent_num = precent

            if 'Бармен' not in record.position:
                if 60000 <= payOrders < 70000:
                    premium = 200
                elif 70000 <= payOrders < 100000:
                    premium = 500
                elif payOrders >= 100000:
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
    return redirect('/bar/end?code=' + code)


def bar_auto_salary(request):
    code = request.GET["code"]
    storage_id = getStorageId(code)
    cafe = getStorageName(code)
    pointOfSale = getPointOfSale(code)
    payOrders = ''
    delivery = 0
    yandex = 0
    precent_num = None

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

            for i in range(len(data["cashlessRecords"])):
                row = Paymenttypes.objects.get(payment_id=data["cashlessRecords"][i]["info"]["paymentTypeId"])
                # obj = Salesbypayments.objects.filter(payment_id=data["cashlessRecords"][i]["info"]["id"]).count()
                if row.name == 'Delivery Club':
                    delivery += int(data["cashlessRecords"][i]["info"]["sum"])
                if row.name == 'Яндекс ЕДА' or row.name == '-Яндекс ЕДА':
                    yandex += int(data["cashlessRecords"][i]["info"]["sum"])

    sum_for_precent = int(total_market) - int(yandex) - int(delivery)

    AutoSalary.objects.all().delete()
    records = Timetable.objects.filter(date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
                                       storage_id=storage_id)
    if records.count() > 0:
        for record in records:

            barmen_count = 0
            barmen_count += int(Timetable.objects.filter(
                date_at=getTime(),
                storage_id=storage_id, position='Бармен основной').count())
            barmen_count += int(Timetable.objects.filter(
                date_at=getTime(),
                storage_id=storage_id, position='Бармен усиление').count())
            barmen_count += int(Timetable.objects.filter(
                date_at=getTime(),
                storage_id=storage_id, position__contains='Бармен вызывной').count())

            if barmen_count > 1:
                precent_num = '2.5'
            else:
                precent_num = '3'

            if 'Повар' in record.position or 'Тех' in record.position or 'Бармен стажер' in record.position:
                precent = 0
            else:
                precent = int(sum_for_precent) * (float(precent_num) / 100)

            if 'Бармен' not in record.position:
                if total_market >= 60000 and total_market < 70000:
                    premium = 200
                elif total_market >= 70000 and total_market < 100000:
                    premium = 500
                elif total_market >= 100000:
                    premium = 1000
                else:
                    premium = 0
            else:
                if 'стажер' not in record.position:
                    if sum_for_precent >= 60000 and sum_for_precent < 70000:
                        premium = 200
                    elif sum_for_precent >= 70000 and sum_for_precent < 100000:
                        premium = 500
                    elif sum_for_precent >= 100000:
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
                    date_at=getTime(),
                    storage_id=storage_id,
                    oklad=record.oklad,
                    precent=precent,
                    premium=premium,
                    fine=fine,
                    total=int(record.oklad) + int(precent) + int(premium) - int(fine)
                )
                row.save()
            else:
                row = AutoSalary.objects.get(storage_id=storage_id,
                                             date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime(
                                                 "%Y-%m-%d"), id=record.employee_id)
                row.id = record.employee_id
                row.fio = Employee.objects.get(id=record.employee_id).fio
                row.oklad = record.oklad
                row.precent = precent
                row.premium = premium
                row.fine = fine
                row.total = int(record.oklad) + int(precent) + int(premium) - int(fine)
                row.save()

    else:
        precent_num = 0

    return render(request, 'bar/bar_auto_salary.html', context={
        "cafe": cafe,
        "storage_id": storage_id,
        "code": code,
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime('%d.%m.%Y'),
        "precent": precent_num,
        "sum_for_precent": sum_for_precent,
        "employees": Employee.objects.all(),
        "rows": AutoSalary.objects.filter(
            date_at=getTime(), storage_id=storage_id),
        "salary_sum":
            AutoSalary.objects.filter(date_at=getTime(),
                                      storage_id=storage_id).aggregate(Sum('total'))['total__sum']
    })


def bar_salary3(request):
    code = request.GET["code"]
    storage_id = getStorageId(code)

    return render(request, 'bar/bar_salary3.html', context={
        "code": code,
        "cafe": getStorageName(code),
        "storage_id": storage_id,
        "a": iiko_connect(),
        "employees": Employee.objects.all(),
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime("%d.%m.%Y"),
        "salary_sum":
            Salary.objects.filter(date=getTime(),
                                  storage_id=storage_id, type='Зарплата').aggregate(Sum('itogo'))['itogo__sum'],
        "timetable": Employee.objects.filter(storage_id=storage_id, is_deleted='Активен'),
        "salaries": Salary.objects.filter(storage_id=storage_id,
                                          date=getTime(),
                                          type='Зарплата'),

    })


def bar_salary3_save(request):
    code = None
    if request.method == 'POST':
        storage_id = request.POST["cafe"]
        code = request.POST["code"]

        count = Employee.objects.filter(storage_id=storage_id, is_deleted='Активен')

        for a in count:
            if request.POST[f"[{a.id}][salary]"] != "":
                rows = Salary.objects.filter(employee_id=a.id,
                                             date=(get_current_time() - datetime.timedelta(hours=2)).strftime(
                                                 "%Y-%m-%d"), type='Зарплата').count()
                if rows == 0:
                    obj = Salary(
                        employee_id=a.id,
                        storage_id=storage_id,
                        type='Зарплата',
                        sum=int(request.POST[f"[{a.id}][salary]"]),
                        date=getTime(),
                        created_at=get_current_time().strftime("%Y-%m-%d %H:%M:%S"),
                        sum_percent=0,
                        premium=0,
                        sum_taxi=request.POST["month"] + ' (' + request.POST["days"] + ')',
                        itogo=int(request.POST[f"[{a.id}][salary]"])
                    )
                    obj.save()
                else:
                    row = Salary.objects.get(employee_id=a.id,
                                             date=(get_current_time() - datetime.timedelta(hours=2)).strftime(
                                                 "%Y-%m-%d"), type="Зарплата")
                    row.created_at = get_current_time().strftime("%Y-%m-%d %H:%M:%S"),
                    row.sum = int(request.POST[f"[{a.id}][salary]"])
                    row.itogo = int(request.POST[f"[{a.id}][salary]"])
                    row.sum_taxi = request.POST["month"] + ' (' + request.POST["days"] + ')'

                    row.save()
    return redirect('/bar/main_salary?code=' + code)


def bar_expenses_delete(request, id):
    record = Expenses.objects.get(id=id)
    storage_id = record.storage_id
    chat_id = '-619967297'

    pay_type = 'Из кассы' if record.is_bn == 0 else 'Картой'

    send_text = 'https://api.telegram.org/bot5127419796:AAH8D8RlH1LL66dCtMzgd1JK59WXYv-0xWA/sendMessage?chat_id=' + chat_id + '&text=Расход №' + str(
        id) + ' удален.%0A%0AЗаведение: ' + getStorageName(getCode(storage_id)) + ' (' + str(
        record.date_at) + ')%0AРасход: ' + record.expense + ' (' + pay_type + ')%0AСумма расхода: ' + str(
        record.sum) + '%0AКомментарий: ' + record.comment + '%0A'
    requests.get(send_text)
    record.delete()
    return redirect('/bar/expenses?code=' + getCode(storage_id))


def bar_employee_delete(request, pk):
    code = request.GET["code"]
    storage_id = getStorageId(code)
    record = Timetable.objects.get(storage_id=storage_id, employee_id=pk,
                                   date_at=getTime())
    record.delete()
    return redirect('/bar?code=' + code)


def bar_employee_salary_now(request):
    code = request.GET["code"]
    employee = Employee.objects.get(code=code)
    employee_id = employee.id
    days = monthrange(datetime.datetime.now().year, int(get_current_time().strftime('%m')))[1]
    month = get_current_time().strftime('%m')
    rows = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id)
    one = \
        Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id).aggregate(Sum('total'))[
            'total__sum']
    one_minus = \
        Salary.objects.filter(date__contains='-' + month + '-', employee_id=employee_id, type="Аванс").aggregate(
            Sum('itogo'))['itogo__sum']
    two = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id,
                                   date_at__day__lte=15).aggregate(Sum('total'))['total__sum']
    two_minus = Salary.objects.filter(date__contains='-' + month + '-', date__day__lte=15, employee_id=employee_id,
                                      type="Аванс").aggregate(Sum('itogo'))['itogo__sum']
    three = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id, date_at__day__gte=16,
                                     date_at__day__lte=days).aggregate(Sum('total'))['total__sum']
    three_minus = Salary.objects.filter(date__contains='-' + month + '-', date__day__gte=16, date__day__lte=days,
                                        employee_id=employee_id, type="Аванс").aggregate(Sum('itogo'))['itogo__sum']
    if one_minus is None:
        one_minus = 0
    if two_minus is None:
        two_minus = 0
    if three_minus is None:
        three_minus = 0
    if three is None:
        three = 0
    if two is None:
        two = 0
    if one is None:
        one = 0
    oklad_one = 0 if \
        Salary.objects.filter(date__contains='-' + month + '-', employee_id=Employee.objects.get(code=code).id,
                              type='Аванс').aggregate(Sum('sum'))['sum__sum'] is None else \
        Salary.objects.filter(date__contains='-' + month + '-', employee_id=Employee.objects.get(code=code).id,
                              type='Аванс').aggregate(Sum('sum'))['sum__sum']
    oklad_two = 0 if Timetable.objects.filter(date_at__contains='-' + month + '-',
                                              employee_id=Employee.objects.get(code=code).id).aggregate(Sum('oklad'))[
                         'oklad__sum'] is None else Timetable.objects.filter(date_at__contains='-' + month + '-',
                                                                             employee_id=Employee.objects.get(
                                                                                 code=code).id).aggregate(Sum('oklad'))[
        'oklad__sum']
    precent_one = 0 if \
        Salary.objects.filter(date__contains='-' + month + '-', employee_id=Employee.objects.get(code=code).id,
                              type='Аванс').aggregate(Sum('sum_percent'))['sum_percent__sum'] is None else \
        Salary.objects.filter(date__contains='-' + month + '-', employee_id=Employee.objects.get(code=code).id,
                              type='Аванс').aggregate(Sum('sum_percent'))['sum_percent__sum']
    precent_two = 0 if Timetable.objects.filter(date_at__contains='-' + month + '-',
                                                employee_id=Employee.objects.get(code=code).id).aggregate(
        Sum('precent'))['precent__sum'] is None else Timetable.objects.filter(date_at__contains='-' + month + '-',
                                                                              employee_id=Employee.objects.get(
                                                                                  code=code).id).aggregate(
        Sum('precent'))['precent__sum']
    premium_one = 0 if \
        Salary.objects.filter(date__contains='-' + month + '-', employee_id=Employee.objects.get(code=code).id,
                              type='Аванс').aggregate(Sum('premium'))['premium__sum'] is None else \
        Salary.objects.filter(date__contains='-' + month + '-', employee_id=Employee.objects.get(code=code).id,
                              type='Аванс').aggregate(Sum('premium'))['premium__sum']
    premium_two = 0 if Timetable.objects.filter(date_at__contains='-' + month + '-',
                                                employee_id=Employee.objects.get(code=code).id).aggregate(
        Sum('premium'))['premium__sum'] is None else Timetable.objects.filter(date_at__contains='-' + month + '-',
                                                                              employee_id=Employee.objects.get(
                                                                                  code=code).id).aggregate(
        Sum('premium'))['premium__sum']
    return render(request, 'bar/bar_employee.html', context={
        "previous": 0,
        "row": Timetable.objects.filter(date_at__contains='-' + get_current_time().strftime('%m') + '-',
                                        employee_id=employee.id).aggregate(Sum('oklad'))['oklad__sum'],
        "rows": Salary.objects.filter(date__contains='-' + get_current_time().strftime('%m') + '-',
                                      employee_id=Employee.objects.get(code=code).id),
        "rows_sum_one": Salary.objects.filter(date__contains='-' + get_current_time().strftime('%m') + '-',
                                              employee_id=Employee.objects.get(code=code).id, type='Аванс').aggregate(
            Sum('itogo'))['itogo__sum'],
        "rows_sum_two": Salary.objects.filter(date__contains='-' + get_current_time().strftime('%m') + '-',
                                              employee_id=Employee.objects.get(code=code).id,
                                              type='Зарплата').aggregate(Sum('itogo'))['itogo__sum'],
        "storages": Storages.objects.all(),
        "employee": employee,
        # "previous": request.GET["previous"],
        "date": get_current_time(),
        "one": one,
        "two": int(two) - int(two_minus),
        "three": int(three) - int(three_minus),
        "records": rows,
        "days": days,
        "oklad": int(oklad_two) - int(oklad_one),
        "precent": int(precent_two) - int(precent_one),
        "premium": int(premium_two) - int(premium_one)
    })


def bar_employee_salary_previous(request):
    code = request.GET["code"]
    employee = Employee.objects.get(code=code)
    employee_id = employee.id
    days = \
        monthrange(datetime.datetime.now().year,
                   int((get_current_time() - datetime.timedelta(days=30)).strftime('%m')))[1]
    month = (get_current_time() - datetime.timedelta(days=30)).strftime('%m')
    rows = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id)
    one = \
        Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id).aggregate(Sum('total'))[
            'total__sum']
    two = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id,
                                   date_at__day__lte=15).aggregate(Sum('total'))['total__sum']
    two_minus = Salary.objects.filter(date__contains='-' + month + '-', date__day__lte=15, employee_id=employee_id,
                                      type="Аванс").aggregate(Sum('itogo'))['itogo__sum']
    three = Timetable.objects.filter(date_at__contains='-' + month + '-', employee_id=employee_id, date_at__day__gte=16,
                                     date_at__day__lte=days).aggregate(Sum('total'))['total__sum']
    three_minus = Salary.objects.filter(date__contains='-' + month + '-', date__day__gte=16, date__day__lte=days,
                                        employee_id=employee_id, type="Аванс").aggregate(Sum('itogo'))['itogo__sum']
    if two_minus is None:
        two_minus = 0
    if three_minus is None:
        three_minus = 0
    if three is None:
        three = 0
    if two is None:
        two = 0
    if one is None:
        one = 0
    oklad_one = 0 if \
        Salary.objects.filter(
            date__contains='-' + (get_current_time() - datetime.timedelta(days=30)).strftime('%m') + '-',
            employee_id=Employee.objects.get(code=code).id, type='Аванс').aggregate(Sum('sum'))[
            'sum__sum'] is None else \
        Salary.objects.filter(
            date__contains='-' + (get_current_time() - datetime.timedelta(days=30)).strftime('%m') + '-',
            employee_id=Employee.objects.get(code=code).id, type='Аванс').aggregate(Sum('sum'))[
            'sum__sum']
    oklad_two = 0 if Timetable.objects.filter(
        date_at__contains='-' + (get_current_time() - datetime.timedelta(days=30)).strftime('%m') + '-',
        employee_id=Employee.objects.get(code=code).id).aggregate(Sum('oklad'))['oklad__sum'] else \
        Timetable.objects.filter(
            date_at__contains='-' + (get_current_time() - datetime.timedelta(days=30)).strftime('%m') + '-',
            employee_id=Employee.objects.get(code=code).id).aggregate(Sum('oklad'))['oklad__sum']
    precent_one = 0 if \
        Salary.objects.filter(
            date__contains='-' + (get_current_time() - datetime.timedelta(days=30)).strftime('%m') + '-',
            employee_id=Employee.objects.get(code=code).id, type='Аванс').aggregate(Sum('sum_percent'))[
            'sum_percent__sum'] is None else \
        Salary.objects.filter(
            date__contains='-' + (get_current_time() - datetime.timedelta(days=30)).strftime('%m') + '-',
            employee_id=Employee.objects.get(code=code).id, type='Аванс').aggregate(Sum('sum_percent'))[
            'sum_percent__sum']
    precent_two = 0 if Timetable.objects.filter(
        date_at__contains='-' + (get_current_time() - datetime.timedelta(days=30)).strftime('%m') + '-',
        employee_id=Employee.objects.get(code=code).id).aggregate(Sum('precent'))['precent__sum'] else \
        Timetable.objects.filter(
            date_at__contains='-' + (get_current_time() - datetime.timedelta(days=30)).strftime('%m') + '-',
            employee_id=Employee.objects.get(code=code).id).aggregate(Sum('precent'))['precent__sum']
    premium_one = 0 if \
        Salary.objects.filter(
            date__contains='-' + (get_current_time() - datetime.timedelta(days=30)).strftime('%m') + '-',
            employee_id=Employee.objects.get(code=code).id, type='Аванс').aggregate(Sum('premium'))[
            'premium__sum'] is None else \
        Salary.objects.filter(
            date__contains='-' + (get_current_time() - datetime.timedelta(days=30)).strftime('%m') + '-',
            employee_id=Employee.objects.get(code=code).id, type='Аванс').aggregate(Sum('premium'))[
            'premium__sum']
    premium_two = 0 if Timetable.objects.filter(
        date_at__contains='-' + (get_current_time() - datetime.timedelta(days=30)).strftime('%m') + '-',
        employee_id=Employee.objects.get(code=code).id).aggregate(Sum('premium'))['premium__sum'] else \
        Timetable.objects.filter(
            date_at__contains='-' + (get_current_time() - datetime.timedelta(days=30)).strftime('%m') + '-',
            employee_id=Employee.objects.get(code=code).id).aggregate(Sum('premium'))['premium__sum']
    return render(request, 'bar/bar_employee.html', context={
        "previous": 1,
        "row": Timetable.objects.filter(
            date_at__contains='-' + (get_current_time() - datetime.timedelta(days=30)).strftime('%m') + '-',
            employee_id=employee.id).aggregate(Sum('oklad'))['oklad__sum'],
        "rows": Salary.objects.filter(
            date__contains='-' + (get_current_time() - datetime.timedelta(days=30)).strftime('%m') + '-',
            employee_id=Employee.objects.get(code=code).id),
        "rows_sum_one": Salary.objects.filter(
            date__contains='-' + (get_current_time() - datetime.timedelta(days=30)).strftime('%m') + '-',
            employee_id=Employee.objects.get(code=code).id, type='Аванс').aggregate(Sum('itogo'))['itogo__sum'],
        "rows_sum_two": Salary.objects.filter(
            date__contains='-' + (get_current_time() - datetime.timedelta(days=30)).strftime('%m') + '-',
            employee_id=Employee.objects.get(code=code).id, type='Зарплата').aggregate(Sum('itogo'))['itogo__sum'],
        "storages": Storages.objects.all(),
        "employee": employee,
        # "previous": request.GET["previous"],
        "date": get_current_time(),
        "one": one,
        "two": int(two) - int(two_minus),
        "three": int(three) - int(three_minus),
        "records": rows,
        "days": days,
        "oklad": int(oklad_two) - int(oklad_one),
        "precent": int(precent_two) - int(precent_one),
        "premium": int(premium_two) - int(premium_one)
    })


def bar_calendar(request):
    code = request.GET["code"]
    storage_id = getStorageId(code)

    return render(request, 'bar/bar_calendar.html', context={
        "code": code,
        "cafe": getStorageName(code),
        "storage_id": storage_id,
    })


def bar_calendar_insert(request):
    if request.user.is_staff == 1:
        if request.method == 'POST':
            code = request.POST["code"]
            record = Calendar(
                storage_id=getStorageId(code),
                employee=request.POST["employee"],
                date_at=request.POST["date_at"]
            )
            record.save()

            return redirect('/bar/calendar?code=' + code)
        code = request.GET["code"]
        return render(request, 'bar/bar_calendar_insert.html', context={
            "storages": Storages.objects.all(),
            "employees": Employee.objects.filter(storage_id=getStorageId(code)),
            "code": code
        })
    else:
        return redirect('/login')


def bar_blacklist(request):
    code = request.GET["code"]

    return render(request, 'bar/blacklist.html', context={
        "code": code,
        "storage_id": getStorageId(code),
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
        "cafe": getStorageName(code),
        "blacklist": Blacklist.objects.filter(storage_id=getStorageId(code))
    })


def bar_beer_request(request):
    if request.method == "POST":
        barmen = request.POST["barmen"]

        for product in Products.objects.all():
            if request.POST.get(f'{product.num}') is not None:
                a = 1
            else:
                a = 0
            record = Products.objects.get(num=product.num)
            if record.supplier_id == '':
                supplier = ''
            else:
                supplier = Suppliers.objects.get(supplier_id=record.supplier_id).name
            if a > 0:
                row = TovarRequests(
                    date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
                    storage_id=Storages.objects.get(code=request.GET.get('code')).id,
                    product_category='Пиво разливное',
                    product_name=record.name,
                    product_unit=record.main_unit,
                    product_amount=a,
                    product_price=0,
                    sum=0,
                    supplier=supplier,
                    employee=barmen,
                    status=0,
                )
                row.save()
                # data += f'{record.name}%0A'
    code = request.GET["code"]
    storage_id = getStorageId(code)

    row = Storages.objects.get(id=storage_id)
    storageId = row.storage_id

    barmen = 'Нет'
    if Timetable.objects.filter(date_at=getTime(),
                                position='Бармен основной', storage_id=storage_id).count() > 0:
        record = Timetable.objects.get(date_at=getTime(),
                                       position='Бармен основной', storage_id=storage_id)
        barmen = Employee.objects.get(id=record.employee_id).fio

    return render(request, 'bar/bar_beer_request.html', context={
        "bar_products": Products.objects.filter(product_category='Пиво разливное'),
        "code": code,
        "cafe": getStorageName(code),
        "storage_id": storage_id,
        "storageId": storageId,
        "barmen": barmen,
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime('%d.%m.%Y'),
        "rows": TovarRequests.objects.filter(product_category__contains='Пиво разливное',
                                             date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime(
                                                 '%Y-%m-%d'), storage_id=getStorageId(code))
    })


def bar_hoz_request(request):
    if request.method == "POST":
        barmen = request.POST["barmen"]
        data = '(@VovaMoskvichev)%0A%0AДата: ' + get_current_time().strftime(
            '%Y-%m-%d') + '%0AЗаведение: ' + Storages.objects.get(
            code=request.GET.get('code')).name + '%0AСотрудник: ' + barmen + '%0A%0A'

        for product in Products.objects.all():
            a = 0
            if request.POST.get(f'{product.num}') == '':
                a = 0
            else:
                a = int(request.POST.get(f'{product.num}')) if request.POST.get(f'{product.num}') is not None else 0
            record = Products.objects.get(num=product.num)
            if record.supplier_id == '':
                supplier = ''
            else:
                supplier = Suppliers.objects.get(supplier_id=record.supplier_id).name
            if a > 0:
                row = TovarRequests(
                    date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
                    storage_id=Storages.objects.get(code=request.GET.get('code')).id,
                    product_category='Хоз. товары',
                    product_name=record.name,
                    product_unit=record.main_unit,
                    product_amount=a,
                    product_price=0,
                    sum=0,
                    supplier=supplier,
                    employee=barmen,
                    status=0,
                )
                row.save()
                data += f'{record.name} - {a}{record.main_unit}%0A'

        send_webhk('-chat_id', data, 1)
    code = request.GET["code"]
    storage_id = getStorageId(code)

    row = Storages.objects.get(id=storage_id)
    storageId = row.storage_id

    return render(request, 'bar/bar_hoz_request.html', context={
        "bar_products": Products.objects.filter(product_category='Хоз.товары'),
        "code": code,
        "cafe": getStorageName(code),
        "storage_id": storage_id,
        "storageId": storageId,
        "timetable": Timetable.objects.filter(date_at=getTime(), storage_id=getStorageId(code)),
        "employees": Employee.objects.all(),
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime('%d.%m.%Y'),
        "rows": TovarRequests.objects.filter(product_category='Хоз. товары',
                                             date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime(
                                                 '%Y-%m-%d'), storage_id=getStorageId(code))
    })


def bar_drinks_request(request):
    if request.method == "POST":
        barmen = request.POST["barmen"]
        data = '(@Barmanager_hp_krd)%0A%0AДата: ' + get_current_time().strftime(
            '%Y-%m-%d') + '%0AЗаведение: ' + Storages.objects.get(
            code=request.GET.get('code')).name + '%0AСотрудник: ' + barmen + '%0A%0A'

        for product in Products.objects.all():
            if request.POST.get(f'{product.num}') == '':
                a = 0
            else:
                a = int(request.POST.get(f'{product.num}')) if request.POST.get(f'{product.num}') is not None else 0
            record = Products.objects.get(num=product.num)
            if record.supplier_id == '':
                supplier = ''
            else:
                supplier = Suppliers.objects.get(supplier_id=record.supplier_id).name
            if a > 0:
                row = TovarRequests(
                    date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
                    storage_id=Storages.objects.get(code=request.GET.get('code')).id,
                    product_category='Бар',
                    product_name=record.name,
                    product_unit=record.main_unit,
                    product_amount=a,
                    product_price=0,
                    sum=0,
                    supplier=supplier,
                    employee=barmen,
                    status=0,
                )
                row.save()
                data += f'{record.name} - {a}{record.main_unit}%0A'
                """for supplier in Suppliers.objects.all():
                    data += '<b>' + supplier.name + '</b>%0A'
                    if supplier.supplier_id == record.supplier_id:
                        data += f'{record.name} - {a}{record.main_unit}%0A'"""

        send_webhk('-chat_id', data, 1)  # -862700192
    code = request.GET["code"]
    storage_id = getStorageId(code)

    row = Storages.objects.get(id=storage_id)
    storageId = row.storage_id

    if Timetable.objects.filter(date_at=getTime(),
                                position='Бармен основной', storage_id=storage_id).count() > 0:
        record = Timetable.objects.get(date_at=getTime(),
                                       position='Бармен основной', storage_id=storage_id)
        barmen = Employee.objects.get(id=record.employee_id).fio

    return render(request, 'bar/bar_drinks_request.html', context={
        "bar_products": Products.objects.filter(product_category='Бар'),
        "code": code,
        "cafe": getStorageName(code),
        "storage_id": storage_id,
        "storageId": storageId,
        "barmen": barmen,
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime('%d.%m.%Y')
    })


def bar_products_request(request):
    if request.method == "POST":
        barmen = request.POST["barmen"]
        data = 'Дата: ' + (get_current_time() - datetime.timedelta(hours=2)).strftime(
            '%Y-%m-%d') + '%0AЗаведение: ' + Storages.objects.get(
            code=request.GET.get('code')).name + '%0AСотрудник: ' + barmen + '%0A%0A'

        for product in Products.objects.all():
            if request.POST.get(f'{product.num}') == '':
                a = 0
            else:
                a = int(request.POST.get(f'{product.num}')) if request.POST.get(f'{product.num}') is not None else 0
            record = Products.objects.get(num=product.num)
            if record.supplier_id == '':
                supplier = ''
            else:
                supplier = Suppliers.objects.get(supplier_id=record.supplier_id).name
            if a > 0:
                row = TovarRequests(
                    date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
                    storage_id=Storages.objects.get(code=request.GET.get('code')).id,
                    product_category='Продукты',
                    product_name=record.name,
                    product_unit=record.main_unit,
                    product_amount=a,
                    product_price=0,
                    sum=0,
                    supplier=supplier,
                    employee=barmen,
                    status=0,
                )
                row.save()
                data += f'{record.name} - {a}{record.main_unit}%0A'

        send_webhk('-chat_id', data, 1)
    code = request.GET["code"]
    storage_id = getStorageId(code)

    row = Storages.objects.get(id=storage_id)
    storageId = row.storage_id

    barmen = 'Нет'
    if Timetable.objects.filter(date_at=getTime(),
                                position='Повар основной', storage_id=storage_id).count() > 0:
        record = Timetable.objects.get(date_at=getTime(),
                                       position='Повар основной', storage_id=storage_id)
        barmen = Employee.objects.get(id=record.employee_id).fio

    return render(request, 'bar/bar_products_request.html', context={
        "bar_products": Products.objects.filter(product_category='Продукты'),
        "code": code,
        "cafe": getStorageName(code),
        "storage_id": storage_id,
        "storageId": storageId,
        "barmen": barmen,
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime('%d.%m.%Y')
    })


def bar_box_request(request):
    if request.method == "POST":
        barmen = request.POST["barmen"]
        data = 'Дата: ' + (get_current_time() - datetime.timedelta(hours=2)).strftime(
            '%Y-%m-%d') + '%0AЗаведение: ' + Storages.objects.get(
            code=request.GET.get('code')).name + '%0AСотрудник: ' + barmen + '%0A%0A'

        for product in Products.objects.all():
            a = 0
            if request.POST.get(f'{product.num}') == '':
                a = 0
            else:
                a = int(request.POST.get(f'{product.num}')) if request.POST.get(f'{product.num}') is not None else 0
            record = Products.objects.get(num=product.num)
            if record.supplier_id == '':
                supplier = ''
            else:
                supplier = Suppliers.objects.get(supplier_id=record.supplier_id).name
            if a > 0:
                row = TovarRequests(
                    date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
                    storage_id=Storages.objects.get(code=request.GET.get('code')).id,
                    product_category='Упаковка',
                    product_name=record.name,
                    product_unit=record.main_unit,
                    product_amount=a,
                    product_price=0,
                    sum=0,
                    supplier=supplier,
                    employee=barmen,
                    status=0,
                )
                row.save()
                data += f'{record.name} - {a}{record.main_unit}%0A'

        send_webhk('chat_id', data, 1)
    code = request.GET["code"]
    storage_id = getStorageId(code)

    row = Storages.objects.get(id=storage_id)
    storageId = row.storage_id

    barmen = 'Нет'
    if Timetable.objects.filter(date_at=getTime(),
                                position='Бармен основной', storage_id=storage_id).count() > 0:
        record = Timetable.objects.get(date_at=getTime(),
                                       position='Бармен основной', storage_id=storage_id)
        barmen = Employee.objects.get(id=record.employee_id).fio

    return render(request, 'bar/bar_boxes_request.html', context={
        "bar_products": Products.objects.filter(product_category='Упаковка'),
        "code": code,
        "cafe": getStorageName(code),
        "storage_id": storage_id,
        "storageId": storageId,
        "barmen": barmen,
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime('%d.%m.%Y')
    })


def bar_beer_arrival(request):
    if request.method == 'POST':
        sum = request.POST["sum"].split('.')[0] if '.' in request.POST["sum"] else request.POST["sum"]
        type = 0 if request.POST.get('typeOpl') is None else 2
        row = BeerArrival(
            date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
            storage_id=getStorageId(request.POST["code"]),
            num=request.POST["num"],
            supplier=Products.objects.get(id=request.POST["beer"]).supplier_id,
            product=request.POST["beer"],
            amount=request.POST["amount"],
            sum=sum,
            type=type
        )
        row.save()
        if type == 2:
            try:
                supplier = Suppliers.objects.get(
                    supplier_id=Products.objects.get(id=request.POST["beer"]).supplier_id).name
            except Suppliers.DoesNotExist:
                supplier = 'Не назначен'
            row = Expenses(
                date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
                storage_id=getStorageId(request.POST["code"]),
                expense='Пиво/напитки',
                sum=sum,
                supplier_id=Products.objects.get(id=request.POST["beer"]).supplier_id,
                product_id=request.POST["beer"],
                num=request.POST["num"],
                is_bn=0,
                comment=supplier + ' // ' + request.POST["num"]
            )
            row.save()

        return redirect('/bar/arrival/beer?code=' + request.POST["code"])
    code = request.GET.get('code')

    return render(request, 'bar/bar_beer_arrival.html', context={
        "code": code,
        "storage_id": getStorageId(code),
        "cafe": getStorageName(code),
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime('%d.%m.%Y'),
        "beers": Products.objects.filter(product_category='Пиво разливное'),
        "products": Products.objects.all(),
        "suppliers": Suppliers.objects.all(),
        "rows": BeerArrival.objects.filter(
            date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
            storage_id=getStorageId(code))
    })


def bar_beer_arrival_delete(request):
    BeerArrival.objects.get(id=request.GET.get('id')).delete()
    return redirect('/bar/arrival/beer?code=' + request.GET.get('code'))


def bar_drinks_arrival(request):
    if request.method == 'POST':
        type = 0 if request.POST.get('typeOpl') is None else 1
        row = BeerArrival(
            date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
            storage_id=getStorageId(request.POST["code"]),
            num=request.POST["num"],
            supplier=Products.objects.get(id=request.POST["beer"]).supplier_id,
            product=request.POST["beer"],
            amount=request.POST["amount"],
            sum=request.POST["sum"],
            type=type
        )
        row.save()
        if type == 1:
            try:
                supplier = Suppliers.objects.get(
                    supplier_id=Products.objects.get(id=request.POST["beer"]).supplier_id).name
            except Suppliers.DoesNotExist:
                supplier = 'Не назначен'
            row = Expenses(
                date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
                storage_id=getStorageId(request.POST["code"]),
                expense='Пиво/напитки',
                sum=request.POST["sum"],
                supplier_id=Products.objects.get(id=request.POST["beer"]).supplier_id,
                product_id=request.POST["beer"],
                num=request.POST["num"],
                is_bn=0,
                comment=supplier + ' // ' + request.POST["num"]
            )
            row.save()

        return redirect('/bar/arrival/drinks?code=' + request.POST["code"])
    code = request.GET.get('code')

    return render(request, 'bar/bar_drinks_arrival.html', context={
        "code": code,
        "storage_id": getStorageId(code),
        "cafe": getStorageName(code),
        "date": (get_current_time() - datetime.timedelta(hours=2)).strftime('%d.%m.%Y'),
        "beers": Products.objects.filter(product_category='Бар'),
        "products": Products.objects.all(),
        "suppliers": Suppliers.objects.all(),
        "rows": BeerArrival.objects.filter(
            date_at=(get_current_time() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d'),
            storage_id=getStorageId(code))
    })


def bar_drinks_arrival_delete(request):
    BeerArrival.objects.get(id=request.GET.get('id')).delete()
    return redirect('/bar/arrival/drinks?code=' + request.GET.get('code'))


def bar_beer_request_delete(request):
    try:
        TovarRequests.objects.get(id=request.GET.get('id')).delete()
    except TovarRequests.DoesNotExist:
        pass
    return redirect('/bar/request/beer?code=' + request.GET.get('code'))
