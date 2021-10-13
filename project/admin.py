from django.contrib import admin
from project.models import Project
# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    pass 

admin.site.register(Project, ProjectAdmin)