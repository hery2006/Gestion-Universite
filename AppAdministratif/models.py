from django.db import models
from AppTools.models import FormationsModels
# Create your models here.
class EleveAjout(models.Model):
    Nom = models.CharField()
    Prenom = models.CharField()
    Sexe = models.CharField()
    Dossier = models.BooleanField()
    Parcours = models.ForeignKey(FormationsModels,on_delete=models.CASCADE)
    Image = models.ImageField(upload_to='static/Images/DataImage', default='default.jpg')