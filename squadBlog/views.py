import requests,random,datetime
from squadBlog.models import Post,Comment,Category
from squadBlog.serializers import PostSerializer,CommentSerializer,CategorySerializer,PostDetailSerializer,CommentCreateSerializer,PostAndQuestionAnswerSerializer
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,AllowAny
from collections import namedtuple
 
#phase 3.3 for automatic progress
#change all stop_showing to stop_showing_temporary 'phase2.6'
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
    queryset = Category.objects.all()    
    serializer_class = CategorySerializer
    pagination_class = ResultsSetPaginationForCategories

    

#show all posts about specific category
@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def ShowPostsCategory(request,category):
    #List all code snippets, or create a new snippet
    paginator = ResultsSetPaginationForCategory()
    query_set  = Post.objects.filter(categories__name__contains = category).filter(stop_showing_temporary=False)
    context = paginator.paginate_queryset(query_set, request)
    serializer = PostSerializer(context,many=True)
    return paginator.get_paginated_response(serializer.data)

#show each post
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'

#create comment
#phase2.4
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create_view(request,slug):
    post_instance = get_object_or_404(Post,slug=slug)
    request.data._mutable = True
    request.data['post'] = post_instance.pk
    serializer = CommentCreateSerializer(data=request.data)
    stop_showing_helper = request.data.get('stop_showing_helper')
    if stop_showing_helper == 'yes':
        post_instance.stop_showing_temporary = True
        post_instance.save()    
    request.data._mutable = False   
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  
#show comments of each post
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_list(request,slug):
    post_instance = get_object_or_404(Post,slug=slug)
    comments = Comment.objects.filter(post=post_instance).filter(validated='no')
    serializer = CommentSerializer(comments, many=True)  
    return Response(data=serializer.data, status=status.HTTP_200_OK)
 
#show  validated comments of each post
#phase2.6
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_list_validated(request,slug):
    post_instance = get_object_or_404(Post,slug=slug)
    comments = Comment.objects.filter(post=post_instance).filter(validated='yes')
    serializer = CommentSerializer(comments, many=True)  
    return Response(data=serializer.data, status=status.HTTP_200_OK)    

#show each post by random
#phase2.6
@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def showPost_instance(request,category):
    posts  = Post.objects.filter(categories__name__contains = category).filter(stop_showing_temporary=False).filter(blocked_by_person_for_answering=False).values_list('id')
    id = random.choice(posts) 
    #convert id tuple to integer 
    id = int(''.join(map(str, id)))
    post_instance = Post.objects.get(id=id)
    if post_instance:
        serializer = PostSerializer(post_instance)
        post_instance.blocked_by_person_for_answering =True
        post_instance.start_time=datetime.timezone #phase3.4
        post_instance.still_blocked=True #phase3.4
        post_instance.save()
        return Response(data=serializer.data)
            
#disengage post when user don`t want to answer
#phase3.3 add get request
@api_view(['PUT']) 
@permission_classes([IsAuthenticated])
def disengage_post(request,id,category):
    post_instance = get_object_or_404(Post,id=id)
    post_instance.blocked_by_person_for_answering = False
    head={'Authorization':request.META.get('HTTP_AUTHORIZATION') }
    r = requests.get('http://127.0.0.1:8000/squadBlog/show_post_random/'+category,headers=head)
    if r.status_code == 204:
        post_instance.still_blocked=False #phase3.4
        post_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:    
        data=r.json()   
        post_instance.still_blocked=False   #phase3.4
        post_instance.save()
        return Response(data,status=status.HTTP_200_OK)
# for phase 3.4,when user wants to finish of works squad in site
@api_view(['PUT']) 
@permission_classes([IsAuthenticated])
def disengage_post_finish(request,id):
    post_instance = get_object_or_404(Post,id=id)
    post_instance.blocked_by_person_for_answering = False
    post_instance.still_blocked=False   #phase3.4
    post_instance.blocked_by_person_for_validating=False  #phase3.4
    post_instance.save()
    return Response(status=status.HTTP_200_OK)

#show an post which has answer for validating by random
#phase3.3 add get request
Timeline = namedtuple('Timeline', ('post', 'comments'))
@api_view(['GET'])   
@permission_classes([IsAuthenticated])    
def post_has_answer_random(request):
    post_list = Post.objects.filter(stop_showing_temporary=True).filter(stop_showing_permanently=False).filter(blocked_by_person_for_validating=False).values_list('id').order_by('id')
    if post_list:
        id = random.choice(post_list)
        id = int(''.join(map(str, id)))
        post_object = Post.objects.get(id=id)
        timeline = Timeline(
            post=post_object,
            comments=Comment.objects.filter(post=post_object).filter(validated='no'),
        )
        serializer = PostAndQuestionAnswerSerializer(timeline)
        post_object.blocked_by_person_for_validating = True
        post_object.still_blocked=True #phase3.4
        post_object.save()
        return Response(data=serializer.data)
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)

#disengage post when user don`t want to validate
#phase3.3 add get request
@api_view(['PUT']) 
@permission_classes([IsAuthenticated])
def disengage_post_validate(request,id):
    post_instance = get_object_or_404(Post,id=id)
    post_instance.blocked_by_person_for_validating = False
    r = requests.get('http://127.0.0.1:8000/squadBlog/post_has_answer_by_random/',headers={'Authorization':request.META.get('HTTP_AUTHORIZATION') })
    if r.status_code == 204:
        post_instance.still_blocked=False   #phase3.4
        post_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:    
        data=r.json()  
        post_instance.still_blocked=False   #phase3.4      
        post_instance.save()
        return Response(data,status=status.HTTP_200_OK)    
 
#validate comments of specific post
#phase 3.3 add get request
@api_view(['POST'])
@permission_classes([IsAuthenticated])   
def validate_comments_of_specific_post(request,id):
    post = get_object_or_404(Post,id=id)
    answer_list = request.POST
    value_list=[] 
    r = requests.get('http://127.0.0.1:8000/squadBlog/post_has_answer_by_random/',headers={'Authorization':request.META.get('HTTP_AUTHORIZATION') })
    for key,value in answer_list.items():
        print(value)
        value_list.append(value) 
        print(int(key))   
        #comment = get_object_or_404(Comment,id=int(key))
        comment = Comment.objects.get(id=int(key))
        if value == "no":
            comment.delete()
        else:
            comment.validated = 'yes'
            comment.save()
        
    if value_list.count('yes') >2:
            post.stop_showing_permanently=True
            post.still_blocked=False   #phase3.4
            post.save()
    else:
        post.stop_showing_temporary=False
        post.blocked_by_person_for_answering=False
        post.blocked_by_person_for_validating=False
        post.still_blocked=False   #phase3.4
        post.save()
    
    if r.status_code == 204:
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:    
        data=r.json()  
        return Response(data,status=status.HTTP_200_OK)  

#phase3.4
#unblock posts which still_blocked true for more than some minutes but they don`t have answer
@api_view(['PUT'])
@permission_classes([AllowAny]) 
def unblocker_post(request):
    posts=Post.objects.filter(still_blocked=True)
    for post in posts:
        h1=post.start_time.time().hour
        m1=post.start_time.time().minute
        post.save()
        h2=post.start_time.time().hour
        m2=post.start_time.time().minute
        if (h2-h1)*60 + (m2-m1) > 1:
            post.still_blocked = False
            post.blocked_by_person_for_answering=False
            post.blocked_by_person_for_validating =False
            post.save()
    return Response(status=status.HTTP_204_NO_CONTENT)        
   
