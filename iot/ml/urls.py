from django.urls import path
from ml import views


app_name = 'ml'
urlpatterns = [
    path('', views.ml, name='ml'),
    path('train/', views.train, name='train'),
    path('isSurvive/', views.isSurvive, name='isSurvive'),
]