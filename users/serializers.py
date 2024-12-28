from rest_framework import serializers

from .models import CustomsUser, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomsUser
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class CustomsUserDetailSerializer(serializers.ModelSerializer):
    payment_history = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = CustomsUser
        fields = ["id", "email", "phone_number", "avatar", "country", "payment_history"]
