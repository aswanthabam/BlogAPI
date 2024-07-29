from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

class User(AbstractUser):
    id = models.CharField(max_length=48, default=uuid4, primary_key=True)
    email = models.EmailField(unique=True, null=False, blank=False)

    class Meta:
        db_table = 'user'

class Post(models.Model):
    post_id = models.CharField(primary_key=True,max_length=48, default=uuid4)
    user_id = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    slug = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now=True, null=False, blank=False)
    edited_on = models.DateTimeField(auto_now=False, null=True, blank=False)

    class Meta:
        db_table = 'post'

