from django.db import models


class Course(models.Model):
    course_name = models.CharField(max_length=150, verbose_name='Название курса', help_text='Укажите название курса',
                                   blank=False)
    course_description = models.TextField(verbose_name='Описание курса', help_text='Укажите описание курса',
                                          blank=False)
    course_preview = models.ImageField(upload_to='course_previews/', verbose_name='Превью',
                                       help_text='Загрузите превью', blank=True)

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['course_name']


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=150, verbose_name='Название урока', help_text='Укажите название урока',
                                   blank=False)
    lesson_description = models.TextField(verbose_name='Описание урока', help_text='Укажите описание урока',
                                          blank=False)
    lesson_preview = models.ImageField(upload_to='lesson_previews/', verbose_name='Превью',
                                       help_text='Загрузите превью', blank=True)
    link_to_the_video = models.URLField(verbose_name='Ссылка на видео', help_text='Укажите ссылку на видео',
                                        blank=False)
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return self.lesson_name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['lesson_name']
