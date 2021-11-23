from django.shortcuts import redirect, render
from datetime import datetime

from django.utils.functional import partition
from .models import MonitorData, Website, WebUser, WebData
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth import authenticate, login as auth_login

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .serializers import MonitorDataSerializer, WebDataSerializer, WebUserSerializer, WebsiteSerializer


# Create your views here.
@csrf_exempt
def websiteApi(request, id=0):
    if request.method == 'GET':
        website = Website.objects.all()
        website_serializer = WebsiteSerializer(data = website, many = True)
        print(website_serializer.is_valid())
        return JsonResponse(website_serializer.data, safe = False)
    elif request.method == 'POST':
        website_data = JSONParser().parse(request)
        website_serializer = WebsiteSerializer(data = website_data)
        print(website_data['name'].lower(), website_data['URL'])
        if website_serializer.is_valid() and is_valid_url(website_data['URL']):
            web_row = Website.objects.filter(name = website_data['name'].lower())
            if not web_row:
                web_row = Website(name = website_data['name'].lower(), URL = website_data['URL'])
                web_row.save()
                return JsonResponse("Added Successfully!!!", safe=False)
            else:
                web_row = Website.objects.filter(name = website_data['name'])[0]
                return JsonResponse("Record Already Exist!!!", safe=False) 
        return JsonResponse("Failed to Add.", safe=False)
    elif request.method == 'PUT':
        website_data = JSONParser().parse(request)
        website = Website.objects.get(name = website_data['key'])
        website_data_temp = {
            'name':website_data['name'].lower(),
            'URL':website_data['URL']
        }
        website_serializer = WebsiteSerializer(website, data = website_data_temp)
        if website_serializer.is_valid():
            website_serializer.save()
            return JsonResponse("Updated Successfully!!!", safe=False)
        return JsonResponse("Failed to Update.")
    elif request.method == 'DELETE':
        website_data = JSONParser().parse(request)
        website = Website.objects.get(name = website_data['name'])
        website.delete()
        return JsonResponse("Deleted Successfully!!!", safe=False)    

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            email = request.POST.get('email')
            row = WebUser(name = request.user, email = email)
            row.save()
            return redirect('add_web')
        else:
            return render(request = request, template_name = "monitor_app/register.html",
                  context={"form":form})
    form = UserCreationForm
    return render(request = request,
                  template_name = "monitor_app/register.html",
                  context={"form":form})

def logout_view(request):
    logout(request)
    return redirect('home')

def add_web(request):
    user = WebUser.objects.get(name=request.user)
    websites = WebData.objects.filter(userInfo = user)
    if request.method == 'POST':
        url = request.POST.get('web_url')
        website_name = request.POST.get('web_name').lower()
        interval = request.POST.get('interval')
        subscription = request.POST.get('subscribe')
        if is_valid_url(url):
            web_row = Website.objects.filter(name = website_name)
            if not web_row:
                web_row = Website(name = website_name, URL = url)
                web_row.save()
            else:
                web_row = Website.objects.filter(name = website_name)[0]
            webdata_row = WebData.objects.filter(userInfo = user, websiteInfo = web_row)
            if subscription and not webdata_row:
                webdata_row = WebData(userInfo = user, websiteInfo = web_row, interval = interval, subscription = 1)
            elif not subscription and not webdata_row:
                webdata_row = WebData(userInfo = user, websiteInfo = web_row, interval = interval, subscription = 0)
            else:
                messgae = 'already exist!'
                return render(request, 'monitor_app/add_web.html', context={'websitesInfo': websites, 'Alert_1': messgae})
            webdata_row.save()
    return render(request, 'monitor_app/add_web.html', context={'websitesInfo': websites})

def login_view(request):
    if request.method == 'POST':
        _username = request.POST.get('username')
        _password = request.POST.get('password')
        user = authenticate(username=_username, password=_password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('add_web')
        else:
            _message = 'Invalid username or password, please try again.'
            return render(request = request, template_name = "monitor_app/login.html",
            context={"form":AuthenticationForm(),"error":_message})
    else:
        form = AuthenticationForm()
    return render(request, 'monitor_app/login.html', {'form':form})

def is_valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)

def home(request):
    return render(
        request,
        'monitor_app/home.html',
        {
            'name': 'Abdul Jalil',
            'date': datetime.now()
        }
    )