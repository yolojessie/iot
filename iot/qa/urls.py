from django.urls import path
from qa import views, webPush, qaCronJob


app_name = 'qa'
urlpatterns = [
    path('', views.qa, name='qa'),
    path('answer/', views.answer, name='answer'),
    path('cloud/', views.cloud, name='cloud'),
    path('subscription/', webPush.subscription, name='subscription'),
    path('notify/', qaCronJob.notify, name='notify'),
    path('saveKeyword/', views.saveKeyword, name='saveKeyword'),
]