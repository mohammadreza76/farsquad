from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from accounts.models import Profile,User #phase2
User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    'new_phase2'
    'add slug in fields' 'phase2.1'
    class Meta:
        model = Profile
        fields = ( 'email','phone','gender', 'date_of_birth','image','major','education_degree','slug','name',) 


class CreateUserSerializer(serializers.ModelSerializer):
    #add name in fields for phase2
    class Meta:
        model = User
        fields = ('phone', 'password','name',)
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    #add name,slug in fields for phase2
    'add slug in fields' 'phase2.1'
    class Meta:
        model = User
        fields = ('id', 'phone', 'first_login', 'name','slug',)#phase2.5

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('mohavereh_score','squad_score','overall_score',)
        


class LoginUserSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            if User.objects.filter(phone=phone).exists():
                user = authenticate(request=self.context.get('request'),
                                    phone=phone, password=password)
                
            else:
                msg = {'detail': 'Phone number is not registered.',
                       'register': False}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail': 'Unable to log in with provided credentials.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class ForgetPasswordSerializer(serializers.Serializer):
    """
    Used for resetting password who forget their password via otp varification
    """
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)        