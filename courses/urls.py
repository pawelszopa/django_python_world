from django.urls import path

from courses import views

app_name = 'courses'

urlpatterns = [
    path('create', views.CreateCourse.as_view(), name='create-course'),
    path('home', views.CreateCourse.as_view(), name='home')


]