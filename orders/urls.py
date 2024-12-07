from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:flower_id>/', views.CreateOrderView.as_view(), name='create_order'),
    path('history/', views.UserOrderHistoryView.as_view(), name='order_history'),

    path('admin/manage/', views.AdminOrderManagementView.as_view(), name='manage_orders'),
    path('admin/update/<int:pk>/', views.AdminUpdateOrderStatusView.as_view(), name='update_order_status'),
]
