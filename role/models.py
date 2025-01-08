# In myapp/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Permission

class UserPermission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.permission.name}"
