
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .constraint import BLOOD_GROUP ,GENDER,COUNTRY
# Create your models here.
def validate_image_size(image):
    max_size_mb = 1  # Maximum file size in MB
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"The image size must not exceed {max_size_mb} MB.",ValidationError=[validate_image_size])
    

class Profile(models.Model):
 
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    image = models.ImageField(upload_to='accounts/media/images',null=True,blank=True)
    age = models.IntegerField(null=True,blank=True)
    gender = models.CharField(max_length=20,choices=GENDER,null=True,blank=True)
    phone = models.CharField(max_length=14,null=True,blank=True)
    blood = models.CharField(max_length=20,choices=BLOOD_GROUP)
    divition = models.CharField(max_length=100,null=True,blank=True) 
    country = models.CharField(max_length=30,choices=COUNTRY,default='Bangladesh',null=True,blank=True)
    created_on = models.DateField(auto_now_add=True,editable=False)

   

    
