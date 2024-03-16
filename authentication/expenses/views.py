from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from .serializers import ExpenseSerializer
from .models import Expense
from .permessions import IsOwner


class ExpenseListApiView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    # for creating expense object
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    # for get expense list
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ExpenseDetailsApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = permissions.IsAuthenticated
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
