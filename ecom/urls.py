from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('rozvoj/', views.rozvoj, name='osobniRozvoj'),
    path('poeziedrama/', views.poezie, name='poeziedrama'),
    path('detimladaz/', views.mladez, name='detimladez'),
    path('naucna/', views.naucna, name='naucna'),
    path('beletrie/', views.beletrie, name='beletrie'),

    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
