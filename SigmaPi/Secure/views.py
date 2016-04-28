from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from Secure.models import CalendarKey

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
    groups = request.user.groups.all()

    for group in groups:
        if len(CalendarKey.objects.filter(group=group)) > 0:
            cal_key = CalendarKey.objects.get(group=group)
            return "https://teamup.com/%s?view=d&sidepanel=c" % cal_key.key

    return False
