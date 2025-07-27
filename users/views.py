from rest_framework import generics
from rest_framework.filters import OrderingFilter

from rest_framework.generics import CreateAPIView

from users.models import User, Payments
from users.serializers import UserSerializer, PaymentsSerializer
from django_filters.rest_framework import DjangoFilterBackend


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class PaymentsListAPIView(generics.ListAPIView, CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ('payment_date',)
    filterset_fields = ('course', 'lesson', 'method')
