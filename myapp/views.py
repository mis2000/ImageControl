from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.views import APIView
import os
import pdb;
import datetime

def form(request):
   if request.method == 'POST' and request.FILES.get('myfile', False):
        print('File found')
        fs = FileSystemStorage()
        pdb.set_trace()
        myfile = request.FILES["myfile"]
        print('File name : '+ myfile.name )
        print(fs.exists(myfile.name))
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'form.html', {
        'uploaded_file_url': uploaded_file_url,
        'message':"File added successfully"
        })
        
        
   return render(request, 'form.html', {'title': 'Opprtunity & Deals', 'cal': 'Opprtunity & Deals'})

class checkFileExists(APIView):
    def get(self, request,format=None):
        print('checkFileExists api called ')
        print(self.request.query_params.get('fileName'))
        folder = os.path.join(settings.MEDIA_ROOT,'Photo')
        fs = FileSystemStorage(folder)
        fileExists =(fs.exists(self.request.query_params.get('fileName')+".jpg"))
        return JsonResponse({'fileExists': fileExists})

def index(request):
   if request.method == 'POST' and request.FILES.get('myfile', False):
        folder = os.path.join(settings.MEDIA_ROOT,'Photo')
        historyFolder = os.path.join(settings.MEDIA_ROOT,'Photo','History')
        fs = FileSystemStorage(location=folder)
        myfile = request.FILES["myfile"]
        if fs.exists(request.POST.get('itemName')+".jpg"):
            os.replace(os.path.join(folder,request.POST.get('itemName')+".jpg"), os.path.join(historyFolder,request.POST.get('itemName')+"_"+datetime.datetime.now().strftime("%Y-%m-%d")+"-"+datetime.datetime.now().strftime("%H-%M-%S")+".jpg"))
        filename = fs.save(request.POST.get('itemName')+".jpg", myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'photo.html', {
        'uploaded_file_url': uploaded_file_url,
        'message':"File added successfully",
        'title': 'Save Photo'
        })  
        
        
   return render(request, 'photo.html', {'title': 'Save Photo'})

class checkAlternativeFileExists(APIView):
    def get(self, request,format=None):
        print('checkFileExists api called ')
        print(self.request.query_params.get('fileName'))
        folder = os.path.join(settings.MEDIA_ROOT,'Alternative')
        fs = FileSystemStorage(folder)
        fileExists =(fs.exists(self.request.query_params.get('fileName')+"_3.jpg"))
        return JsonResponse({'fileExists': fileExists})

def alternativeImage(request):
   if request.method == 'POST' and request.FILES.get('myfile', False):
        folder = os.path.join(settings.MEDIA_ROOT,'Alternative')
        historyFolder = os.path.join(settings.MEDIA_ROOT,'Alternative','History')
        fs = FileSystemStorage(location=folder)
        #pdb.set_trace()
        #request.FILES.getlist("myfile")
        fileCount= 0
        for file in request.FILES.getlist("myfile"):
            fileCount= fileCount+1
            if fileCount == 1 :
               if fs.exists(request.POST.get('itemName')+"_3"+".jpg"):
                 os.replace(os.path.join(folder,request.POST.get('itemName')+"_3.jpg"), os.path.join(historyFolder,request.POST.get('itemName')+"_3_"+datetime.datetime.now().strftime("%Y-%m-%d")+"-"+datetime.datetime.now().strftime("%H-%M-%S")+".jpg"))
               fs.save(request.POST.get('itemName')+"_3"+".jpg", file)             
            if fileCount == 2 :
               if fs.exists(request.POST.get('itemName')+"_4"+".jpg"):
                 os.replace(os.path.join(folder,request.POST.get('itemName')+"_4.jpg"), os.path.join(historyFolder,request.POST.get('itemName')+"_4_"+datetime.datetime.now().strftime("%Y-%m-%d")+"-"+datetime.datetime.now().strftime("%H-%M-%S")+".jpg"))
               fs.save(request.POST.get('itemName')+"_4"+".jpg", file) 
            if fileCount == 3 :
               if fs.exists(request.POST.get('itemName')+"_5"+".jpg"):
                 os.replace(os.path.join(folder,request.POST.get('itemName')+"_5.jpg"), os.path.join(historyFolder,request.POST.get('itemName')+"_5_"+datetime.datetime.now().strftime("%Y-%m-%d")+"-"+datetime.datetime.now().strftime("%H-%M-%S")+".jpg"))
               fs.save(request.POST.get('itemName')+"_5"+".jpg", file) 
        return render(request, 'alternativeImage.html', {
        'message':"File added successfully",
        'title': 'Save Alternative Image'
        })  
        
        
   return render(request, 'alternativeImage.html', {'title': 'Save Alternative Image'})

 

