from django.urls import path, include     
from .import views


urlpatterns = [
    path('', views.index, name='home'),	
    path('clients', views.clients, name='clients'),
    path('companies', views.companies, name='companies'),
    path('rents', views.rents, name='rents'),
    path('funtionsResult/<int:idFuntion>', views.funtionsResult, name='funtionsResult'),
    
]