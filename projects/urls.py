from django.urls import path

from . import views

urlpatterns =[
    path('',views.projects,name='projects'),
    path('individual',views.editpage,name='project_indiv'),
]