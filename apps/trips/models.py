from __future__ import unicode_literals

from django.db import models
import bcrypt
import re
from datetime import date, datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
	def validName(self, name, username):
		if len(name) < 3:
			return(False, "name")
		if len(username) < 3:
			return(False, "username")
		if len(User.objects.filter(username=username)) > 0:
			return(False, "usedname")
		return True
	def validEmail(self, email):
		if len(email) < 1:
			return(False, "email")
		elif not re.match(EMAIL_REGEX, email):
			return(False, "email")
		return True
	def validPass(self, pass1, pass2):
		if len(pass1) < 8:
			return(False, "pass1")
		if pass2 == pass1:
			return True
		else:
			return(False, "pass2")
	def validate(self, name, username, email, pass1, pass2):
		nameResults = User.userManager.validName(name, username)
		emailResults = User.userManager.validEmail(email)
		passResults = User.userManager.validPass(pass1, pass2)
		if nameResults==True:
			pass
		else:
			return nameResults
		if emailResults==True:
			pass
		else:
			return emailResults
		if passResults==True:
			pass
		else:
			return passResults
		pass1 = pass1.encode(encoding="utf-8", errors="strict")
		hashed = bcrypt.hashpw(pass1, bcrypt.gensalt())
		currentUser = User.objects.create(name=name, username=username, email=email, password=hashed)
		return(True, currentUser)
	def login(self, username, pass1):
		if len(User.objects.filter(username=username)) == 0:
			return (False, "username")
		else:
			userInfo = User.objects.filter(username=username)
		if bcrypt.hashpw(pass1.encode(encoding="utf-8", errors="strict"), userInfo[0].password.encode(encoding="utf-8", errors="strict")) == userInfo[0].password.encode(encoding="utf-8", errors="strict"):
			return True
		else:
			return (False, "pass")


class TripManager(models.Manager):
	def validD(self, destination, description):
		if len(destination) < 1:
			return(False, "dest")
		if len(description) < 1:
			return(False, "desc")
		return True
	def validDate(self, date_from, date_to):
		print "Made it to validDate", date_from, date_to
		if date_from == "":
			return(False, "from")
		if date_to == "":
			return(False, "to")
		date_from = datetime.strptime(date_from,'%m/%d/%Y')
		date_to = datetime.strptime(date_to,'%m/%d/%Y')
		print date_from
		if datetime.today() < date_from:
			print date.today(), date_from
		else:
			print "date_from is before today"
			return(False, "from")
		if date_to > date_from:
			print "date_to is after date_from"
		else:
			print "date_to is BEFORE date_from"
			return(False, "to")
		return True
	def validTrip(self, destination, description, date_from, date_to, id):
		planned_by = User.objects.get(id=id)
		dResults = Trip.tripManager.validD(destination, description)
		dateResults = Trip.tripManager.validDate(date_from, date_to)
		if dResults == True:
			print "dest and desc are valid"
		else:
			print "dest or desc are not valid"
			return dResults
		if dateResults == True:
			print "dates are good"
		else:
			print "dates bad, very bad"
			return dateResults
		date_from = datetime.strptime(date_from,'%m/%d/%Y')
		date_to = datetime.strptime(date_to,'%m/%d/%Y')
		lastTrip = Trip.objects.create(destination=destination, description=description, date_from=date_from, date_to=date_to, planned_by=planned_by)
		print lastTrip, lastTrip.destination, lastTrip.description, lastTrip.date_from, lastTrip.planned_by
		return True
	def join(self, trip, id):
		joined_by = User.objects.get(id=id)
		trip = Trip.objects.get(id=trip)
		trip.joined_by = joined_by
		trip.save()
		return True


# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=200)
	username = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	userManager = UserManager()
	objects = models.Manager()

class Trip(models.Model):
	destination = models.CharField(max_length=200)
	description = models.TextField(max_length=500)
	date_from = models.DateField()
	date_to = models.DateField()
	planned_by = models.ForeignKey(User)
	joined_by = models.ForeignKey(User, related_name='User2', default=0, on_delete=models.DO_NOTHING)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	tripManager = TripManager()
	objects = models.Manager()