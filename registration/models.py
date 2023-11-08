from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username