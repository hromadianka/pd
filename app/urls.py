from django.contrib import admin
from django.urls import path, include
from pd import settings
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('publications', views.publications, name='publications'),
    path('publications/<str:pk>', views.publication, name='publication'),
    path('signin', views.signin, name='signin'),
    path('publish', views.publish, name='publish'),
    path('materials', views.materials, name='materials'),
    path('game', views.game, name='game'),
    # path('branches', views.branches, name='branches'),
]