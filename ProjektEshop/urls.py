from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static

admin.site.site_header = "Knihkupectví Kavka"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ecom.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
