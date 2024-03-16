from django.urls import path
from . import views

urlpatterns = [
    path('', views.IncomeListApiView.as_view(), name='incomes'),
    path('<int:id>', views.IncomeDetailsApiView.as_view(), name='income')
]
