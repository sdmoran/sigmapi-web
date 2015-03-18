from django.shortcuts import render

def index(request):
	"""
		View for the static index page
	"""
	return render(request, 'home.html', None)
	
def history(request):
	"""view for the static chapter history page"""
	return render(request, 'history.html', None)

def service(request):
	"""view for the static chapter service page"""
	return render(request, 'service.html', None)

def donate(request):
	"""view for the static donate page"""
	return render(request, 'donate.html', None)

def permission_denied(request):
	""" View for 403 (Permission Denied) error """
	return render(request, '403.html', None)