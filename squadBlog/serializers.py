from rest_framework import serializers
from squadBlog.models import Category,Comment,Post

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['question_body','answer_body']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['question_body','answer_body','post']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['text','categories','slug']                


class PostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['text','categories','slug'] 

