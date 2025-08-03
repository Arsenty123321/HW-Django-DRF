from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import validate_video_link


class LessonSerializer(serializers.ModelSerializer):
    link_to_the_video = serializers.URLField(validators=[validate_video_link])
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'
        extra_kwargs = {
            'owner': {'required': False}
        }


class CourseSerializer(serializers.ModelSerializer):
    course_lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(read_only=True, many=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_course_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = ('id', 'course_name', 'course_description', 'course_preview', 'course_lessons_count', 'lessons',
                  'owner', 'is_subscribed')
        extra_kwargs = {
            'owner': {'required': False}
        }


class CourseSubscriptionSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
