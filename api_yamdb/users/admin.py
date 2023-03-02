"""Admin integration of Users."""
from django.contrib import admin

from .models import User

admin.site.register(User)
