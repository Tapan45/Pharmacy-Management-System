
from django.contrib import admin
from django.urls import path
from Exam import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #Home Website
    path('',views.home),
  #inventory
path('add_inventory',views.add_inventory,name="add_inventory"),
  path('view-inventory/',views.view_inventory, name='view_inventory'),
path('add_supplier',views.add_supplier,name="add_supplier"),
  path('get_supplier_details/',views.get_supplier_details, name='get_supplier_details'),

  path('view_suppliers/',views.view_suppliers, name='view_suppliers'),
    path('delete-supplier/<int:supplier_id>/',views.delete_supplier, name='delete_supplier'),
path('add_client',views.add_client,name="add_client"),
path('add_purchase',views.add_purchase,name="add_purchase"),
path('dashboard',views.dashboard,name="dashboard"),

path('order_invoice',views.order_invoice, name='order_invoice'),


  path('order_request',views.order_request, name='order_request'),

 path('get_user_details/',views.get_user_details, name='get_user_details'),
  
     path('search_medicine/', views.search_medicine, name='search_medicine'),
 #pharmassist
   path('inventory_dashboard',views.inventory_dashboard,name="inventory_dashboard"),
  path('pharmassist_dashboard',views.pharmassist_dashboard,name="pharmassist_dashboard"),
  path('add_medicine',views.add_medicine,name="add_medicine"),
    path('view_medicine',views.view_medicine,name="view_medicine"),
     path('delete_medicine/<int:medicine_id>/',views.delete_medicine,name='delete_medicine'),
    
path('create_sales',views.create_sales,name="create_sales"),
path('prescription_list',views.view_prescription,name="view_prescription"),
path('delete_prescription/<int:prescription_id>/',views.delete_prescription, name='delete_prescription'),
path('create_holidays',views.create_holidays,name="create_holidays"),

 
   path('change_password',views.change_password,name="change_password"),
    path('create_holidays',views.create_holiday,name="create_holidays"),
     path('salary_slip',views.salary_slip,name='salary_slip'),
     path('get_user_details/',views.get_user_details, name='get_user_details'),
    


     
#Customer
 path('customer_dashboard',views.customer_dashboard,name="customer_dashboard"),
path('customer_create',views.customer_create,name="customer_create"),
 path('customer_login',views.customer_login,name="customer_login"),
path('add_prescription',views.add_prescription,name="add_prescription"),
path('order_status',views.my_order,name="order_status"),
path('notifications',views.notifications,name="notifications"),
path('medicine/<int:medicine_id>/',views.medicine_detail, name='medicine_detail'),
path('cart_view',views.cart_view, name='cart_view'),
 path('cart/count/',views.get_cart_count, name='cart_count_endpoint'),
path('add_to_cart/<int:medicine_id>/',views.add_to_cart, name='add_to_cart'),

 path('make-payment/',views.make_payment, name='make_payment'),
  

path('view_coupon',views.view_coupon,name="view_coupon"),
 
 
path('change/password',views.password_change, name='change_password'),
path('profile_view',views.profile_view, name='profile_view'),
path('update_quantity/',views.update_quantity, name='update_quantity'),
path('delete_cart_item/',views.delete_cart_item, name='delete_cart_item'),
path('lab_test/',views.lab_test, name='lab_test'),
  path('address/',views.add_address, name='address'),
  
     path('captcha',views.captcha, name='captcha'),
       path('order_placed',views.order_placed, name='orderplaced'),
         path('save_payment/',views.save_payment, name='save_payment'),
         path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
         
      path('select-address/', views.select_address, name='select_address'),   
 #Admin
 
  path('admin_dashboard',views.admin_dashboard,name="admin_dashboard"),
  path('add_salary',views.add_salary,name="add_salary"),
 
 
 
   path('view_coupon/',views.view_coupon, name='view_coupon'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)