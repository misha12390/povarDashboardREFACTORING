import datetime
import requests
from .models import Brand, Products

url = 'https://khmelnoy-povar.iiko.it:443'
departmentId = '886e9a6b-68e5-129d-0172-e616e8710011'

def get_current_time() -> datetime:
    delta = datetime.timedelta(hours=3, minutes=0)
    return datetime.datetime.now(datetime.timezone.utc) + delta

def iiko_connect():
    brand = Brand.objects.get(id = 1)

    send_text = brand.url_api + '/resto/api/auth?login=' + brand.login_api + '&pass=' + brand.pass_api
    r = requests.get(send_text)
    brand.key_api = r.text
    brand.key_updated_at = get_current_time().strftime('%Y-%m-%d %H:%M:%S')
    brand.save()
    return brand.key_api

def iiko_disconnect():
    brand = Brand.objects.get(id = 1)

    send_text = brand.url_api + '/resto/api/logout?key=' + brand.key_api
    r = requests.get(send_text)
    return r.text

def getIikoMuchSales(dateFrom, dateTo):
    token = iiko_connect()
    send_text = url + '/resto/api/reports/olap?key=' + token + '&report=SALES&from=' + dateFrom + '&to=' + dateTo + '&groupRow=DishName&groupRow=OpenTime&groupRow=OrderDeleted&groupRow=DishMeasureUnit&groupRow=DishAmountInt&groupRow=DishCategory&agr=fullSum&agr=OrderNum&groupRow=Store.Name'
    r = requests.get(send_text)
    iiko_disconnect()
    return r.text

def getIikoNomenclatureByBrand():
    token = iiko_connect()
    send_text = url + '/resto/api/products?includeDeleted=false&key=' + token
    r = requests.get(send_text)
    iiko_disconnect()
    return r.text


def getIikoKassaByBrand():
    token = iiko_connect()
    send_text = url + '/resto/api/corporation/groups?key=' + token
    r = requests.get(send_text)
    iiko_disconnect()
    return r.text


def getIikoCashShifts(dateFrom, dateTo):
    token = iiko_connect()
    send_text = url + '/resto/api/closeSession/list?dateFrom=' + dateFrom + '&dateTo=' + dateTo + '&key=' + token
    r = requests.get(send_text)
    iiko_disconnect()
    return r.text

def getIikoCashShifts2(dateFrom, dateTo):
    token = iiko_connect()
    send_text = url + '/resto/api/v2/cashshifts/list?openDateFrom=' + dateFrom + '&openDateTo=' + dateTo + '&status=ANY&key=' + token
    r = requests.get(send_text)
    iiko_disconnect()
    return r.text

def getIikoPaymentTypes():
    token = iiko_connect()
    send_text = url + '/resto/api/v2/entities/list?rootType=PaymentType&key=' + token
    r = requests.get(send_text)
    iiko_disconnect()
    return r.text

def getIikoTovarNomenclature(dateFrom, dateTo):
    token = iiko_connect()
    send_text = url + '/resto/api/documents/export/incomingInvoice?key=' + token + '&from=' + dateFrom + '&to=' + dateTo
    r = requests.get(send_text)
    iiko_disconnect()
    return r.text

def getIikoSuppliersByBrand():
    token = iiko_connect()
    send_text = url + '/resto/api/suppliers?key=' + token
    r = requests.get(send_text)
    iiko_disconnect()
    return r.text

def getIikoUserCategories():
    token = iiko_connect()
    send_text = url + '/resto/api/v2/entities/products/category/list?key=' + token
    r = requests.get(send_text)
    iiko_disconnect()
    return r.text

def checkInventory(storageId, productCategory):
    token = iiko_connect()
    send_text = url + '/resto/api/documents/check/incomingInventory?key=' + token
    year = get_current_time().strftime('%Y')
    month = get_current_time().strftime('%m')
    day = get_current_time().strftime('%d')
    items = Products.objects.filter(product_category = productCategory)
    items_str = '<items>'
    for item in items:
        items_str += f'<item><productId>{item.product_id}</productId><amountContainer>0</amountContainer></item>'
    items_str += '</items>'

    data = f"<?xml version=\"1.0\"?>\r\n<document>\r\n  <documentNumber>{get_current_time().strftime('%Y%m%d%H%M%S')}</documentNumber>\r\n  <dateIncoming>{datetime.date(int(year), int(month), int(day)) - datetime.timedelta(days=0)}T23:59:59</dateIncoming>\r\n  <status>NEW</status>\r\n  <storeId>{storageId}</storeId>\r\n  <comment> </comment>\r\n{items_str}</document>"
    r = requests.post(send_text, data=data, headers={'Content-Type': 'application/xml;charset=UTF-8'})
    iiko_disconnect()
    return r.text


def getIikoStorages():
    token = iiko_connect()
    send_text = url + '/resto/api/corporation/stores?key=' + token
    r = requests.get(send_text)
    iiko_disconnect()
    return r.text


def getSalesByDepartment(sessionId):
    token = iiko_connect()
    send_text = url + '/resto/api/v2/cashshifts/payments/list/' + sessionId + '?key=' + token + '&hideAccepted=false'
    r = requests.get(send_text)
    iiko_disconnect()
    return r.text