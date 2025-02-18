from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet


router = DefaultRouter()
router.register(r'payment', PaymentViewSet, basename='payment')
# router.register(r'pay', PayViewSet, basename='pay')

urlpatterns = [
    path('', include(router.urls)),
    # path('', include(router.urls)),
    # path('pay/', PayViewSet.as_view(), name='pay'),
]