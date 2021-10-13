from project import views
from django.urls import path
try:
    urlpatterns = [
        path('projects_detail/',views.ProjectList.as_view(),name='projects-list'),
    ]
except:
    urlpatterns=[] 
