from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('download/<path:file_path>/', views.download_view, name='download'),
]