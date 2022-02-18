from rest_framework import serializers
from User.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("name","email","phone_number","address",)