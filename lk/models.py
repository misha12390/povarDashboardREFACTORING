# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bankparser(models.Model):
    date_at = models.CharField(max_length=256)
    type = models.IntegerField()
    number = models.CharField(max_length=256)
    sum = models.CharField(max_length=256)
    payer = models.CharField(max_length=256)
    payer_inn = models.CharField(max_length=256)
    date = models.CharField(max_length=256)
    recipient = models.CharField(max_length=256)
    payment = models.CharField(max_length=256)
    card_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'BankParser'


class Cashshifts(models.Model):
    session_id = models.CharField(max_length=256)
    opendate = models.CharField(db_column='openDate', max_length=256)  # Field name made lowercase.
    closedate = models.CharField(db_column='closeDate', max_length=256)  # Field name made lowercase.
    payorders = models.CharField(db_column='payOrders', max_length=256)  # Field name made lowercase.
    salescash = models.CharField(db_column='salesCash', max_length=256)  # Field name made lowercase.
    salescard = models.CharField(db_column='salesCard', max_length=256)  # Field name made lowercase.
    payin = models.CharField(db_column='payIn', max_length=256)  # Field name made lowercase.
    payout = models.CharField(db_column='payOut', max_length=256)  # Field name made lowercase.
    pointofsale = models.CharField(db_column='pointOfSale', max_length=256)  # Field name made lowercase.
    cafe = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'Cashshifts'


class Expenses(models.Model):
    created_at = models.CharField(max_length=256)
    date_at = models.DateField()
    storage_id = models.IntegerField()
    expense = models.CharField(max_length=256)
    comment = models.CharField(max_length=256)
    sum = models.CharField(max_length=256)
    is_bn = models.IntegerField()
    supplier_id = models.CharField(max_length=256, blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    num = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Expenses'


class Files(models.Model):
    filename = models.CharField(max_length=128)
    preparation = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Files'


class Paymenttypes(models.Model):
    payment_id = models.CharField(max_length=256)
    code = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'PaymentTypes'


class Pays(models.Model):
    created_at = models.CharField(max_length=256)
    date_at = models.CharField(max_length=256)
    storage_id = models.IntegerField()
    type = models.IntegerField()
    comment = models.CharField(max_length=256)
    sum = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'Pays'


class Povarlogs(models.Model):
    date = models.CharField(max_length=128)
    writer = models.CharField(max_length=128)
    sum = models.IntegerField()
    worker = models.CharField(max_length=128)
    cafe = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    fromtype = models.CharField(max_length=128, blank=True, null=True)
    comment = models.CharField(max_length=128, blank=True, null=True)
    photo = models.CharField(max_length=128, blank=True, null=True)
    photoblob = models.TextField(db_column='photoBLOB', blank=True, null=True)  # Field name made lowercase.
    yur_lico = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Povarlogs'


class Secondpovar(models.Model):
    date = models.CharField(max_length=128)
    writer = models.CharField(max_length=128)
    sum = models.IntegerField()
    worker = models.CharField(max_length=128)
    cafe = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    fromtype = models.CharField(max_length=128, blank=True, null=True)
    comment = models.CharField(max_length=128, blank=True, null=True)
    photo = models.CharField(max_length=128, blank=True, null=True)
    photoblob = models.TextField(db_column='photoBLOB', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SecondPovar'


class Sumofdeal(models.Model):
    num = models.IntegerField()
    date = models.CharField(max_length=64)
    month = models.CharField(max_length=64)
    sum = models.IntegerField()
    precent = models.IntegerField()
    first_sum = models.CharField(max_length=64)
    second_sum = models.CharField(max_length=64)
    third_sum = models.CharField(max_length=64)
    fourth_sum = models.CharField(max_length=64)
    comment = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'SumOfDeal'


class Tglogs(models.Model):
    worker = models.CharField(max_length=128, db_collation='utf8_general_ci')
    number = models.CharField(max_length=128, db_collation='utf8_general_ci')
    date = models.CharField(max_length=64, db_collation='utf8_general_ci')
    sum = models.IntegerField()
    note_photo = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    note_photo2 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    note_photo3 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    tovar_photo = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    tovar_photo2 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    tovar_photo3 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    tovar_photo4 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    tovar_photo5 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    sklad = models.TextField(db_collation='utf8_general_ci')
    comment = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    note_photoblob = models.TextField(db_column='note_photoBLOB', blank=True, null=True)  # Field name made lowercase.
    note_photo2blob = models.TextField(db_column='note_photo2BLOB', blank=True, null=True)  # Field name made lowercase.
    note_photo3blob = models.TextField(db_column='note_photo3BLOB', blank=True, null=True)  # Field name made lowercase.
    tovar_photoblob = models.TextField(db_column='tovar_photoBLOB', blank=True, null=True)  # Field name made lowercase.
    tovar_photo2blob = models.TextField(db_column='tovar_photo2BLOB', blank=True, null=True)  # Field name made lowercase.
    tovar_photo3blob = models.TextField(db_column='tovar_photo3BLOB', blank=True, null=True)  # Field name made lowercase.
    tovar_photo4blob = models.TextField(db_column='tovar_photo4BLOB', blank=True, null=True)  # Field name made lowercase.
    tovar_photo5blob = models.TextField(db_column='tovar_photo5BLOB', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TGlogs'


class Tgmsklogs(models.Model):
    worker = models.CharField(max_length=128, db_collation='utf8_general_ci')
    number = models.CharField(max_length=128, db_collation='utf8_general_ci')
    date = models.CharField(max_length=64, db_collation='utf8_general_ci')
    sum = models.IntegerField()
    note_photo = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    note_photo2 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    note_photo3 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    tovar_photo = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    tovar_photo2 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    tovar_photo3 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    tovar_photo4 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    tovar_photo5 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    sklad = models.TextField(db_collation='utf8_general_ci')
    comment = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    note_photoblob = models.TextField(db_column='note_photoBLOB', blank=True, null=True)  # Field name made lowercase.
    note_photo2blob = models.TextField(db_column='note_photo2BLOB', blank=True, null=True)  # Field name made lowercase.
    note_photo3blob = models.TextField(db_column='note_photo3BLOB', blank=True, null=True)  # Field name made lowercase.
    tovar_photoblob = models.TextField(db_column='tovar_photoBLOB', blank=True, null=True)  # Field name made lowercase.
    tovar_photo2blob = models.TextField(db_column='tovar_photo2BLOB', blank=True, null=True)  # Field name made lowercase.
    tovar_photo3blob = models.TextField(db_column='tovar_photo3BLOB', blank=True, null=True)  # Field name made lowercase.
    tovar_photo4blob = models.TextField(db_column='tovar_photo4BLOB', blank=True, null=True)  # Field name made lowercase.
    tovar_photo5blob = models.TextField(db_column='tovar_photo5BLOB', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TGmsklogs'


class Tgmskotlogs(models.Model):
    order_number = models.IntegerField()
    order_fio = models.TextField(db_collation='utf8_general_ci')
    ottovar_photo = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    ottovar_photo2 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    ottovar_photo3 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    ottovar_photo4 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    ottovar_photo5 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    otnote_photo = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    otnote_photo2 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    otnote_photo3 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    otcomment = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    otnote_photoblob = models.TextField(db_column='otnote_photoBLOB', blank=True, null=True)  # Field name made lowercase.
    otnote_photo2blob = models.TextField(db_column='otnote_photo2BLOB', blank=True, null=True)  # Field name made lowercase.
    otnote_photo3blob = models.TextField(db_column='otnote_photo3BLOB', blank=True, null=True)  # Field name made lowercase.
    ottovar_photoblob = models.TextField(db_column='ottovar_photoBLOB', blank=True, null=True)  # Field name made lowercase.
    ottovar_photo2blob = models.TextField(db_column='ottovar_photo2BLOB', blank=True, null=True)  # Field name made lowercase.
    ottovar_photo3blob = models.TextField(db_column='ottovar_photo3BLOB', blank=True, null=True)  # Field name made lowercase.
    ottovar_photo4blob = models.TextField(db_column='ottovar_photo4BLOB', blank=True, null=True)  # Field name made lowercase.
    ottovar_photo5blob = models.TextField(db_column='ottovar_photo5BLOB', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TGmskotlogs'


class Tgotlogs(models.Model):
    order_number = models.IntegerField()
    order_fio = models.TextField(db_collation='utf8_general_ci')
    ottovar_photo = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    ottovar_photo2 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    ottovar_photo3 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    ottovar_photo4 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    ottovar_photo5 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    otnote_photo = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    otnote_photo2 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    otnote_photo3 = models.CharField(max_length=128, db_collation='utf8_general_ci', blank=True, null=True)
    otcomment = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    otnote_photoblob = models.TextField(db_column='otnote_photoBLOB', blank=True, null=True)  # Field name made lowercase.
    otnote_photo2blob = models.TextField(db_column='otnote_photo2BLOB', blank=True, null=True)  # Field name made lowercase.
    otnote_photo3blob = models.TextField(db_column='otnote_photo3BLOB', blank=True, null=True)  # Field name made lowercase.
    ottovar_photoblob = models.TextField(db_column='ottovar_photoBLOB', blank=True, null=True)  # Field name made lowercase.
    ottovar_photo2blob = models.TextField(db_column='ottovar_photo2BLOB', blank=True, null=True)  # Field name made lowercase.
    ottovar_photo3blob = models.TextField(db_column='ottovar_photo3BLOB', blank=True, null=True)  # Field name made lowercase.
    ottovar_photo4blob = models.TextField(db_column='ottovar_photo4BLOB', blank=True, null=True)  # Field name made lowercase.
    ottovar_photo5blob = models.TextField(db_column='ottovar_photo5BLOB', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TGotlogs'


class Tables(models.Model):
    username = models.CharField(max_length=128)
    chat_id = models.CharField(max_length=64)
    date = models.CharField(max_length=64)
    time = models.CharField(max_length=64)
    cafe = models.CharField(max_length=64)
    hour = models.CharField(max_length=16)
    status = models.CharField(max_length=32)
    asd = models.TextField()

    class Meta:
        managed = False
        db_table = 'Tables'


class Yablopovar(models.Model):
    date = models.CharField(max_length=128)
    writer = models.CharField(max_length=128)
    sum = models.IntegerField()
    worker = models.CharField(max_length=128)
    cafe = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    fromtype = models.CharField(max_length=128, blank=True, null=True)
    comment = models.CharField(max_length=128, blank=True, null=True)
    photo = models.CharField(max_length=128, blank=True, null=True)
    photoblob = models.TextField(db_column='photoBLOB', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'YabloPovar'


class Zapadpovar(models.Model):
    date = models.CharField(max_length=128)
    writer = models.CharField(max_length=128)
    sum = models.IntegerField()
    worker = models.CharField(max_length=128)
    cafe = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    fromtype = models.CharField(max_length=128, blank=True, null=True)
    comment = models.CharField(max_length=128, blank=True, null=True)
    photo = models.CharField(max_length=128, blank=True, null=True)
    photoblob = models.TextField(db_column='photoBLOB', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ZapadPovar'


class AccountEmailaddress(models.Model):
    email = models.CharField(unique=True, max_length=254)
    verified = models.IntegerField()
    primary = models.IntegerField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailaddress'


class AccountEmailconfirmation(models.Model):
    created = models.DateTimeField()
    sent = models.DateTimeField(blank=True, null=True)
    key = models.CharField(unique=True, max_length=64)
    email_address = models.ForeignKey(AccountEmailaddress, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailconfirmation'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    telegram_id = models.CharField(max_length=256, blank=True, null=True)
    is_lk = models.IntegerField()
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AutoSalary(models.Model):
    fio = models.CharField(max_length=256)
    date_at = models.CharField(max_length=256)
    storage_id = models.IntegerField()
    oklad = models.IntegerField()
    precent = models.IntegerField()
    premium = models.IntegerField()
    fine = models.IntegerField()
    total = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auto_salary'


class BeerArrival(models.Model):
    date_at = models.DateField()
    storage_id = models.IntegerField()
    num = models.CharField(max_length=64)
    supplier = models.CharField(max_length=256)
    product = models.IntegerField()
    amount = models.IntegerField()
    sum = models.IntegerField()
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'beer_arrival'


class Blacklist(models.Model):
    date_at = models.DateField()
    storage_id = models.IntegerField()
    photo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'blacklist'


class Brand(models.Model):
    name = models.CharField(max_length=24)
    url_api = models.CharField(max_length=255, blank=True, null=True)
    key_api = models.CharField(max_length=36, blank=True, null=True)
    key_updated_at = models.DateTimeField(blank=True, null=True)
    login_api = models.CharField(max_length=24, blank=True, null=True)
    pass_api = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brand'


class CalculatedSum(models.Model):
    storage_id = models.IntegerField()
    sum = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'calculated_sum'


class Calendar(models.Model):
    storage_id = models.IntegerField()
    employee = models.CharField(max_length=256)
    date_at = models.DateField()
    position_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'calendar'


class Cards(models.Model):
    num = models.CharField(max_length=256)
    storage_id = models.IntegerField(blank=True, null=True)
    cafe = models.CharField(max_length=256)
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cards'


class Catalog(models.Model):
    text = models.CharField(max_length=128)
    types = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog'


class Categories(models.Model):
    category_id = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    is_remains = models.IntegerField()
    is_sales = models.IntegerField()
    is_income = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'categories'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


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
        managed = False
        db_table = 'employee'


class EventsDate(models.Model):
    date = models.CharField(max_length=256, blank=True, null=True)
    event = models.CharField(max_length=256, blank=True, null=True)
    poster = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events_date'


class ExpensesSource(models.Model):
    text = models.CharField(max_length=256, blank=True, null=True)
    type = models.IntegerField()
    is_active = models.IntegerField()
    input_name = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expenses_source'


class ExpensesTypes(models.Model):
    text = models.CharField(max_length=256, blank=True, null=True)
    type = models.IntegerField()
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'expenses_types'


class ExpensesTypesTable(models.Model):
    text = models.CharField(max_length=256)
    sum = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expenses_types_table'


class Fines(models.Model):
    text = models.CharField(max_length=256, blank=True, null=True)
    sum = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fines'


class FinesDirectory(models.Model):
    date_at = models.DateField()
    employee_id = models.IntegerField()
    fine_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'fines_directory'


class Fixes(models.Model):
    date_at = models.CharField(max_length=64)
    storage_id = models.IntegerField()
    writer = models.CharField(max_length=64)
    text = models.CharField(max_length=256)
    first_photo = models.TextField(blank=True, null=True)
    second_photo = models.TextField(blank=True, null=True)
    third_photo = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fixes'


class IikoArrivals(models.Model):
    document_id = models.CharField(max_length=128)
    date_at = models.DateField()
    storage_id = models.IntegerField()
    supplier_id = models.IntegerField()
    invoice_num = models.CharField(max_length=64, blank=True, null=True)
    product_id = models.IntegerField()
    amount = models.IntegerField()
    sum = models.IntegerField()
    paid_sum = models.IntegerField()
    category_id = models.IntegerField()
    comment = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iiko_arrivals'


class InfoCategories(models.Model):
    name = models.CharField(max_length=128)
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'info_categories'


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
    gagarina = models.IntegerField(blank=True, null=True)
    itogo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventory'


class JobPosition(models.Model):
    position = models.CharField(max_length=256, blank=True, null=True)
    oklad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_position'


class Kassa(models.Model):
    department_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    is_main = models.IntegerField(blank=True, null=True)
    iiko_id = models.CharField(max_length=36)
    group_iiko_id = models.CharField(max_length=36)
    group_name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    storage_id = models.IntegerField(blank=True, null=True)
    real_name = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'kassa'


class Money(models.Model):
    storage_id = models.IntegerField()
    created_at = models.DateTimeField()
    date_at = models.DateField()
    sum_cash_morning = models.IntegerField(blank=True, null=True)
    total_cash = models.IntegerField(blank=True, null=True)
    total_bn = models.IntegerField(blank=True, null=True)
    total_day = models.IntegerField(blank=True, null=True)
    sum_cash_end_day = models.IntegerField(blank=True, null=True)
    sum_for_precent = models.IntegerField(blank=True, null=True)
    difference = models.CharField(max_length=256, blank=True, null=True)
    difference2 = models.CharField(max_length=256, blank=True, null=True)
    total_market = models.IntegerField(blank=True, null=True)
    payin = models.IntegerField(blank=True, null=True)
    payout = models.IntegerField(blank=True, null=True)
    total_salary = models.IntegerField(blank=True, null=True)
    total_expenses = models.IntegerField(blank=True, null=True)
    deposit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'money'


class Muchsales(models.Model):
    name = models.CharField(max_length=256)
    garazh = models.CharField(max_length=256)
    nevkipelogo = models.CharField(max_length=256)
    cherkass = models.CharField(max_length=256)
    esenina = models.CharField(max_length=256)
    chekistov = models.CharField(max_length=256)
    sormovskaya = models.CharField(max_length=256)
    itogo = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'muchsales'


class Orders(models.Model):
    order_data = models.CharField(max_length=1024)
    total_price = models.CharField(max_length=1024)
    comment = models.CharField(max_length=1024)
    address = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'orders'


class Partners(models.Model):
    storage_id = models.IntegerField()
    name = models.CharField(max_length=256)
    type = models.CharField(max_length=128)
    inn = models.BigIntegerField()
    status = models.IntegerField()
    friendly_name = models.CharField(max_length=256, blank=True, null=True)
    supplier_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partners'


class PayinText(models.Model):
    text = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'payin_text'


class Positions(models.Model):
    position = models.CharField(max_length=256, blank=True, null=True)
    oklad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'positions'


class Price(models.Model):
    price = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'price'


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
        managed = False
        db_table = 'products'


class Salary(models.Model):
    employee_id = models.IntegerField(blank=True, null=True)
    storage_id = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=32, blank=True, null=True)
    sum = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    created_at = models.CharField(max_length=256, blank=True, null=True)
    sum_percent = models.IntegerField(blank=True, null=True)
    premium = models.IntegerField(blank=True, null=True)
    sum_taxi = models.CharField(max_length=256, blank=True, null=True)
    fine = models.IntegerField(blank=True, null=True)
    itogo = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'salary'


class Salesbypayments(models.Model):
    date = models.CharField(max_length=256)
    cafe = models.CharField(max_length=256)
    card = models.CharField(max_length=256)
    money = models.CharField(max_length=256)
    money_w_point = models.CharField(max_length=256)
    qr = models.CharField(max_length=256)
    delivery = models.CharField(max_length=256)
    yandex = models.CharField(max_length=256)
    points = models.CharField(max_length=256)
    total = models.CharField(max_length=256)
    totalcash = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'salesByPayments'


class Salescafepayments(models.Model):
    name = models.CharField(max_length=256)
    card = models.CharField(max_length=256)
    money = models.CharField(max_length=256)
    money_w_point = models.CharField(max_length=256)
    yandex = models.CharField(max_length=256)
    delivery = models.CharField(max_length=256)
    points = models.CharField(max_length=256)
    qr = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'salesCafePayments'


class Statement(models.Model):
    date_at = models.CharField(max_length=64)
    type = models.IntegerField()
    number = models.IntegerField()
    sum = models.CharField(max_length=256)
    date = models.CharField(max_length=64)
    payment = models.CharField(max_length=512)
    payer_id = models.IntegerField(blank=True, null=True)
    recipient_id = models.IntegerField(blank=True, null=True)
    card_id = models.IntegerField()
    storage_id = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statement'


class Storages(models.Model):
    code = models.CharField(max_length=256)
    storage_id = models.CharField(max_length=256)
    pointofsale = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256)
    yur_lico = models.CharField(max_length=128)
    small_name = models.CharField(max_length=256)
    phone = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'storages'


class Suppliers(models.Model):
    supplier_id = models.CharField(max_length=256)
    code = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    deleted = models.CharField(max_length=128)
    supplier = models.CharField(max_length=128)
    employee = models.CharField(max_length=128)
    client = models.CharField(max_length=128)
    category = models.CharField(max_length=256)
    friendly_name = models.CharField(max_length=256)
    is_revise = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suppliers'


class Tasks(models.Model):
    date_at = models.DateField()
    writer = models.CharField(max_length=256, blank=True, null=True)
    section = models.IntegerField(blank=True, null=True)
    task = models.CharField(max_length=1048, blank=True, null=True)
    priority = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tasks'


class Timetable(models.Model):
    employee_id = models.IntegerField()
    storage_id = models.IntegerField()
    created_at = models.DateTimeField()
    date_at = models.DateField()
    position = models.CharField(max_length=256, blank=True, null=True)
    position_base_id = models.IntegerField(blank=True, null=True)
    oklad = models.IntegerField()
    precent = models.IntegerField(blank=True, null=True)
    premium = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    payorders = models.IntegerField(blank=True, null=True)
    sumforprecent = models.IntegerField(blank=True, null=True)
    precent_num = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timetable'


class Tovarnomenclature(models.Model):
    document_id = models.CharField(max_length=256)
    date = models.CharField(max_length=256)
    yur_lico = models.CharField(max_length=256)
    cafe = models.CharField(max_length=256)
    supplier = models.CharField(max_length=256)
    number = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    amount = models.CharField(max_length=256)
    price = models.CharField(max_length=256)
    sum = models.CharField(max_length=256)
    comment = models.CharField(max_length=256)
    pay_sum = models.CharField(max_length=256)
    category = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'tovarNomenclature'


class TovarRequests(models.Model):
    date_at = models.DateField()
    storage_id = models.IntegerField()
    product_category = models.CharField(max_length=64)
    product_name = models.CharField(max_length=128)
    product_unit = models.CharField(max_length=32)
    product_amount = models.IntegerField()
    product_price = models.IntegerField()
    sum = models.IntegerField()
    supplier = models.CharField(max_length=128)
    employee = models.CharField(max_length=128)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tovar_requests'


class TransportationRequests(models.Model):
    date_at = models.CharField(max_length=64)
    status = models.IntegerField()
    writer = models.CharField(max_length=64)
    sender = models.CharField(max_length=128, blank=True, null=True)
    from_send = models.CharField(max_length=128, blank=True, null=True)
    where_take = models.CharField(max_length=128, blank=True, null=True)
    item = models.CharField(max_length=128, blank=True, null=True)
    photo_src = models.CharField(max_length=256, blank=True, null=True)
    photo_blob = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transportation_requests'


class TypeNames(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_names'


class Users(models.Model):
    date = models.CharField(max_length=32)
    username = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    promouter = models.CharField(max_length=128)
    party_day = models.CharField(max_length=32)
    wait = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'users'


class Writers(models.Model):
    username = models.CharField(max_length=128)
    chat_id = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'writers'
