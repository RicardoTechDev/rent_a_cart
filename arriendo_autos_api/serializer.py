from rest_framework.serializers import ModelSerializer
from arriendo_autos_app.models import Cliente, Empresa, Arriendo 

class ClienteSerializer(ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'



class EmpresaSerializer(ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'



class ArriendoSerializer(ModelSerializer):
    class Meta:
        model = Arriendo
        fields = '__all__'
