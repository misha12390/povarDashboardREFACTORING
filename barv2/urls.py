from django.urls import path
from bar import views
app_name = "Bar"

urlpatterns = [
    path('', views.index, name="index"),
    path('timetable/save', views.timetable_save, name="timetable_save"),
    path('employee/delete', views.timetable_delete, name="timetable_delete"),
    path('expenses', views.expenses, name="expenses"),
    path('expenses/save', views.expenses_save, name="expenses_save"),
    path('expenses/delete', views.expenses_delete, name="expenses_delete"),
    path('pays/save', views.pays_save, name="pays_save"),
    path('salary', views.salary, name="salary"),
    path('salary/save', views.salary_save, name="salary_save"),
    path('month_salary', views.month_salary, name="month_salary"),
    path('month_salary/save', views.month_salary_save, name="month_salary_save"),
    path('auto_salary', views.auto_salary, name="auto_salary"),
    path('end', views.end_day, name="end"),
    path('end/save', views.end_day_save, name="end_save"),
    path('inventory', views.inventory, name="inventory"),
    path('inventory/table', views.inventory_table, name="inventory_table"),
    path('inventory/form/<str:storageId>', views.inventory_form, name="inventory_form")
]
