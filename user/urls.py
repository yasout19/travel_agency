from django.urls import path
from . import views
app_name = 'user'
urlpatterns=[
    path('index/',views.user_home,name='home'),
    path('contact/',views.contact,name='contact'),
    
]