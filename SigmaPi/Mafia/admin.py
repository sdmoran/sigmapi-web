from django.contrib import admin
from .models import *

admin.site.register(MafiaGame)
admin.site.register(MafiaPlayer)
admin.site.register(MafiaAction)
admin.site.register(MafiaNightResult)

