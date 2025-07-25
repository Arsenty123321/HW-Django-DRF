from rest_framework.routers import DefaultRouter
from django.urls import include, path
from lms.apps import LmsConfig
from lms.views import CourseViewSet

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
