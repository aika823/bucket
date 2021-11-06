from django.db import models
import datetime
import os
from django.db.models.base import Model
from django.utils.deconstruct import deconstructible

@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        now = datetime.datetime.now()
        date_time = now.strftime("%y%m%d_%H%M%S")
        filename = 'img_product_{}.{}'.format(str(date_time), str(ext))
        return os.path.join(self.path, filename)

class User(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=128)
    phone = models.CharField(max_length=11)
    image = models.ImageField(upload_to=PathAndRename("user/"),blank=True, null=True)
    social_login = models.CharField(max_length=10, null=True)
    social_id = models.CharField(max_length=200, null=True)
    class Meta:
        db_table = 'user'

class Interest(models.Model):
    interest = models.CharField(max_length=10, unique=True)
    class Meta:
        db_table = "interest"

class UserInterest(models.Model):
    user_id = models.ForeignKey(to=User, db_column='user_id', null=False, on_delete=models.CASCADE)
    interest_id = models.ForeignKey(to=Interest, db_column='interest_id', null=False, on_delete=models.CASCADE)
    class Meta:
        db_table = "user_interest"