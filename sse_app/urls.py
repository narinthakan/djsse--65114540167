from django.urls import path
from . import views, consumers

urlpatterns = [
    path('sse/', consumers.sse_view, name='sse'),
    path('', views.index, name='index'),
    
]
