from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name=
  'home'),
  path('about/', views.about, name='about'),
  path('gear/', views.gear_index, name='gear_index'),
  path('gear/<int:gear_id>/', views.gear_detail, name='gear_detail')
]