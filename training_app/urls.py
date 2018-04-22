from django.urls import path,include
from training_app import views


app_name='training_app'
urlpatterns=[
    path('index/', views.HomePage.as_view(), name='index'),
    path('drebin/',views.DrebinTrainingView.as_view(),name='drebin'),
    path('apks/', views.ApkListView.as_view (), name='apks'),
    path ('apks/<int:pk>/', views.ApkDetailView.as_view (), name='detail'),
    path('model', views.ModelGenerationView.as_view(), name='model'),
    path('download/',views.DownloadView.as_view(),name='download'),
    path('download/file', views.DownloadCSV.as_view(), name='download_csv')


]