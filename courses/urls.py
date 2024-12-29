from django.urls import path
from rest_framework.routers import DefaultRouter

from courses.apps import CoursesConfig
from courses.views import (CourseViewSet, LessonCreateAPIView,
                           LessonDestroyAPIView, LessonListAPIView,
                           LessonRetrieveAPIView, LessonUpdateAPIView,
                           SubscriptionView)

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r"course", CourseViewSet, basename="course")

urlpatterns = [
    path("lesson_create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson_list/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path("lesson/<int:pk>/update", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path(
        "lesson/<int:pk>/delete", LessonDestroyAPIView.as_view(), name="lesson_delete"
    ),
    path("subscription/", SubscriptionView.as_view(), name="subscription"),
] + router.urls
