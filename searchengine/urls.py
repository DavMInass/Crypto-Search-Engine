from django.urls import path 
from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('search', views.Search.as_view(), name='search'),
    path('completequery', views.complete, name='complete')
]