from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from project.models import Project
from project.serializers import ProjectSerializer
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class ResultsSetPaginationForProject(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 3000000


class ProjectList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()    
    serializer_class = ProjectSerializer
    pagination_class = ResultsSetPaginationForProject