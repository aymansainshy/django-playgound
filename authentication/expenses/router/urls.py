from django.urls import path
from expenses.controllers.expenses_controller import ExpenseListController, ExpenseDetailsController

urlpatterns = [
    path('', ExpenseListController.as_view(), name='expenses'),
    path('<int:id>', ExpenseDetailsController.as_view(), name='expense')
]
