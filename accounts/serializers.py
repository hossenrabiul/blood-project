from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User


class ProfileSerializers(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user = serializers.StringRelatedField(many=False)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = Profile 
        fields = ['user_id','user','first_name','last_name','email','phone','image','age','gender','blood','divition','country','image']
    
    

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name','last_login','is_active']
    
  
        
     
class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    blood = serializers.CharField()

    class Meta:
        model = User 
        fields = ["username",'first_name','last_name','email','password','confirm_password','blood']
        
    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        blood = self.validated_data['blood']

        if password != password2:
            raise serializers.ValidationError({'error':"Password Doesnot mathc"})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error':"Email Already Exists!"})
        user = User(username=username,email=email,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.is_active = False 
        user.save() 

        profile = Profile.objects.create(
            user=user,
            blood = blood,
        )
        profile.save()


        return user
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)