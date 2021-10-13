from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes#phase2.5
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from .serializers import (ProfileSerializer,CreateUserSerializer,UserSerializer, LoginUserSerializer,ForgetPasswordSerializer,ScoreSerializer)                 
from accounts.models import User, PhoneOTP, Profile
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
import random
from ippanel import Client
from rest_framework.permissions import IsAuthenticated #phase2
from rest_framework.parsers import MultiPartParser, FormParser #phase2
from mohavereh.models import FormalText
from squadBlog.models import Comment

class ValidatePhoneSendOTP(APIView):
    '''
    This class view takes phone number and if it doesn't exists already then it sends otp for
    first coming phone numbers'''

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'status': status.HTTP_403_FORBIDDEN, 'detail': 'Phone Number already exists'})
                 # logic to send the otp and store the phone number and that otp in table. 
            else:
                
                otp=random.randint(500,99999)
                #print(phone, otp)
                if otp:
                    otp = str(otp)
                    count = 1
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        oldd=old.first()
                        count = oldd.count
                        oldd.count = count + 1
                        print(count)
                        if count > 7:
                            return Response({
                                'status' : status.HTTP_403_FORBIDDEN, 
                                'detail' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                            })
                        else:
                            oldd.otp=otp
                            oldd.save()
                            send_otp(phone,otp)
                    
                    else:
                        count = count + 1
               
                        PhoneOTP.objects.create(
                             phone =  phone, 
                             otp =   otp,
                             count = count
        
                             )
                        send_otp(phone,otp) 
                    
                else:
                    return Response({
                                'status': status.HTTP_503_SERVICE_UNAVAILABLE, 'detail' : "OTP sending error. Please try after some time."
                            })

                return Response({
                    'status': True, 'detail': 'Otp has been sent successfully.'
                })
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST, 'detail' : "I haven't received any phone number. Please do a POST request."
            })


class ValidateOTP(APIView):
    '''
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password
    
    '''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent   = request.data.get('otp', False)
        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.save()

                    return Response({
                        'status' : True, 
                        'detail' : 'OTP matched, kindly proceed to save password'
                    })
                else:
                    return Response({
                        'status' : status.HTTP_404_NOT_FOUND, 
                        'detail' : 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status' : status.HTTP_404_NOT_FOUND,
                    'detail' : 'Phone not recognised. Kindly request a new otp with this number'
                })


        else:
            return Response({
                'status' : status.HTTP_400_BAD_REQUEST,
                'detail' : 'Either phone or otp was not recieved in Post request'
            })            

class ValidatePhoneForgot(APIView):
    '''
    Validate if account is there for a given phone number and then send otp for forgot password reset'''

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                otp =random.randint(500,99999)
                #print(phone, otp)
                if otp:
                    otp = str(otp)
                    count = 1
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        old = old.first()
                        k = old.count
                        if k > 10:
                            return Response({
                                'status' : status.HTTP_403_FORBIDDEN, 
                                'detail' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                            })
                        old.count = k + 1
                        old.save()
                        send_otp_forgot(phone,otp)
                        return Response({'status': True, 'detail': 'OTP has been sent for password reset. Limits about to reach.'})
                    
                    else:
                        count = count + 1
               
                        PhoneOTP.objects.create(
                             phone =  phone, 
                             otp =   otp,
                             count = count,
                             forgot = True,         
                             )
                        send_otp_forgot(phone,otp)     
                        return Response({'status': True, 'detail': 'OTP has been sent for password reset'})
                    
                else:
                    return Response({
                                    'status': status.HTTP_503_SERVICE_UNAVAILABLE, 'detail' : "OTP sending error. Please try after some time."
                                })
            else:
                return Response({
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'detail' : 'Phone number not recognised. Kindly try a new account for this number'
                })


def send_otp(phone,key):
    """
    This is an helper function to send otp to session stored phones or 
    passed phone number as argument.
    """
    
    # you api key that generated from panel
    api_key = "artJcX_XowCxqB8mcWbjMJcTuBRRnuRn5yvhUxVlN8E="
    if phone:
        sms = Client(api_key)
        pattern = sms.create_pattern(r"کد احراز هویت شما در فاسکواد : %verification-code%", False)
        pattern_values = {
            "verification-code":str(key),
        }

        sms.send_pattern(
            "zdtwaeyqz1",    # pattern code
            "50002620000528",      # originator
            phone,  # recipient
            pattern_values,  # pattern values
        )

        return key
    else:
        return False 


def send_otp_forgot(phone,key):
    api_key = "artJcX_XowCxqB8mcWbjMJcTuBRRnuRn5yvhUxVlN8E="
    if phone:
        phone = str(phone)
        otp_key = str(key)
        user = get_object_or_404(User, phone__iexact = phone)
        if user.name: 
            name = user.name
        else:
            name = phone
        sms = Client(api_key)
        sms.create_pattern(r"کد احراز هویت شما در فاسکواد : %verification-code%", False)
        pattern_values = {
            "verification-code":otp_key,
        }

        sms.send_pattern(
            "zdtwaeyqz1",    # pattern code
            "50002620000528",      # originator
            phone,  # recipient
            pattern_values,  # pattern values
        )

        return otp_key
    else:
        return False


class Register(APIView):

    '''Takes phone and a password and creates a new user only if otp was verified and phone is new'''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        name = request.data.get('name', False) #phase2

        if phone and password:
            phone = str(phone)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'status': status.HTTP_406_NOT_ACCEPTABLE, 'detail': 'Phone Number already have account associated. Kindly try forgot password'})
            else:
                old = PhoneOTP.objects.filter(phone__iexact = phone)
                if old.exists():
                    old = old.first()
                    if old.logged:
                        Temp_data = {'phone': phone, 'password': password ,'name':name} #phase2

                        serializer = CreateUserSerializer(data=Temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save()
                        user.save()

                        old.delete()
                        return Response({
                            'status' : True, 
                            'detail' : 'Congrts, user has been created successfully.',
                        })

                    else:
                        return Response({
                            'status': status.HTTP_403_FORBIDDEN,
                            'detail': 'Your otp was not verified earlier. Please go back and verify otp'

                        })
                else:
                    return Response({
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'detail' : 'Phone number not recognised. Kindly request a new otp with this number'
                })
                    

        else:
            return Response({
                'status' : status.HTTP_400_BAD_REQUEST,
                'detail' : 'Either phone or password was not recieved in Post request'
            })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    
    def get_post_response_data(self, request, token, instance):
        UserSerializer = self.get_user_serializer_class()

        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token,
            'slug': request.user.slug #phase2.1
        }
        if UserSerializer is not None:
            data["user"] = UserSerializer(
                request.user,
                context=self.get_serializer_context()
            ).data
        return data 

    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.last_login is None :
            user.first_login = True
            user.save()
            
        elif user.first_login:
            user.first_login = False
            user.save()
            
        login(request, user)
        return super().post(request, format=None)     



class ForgotValidateOTP(APIView):
    '''
    If you have received an otp, post a request with phone and that otp and you will be redirected to reset  the forgotted password
    
    '''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent   = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                if old.forgot == False:
                    return Response({
                        'status' : status.HTTP_406_NOT_ACCEPTABLE, 
                        'detail' : 'This phone havenot send valid otp for forgot password. Request a new otp or contact help centre.'
                     })
                    
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.forgot_logged = True
                    old.save()

                    return Response({
                        'status' : True, 
                        'detail' : 'OTP matched, kindly proceed to create new password'
                    })
                else:
                    return Response({
                        'status' : status.HTTP_400_BAD_REQUEST, 
                        'detail' : 'OTP incorrect, please try again'

                    })
            else:
                return Response({
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'detail' : 'Phone not recognised. Kindly request a new otp with this number'
                })


        else:
            return Response({
                'status' : status.HTTP_400_BAD_REQUEST,
                'detail' : 'Either phone or otp was not recieved in Post request'
            })            

class ForgetPasswordChange(APIView):
    '''
    if forgot_logged is valid and account exists then only pass otp, phone and password to reset the password. All three should match.APIView
    '''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp   = request.data.get("otp", False)
        password = request.data.get('password', False)

        if phone and otp and password:
            old = PhoneOTP.objects.filter(Q(phone__iexact = phone) & Q(otp__iexact = otp))
            if old.exists():
                old = old.first()
                if old.forgot_logged:
                    post_data = {
                        'phone' : phone,
                        'password' : password
                    }
                    user_obj = get_object_or_404(User, phone__iexact=phone)
                    serializer = ForgetPasswordSerializer(data = post_data)
                    serializer.is_valid(raise_exception = True)
                    if user_obj:
                        user_obj.set_password(serializer.data.get('password'))
                        user_obj.active = True
                        user_obj.save()
                        old.delete()
                        return Response({
                            'status' : True,
                            'detail' : 'Password changed successfully. Please Login'
                        })

                else:
                    return Response({
                'status' : status.HTTP_404_NOT_FOUND,
                'detail' : 'OTP Verification failed. Please try again in previous step'
                                 })

            else:
                return Response({
                'status' : status.HTTP_404_NOT_FOUND,
                'detail' : 'Phone and otp are not matching or a new phone has entered. Request a new otp in forgot password'
            })

        else:
            return Response({
                'status' : status.HTTP_400_BAD_REQUEST,
                'detail' : 'Post request have parameters mising.'
            })

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    #phase 2
    "delete and retritive and update profile"
    'add slug in in this class' 'phase2.1'
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'slug'


class ProfileListView(generics.ListAPIView):
    #phase2
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()  

#phase2.5
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_score(request,slug):
    try:
        user = get_object_or_404(User,slug=slug)
        user.mohavereh_score = FormalText.objects.filter(owner=user).count()
        user.squad_score = Comment.objects.filter(owner=user).count()
        user.overall_score = user.mohavereh_score + user.squad_score
        user.save()
        data_show = {'mohavereh_score':user.mohavereh_score,'overall_score':user.overall_score,'squad_score':user.squad_score,}
        serializer = ScoreSerializer(data=data_show)
        serializer.is_valid(raise_exception = True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)  
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)    