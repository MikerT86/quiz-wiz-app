from django.contrib import admin
from .models import ExtendedUser, Quiz
from django.contrib.auth.models import User

admin.site.unregister(User)  # Unregister the default User model
admin.site.register(ExtendedUser)
admin.site.register(Quiz)
