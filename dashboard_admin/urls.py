from django.urls import path
from . import views
from django.urls import reverse_lazy
app_name = 'dash_admin'
urlpatterns=[
    path('home/',views.index,name='home'),
    path('profil/',views.UserEditView.as_view(),name='profil'),
    path('password/',views.PasswordChangeView.as_view(template_name = 'nice-html/pages/password_admin.html',success_url = reverse_lazy('dash_admin:password_succes')),name='password'),
    path('password_succes',views.password_succes,name='password_succes'),
    path('users/',views.showusers,name='users'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('categories/',views.categories,name='categories'),
    path('delete_cat/<int:cat_id>/', views.delete_cat, name='delete_cat'),
    path('voyages/',views.voyages,name='voyages'),
    path('reservation/',views.reservation,name='reservation'),
    path('delete_voyage/<int:cat_id>/', views.delete_voyage, name='delete_voyage'),
    path('edit_cat/<int:cat_id>/', views.edit_cat, name='edit_cat'),
    path('edit_voy/<int:voy_id>/', views.edit_voy, name='edit_voy'),
    path('hotels/',views.hotels,name='hotels'),
    path('delete_hot/<int:hot_id>/', views.delete_hot, name='delete_hot'),
    path('edit_hot/<int:hot_id>/', views.edit_hot, name='edit_hot'),
    path('vols/',views.vols,name='vols'),
    path('delete_vol/<int:vol_id>/', views.delete_vol, name='delete_vol'),
    path('edit_vol/<int:vol_id>/', views.edit_vol, name='edit_vol'),
]