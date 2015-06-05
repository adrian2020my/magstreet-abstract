from django.db import models
from auth_user.models import MyUser

# Create your models here.


class Category(models.Model):
    user = models.ManyToManyField(MyUser, related_name='user_ids')
    name = models.CharField(max_length=250)
    img = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
