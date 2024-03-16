from rest_framework import serializers

from expenses.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('id', 'date', 'description', 'amount', 'category')

        extra_kwargs = {
            'id': {"read_only": True},
        }

    # def create(self, validated_data):
    #     pass
    #
    # def update(self, validated_data):
    #     pass
    #
    # def save(self, validated_data):
    #     pass
    #
    # def validate(self, validated_data):
    #     pass
