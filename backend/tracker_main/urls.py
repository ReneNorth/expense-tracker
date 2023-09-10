from django.conf import settings
from django.contrib import admin
from django.urls import path
from tracker_main import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
