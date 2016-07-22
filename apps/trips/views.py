from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse

import re

# Create your views here.
def index(request):
	return render(request, 'trips/index.html')