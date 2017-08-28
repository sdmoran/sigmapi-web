from django.contrib import admin
from common.utils import register_model_admin
from .models import Party, Guest, PartyGuest, BlacklistedGuest

# Admin site for parties
class PartyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"path": ("name",)}

# Register your models here.
register_model_admin(Party)
register_model_admin(Guest)
register_model_admin(PartyGuest)
register_model_admin(BlacklistedGuest)
