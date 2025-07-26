from rest_framework import serializers

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    course_lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(read_only=True, many=True)

    def get_course_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'
