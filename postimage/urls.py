from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from postimage import views as homeViews
from django.conf.urls import url
from django.conf.urls import url
from django.contrib import admin
from super_resolution import views as homeViews

from django.urls import path,re_path


from . import views
urlpatterns = [
    path('', views.index, name='Index'),
    url('upload_avatar/',homeViews.upload_avatar), # 上傳頭像
    re_path(r'download/(?P<file_path>.*)/$', views.file_response_download1, name='file_download'),

]


