from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import validate_video_link


class LessonSerializer(serializers.ModelSerializer):
    link_to_the_video = serializers.URLField(validators=[validate_video_link])

    class Meta:
        model = Lesson
        fields = '__all__'
        extra_kwargs = {
            'owner': {'required': False}
        }


class CourseSerializer(serializers.ModelSerializer):
    course_lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(read_only=True, many=True)

    def get_course_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ('id', 'course_name', 'course_description', 'course_preview', 'course_lessons_count', 'lessons',
                  'owner',)
        extra_kwargs = {
            'owner': {'required': False}
        }
