from django.conf.urls import url
from django.contrib import admin
from super_resolution import views as homeViews
urlpatterns = [
url('upload_avatar/',homeViews.upload_avatar), # 上傳頭像
url('test/',homeViews.test), # 測試頁面
]