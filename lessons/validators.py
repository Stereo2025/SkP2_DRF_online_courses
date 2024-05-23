import re
from typing import Any, Dict
from rest_framework.serializers import ValidationError


class VideoUrlValidator:
    def __init__(self, field: str):
        """
        Инициализирует валидатор именем поля для проверки в словаре.
        Поле :param: Ключ, который будет проверяться во входящем словаре.
        """
        self.field = field

    def __call__(self, value: Dict[str, Any]) -> None:
        """
        Проверяет, что указанное поле в словаре «значение» является действительным URL-адресом YouTube.

        Значение :param: Словарь, в котором URL-адрес видео должен находиться под `self.field`.
        :raises ValidationError: Если URL-адрес недействителен или отсутствует.
        """
        reg = re.compile(r'^https://(www\.)?youtube\.com/watch\?v=[\w-]+|youtu.be/[\w-]+$')
        field_value = value.get(self.field)

        if field_value is None:
            raise ValidationError(f'Поле {self.field} не найдено в данных.')

        if not reg.match(field_value):
            raise ValidationError('Ссылка на урок может быть только с YouTube.')
