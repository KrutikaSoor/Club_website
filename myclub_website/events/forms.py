from dataclasses import field
from django import forms
from django.forms import ModelForm
from .models import Venue,Event

#Create a venue Form
class EventForm(ModelForm):
    class Meta:
      model = Event
      fields = ('name','event_date','venue','manager','description','atendees')
      labels = {
        'name': '',
        'event_date': 'YYYY-MM-DD',
        'venue': 'Destination',
        'manager' : 'Manager',
        'description': '',
        'atendees': 'Travellers',
      }
      widgets = {
        'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'From'}),
        'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Date'}),
        'venue': forms.Select(attrs={'class':'form-select', 'placeholder':'Venue'}),
        'manager' : forms.Select(attrs={'class':'form-control', 'placeholder':'Manager'}),
        'description':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
        'atendees':forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Atendees'}),
      }
   
class VenueForm(ModelForm):
    class Meta:
      model = Venue
      fields = ('name','address','zip_code','phone','web','email_address')
      labels = {
        'name': '',
        'address': '',
        'zip_code': '',
        'phone' : '',
        'web': '',
        'email_address': '',
      }
      widgets = {
        'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'To'}),
        'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'From'}),
        'zip_code': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Aadhar number'}),
        'phone' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}),
        'web':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Passport number'}),
        'email_address':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email id'}),
      }
  