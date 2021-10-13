import requests,random,datetime
from mohavereh.models import InformalText,FormalText
from mohavereh.serializers import InformalTextSerializer,FormalTextSerializer,InformalAndAnswerSerializer
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,AllowAny
from collections import namedtuple
# Create your views here.
#phase 3.3 for automatic progress

#declare pagination for handling the number of instances of informal text shows in page
class ResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 3000000

#show each Informal Text
class InformalTextDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = InformalText.objects.all()
    serializer_class = InformalTextSerializer
    lookup_field = 'slug'  

#create formal text
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def formal_text_create_view(request,slug):
    informalـtext_instance = get_object_or_404(InformalText,slug=slug)
    informalـtext_instance.has_answer='yes'
    informalـtext_instance.save()
    request.data._mutable = True
    request.data['informalـtext'] = informalـtext_instance.pk
    request.data._mutable = False
    serializer = FormalTextSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED) 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#show formal text of each informal text
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def formal_text(request,slug):
    try:
        informal_text = InformalText.objects.get(slug=slug)
        formal_text = FormalText.objects.filter(informalـtext=informal_text)
        serializer = FormalTextSerializer(formal_text, many=True)  
        return Response(data=serializer.data, status=status.HTTP_200_OK)    
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)    

#show all informal text 
@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def showInformalText(request):
    #List all code snippets, or create a new snippet
    paginator = ResultsSetPagination()
    query_set  = InformalText.objects.filter(has_answer='no')
    context = paginator.paginate_queryset(query_set, request)
    serializer = InformalTextSerializer(context,many=True)
    return paginator.get_paginated_response(serializer.data)   

#show list of informal text which has answer for validating
class InformalTextHasAnswerList(generics.ListAPIView):
    serializer_class = InformalTextSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the informal textes which 
        has answer field is true.
        """
        return InformalText.objects.filter(has_answer='yes').filter(validate_answer='no')
 
#validate each formal text
#phase3.3 add get request
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_formal_text(request,slug):
    #copy whole code of this funtion
    informalـtext_instance = get_object_or_404(InformalText,slug=slug)
    validate_answer = request.data.get('validate_answer')
    r = requests.get('http://127.0.0.1:8000/mohavereh/informal_text_has_answer_random',headers={'Authorization':request.META.get('HTTP_AUTHORIZATION') })
    if validate_answer == 'no':
        formalـtext_instance = get_object_or_404(FormalText,informalـtext_id=informalـtext_instance.pk)
        formalـtext_instance.delete()
        informalـtext_instance.has_answer = 'no'
        informalـtext_instance.blocked_by_person_for_answering=False
        informalـtext_instance.blocked_by_person_for_validating=False
        informalـtext_instance.still_blocked=False   #phase3.4
        informalـtext_instance.save()
    else:#phase2.5
        informalـtext_instance.validate_answer = 'yes'  
        informalـtext_instance.still_blocked=False   #phase3.4 
        informalـtext_instance.save() 
    if r.status_code == 204:
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:    
        data=r.json()     
    return Response(data,status=status.HTTP_200_OK)    
  
#show each informal text by random
#phase2.6
@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def showInformalText_instance(request):
    informal_textes  = InformalText.objects.filter(has_answer='no').filter(blocked_by_person_for_answering=False).values_list('id')
    id = random.choice(informal_textes) 
    #convert id tuple to integer 
    id = int(''.join(map(str, id)))
    post_instance = InformalText.objects.get(id=id)
    if post_instance:
        serializer = InformalTextSerializer(post_instance)
        post_instance.blocked_by_person_for_answering =True
        post_instance.start_time=datetime.timezone #phase3.4
        post_instance.still_blocked=True #phase3.4
        post_instance.save()
        return Response(data=serializer.data)
            
#disengage informaltext when user don`t want to answer
#phase3.3 add get request
@api_view(['PUT']) 
@permission_classes([IsAuthenticated])
def disengage_informaltext(request,id):
    informalـtext_instance = get_object_or_404(InformalText,id=id)
    informalـtext_instance.blocked_by_person_for_answering = False
    r = requests.get('http://127.0.0.1:8000/mohavereh/show_informal_text_random',headers={'Authorization':request.META.get('HTTP_AUTHORIZATION') })
    if r.status_code == 204:
        informalـtext_instance.still_blocked=False #phase3.4
        informalـtext_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:    
        data=r.json() 
        informalـtext_instance.still_blocked=False #phase3.4            
        informalـtext_instance.save()
        return Response(data,status=status.HTTP_200_OK)

#show an informal text which has answer for validating by random
#phase3.3 add get request
Timeline = namedtuple('Timeline', ('informal', 'formal'))
@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def informal_text_has_answer(request): 
    informal_textes = InformalText.objects.filter(has_answer='yes').filter(validate_answer='no').filter(blocked_by_person_for_validating=False).values_list('id')
    if informal_textes:
        id = random.choice(informal_textes) 
        #convert id tuple to integer 
        id = int(''.join(map(str, id)))
        post_instance = InformalText.objects.get(id=id)
        timeline = Timeline(
            informal=post_instance,
            formal=FormalText.objects.filter(informalـtext=post_instance)
        )
        serializer = InformalAndAnswerSerializer(timeline)
        post_instance.blocked_by_person_for_validating =True
        post_instance.still_blocked=True #phase3.4
        post_instance.save() 
        return Response(data=serializer.data)     
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)        


#disengage informaltext when user don`t want to validate
#phase3.3 add get request
@api_view(['PUT']) 
@permission_classes([IsAuthenticated])
def disengage_informaltext_validate(request,id):
    informalـtext_instance = get_object_or_404(InformalText,id=id)
    informalـtext_instance.blocked_by_person_for_validating = False
    r = requests.get('http://127.0.0.1:8000/mohavereh/informal_text_has_answer_random',headers={'Authorization':request.META.get('HTTP_AUTHORIZATION') })
    if r.status_code == 204:
        informalـtext_instance.still_blocked=False   #phase3.4
        informalـtext_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:    
        data=r.json() 
        informalـtext_instance.still_blocked=False   #phase3.4        
        informalـtext_instance.save()        
        return Response(data,status=status.HTTP_200_OK)

# for phase 3.4,when user wants to finish of works mohavereh in site
@api_view(['PUT']) 
@permission_classes([IsAuthenticated])
def disengage_informal_text_finish(request,id):
    informalـtext_instance = get_object_or_404(InformalText,id=id)
    informalـtext_instance.blocked_by_person_for_answering = False
    informalـtext_instance.still_blocked=False   #phase3.4
    informalـtext_instance.blocked_by_person_for_validating=False  #phase3.4
    informalـtext_instance.save()
    return Response(status=status.HTTP_200_OK)

#phase3.4
#unblock informal texts which still_blocked true for more than some minutes but they don`t have answer
@api_view(['PUT'])
@permission_classes([AllowAny]) 
def unblocker_informaltext(request):
    informalـtext_list=InformalText.objects.filter(still_blocked=True)
    for informaltext in informalـtext_list:
        h1=informaltext.start_time.time().hour
        m1=informaltext.start_time.time().minute
        informaltext.save()
        h2=informaltext.start_time.time().hour
        m2=informaltext.start_time.time().minute
        if (h2-h1)*60 + (m2-m1) > 1:
            informaltext.still_blocked = False
            informaltext.blocked_by_person_for_answering=False
            informaltext.blocked_by_person_for_validating =False
            informaltext.save()
    return Response(status=status.HTTP_204_NO_CONTENT)            