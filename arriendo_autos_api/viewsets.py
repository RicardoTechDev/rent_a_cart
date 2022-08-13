from rest_framework.viewsets import ModelViewSet
from arriendo_autos_app.models import Cliente, Empresa, Arriendo 
from .serializer import ClienteSerializer, EmpresaSerializer, ArriendoSerializer 

#clases para definir la estructura CRUD que vamos a utilizar
class ClienteViewSet(ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer



class EmpresaViewSet(ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer



class ArriendoViewSet(ModelViewSet):
    queryset = Arriendo.objects.all()
    serializer_class = ArriendoSerializer    