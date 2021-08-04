from django.shortcuts import render,redirect
from .forms import UploadModelForm
from .models import Photo
from django.http.response import HttpResponse
from django.http import StreamingHttpResponse
from django.utils import timezone
from django.core.files import File  # you need this somewhere
from django.http import FileResponse  
import os
from django.http import HttpResponse, Http404, StreamingHttpResponse, FileResponse
from .CorpImg import *
import os
import time
import tkinter
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image
from PIL import ImageTk
from .Wicket import Wicket
from postimage import CorpImg
from django.core.files.images import ImageFile



def index(request):
    photos = Photo.objects.all()  #查詢所有資料
    form = UploadModelForm ()
    if request.method == "POST":
        form = UploadModelForm(request.POST, request.FILES)
        print("form1:",form)
    if form.is_valid():
 ##       form.save()
        print("form.save")
        print("form2:",form)
        test=request.FILES
        corp = Crop()
        print("mode",form.Meta().model)
        corp.create_window()
        corp.set_window_title('Window')
        corp.set_window_size('max')
        corp.choose_img(test)
        corp.show_window()


    
            
              
        if corp.get_corp()!=None:
            print("test",test,",",type(test))
            file1=corp.get_corp
            file_path=corp.get_corp_path()
            print("filepath",file_path)
            print(form.Meta().model.image)
            print("form3:",form)
            m=Photo()
            m.image=file_path
            m.save()


            if form.is_valid():
     ##           form.save()
                print("form.save")
            
                return redirect('/postimage/')
            
            else:
                print("not save")
        else:
            print("123123123123")
            

        return redirect('/postimage/')
    else:
        print("fail form") 
    context = {
        'photos':photos,
        'form': form
    }
    

    return render(request, 'photos/index.html', context)

def upload_avatar(request):
    file_obj = request.FILES.get('avatar')
    print(file_obj)
    file_path = os.path.join('/static/images/', file_obj.name)
    with open(file_path, 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    return HttpResponse(file_path)

# Create your views here.

def file_response_download1(request, file_path):
    try:
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        
        
        return response
    except Exception:
        raise Http404

def file_download(request, file_path):
    # do something...
    with open(file_path) as f:
        c = f.read()
    return HttpResponse(c)

def file_response_download(request, file_path):
    ext = os.path.basename(file_path).split('.')[-1].lower()
    # cannot be used to download py, db and sqlite3 files.
    if ext not in ['py', 'db',  'sqlite3']:
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    else:
        raise Http404
