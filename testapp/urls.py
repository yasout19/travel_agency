from django.urls import path
from . import views
app_name = 'testapp'
urlpatterns=[
    path('index/',views.index,name='home'),
    path('about/',views.about,name='about'),
    path('service/',views.services,name='service'),
    path('distination/',views.distination,name='distination'),
    path('contact/',views.contact,name='contact'),
    path('packages/',views.packages,name='package'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),
]
handler404 = 'testapp.views.error_404'