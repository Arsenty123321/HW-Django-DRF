from rest_framework import serializers
from users.models import User, Payments


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class PaymentsSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if not data.get('course') and not data.get('lesson'):
            raise serializers.ValidationError("Необходимо указать курс (course:) или урок (lesson:).")
        return data

    class Meta:
        model = Payments
        fields = ('user', 'course', 'lesson', 'amount', 'method', 'payment_session_id', 'payment_link')
        extra_kwargs = {
            'user': {'required': False}
        }
