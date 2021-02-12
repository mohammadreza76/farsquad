from squadBlog.models import Post,Comment,Category
from squadBlog.serializers import PostSerializer,CommentSerializer,CategorySerializer,PostDetailSerializer,CommentCreateSerializer
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes

# Create your views here.
#declare pagination for handling the number of categories show in page
class ResultsSetPaginationForCategories(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100000

#declare pagination for handling the number of instance post show in page
class ResultsSetPaginationForCategory(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 3000000

#show list of Categories
class ShowAllCategories(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,]
    queryset = Category.objects.all()    
    serializer_class = CategorySerializer
    pagination_class = ResultsSetPaginationForCategories


#show all posts about specific category
@api_view(['GET']) 
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def ShowPostsCategory(request,category):
    #List all code snippets, or create a new snippet
    paginator = ResultsSetPaginationForCategory()
    query_set  = Post.objects.filter(categories__name__contains = category)
    context = paginator.paginate_queryset(query_set, request)
    serializer = PostSerializer(context,many=True)
    return paginator.get_paginated_response(serializer.data)

#show each post
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'

   

#create comment
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def comment_create_view(request,slug):
    post_instance = get_object_or_404(Post,slug=slug)
    request.data['post'] = post_instance.pk
    serializer = CommentCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  
#show comments of each post
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def comment_list(request,slug):
    post = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(post=post)
    serializer = CommentSerializer(comments, many=True)  
    return Response(data=serializer.data, status=status.HTTP_200_OK)
