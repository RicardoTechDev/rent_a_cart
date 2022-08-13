from django.db import models

class Cliente(models.Model):
    rut =  models.CharField(max_length=10)
    name = models.CharField(max_length=255) 



class Empresa(models.Model):
    name = models.CharField(max_length=255) 



class Arriendo(models.Model):
    cliente = models.ForeignKey(Cliente, related_name="arriendo", on_delete = models.CASCADE)
    empresa = models.ForeignKey(Empresa, related_name="arriendo", on_delete = models.CASCADE) 
    costo_diario = models.IntegerField()
    dias = models.IntegerField()

