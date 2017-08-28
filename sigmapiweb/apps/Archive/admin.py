from common.utils import register_model_admin
from .models import Guide, HouseRules, Bylaws

# I'm commenting this stuff out because it doesn't do anything necessary,
# and is mildly confusing. Will remove later if nothing breaks.
# class GuideAdmin(admin.ModelAdmin):
    # prepopulated_fields = {"path": ("name",)}
# admin.site.register(Guide, GuideAdmin)

# Register models to appear in the Django Admin DB Site
register_model_admin(Guide)
register_model_admin(HouseRules)
register_model_admin(Bylaws)
