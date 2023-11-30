from django.urls import include, path
from rest_framework import routers

from .views import ExpensesViewSet, CategoryViewSet

router1 = routers.SimpleRouter()
router1.register('expenses', ExpensesViewSet, basename='expenses')
router1.register('categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('v1/', include(router1.urls)),
]
