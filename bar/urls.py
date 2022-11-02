from bar import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.defaults import page_not_found, server_error

app_name = "Bar"

urlpatterns = [
    path('', views.bar, name="bar"),
    path('expenses', views.bar_expenses, name="bar_expenses"),
    path('expenses/save', views.bar_expenses_save, name="bar_expenses_save"),
    path('pays/save', views.bar_pays_save, name="bar_pays_save"),
    path('delete/<int:pk>', views.bar_employee_delete, name="bar_employee_delete"),
    path('salary', views.bar_salary, name="bar_salary"),
    path('salary/save', views.bar_salary_save, name="bar_salary_save"),
    path('invent', views.bar_invent, name="bar_invent"),
    path('end', views.bar_end, name="bar_end"),
    path('invent', views.bar_invent, name="bar_invent"),
    path('invent/form/<str:storageId>', views.bar_invent_form, name="bar_invent_form"),
    path('invent/table', views.bar_invent_table, name="bar_invent_table"),
    path('end/save', views.bar_end_save, name="bar_end_save"),
    path('auto_salary', views.bar_auto_salary, name="bar_auto_salary"),
    path('main_salary', views.bar_salary3, name="bar_salary3"),
    path('main_salary/save', views.bar_salary3_save, name="bar_salary3_save"),
    path('expenses/delete/<int:id>', views.bar_expenses_delete, name="bar_expenses_delete"),
    path('employee', views.bar_employee_salary_now, name="bar_employee_salary_now"),
    path('employee/previous', views.bar_employee_salary_previous, name="bar_employee_salary_previous"),
    path('calendar', views.bar_calendar, name="bar_calendar"),
    path('calendar/insert', views.bar_calendar_insert, name="bar_calendar_insert"),
    path('blacklist', views.bar_blacklist, name="bar_blacklist"),
    path('invent/second', views.bar_invent_second, name="bar_invent_second"),
    path('invent/second/form/<str:storageId>', views.bar_invent_form_second, name="bar_invent_form_second"),
    path('invent/second/table', views.bar_invent_table_second, name="bar_invent_table_second"),
    path('request/beer', views.bar_beer_request, name="bar_beer_request"),
    path('request/box', views.bar_box_request, name="bar_box_request"),
    path('request/products', views.bar_products_request, name="bar_products_request"),
    path('request/bar', views.bar_drinks_request, name="bar_drinks_request"),
    path('arrival/beer', views.bar_beer_arrival, name="bar_beer_arrival"),
    path('arrival/beer/delete', views.bar_beer_arrival_delete, name="bar_beer_arrival_delete"),
    path('arrival/drinks', views.bar_drinks_arrival, name="bar_drinks_arrival"),
    path('arrival/drinks/delete', views.bar_drinks_arrival_delete, name="bar_drinks_arrival_delete"),
    path('request/beer/delete', views.bar_beer_request_delete, name="bar_beer_request_delete"),
    path('request/hoz', views.bar_hoz_request, name="bar_hoz_request"),
]
