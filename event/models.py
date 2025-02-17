from django.db import models
from django.contrib.auth.models import User

from .constraint import DONER_CHOICE ,STATUS_CHOICES
from accounts.constraint import BLOOD_GROUP
from django.core.exceptions import ValidationError

# Create your models here.
class Event(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True,related_name='events')
    doner = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True,related_name='doner')
    doner_message = models.TextField(blank=True,null=True,default=None)
    title = models.CharField(max_length=27)
    location = models.CharField(max_length=50,null=True)
    blood = models.CharField(max_length=10,choices=BLOOD_GROUP)
    description = models.TextField()
    event_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Ongoing')
    event_time = models.TimeField() 
    created_on = models.DateField(auto_now_add=True)
 
    def __str__(self):
            return self.title
    
    def clean(self):
        # Ensure user and doner are not the same
        if self.user and self.doner and self.user == self.doner:
            raise ValidationError("The user and doner cannot be the same person")
 