from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from tracker_main import views

urlpatterns = [
    # path('', views.home_view, name='home'),
    path('', include('expenses.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
