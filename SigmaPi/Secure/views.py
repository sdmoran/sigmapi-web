from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	""" View for the index landing page of the site """
	context = RequestContext(request,{
		'title': 'Sigma Pi - Secure',
		'secure_index': True
	})
	return render(request,'secure_home.html',context)
