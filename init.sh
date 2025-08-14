#!/bin/bash

# Миграции при первом запуске
if [ ! -f .migrated ]; then
  python ./manage.py migrate
  touch .migrated
fi

# Создать суперпользователя при первом запуске
if [ ! -f .superuser_created ]; then
  echo "Creating superuser..."
  python ./manage.py csu
  touch .superuser_created
fi

# Создать группы 'Moderators' через кастомную команду
if [ ! -f .moderator_group_created ]; then
  echo "Creating moderator_group..."
  python ./manage.py add_moderator_group
  touch .moderator_group_created
fi

# Запуск основного приложения
exec "$@"