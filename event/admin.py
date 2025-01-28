from django.contrib import admin


from .models import Event   
# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ['user','doner','title','blood','status','event_date','created_on']

admin.site.register(Event,EventAdmin)
