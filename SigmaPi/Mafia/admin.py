from django.contrib import admin
from .models import *

admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Action)
admin.site.register(NightResult)
admin.site.register(Vote)
admin.site.register(DayResult)

