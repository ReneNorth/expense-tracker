from django.urls import path

from . import views

app_name = 'expenses'
urlpatterns = [
    path('', views.expenses_list_view, name='list'),
]
