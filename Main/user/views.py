from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render
from user.utilities.helpers import get_login_session, get_tokens, invalidate_session
from user.models import user
from user.serializers import ConfirmRegistrationVerificationCodeSerializer, LoginSerializer, RegisterUserSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
import uuid;
# Create your views here.


def get_random_string(string_length=10):
    random = str(uuid.uuid4()) 
    random = random.upper()  
    random = random.replace("-", "") 
    return random[0:string_length] 

class RegsiterUserView(APIView):
    def post(self, request):
        register_serializer=RegisterUserSerializer(data=request.data)
        if register_serializer.is_valid():
            user_data=register_serializer.validated_data
            user_object=user.objects.filter(email=user_data.get('email')).first()

            if user_object and user_object.verified==True:
                return Response({'message': 'user already exists'}, status=status.HTTP_400_BAD_REQUEST)  
            elif user_object and user_object.verified==False:
                return Response({'message': 'user exists but not verified'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                validation_code = get_random_string(6)
                new_user=user.objects.create(email=user_data.get('email'),
                    password= make_password(user_data.get('password')),
                    firstname= user_data.get('firstname' , ""),
                    lastname= user_data.get('lastname' , ""),
                    address= user_data.get("address", ""),
                    validation_code= validation_code,
                    verified= False)
            return Response({"message": "verification email sent"}, status=status.HTTP_200_OK)
        else:
            return Response({'data': register_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  


def check_is_token_expired(last_logged_in) -> bool:

    # print( datetime.now() ,  last_logged_in)
    return True

class RegistrationVerificationCodeView(APIView):
    def post(self, request):
        confirm_validation_code_Serializer=ConfirmRegistrationVerificationCodeSerializer(data=request.data)
        if confirm_validation_code_Serializer.is_valid():
            confirmation_data=confirm_validation_code_Serializer.validated_data
            
            try:
                user_object=user.objects.get(email=confirmation_data.get('email'), validation_code=confirmation_data.get('validation_code'))
            except user.DoesNotExist:
                return Response({'message': 'user does not exist or invalid verification code'}, status=status.HTTP_400_BAD_REQUEST) 

            if user_object.verified:
                return Response({'message': 'user is already validated'}, status=status.HTTP_400_BAD_REQUEST) 
            # elif check_is_token_expired(user_object.createdAt):
                # user.objects.filter(email=confirmation_data.get('email'), validation_code=confirmation_data.get('validation_code')).delete()
                # return Response({'message': 'Validation Code Expired, Please Register Again'}, status=status.HTTP_400_BAD_REQUEST) 
            else:
                user_object.verified=True
                user_object.save()
                return Response({'message': 'successfully verified the account'}, status=status.HTTP_201_CREATED) 

                
        else:
            return Response({'data': confirm_validation_code_Serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


            #User login view
class UserLoginView(APIView):
    def post(self, request):
        login_serializer= LoginSerializer(data=request.data)
        if login_serializer.is_valid():
            login_data=login_serializer.validated_data
            try:
                get_user=user.objects.get(email=login_data.get('email'))
            except user.DoesNotExist:
                return Response({'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            user_validity=check_password(login_data.get('password'), get_user.password)
            if user_validity:
                user_object=get_object_or_404(user, email=login_data.get('email'))

                if user_object.verified==True:

                    resp=dict()
                    data=dict()

                    previous_login_sessions = get_login_session(user_email=user_object.email)
                    print(previous_login_sessions)
                    if len(previous_login_sessions)>0 : 
                        for  previous_login_session in previous_login_sessions :  
                            print(previous_login_session)
                            invalidate_session(login_session=previous_login_session)

                   
                    access_token, refresh_token = get_tokens(user=user_object)
                    user_serializer=UserSerializer(model_to_dict(user_object))
 
                    resp['message'] = 'logged in'
                    data['access_token'] = access_token
                    data['refresh_token'] = refresh_token
                    data.update(user_serializer.data)
                    resp['data'] = data

                    return Response(resp, status=status.HTTP_200_OK)
                else:
                    return Response({'message': "User is not verified"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': "Either email or password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'data': login_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)