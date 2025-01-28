from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
# Create your views here.
from .models import Profile
from .serializers import (
    ProfileSerializers,
    RegistrationSerializer,
    UserLoginSerializer,
    UserSerializers,
)
from rest_framework.response import Response

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.shortcuts import redirect 
from django.contrib.auth import authenticate ,logout , login 
from rest_framework.authtoken.models import Token

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action


class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Get query parameters
        user_id = self.request.query_params.get('user_id', None)
        blood = self.request.query_params.get('blood', None)
        division = self.request.query_params.get('division', None)
        gender = self.request.query_params.get('gender', None)

        if user_id:
            queryset = queryset.filter(user_id=user_id)   

        return queryset
    
    @action(detail=True,methods=['put'],url_path='update-image') 
    def update_image(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            profile = Profile.objects.get(user=user)

        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        image = request.data.get('image', None)

        if not image:
            return Response({'error': 'Image is required.'}, status=status.HTTP_400_BAD_REQUEST)

        profile.image = image
        profile.save()
        serializer = ProfileSerializers(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], url_path='update-profile')
    def update_profile(self, request, pk=None):
        user = User.objects.get(pk=pk)
        profile = Profile.objects.get(user=user)

        # Ensure 'user' and 'profile' data are passed in the request body
        user_data = request.data.get('user', None)
        profile_data = request.data.get('profile', None)

        if user_data is None or profile_data is None:
            return Response({"detail": "Invalid data format. Please provide 'user' and 'profile' fields."}, status=status.HTTP_400_BAD_REQUEST)

        # Update User fields
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.save()

        # Update Profile fields
        profile.phone = profile_data.get('phone', profile.phone)
        # profile.image = profile_data.get('image', profile.image)
        profile.age = profile_data.get('age', profile.age)
        profile.gender = profile_data.get('gender', profile.gender)
        profile.blood = profile_data.get('blood', profile.blood)
        profile.divition = profile_data.get('divition', profile.divition)
        profile.country = profile_data.get('country', profile.country)
        profile.save()

        # Return the updated profile data
        serializer = ProfileSerializers(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('id')  

        if user_id:
            queryset = queryset.filter(id=user_id)  
        
        return queryset

# APIView -> django.views import views ar moto -> 12 batari

class UserRegistrationApiView(APIView):
    serializer_class = RegistrationSerializer

    def post(self,requert):
        serializer = self.serializer_class(data=requert.data)
        
        if serializer.is_valid():
            username = serializer._validated_data['username']
            email = serializer._validated_data['email']
            if User.objects.filter(email=email).exists():
                return Response({'auth':f"[{email} \n] Email already exist!"})
 
            if User.objects.filter(username=username).exists():
                return Response({'auth':f"[{username}] Username already exist!"})
            
            user = serializer.save() 
            print(user)
            token = default_token_generator.make_token(user)
            print(token)
            uid = urlsafe_base64_encode(force_bytes(user.pk)) # unique url make kora
            print("UID: ",uid)
            confirm_link = f"http://127.0.0.1:8000/accounts/active/{uid}/{token}"
        
            email_subject = "Confirm Your Email! "
            email_body = render_to_string('confirm_email.html',{'confirm_link':confirm_link})

            email = EmailMultiAlternatives(
                subject=email_subject,
                body='',
                from_email= '', 
                to =[user.email]
            )
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Done")
        return Response(serializer.errors)
    

def activate(request,uid64,token):
    print("hello word")

    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True 
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    
    
class UserLoignView(APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer._validated_data['username']
            password = serializer._validated_data['password']

            user = authenticate(username=username,password=password)
            
            if user:
                token , _ = Token.objects.get_or_create(user=user)
                login(request,user)
                return Response({"token":token.key,"user_id":user.id,})
            else:
                return Response({"error":"Invalid Credential"})
        return Response(serializer.errors)

#  Nomaly post request ar jonnno API View use kora hoy

class UserLogoutView(APIView):
    def get(self,request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')