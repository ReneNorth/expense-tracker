from django.urls import include, path
from rest_framework import routers
from .views import ExpensesViewSet

router1 = routers.SimpleRouter()
router1.register('expenses', ExpensesViewSet, basename='expenses')

urlpatterns = [
    path('v1/', include(router1.urls)),
]
