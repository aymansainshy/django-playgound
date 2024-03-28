from django.shortcuts import render
from rest_framework.views import APIView
from expenses.models.expense_model import Expense
from income.models import Income
from rest_framework import status, response
import datetime


class ExpensesSummaryStats(APIView):

    def get(self, request):
        todays_date = datetime.datetime.now()
        ayear_ago = todays_date - datetime.timedelta(days=30 * 12)
        expenses = Expense.objects.filter(owner=request.user,
                                          date__gte=ayear_ago,
                                          date__lte=todays_date)

        result = {}
        categories = list(set(map(self.get_category, expenses)))

        for expense in expenses:
            for category in categories:
                result[category] = self.get_amount_for_category(expenses, category)

        return response.Response(
            data={'category_data': result},
            status=status.HTTP_200_OK
        )

    def get_category(self, expense):
        return expense.category

    def get_amount_for_category(self, expenses_list, category):
        expenses = expenses_list.filter(category=category)

        amount = 0
        for expense in expenses:
            amount += expense.amount
        return {'amount': str(amount)}


class IncomeSourcesSummaryStats(APIView):

    def get(self, request):
        todays_date = datetime.datetime.now()
        ayear_ago = todays_date - datetime.timedelta(days=30 * 12)
        incomes = Income.objects.filter(owner=request.user,
                                        date__gte=ayear_ago,
                                        date__lte=todays_date)

        result = {}
        sources = list(set(map(self.get_source, incomes)))

        for i in incomes:
            for source in sources:
                result[source] = self.get_amount_for_source(incomes, source)

        return response.Response(
            data={'income_source_data': result},
            status=status.HTTP_200_OK
        )

    def get_source(self, income):
        return income.source

    def get_amount_for_source(self, incomes_list, source):
        incomes = incomes_list.filter(source=source)

        amount = 0
        for income in incomes:
            amount += income.amount
        return {'amount': str(amount)}
