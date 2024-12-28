from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from courses.models import Course
from users.models import CustomsUser, Payment
from users.serializers import (
    CustomsUserDetailSerializer,
    PaymentSerializer,
    UserSerializer,
)
from users.services import (
    creating_price_stripe,
    creating_product_stripe,
    creating_session_stripe,
)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = CustomsUser.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomsUser.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        serializer.save()


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("payment_method", "paid_course", "paid_lesson")
    ordering_fields = ("payment_date",)

    def perform_create(self, serializer):
        amount = self.request.data.get("payment_amount")
        course_id = self.request.data.get("course_id")

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND
            )

        payment = serializer.save(user=self.request.user, payment_amount=amount)

        # Создание продукта в Stripe
        product = creating_product_stripe(course)

        # Создание цены в Stripe
        price = creating_price_stripe(payment.payment_amount, product.id)

        # Создание сессии в Stripe
        session_id, session_url = creating_session_stripe(price.id)

        if session_url is None:
            return Response(
                {"error": "Failed to create payment session"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Обновление платежа с информацией о методе оплаты и курсе
        payment.payment_method = "Stripe"
        payment.paid_course = course
        payment.save()

        return Response(
            {
                "session_id": session_id,
                "payment_id": payment.id,
                "url": session_url,  # Убедитесь, что это поле присутствует
            },
            status=status.HTTP_201_CREATED,
        )


class CustomsUserViewSet(viewsets.ModelViewSet):
    queryset = CustomsUser.objects.all()
    serializer_class = CustomsUserDetailSerializer
