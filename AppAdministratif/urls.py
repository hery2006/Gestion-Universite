from django.urls import path
from .views import *
import hashlib
from typing import *
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
urlpatterns = [
    path(f'{CreateUniquePath('EMainPages')}',EleveAffiche,name='E_MainPages'),
    path(f'{CreateUniquePath('EModification')}',Modification,name='EModification'),
    path(f'{CreateUniquePath('EAjout')}/<int:id>',AjoutEleve,name='EAjout'),
    path(f'{CreateUniquePath('EASave')}',AjoutSaves,name='EAjoutSave'),
    path(f'{CreateUniquePath('ESeePass')}/<int:id>',IdPassEnter,name='ESeePass'),
    path(f'{CreateUniquePath('EAfficheEleve')}',SeeAjout,name='EAfficheEleve'),
    path(f'{CreateUniquePath('EleveDelete')}/<int:id>',DeleteEleve,name='Edelete')
]
