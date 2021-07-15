from django.shortcuts import render, HttpResponse
import os

def test(request):
    return render(request, 'test.html')
    
def upload_avatar(request):
    file_obj = request.FILES.get('avatar')
    print(file_obj)
    file_path = os.path.join('/static/images/', file_obj.name)
    with open(file_path, 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    return HttpResponse(file_path)
