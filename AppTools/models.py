from django.db import models

# Create your models here.
class  DiplomesModels(models.Model):
    Nom = models.CharField(max_length=80)
    Duree = models.IntegerField(null=False)
    Creation = models.DateTimeField(auto_now_add=True)

class FormationsModels(models.Model):
    Nom = models.CharField(max_length=80) 
    Categorie = models.CharField()
    Duree = models.FloatField()
    Nombre_Diplome = models.CharField()
    Nombre_Heure = models.FloatField()
    Date_Creation = models.DateTimeField(auto_now_add=True)