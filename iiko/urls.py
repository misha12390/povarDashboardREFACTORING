from iiko import views
from django.urls import path


app_name = "IIKO"

urlpatterns = [
    path('', views.iiko, name="iiko"),
    path('suppliers', views.suppliers, name="suppliers"),
    path('suppliers/edit', views.supplier_edit, name="supplier_edit"),
    path('nomenclature', views.nomenclature, name="nomenclature"),
    path('categories', views.categories, name="categories"),
    path('sales_by_types', views.sales_by_types, name="sales_by_types"),
    path('sales', views.sales, name="sales"),
    path('arrivals', views.arrivals, name="arrivals"),
    path('inventory', views.inventory, name="inventory"),
    path('nomenclature/edit', views.nomenclature_edit, name="nomenclature_edit"),
    path('inventory/send', views.inventory_send, name="inventory_send")
]
