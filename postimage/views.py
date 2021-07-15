from django.shortcuts import render,redirect
from .forms import UploadModelForm
from .models import Photo
from django.http.response import HttpResponse
from django.http import StreamingHttpResponse
from django.http import FileResponse  
import os
from django.http import HttpResponse, Http404, StreamingHttpResponse, FileResponse

def index(request):
    photos = Photo.objects.all()  #查詢所有資料
    
    form = UploadModelForm()
    if request.method == "POST":
        form = UploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/postimage/')
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
