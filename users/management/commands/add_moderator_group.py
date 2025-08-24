from django.core.management import BaseCommand
from django.contrib.auth.models import Group

from dotenv import load_dotenv

load_dotenv(override=True)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        group_name = 'Moderators'

        # Создаем группу
        moderator_group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" была успешно создана.'))
        else:
            self.stdout.write(self.style.WARNING(f'Группа "{group_name}" уже существует.'))
