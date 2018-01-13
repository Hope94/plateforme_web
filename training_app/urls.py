from django.urls import path,include
from training_app import views


app_name='training_app'
urlpatterns=[
    path('index/', views.HomePage.as_view(), name='index'),
    path('thanks/', views.ThanksPage.as_view(), name='thanks'),
    path('model', views.ModelGenerationView.as_view(), name='model'),

]