from django.contrib import admin

from lms.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_name')
    search_fields = ('course_name',)
    ordering = ("id",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson_name')
    search_fields = ('lesson_name',)
    ordering = ("id",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course')
    search_fields = ('user',)
    ordering = ("id",)
