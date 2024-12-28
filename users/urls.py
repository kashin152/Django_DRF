from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    CustomsUserViewSet,
    PaymentViewSet,
    UserCreateAPIView,
    UserProfileViewSet,
)

app_name = UsersConfig.name


router = DefaultRouter()
router.register(r"profile", UserProfileViewSet, basename="user-profile")
router.register(r"payments", PaymentViewSet, basename="payments")
router.register(r"users", CustomsUserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
