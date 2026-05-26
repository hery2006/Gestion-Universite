from django.urls import path
from .views import *
from typing import *
import os,re,difflib,shutil,random,hashlib

# creation path unique
def Cryptage(Text:str ) ->str:
    Htext =hashlib.sha224()
    Htext.update(Text.encode('utf-8'))
    return Htext.hexdigest()
def CreateUniquePath(Text:str) -> str:
    Alphabet:str = 'qwertyuiopasdfghjklzxcvbnm'
    LienCommun:str = '0/path-'

    # normalisation
    Text = Text.lower()
    Lien:List = []
    for i in Text:
        if str(i) in Alphabet:
            Lien.append(str(Alphabet.find(i)))

    return str(LienCommun + str(Cryptage(str(''.join(x for x in Lien))))[0:25])

urlpatterns=[
    path('',AffichePages,name='HomePages'),
    path(f'{CreateUniquePath('Login')}',LoginPages,name='PassLogin'),
    path(f'{CreateUniquePath('Formations')}',FormationsPages,name='Formations')
]

