from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	""" View for the index landing page of the site """
	context = {
		'title': 'Sigma Pi - Secure',
		'secure_index': True,
		'calendar_url': get_url(request)
	}
	return render(request,'secure_home.html',context)

def get_url(request):
	groups = request.user.groups

	url = None
	if (len(groups.filter(name="Philanthropy Chair")) > 0):
		url = "https://teamup.com/ksa354443e2fdb07ef?view=d&sidepanel=c"
	elif (len(groups.filter(name="Social Chair")) > 0):
		url = "https://teamup.com/ks8866f0514e5d6a2f?view=d&sidepanel=c"

	return url;
