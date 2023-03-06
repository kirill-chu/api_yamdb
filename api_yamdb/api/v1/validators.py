"""Validators for API app."""
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

regexp_validator = RegexValidator(
    r'^[\w.@+-]+\Z',
    message='not valid regexp'
)


def validate_year(value):
    if value > datetime.now().year:
        raise ValidationError('Check year')
