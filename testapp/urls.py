from django.urls import path
from . import views
app_name = 'testapp'
urlpatterns=[
    path('index/',views.index,name='home'),
    path('about/',views.about,name='about'),
    path('service/',views.service_app,name='service'),
    path('contact/',views.contact,name='contact'),
    path('packages/',views.packages,name='package'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('details_voy/<int:voyage_id>', views.detail_voy, name='details_voy'),
    path('details_categ/<int:id_categorie>', views.detail_categ, name='detail_categ'),
    path('chercher_voy/', views.recherche_voy, name='recherche_voy'),
]
handler404 = 'testapp.views.error_404'