from django.shortcuts import render,redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event,Venue
from .forms import VenueForm,EventForm
from django.http import HttpResponseRedirect,FileResponse
from django.http import HttpResponse
import io
from reportlab.pdfgen import canvas
import csv
from django.http import FileResponse
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator
#Generate text file venue list
def venue_pdf(request):
    #   Create bytestream buffer
    buf= io.BytesIO()
    c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
    #create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)
    #lines=["line1",
     #      "line2",
      #     "line3",]
      
    venues= Venue.objects.all()
    lines=[]
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(" ")
        
    for line in lines:
        textob.textLine(line)
    
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    
    return FileResponse(buf,as_attachment=True,filename="venue.pdf")
    
def venue_csv(request):
    response= HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment ;filename=venues.csv'
    #Create a csv writer
    writer = csv.writer(response)
    #Add column headings to the csv file
    writer.writerow(['Venue Name','Address','Zip code','Phone','Web address','Email'])
    #Loop through and output
    
    #designate the model
    venues= Venue.objects.all()
    #Create blank list
    #Loop through and output
    for venue in venues:
        writer.writerow([venue.name,venue.address,venue.zip_code,venue.phone,venue.web,venue.email_address])
    return response
 
def venue_text(request):
    response= HttpResponse(content_type='text/plain')
    response['Content-Disposition']='attachment ;filename=venues.txt'
    #designate the model
    venues= Venue.objects.all()
    #Create blank list
    lines=[]
    #Loop through and output
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n\n\n')
    #lines=["This is line one\n"
     #      "This is line 2\n"
      #     "THia is 3\n"]
    response.writelines(lines)
    return response


# Create your views here
def delete_venue(request,venue_id):
    venue =Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venue')

def delete_event(request,event_id):
    event =Event.objects.get(pk=event_id)
    event.delete()
    return redirect('list-events')
    
def update_event(request,event_id):
    event =Event.objects.get(pk=event_id)
    form=EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request,'events/update_event.html',{'event':event,'form':form})
    
def update_venue(request,venue_id):
    venue =Venue.objects.get(pk=venue_id)
    form=VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venue')
    return render(request,'events/update_venue.html',{'venue':venue,'form':form})
    
def add_event(request):
    submitted =False
    if request.method == "POST":
        form =EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_events?submitted=True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted =True
    return render(request,'events/add_events.html',{'form':form,'submitted': submitted})

def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request,'events/search_venues.html',{'searched':searched,'venues':venues})
    else:
        return render(request,'events/search_venues.html',{})
        
        

def show_venue(request, venue_id):
    venue =Venue.objects.get(pk=venue_id)
    return render(request,'events/show_venue.html',{'venue':venue})

def list_venues(request):
    venue_list = Venue.objects.all()
    #Set up  tion   objects.all()
    p=Paginator(Venue.objects.all(),2)
    page=request.GET.get('page')
    venues=p.get_page(page)   
    nums= "a" * venues.paginator.num_pages       
    return render(request,'events/venue.html',{'venue_list':venue_list , 'venues':venues,'nums':nums })
    
def add_venue(request):
    submitted =False
    if request.method == "POST":
        form =VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted =True
    return render(request,'events/add_venue.html',{'form':form,'submitted': submitted})


def all_events(request):
    event_list = Event.objects.all().order_by('event_date')
    return render(request,'events/event_list.html',{'event_list':event_list})
    
def home(request,year=datetime.now().year,month = datetime.now().strftime('%B')):
    name = "Krutika"
    #convert name from string to no.
    month = month.capitalize()
    month_no = list(calendar.month_name).index(month)
    month_no = int(month_no)
    
    #create a calendar
    cal= HTMLCalendar().formatmonth(year,month_no)
    
    #get current year
    now = datetime.now()
    current_year= now.year
    #get current time
    time =now.strftime('%I : %M : %S %p')
    return render(request,'events/home.html',{"name":name, "year":year, "month":month, "month_no":month_no , "cal":cal, "current_year":current_year,"time":time})
