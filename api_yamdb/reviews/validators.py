from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(year):
    if not 0 <= year <= timezone.now().year:
        raise ValidationError(
            f'Проверьте, правильно ли указан {year}!'
        )
    return year
