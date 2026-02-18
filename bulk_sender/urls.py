from django.urls import path
from . import views


app_name = 'bulk_sender'
urlpatterns = [
    path('send-email/', views.index, name='index'),
]