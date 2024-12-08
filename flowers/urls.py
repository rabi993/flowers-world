from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()

router.register('list', views.FlowerViewset) 
router.register('reviews', views.ReviewViewset) 
# # router.register('reviews/filter', views.ReviewFlowerIdViewset)
# router.register('reviews/filter', views.ReviewFlowerIdViewset, basename='review_filter')

urlpatterns = [
    path('', include(router.urls)),
]