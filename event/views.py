from django.shortcuts import render ,get_object_or_404
from rest_framework import viewsets 

from .serializers import EventSerializer
from .models import Event

from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime

from django_filters import rest_framework 
from .filters import EventFilter
 
from accounts.models import Profile

class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = EventFilter

    def get_queryset(self): 
        queryset = super().get_queryset()
        last_donate = self.request.query_params.get('last_donate')

        if last_donate:
            try:
                user = User.objects.get(pk=last_donate)
                latest_event = Event.objects.filter(doner=user, status='Completed').order_by('-created_on').first()

                if latest_event: 
                    return Event.objects.filter(pk=latest_event.pk)
                else: 
                    return Event.objects.none()
            except User.DoesNotExist:
                pass  
    
    @action(detail=False, methods=['post'], url_path='create')
    def event_create(self, request):
        # Extract data from the request body
        user_id = request.data.get('user')
        title = request.data.get('title')
        description = request.data.get('description', '')
        event_date = request.data.get('event_date', None)
        event_time = request.data.get('event_time', None)
        blood = request.data.get('blood', None)
         
        try:
            # Get the user by ID
            user = get_object_or_404(User, pk=user_id)

            # Create the event
            event = Event.objects.create(
                user=user,
                title=title,
                description=description,
                event_date=event_date,
                event_time=event_time,
                blood=blood,
            ) 
            profile_users = Profile.objects.filter(blood=event.blood)
            current_date = datetime.now().strftime("%B %d %Y") 
 
            context = {
                'host_name': user.username,
                'blood': event.blood,
                'title': event.title,
                'date':event.event_date,
                'time': event_time,
                'location': event.location, 
            }
          
            serializer = self.get_serializer(event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='accepted')
    def event_accepted(self, request, pk=None):
        # Fetch the event object
        event = get_object_or_404(Event, pk=pk)
        print(event.user.username)
        doner_id = request.data.get('doner_id',None)
        doner_message = request.data.get('doner_message', None)
        print(doner_id,'  ', doner_message)
        print('asfasd')

        try: 
            doner_id = request.data.get('doner_id')
            doner_message = request.data.get('doner_message', None)
 
            if not doner_id:
                return Response({'error': "Donor ID is required."}, status=status.HTTP_400_BAD_REQUEST)
 
            doner = get_object_or_404(User, pk=doner_id)
 
            if event.user == doner:
                return Response({'error': "The donor cannot be the same as the event creator."},
                                status=status.HTTP_400_BAD_REQUEST)
            event.doner = doner
            event.status = 'Pending' 
            if doner_message:
                event.doner_message = doner_message
            event.save()
 
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='received')
    def blood_received(self,request,pk=None):
        event = get_object_or_404(Event, pk=pk) 
        event.status = 'Completed'
        event.save()
        current_date = datetime.now().strftime("%B %d %Y") 
        serializer = EventSerializer(event)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)