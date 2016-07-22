from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=200)
	username = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Trip(models.Model):
	destination = models.CharField(max_length=200)
	description = models.TextField(max_length=500)
	date_from = models.DateTimeField()
	date_to = models.DateTimeField()
	planned_by = models.ForeignKey(User)
	joined_by = models.ForeignKey(User, related_name='User2')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)