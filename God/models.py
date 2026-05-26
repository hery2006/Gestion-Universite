from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class GodRegisterTable(AbstractUser):
    Nom = models.CharField(max_length=150)
    Prenom = models.CharField(max_length=150)
    Mot_de_Passe = models.CharField()
    email = models.EmailField(unique=True)
    Image = models.ImageField('static/Images/DataImage')
    Sexe = models.CharField()