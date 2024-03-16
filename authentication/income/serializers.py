from rest_framework import serializers

from .models import Income


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ('id', 'date', 'description', 'amount', 'source')

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
