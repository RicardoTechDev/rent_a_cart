from django.urls import path, include     
from .import views
from rest_framework.routers import SimpleRouter
from .viewsets import ClienteViewSet, EmpresaViewSet, ArriendoViewSet


route = SimpleRouter()
route.register('cliente', ClienteViewSet)
route.register('empresa', EmpresaViewSet)
route.register('arriendo', ArriendoViewSet)

urlpatterns = route.urls