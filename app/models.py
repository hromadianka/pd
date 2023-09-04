from django.db import models
import uuid
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Publication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    heading = models.TextField(default='', blank=True)
    text = models.TextField(default='', blank=True)
    image = models.ImageField(upload_to='media/', height_field=None, width_field=None, blank=True, null=True)

    def __str__(self):
        return str(self.heading)

