from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer, LessonSerializer, CourseSubscriptionSerializer
from users.permissions import IsOwner, IsNotModerator, IsOwnerOrModerator, MODERATOR_GROUP_NAME


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name=MODERATOR_GROUP_NAME).exists():
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=user)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action == ['update', 'retrieve', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        elif self.action == ['destroy']:
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            # list
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name=MODERATOR_GROUP_NAME).exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner, IsNotModerator]


class CourseSubscriptionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CourseSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        course_id = serializer.validated_data['course_id']
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            # Если подписка у пользователя на этот курс есть - удаляем ее
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            # Если подписки у пользователя на этот курс нет - создаем ее
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        return Response({"message": message})
