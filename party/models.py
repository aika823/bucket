from django.db import models
import datetime
import os
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.utils.deconstruct import deconstructible

import user

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

class Party(models.Model):
    name = models.CharField(max_length=32)
    host = models.ForeignKey(to='user.User',db_column='host', on_delete=CASCADE)
    date = models.DateField()
    time = models.TimeField(default=None)
    address = models.CharField(max_length=200)
    headcount = models.IntegerField()
    price = models.IntegerField()
    detail = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    class Meta:
        db_table = 'party'

class UserParty(models.Model):
    user_id = models.ForeignKey(to='user.User', db_column='user_id', null=True, on_delete=CASCADE)
    party_id = models.ForeignKey(to=Party, db_column='party_id', null=True, on_delete=CASCADE)
    is_host = models.BooleanField(default=False)
    is_join = models.BooleanField(default=False)
    is_like = models.BooleanField(default=False)
    class Meta:
        db_table = 'user_party'

class Comment(models.Model):
    content = models.CharField(max_length=100, db_column='content', null=False)
    user = models.ForeignKey(to='user.User', db_column='user', null=True, on_delete=CASCADE)
    class Meta:
        db_table = 'comment'
    
class PartyComment(models.Model):
    party_id = models.ForeignKey(to=Party, db_column='party_id', null=True, on_delete=CASCADE)
    comment_id = models.ForeignKey(to=Comment, db_column='comment_id', null=True, on_delete=CASCADE)
    class Meta:
        db_table = 'party_comment'


