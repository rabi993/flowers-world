from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter() 

router.register('', views.ServiceViewset) 
urlpatterns = [
    path('', include(router.urls)),
]

# from django.urls import path
# from .views import ServiceList

# urlpatterns = [
#     path('services/', ServiceList.as_view(), name='service-list'),
# ]

