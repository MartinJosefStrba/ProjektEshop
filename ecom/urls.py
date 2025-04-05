from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('rozvoj/', views.rozvoj, name='osobniRozvoj'),
    path('poeziedrama/', views.poezie, name='poeziedrama'),
    path('detimladaz/', views.mladez, name='detimladez'),
    path('naucna/', views.naucna, name='naucna'),
    path('beletrie/', views.beletrie, name='beletrie'),

    path('product/<int:pk>', views.product, name='product'),

    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_info/', views.update_info, name='update_info'),
]
