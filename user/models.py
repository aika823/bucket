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
        ext = filename.split(".")[-1]
        now = datetime.datetime.now()
        date_time = now.strftime("%y%m%d_%H%M%S")
        filename = "img_user_{}.{}".format(str(date_time), str(ext))
        return os.path.join(self.path, filename)


class User(models.Model):
    name = models.CharField(max_length=32, null=False)
    password = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=128, null=False)
    phone = models.CharField(max_length=11, null=True)
    image = models.ImageField(upload_to=("user/"), default="default_image.jpg")
    detail = models.CharField(max_length=500, null=True)
    social_login = models.CharField(max_length=10, null=True)
    social_id = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(null=False, default=False)
    is_admin = models.BooleanField(null=False, default=False)
    instagram = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "user"


class Interest(models.Model):
    interest = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = "interest"


class UserInterest(models.Model):
    user_id = models.ForeignKey(
        to=User, db_column="user_id", null=False, on_delete=models.CASCADE
    )
    interest_id = models.ForeignKey(
        to=Interest, db_column="interest_id", null=False, on_delete=models.CASCADE
    )

    class Meta:
        db_table = "user_interest"