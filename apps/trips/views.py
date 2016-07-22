from django.shortcuts import render, redirect
from .models import User, Trip
from django.contrib import messages
from django.core.urlresolvers import reverse

import re

# Create your views here.
def index(request):
	return render(request, 'trips/index.html')

def register(request):
	valid = User.userManager.validate(request.POST['name'], request.POST['username'], request.POST['email'], request.POST['pass1'], request.POST['pass2'])
	if valid[0]==True:
		request.session['currUseruserName'] = valid[1].username
		request.session['currUserID'] = valid[1].id
		return redirect(reverse('trips_trips'))
	else:
		if valid[1] == "name":
			messages.info(request, "Name must be at least 3 characters")
		elif valid[1] == "username":
			messages.info(request, "Username must be at least 3 character")
		elif valid[1] == "usedname":
			messages.info(request, "Sorry, that Username has already been taken")
		elif valid[1] == "email":
			messages.info(request, "Please enter a valid email")
		elif valid[1] == "pass1":
			messages.info(request, "Password must be at least 8 characters")
		elif valid[1] == "pass2":
			messages.info(request, "Passwords do not match")
		return redirect('/')

def login(request):
	if User.userManager.login(request.POST['username'], request.POST['pass1']) == True:
		user = User.objects.filter(username=request.POST['username'])
		request.session['currUseruserName'] = user[0].username
		request.session['currUserID'] = user[0].id
		return redirect(reverse('trips_trips'))
	else:
		messages.warning(request, 'Username and Password do not match')
		return redirect(reverse('trips_index'))

def logout(request):
	del request.session['currUseruserName']
	del request.session['currUserID']
	return redirect(reverse('trips_index'))

def trips(request):
	context = {
		"trips": Trip.objects.all().order_by("date_from"),
		"userTrips": Trip.objects.filter(planned_by=request.session['currUserID']),
		"tripsJoined": Trip.objects.filter(joined_by=request.session['currUserID'])
	}
	return render(request, 'trips/trips.html', context)

def join(request, id):
	trip = request.POST['join']
	join = Trip.tripManager.join(trip, id)
	if join == True:
		return redirect(reverse('trips_trips'))
	return redirect(reverse('trips_trips'))

def leave(request, id):
	trip = request.POST['trip']
	leave = Trip.tripManager.leave(trip, id)
	if leave == True:
		return redirect(reverse('trips_trips'))
	return redirect(reverse('trips_trips'))

def destination(request, id):
	context = {
		"trips": Trip.objects.filter(id=id)
	}
	return render(request, 'trips/destination.html', context)

def add(request):
	return render(request, 'trips/add.html')

def addTrip(request, id):
	destination = request.POST['destination']
	description = request.POST['description']
	date_from = request.POST['date_from']
	date_to = request.POST['date_to']

	valid = Trip.tripManager.validTrip(destination
	, description, date_from, date_to, id)

	if valid == True:
		return redirect(reverse('trips_trips'))
	else:
		if valid[1] == "dest":
			messages.info(request, "Destination is required")
		elif valid[1] == "desc":
			messages.info(request, "Description is required")
		elif valid[1] == "from":
			messages.info(request, "The trip must start after today's date")
		elif valid[1] == "to":
			messages.info(request, "The trip must end after the trip has started")
		return redirect(reverse('trips_add'))



