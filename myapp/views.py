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
        photoFolder = os.path.join(settings.MEDIA_ROOT,'Photo')
        photoHistoryFolder = os.path.join(settings.MEDIA_ROOT,'Photo','History')
        photoFs = FileSystemStorage(location=photoFolder)
       
        #alternative folder
        alternativeFolder = os.path.join(settings.MEDIA_ROOT,'Alternative')
        alternativeHistoryFolder = os.path.join(settings.MEDIA_ROOT,'Alternative','History')
        alternativeFs = FileSystemStorage(location=alternativeFolder)
        fileCount= 0

        fileNames  = self.request.query_params.get('fileName').split(",")
        for fileName in fileNames  :
            if fileName.strip() !="" :
               if fileName.find("_") == -1 :
                   if (photoFs.exists(fileName)) :
                       fileCount = fileCount+1
               else :
                    if (alternativeFs.exists(fileName)) :
                       fileCount = fileCount+1
       
        if fileCount > 0  :
           print("exists")
           fileExists= True
        else :
           print("not exists")
           fileExists = False
        return JsonResponse({'fileExists': fileExists})


def alternativeImage(request):
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
def index(request):
   if request.method == 'POST' and request.FILES.get('myfile', False):
        print("photo folder") 
        #photo folder
        photoFolder = os.path.join(settings.MEDIA_ROOT,'Photo')
        photoHistoryFolder = os.path.join(settings.MEDIA_ROOT,'Photo','History')
        photoFs = FileSystemStorage(location=photoFolder)
       
        #alternative folder
        alternativeFolder = os.path.join(settings.MEDIA_ROOT,'Alternative')
        alternativeHistoryFolder = os.path.join(settings.MEDIA_ROOT,'Alternative','History')
        alternativeFs = FileSystemStorage(location=alternativeFolder)
        fileCount= 0
        maxFileError=0
        maxFileErrorMessage="Too many alternative images exists for"

        for file in request.FILES.getlist("myfile"):
            fileCount= fileCount+1
            if file.name.find("_") == -1 :
               if str( request.POST.get('overWrite'))=="1":
                   print("overWrite")
                   if photoFs.exists(file.name):
                     print("Exists")
                     os.replace(os.path.join(photoFolder,file.name), os.path.join(photoHistoryFolder,file.name+"_"+datetime.datetime.now().strftime("%Y-%m-%d")+"-"+datetime.datetime.now().strftime("%H-%M-%S")+".jpg"))
                     photoFs.save(file.name, file)
               else :
                  print("Not Exists")
                  if (photoFs.exists(file.name)) == False:
                     photoFs.save(file.name, file)
            else :
               if str( request.POST.get('overWrite'))=="1":
                  if alternativeFs.exists(file.name):
                     os.replace(os.path.join(alternativeFolder,file.name), os.path.join(alternativeHistoryFolder,file.name+"_"+datetime.datetime.now().strftime("%Y-%m-%d")+"-"+datetime.datetime.now().strftime("%H-%M-%S")+".jpg"))
                     alternativeFs.save(file.name, file)
                  else :
                     if(checkMaxFileCount(alternativeFs,file.name)<3):
                        alternativeFs.save(file.name, file)
                     else :
                         if maxFileError==0 :
                            maxFileError=1
                            maxFileErrorMessage=maxFileErrorMessage +" "+file.name.split("_")[0]+".jpg"
                         else :
                           maxFileErrorMessage=maxFileErrorMessage +" , "+file.name.split("_")[0]+".jpg"
                  
               else :
                  if (alternativeFs.exists(file.name)) == False:
                     if(checkMaxFileCount(alternativeFs,file.name)<3):
                        alternativeFs.save(file.name, file)
                     else :
                         if maxFileError==0 :
                            maxFileError=1
                            maxFileErrorMessage=maxFileErrorMessage +" "+file.name.split("_")[0]+".jpg"
                         else:
                           maxFileErrorMessage=maxFileErrorMessage +" , "+file.name.split("_")[0]+".jpg"
                        

        print(maxFileErrorMessage)
        print(maxFileError)

        return render(request, 'photo.html', {
        'message':"File added successfully",
        'title': 'Save Alternative Image',
        'maxFileError' : str(maxFileError),
        'maxFileErrorMessage':maxFileErrorMessage

        })
   return render(request, 'photo.html', {'title': 'Save Alternative Image'})

def checkMaxFileCount(alternativeFs,fullFileName):
   fileCount= 0
   fileName = fullFileName.split("_")[0]
   alternativeFileNameExtensions = ["3","4","5","6","7","8","9"]
   for alternativeFileNameExtension in alternativeFileNameExtensions:
      if(alternativeFs.exists(fileName+"_"+alternativeFileNameExtension+".jpg")):
         fileCount= fileCount+1
   
   return fileCount











