from django.contrib import admin
import re
from .models import *
# Register your models here.

class Admin_GodRegisterTable(admin.ModelAdmin):
    list_display = ('Nom','Prenom','Mot_de_Passe','email','Image',"Sexe")


admin.site.register(GodRegisterTable,Admin_GodRegisterTable)