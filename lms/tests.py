from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from lms.models import Course, Subscription, Lesson
from users.models import User
from users.permissions import MODERATOR_GROUP_NAME


class SubscriptionsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='tester@megatest.mega', password='megatest')
        self.course = Course.objects.create(course_name='Test Course', course_description='Test Course description',
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe_success(self):
        """Тест - подписаться на курс."""
        url = reverse('lms:subscription-switch')
        data = {'course_id': self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_success(self):
        """Тест - отписаться от курса."""
        url = reverse('lms:subscription-switch')
        data = {'course_id': self.course.pk}
        # Подписываемся на курс
        self.client.post(url, data)
        # Отписываемся от курса
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_is_unsubscribe_field(self):
        """Проверка поля is_subscribed в выводе информации курсе."""
        url = reverse('lms:course-detail', kwargs={'pk': self.course.pk})

        # Проверяем без подписки
        response = self.client.get(url, format='json')
        self.assertFalse(response.data.get('is_subscribed'))

        # Добавляем подписку
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.get(url, format='json')
        self.assertTrue(response.data.get('is_subscribed'))


class LessonCRUDTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='user@megatest.mega', password='megatest')
        self.moderator = User.objects.create(email='moderator@megatest.mega', password='e2e4ed')

        moderator_group = Group.objects.create(name=MODERATOR_GROUP_NAME)
        self.moderator.groups.add(moderator_group)

        self.course = Course.objects.create(course_name='Test Course', course_description='Test Course description',
                                            owner=self.user)
        self.lesson = Lesson.objects.create(
            lesson_name='Test Lesson',
            lesson_description='Test Lesson',
            link_to_the_video='https://youtube.com/watch?v=123',
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson_owner(self):
        """Создание урока владельцем курса."""
        url = reverse('lms:lesson-create')

        data = {
            'lesson_name': 'Test Lesson 2',
            'lesson_description': 'Test Lesson 2',
            'link_to_the_video': 'https://youtube.com/watch?v=test',
            'course': self.course.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_update_lesson_owner(self):
        """Обновление урока владельцем."""
        url = reverse('lms:lesson-update', kwargs={'pk': self.lesson.pk})

        data = {'lesson_name': 'New Lesson name'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.lesson_name, 'New Lesson name')

    def test_delete_lesson_owner(self):
        """Удаление урока владельцем."""
        url = reverse('lms:lesson-destroy', kwargs={'pk': self.lesson.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_delete_lesson_not_owner(self):
        """Удаление чужого урока невозможно."""
        # Создаем пользователя user2
        self.user2 = User.objects.create(email='user2@megatest.mega', password='megatest2')
        self.client.force_authenticate(user=self.user2)

        url = reverse('lms:lesson-destroy', kwargs={'pk': self.lesson.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_list_lessons_for_owner(self):
        """Владелец видит только свои уроки."""
        # Создаем пользователя user2 и урок от его имени
        self.user2 = User.objects.create(email='user2@megatest.mega', password='megatest2')
        self.lesson = Lesson.objects.create(
            lesson_name='Test Lesson',
            lesson_description='Test Lesson',
            link_to_the_video='https://youtube.com/watch?v=123',
            course=self.course,
            owner=self.user2,
        )

        self.client.force_authenticate(user=self.user)
        url = reverse('lms:lesson-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_by_moderator_forbidden(self):
        """Модератор не может создать урок."""
        self.client.force_authenticate(user=self.moderator)
        url = reverse('lms:lesson-create')

        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lesson_moderator_forbidden(self):
        """Модератор не может удалить урок."""
        self.client.force_authenticate(user=self.moderator)
        url = reverse('lms:lesson-destroy', kwargs={'pk': self.lesson.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)
