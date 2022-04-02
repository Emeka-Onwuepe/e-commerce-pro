from rest_framework import serializers

from Sales.models import Sales

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = "__all__"