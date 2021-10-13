from rest_framework import serializers
from squadBlog.models import Category,Comment,Post

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class CommentSerializer(serializers.ModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.phone')  #show phone number 
    class Meta:
        model = Comment
        fields = ['question_body','answer_body','post','stop_showing_helper','validated','id']#phase2.4 #phase2.6 validated #phase3.0 add (id)

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['question_body','answer_body','post','stop_showing_helper']#phase2.4

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['text','categories','slug','stop_showing_temporary','blocked_by_person_for_answering','id','stop_showing_permanently','blocked_by_person_for_validating','title','start_time','still_blocked']  #phase2.4 , #phase2.6   #add title phase3.1 ,#add still_blocked,start_time phase3.4  


class PostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['text','categories','slug','blocked_by_person_for_answering','id','blocked_by_person_for_validating','title','start_time','still_blocked'] #phase2.6 , #add title phase3.1 ,#add still_blocked,start_time phase3.4

class PostAndQuestionAnswerSerializer(serializers.Serializer):
    post = PostDetailSerializer()
    comments = CommentSerializer(many=True)
