from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'trips_index'),
	url(r'^register$', views.register, name = 'trips_register'),
	url(r'^login$', views.login, name = 'trips_login'),
	url(r'^logout$', views.logout, name = 'trips_logout'),
	url(r'^trips$', views.trips, name = 'trips_trips'),
	url(r'^trips/join/(?P<id>\d+)$', views.join, name = 'trips_join'),
	url(r'^trips/destination/(?P<id>\d+)$', views.destination, name = 'trips_destination'),
	url(r'^trips/add$', views.add, name = 'trips_add'),
	url(r'^trips/addTrip/(?P<id>\d+)$', views.addTrip, name = 'trips_addTrip')
]