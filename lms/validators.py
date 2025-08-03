import re
from rest_framework.serializers import ValidationError


def validate_video_link(value):
    """Проверка URL на youtube.com."""

    link_patterns = r'^(https?:\/\/)?(www\.)?youtube\.com\/[^\s,]*$'

    if not re.fullmatch(link_patterns, value):
        raise ValidationError('Допустимы ссылки только на YouTube - youtube.com.')
