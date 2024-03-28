from .views import ExpensesSummaryStats, IncomeSourcesSummaryStats
from django.urls import path

urlpatterns = [
    path('expenses-category-data', ExpensesSummaryStats.as_view(), name='expenses-category-summary'),
    path('incomes-source-data', IncomeSourcesSummaryStats.as_view(), name='incomes-source-data')
]
