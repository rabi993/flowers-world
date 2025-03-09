
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from . views import UserViewSet
router = DefaultRouter()
router.register('users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('contact_us/', include('contact_us.urls')),
    path('services/', include('services.urls')),
    path('buyers/', include('buyers.urls')),
    path('flowers/', include('flowers.urls')),
    path('orders/', include('orders.urls')),
    path('categories/', include('categories.urls')),
    path('colors/', include('colors.urls')),
    path('payment/', include('payment.urls')),
    path('newsletter/', include('newsletter.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)