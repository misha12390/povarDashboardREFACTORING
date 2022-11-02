# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Paymenttypes(models.Model):
    payment_id = models.CharField(max_length=256)
    code = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    is_active = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'PaymentTypes'


class AutoSalary(models.Model):
    fio = models.CharField(max_length=256)
    date_at = models.CharField(max_length=256)
    storage_id = models.IntegerField()
    oklad = models.IntegerField()
    percent = models.IntegerField()
    premium = models.IntegerField()
    fine = models.IntegerField()
    total = models.IntegerField()

    class Meta:
        
        managed = True
        db_table = 'auto_salary'


class Blacklist(models.Model):
    date_at = models.DateField()
    storage_id = models.IntegerField()

    class Meta:
        
        managed = True
        db_table = 'blacklist'


class Brand(models.Model):
    name = models.CharField(max_length=24)
    url_api = models.CharField(max_length=255, blank=True, null=True)
    key_api = models.CharField(max_length=36, blank=True, null=True)
    key_updated_at = models.DateTimeField(blank=True, null=True)
    login_api = models.CharField(max_length=24, blank=True, null=True)
    pass_api = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        
        managed = True
        db_table = 'brand'


class Categories(models.Model):
    category_id = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    is_remains = models.IntegerField()
    is_sales = models.IntegerField()
    is_income = models.IntegerField()

    class Meta:
        
        managed = True
        db_table = 'categories'


class Employee(models.Model):
    code = models.CharField(max_length=256, blank=True, null=True)
    photo = models.IntegerField(blank=True, null=True)
    fio = models.CharField(max_length=64)
    birth_date = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    type = models.CharField(max_length=24, blank=True, null=True)
    storage_id = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    first_work_day = models.CharField(max_length=256, blank=True, null=True)
    oklad = models.IntegerField()
    is_deleted = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        
        managed = True
        db_table = 'employee'


class Expenses(models.Model):
    created_at = models.DateField()
    date_at = models.DateField()
    storage_id = models.IntegerField()
    name = models.CharField(max_length=128)
    sum = models.IntegerField()
    comment = models.CharField(max_length=256, blank=True, null=True)
    is_bn = models.IntegerField()

    class Meta:
        
        managed = True
        db_table = 'expenses'


class ExpensesSource(models.Model):
    text = models.CharField(max_length=256, blank=True, null=True)
    type = models.IntegerField()
    is_active = models.IntegerField()
    input_name = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        
        managed = True
        db_table = 'expenses_source'


class Inventory(models.Model):
    name = models.CharField(max_length=256)
    amount = models.CharField(max_length=256)
    difference = models.CharField(max_length=256)
    fact = models.CharField(max_length=256)
    garazh = models.IntegerField(blank=True, null=True)
    esenina = models.IntegerField(blank=True, null=True)
    nevkipelogo = models.IntegerField(blank=True, null=True)
    cherkasskaya = models.IntegerField(blank=True, null=True)
    chekistov = models.IntegerField(blank=True, null=True)
    sormovskaya = models.IntegerField(blank=True, null=True)
    itogo = models.IntegerField(blank=True, null=True)

    class Meta:
        
        managed = True
        db_table = 'inventory'


class Money(models.Model):
    created_at = models.DateField()
    date_at = models.DateField()
    storage_id = models.IntegerField()
    sum_cash_morning = models.IntegerField()
    sum_cash_end_day = models.IntegerField(blank=True, null=True)
    total_cash = models.IntegerField(blank=True, null=True)
    total_bn = models.IntegerField(blank=True, null=True)
    total_market = models.IntegerField(blank=True, null=True)
    total_day = models.IntegerField(blank=True, null=True)
    calculated = models.IntegerField(blank=True, null=True)
    difference = models.IntegerField(blank=True, null=True)
    total_salary = models.IntegerField(blank=True, null=True)
    total_expenses = models.IntegerField(blank=True, null=True)
    payin = models.IntegerField(blank=True, null=True)
    payout = models.IntegerField(blank=True, null=True)

    class Meta:
        
        managed = True
        db_table = 'money'


class PayinText(models.Model):
    text = models.CharField(max_length=256)

    class Meta:
        
        managed = True
        db_table = 'payin_text'


class Pays(models.Model):
    created_at = models.DateField()
    date_at = models.DateField()
    storage_id = models.IntegerField()
    type = models.IntegerField()
    sum = models.IntegerField()
    comment = models.CharField(max_length=128)

    class Meta:
        
        managed = True
        db_table = 'pays'


class Positions(models.Model):
    position = models.CharField(max_length=256, blank=True, null=True)
    type = models.CharField(max_length=64)
    oklad = models.IntegerField(blank=True, null=True)

    class Meta:
        
        managed = True
        db_table = 'positions'


class Products(models.Model):
    product_id = models.CharField(max_length=256, blank=True, null=True)
    parent_id = models.CharField(max_length=256, blank=True, null=True)
    num = models.CharField(max_length=256, blank=True, null=True)
    code = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    product_type = models.CharField(max_length=256, blank=True, null=True)
    main_unit = models.CharField(max_length=256, blank=True, null=True)
    product_category = models.CharField(max_length=256, blank=True, null=True)
    supplier_id = models.CharField(max_length=256)
    minimal = models.IntegerField(blank=True, null=True)
    wanna_order = models.IntegerField(blank=True, null=True)

    class Meta:
        
        managed = True
        db_table = 'products'


class Salary(models.Model):
    created_at = models.DateField()
    date_at = models.DateField()
    storage_id = models.IntegerField()
    employee_id = models.IntegerField()
    type = models.IntegerField()
    oklad = models.IntegerField()
    percent = models.IntegerField()
    premium = models.IntegerField()
    month = models.CharField(max_length=64, blank=True, null=True)
    days = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        
        managed = True
        db_table = 'salary'


class Storages(models.Model):
    code = models.CharField(max_length=256)
    storage_id = models.CharField(max_length=256)
    pointofsale = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256)
    yur_lico = models.CharField(max_length=128)

    class Meta:
        
        managed = True
        db_table = 'storages'


class Timetable(models.Model):
    created_at = models.DateField()
    date_at = models.DateField()
    storage_id = models.IntegerField()
    employee_id = models.IntegerField()
    position_id = models.IntegerField()
    oklad = models.IntegerField()

    class Meta:
        
        managed = True
        db_table = 'timetable'
