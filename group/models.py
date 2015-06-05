from django.db import models
from categories.models import Category
from auth_user.models import MyUser

# Create your models here.


class Group(models.Model):
    user = models.ManyToManyField(MyUser, related_name='user_d')
    category = models.ForeignKey(Category, null=True)
    img = models.CharField(max_length=250, default=' ')
    name = models.CharField(max_length=250)
    description = models.TextField(default=' ')
    type = models.IntegerField(verbose_name='Group Access Type')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)