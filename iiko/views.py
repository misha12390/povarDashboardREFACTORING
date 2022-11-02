from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Suppliers, Categories, Products, Storages, IikoArrivals, BeerArrival
import xml.etree.ElementTree as ET
import json
from functions import *


@login_required
def iiko(request):
    return render(request, 'base.html')


@login_required
def suppliers(request):
    root = ET.fromstring(getIikoSuppliersByBrand())

    for country in root.findall('employee'):
        id = country.find('id').text
        code = country.find('code').text
        name = country.find('name').text
        deleted = country.find('deleted').text
        supplier = country.find('supplier').text
        employee = country.find('employee').text
        client = country.find('client').text

        obj = Suppliers.objects.filter(supplier_id=id).count()
        if obj == 0:
            supplier = Suppliers(
                supplier_id=id,
                code=code,
                name=name,
                deleted=deleted,
                supplier=supplier,
                employee=employee,
                client=client,
                friendly_name=name
            )
            supplier.save()
    return render(request, 'iiko/suppliers.html', context={
        "suppliers": Suppliers.objects.all(),
    })


@login_required
def supplier_edit(request):
    if request.method == 'POST':
        category = request.POST["category"]
        name = request.POST["name"]

        record = Suppliers.objects.get(id=request.GET.get('id'))
        record.friendly_name = name
        record.category = category
        record.is_revise = request.POST.get("is_revise") if request.POST.get('is_revise') is not None else 0
        record.save()

        return redirect('/iiko/suppliers')

    return render(request, 'iiko/supplier_edit.html', context={
        "categories": Categories.objects.all(),
        "supplier": Suppliers.objects.get(id=request.GET.get('id'))
    })


@login_required()
def nomenclature(request):
    if request.GET.get('update') is not None:
        root = ET.fromstring(getIikoNomenclatureByBrand())

        id = ''
        parentId = ''
        num = ''
        code = ''
        name = ''
        productType = ''
        productCategory = ''
        mainUnit = ''

        for country in root.findall('productDto'):
            if country.find('id') is not None:
                id = country.find('id').text
            if country.find('parentId') is not None:
                parentId = country.find('parentId').text
            if country.find('num') is not None:
                num = country.find('num').text
            if country.find('code') is not None:
                code = country.find('code').text
            if country.find('name') is not None:
                name = country.find('name').text
            if country.find('productType') is not None:
                productType = country.find('productType').text
            if country.find('mainUnit') is not None:
                mainUnit = country.find('mainUnit').text
            if country.find('productCategory') is not None:
                productCategory = country.find('productCategory').text

            if country.find('productGroupType') is None:
                if country.find('productType').text != 'MODIFIER':
                    if country.find('productCategory') is not None:
                        obj = Products.objects.filter(product_id=id).count()
                        if obj == 0:
                            product = Products(
                                product_id=id,
                                parent_id=parentId,
                                num=num,
                                code=code,
                                name=name,
                                product_type=productType,
                                main_unit=mainUnit,
                                product_category=productCategory,
                            )
                            product.save()
                        else:
                            product = Products.objects.get(product_id=id)
                            product.name = name
                            product.product_type = productType
                            product.main_unit = mainUnit
                            product.product_category = productCategory
                            product.save()
                    else:
                        obj = Products.objects.filter(product_id=id).count()
                        if obj == 0:
                            product = Products(
                                product_id=id,
                                parent_id=parentId,
                                num=num,
                                code=code,
                                name=name,
                                product_type=productType,
                                main_unit=mainUnit,
                                product_category='None',
                            )
                            product.save()
                        else:
                            object = Products.objects.get(product_id=id)
                            object.name = name
                            object.product_type = productType
                            object.main_unit = mainUnit
                            object.product_category = 'None'
                            object.save()
        return redirect('/iiko/nomenclature')
    return render(request, 'iiko/nomenclature.html', context={
        "type": request.GET.get('type'),
        "products": Products.objects.all(),
        "suppliers": Suppliers.objects.all()
    })


@login_required()
def nomenclature_edit(request):
    if request.method == 'POST':
        supplier = request.POST["supplier"]
        wanna_order = request.POST["wanna_order"]
        minimal = request.POST["minimal"]

        obj = Products.objects.get(id=request.GET.get('id'))
        obj.supplier_id = supplier
        obj.wanna_order = wanna_order
        obj.minimal = minimal
        obj.save()

        rows = BeerArrival.objects.filter(product=request.GET.get('id'))
        for row in rows:
            row.supplier = supplier
            row.save()

        return redirect('/iiko/nomenclature')
    return render(request, 'iiko/nomenclature_edit.html', context={
        "suppliers": Suppliers.objects.all(),
        "object": Products.objects.get(id=request.GET.get('id'))
    })


@login_required()
def categories(request):
    if request.GET.get('update') is not None:
        jsonData = getIikoUserCategories()
        dictData = json.loads(jsonData)

        for i in range(len(dictData)):
            obj = Categories.objects.filter(category_id=dictData[i]["id"]).count()
            if obj == 0:
                category = Categories(
                    category_id=dictData[i]["id"],
                    name=dictData[i]["name"],
                    is_remains=0,
                    is_sales=0,
                    is_income=0
                )
                category.save()

        return redirect('/iiko/categories')
    return render(request, 'iiko/categories.html', context={
        "categories": Categories.objects.all()
    })


@login_required()
def sales(request):
    pass


@login_required()
def sales_by_types(request):
    pass


@login_required()
def arrivals(request):
    if request.method == 'POST':
        dateFrom = request.POST["dateFrom"]
        dateTo = request.POST["dateTo"]
        root = ET.fromstring(getIikoTovarNomenclature(dateFrom, dateTo))
        for c in root.findall('document'):
            document_id = c.find('id').text
            if IikoArrivals.objects.filter(document_id=document_id).count() == 0:
                date = c.find('incomingDate').text
                store = c.find('defaultStore').text
                supplier = c.find('supplier').text
                number = '' if c.find('incomingDocumentNumber') is None else c.find('incomingDocumentNumber').text
                comment = '' if c.find('comment') is None else c.find('comment').text
                storage_id = Storages.objects.get(storage_id=store).id
                supplier_id = Suppliers.objects.get(supplier_id=supplier).id
                for cc in c.findall('items/item'):
                    tovar = cc.find('product').text
                    sum = cc.find('sum').text
                    amount = cc.find('amount').text
                    comment = '' if comment is None else comment
                    paid_sum = 0 if 'не' in comment or len(comment) == 0 else sum
                    try:
                        product_category = Products.objects.get(product_id=tovar).product_category
                    except Products.DoesNotExist:
                        product_category = -1
                    try:
                        category_id = Categories.objects.get(name=product_category).id
                    except Categories.DoesNotExist:
                        category_id = -1
                    try:
                        product_id = Products.objects.get(product_id=tovar).id
                    except Products.DoesNotExist:
                        product_id = -1
                    row = IikoArrivals(
                        document_id=document_id,
                        date_at=date,
                        storage_id=storage_id,
                        supplier_id=supplier_id,
                        invoice_num=number,
                        product_id=product_id,
                        amount=-1 if amount is None else amount.split('.')[0],
                        sum=-1 if sum is None else sum.split('.')[0],
                        paid_sum=str(paid_sum).split('.')[0],
                        comment=comment,
                        category_id=category_id
                    )
                    row.save()

    return render(request, 'iiko/arrivals.html', context={
        "tovars": IikoArrivals.objects.all(),
        "categories": Categories.objects.all(),
        "suppliers": Suppliers.objects.all(),
        "products": Products.objects.all(),
        "storages": Storages.objects.all(),
        "date": get_current_time().strftime('%Y-%m-%d')
    })


@login_required()
def inventory(request):
    rows = []
    records = dict()
    productCategory = Categories.objects.get(id=request.GET.get('category')).name if request.GET.get('category') is not None else None
    if request.GET.get('storage_id') is not None:
        if request.GET.get('storage_id') == '0':
            for storage in Storages.objects.all():
                xml = checkInventory(storage.storage_id, productCategory)
                items = ET.fromstring(xml)
                dictionary = dict()
                products = dict()
                total = 0
                for item in items.findall('items/item'):
                    name = None
                    for product in item.findall('product'):
                        name = product.find('name').text
                    expectedAmount = item.find('expectedAmount').text
                    products[name] = expectedAmount
                    total += float(expectedAmount)
                products['total'] = total
                dictionary[storage.id] = products
                rows.append(dictionary)
        else:
            storage_id = Storages.objects.get(id=request.GET.get('storage_id')).storage_id
            xml = checkInventory(storage_id, productCategory)
            items = ET.fromstring(xml)
            for item in items.findall('items/item'):
                name = None
                for product in item.findall('product'):
                    name = product.find('name').text
                expectedAmount = item.find('expectedAmount').text
                records[name] = expectedAmount
    return render(request, 'iiko/inventory.html', context={
        "storage_id": int(request.GET.get('storage_id')) if request.GET.get('storage_id') is not None else None,
        "categories": Categories.objects.filter(is_remains=1),
        "storages": Storages.objects.all(),
        "products": Products.objects.filter(product_category=productCategory),
        "rows": rows,
        "records": records
    })


@login_required()
def inventory_send(request):
    root = ET.fromstring(getIikoStorages())
    categoryId = request.GET.get('categoryId')
    for country in root.findall('corporateItemDto'):
        storage_id = country.find('id').text
        cat = Categories.objects.filter(is_remains=1)
        for ca in cat:
            if categoryId == 'bar':
                if ca.name == 'Бар':
                    xml = checkInventory(storage_id, ca.name)
                    root = ET.fromstring(xml)
                    storage = Storages.objects.get(storage_id=storage_id).name
                    data = 'Заведение: ' + storage + '%0A'
                    name = None
                    id = None
                    for cc in root.findall('items/item'):
                        for c in cc.findall('product'):
                            name = c.find('name').text
                            id = c.find('id').text
                        expectedAmount = cc.find('expectedAmount').text
                        minimal = Products.objects.get(product_id=id)
                        if minimal.minimal is None:
                            min = 0
                        else:
                            min = minimal.minimal
                        if expectedAmount is None:
                            am = 0
                        else:
                            am = expectedAmount
                        if int(round(float(am))) <= int(min):
                            amount = f'{int(round(float(expectedAmount)))}'
                            # worker.name
                            data += '%0A' + name + ': ' + amount
                    if len(data) > 40:
                        send_webhook('-chat_id', data, 1)
            elif categoryId == 'beer':
                if ca.name == 'Пиво разливное':
                    xml = checkInventory(storage_id, ca.name)
                    root = ET.fromstring(xml)
                    storage = Storages.objects.get(storage_id=storage_id).name
                    data = 'Заведение: ' + storage + '%0A'
                    name = None
                    id = None
                    for cc in root.findall('items/item'):
                        for c in cc.findall('product'):
                            name = c.find('name').text
                            id = c.find('id').text
                        expectedAmount = cc.find('expectedAmount').text
                        minimal = Products.objects.get(product_id=id)

                        if int(round(float(expectedAmount))) <= int(minimal.minimal):
                            amount = f'{int(round(float(expectedAmount)))}'
                            # worker.name
                            data += '%0A' + name + ': ' + amount
                    if len(data) > 40:
                        send_webhook('-chat_id', data, 1)

    return redirect('/iiko')
