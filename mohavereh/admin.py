from django.contrib import admin
from mohavereh.models import InformalText,FormalText

# Register your models here.
class InformalTextAdmin(admin.ModelAdmin):
    pass 


class FormalTextAdmin(admin.ModelAdmin):
    pass 

admin.site.register(FormalText, FormalTextAdmin)
admin.site.register(InformalText, InformalTextAdmin)