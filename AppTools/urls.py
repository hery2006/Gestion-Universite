from django.urls import path
from .views import *
import hashlib
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
    path(f'{CreateUniquePath('FAjout')}/<int:id>',FormationAjout,name='F_Ajout'),
    path(f'{CreateUniquePath('FSave')}',Formations_Save,name='F_Save'),
    path(f'{CreateUniquePath('FEnter')}/<int:id>',Id_EnterFormation,name='F_Enter'),
    path(f'{CreateUniquePath('FLoad')}',Enter_Formation,name='F_Load'),
    path(f'{CreateUniquePath('Frecherche')}',F_RechercheFonction,name='F_recherche'),
    path(f'{CreateUniquePath('FDelete')}/<int:id>',F_DeleteFonction,name='F_Delete')
]
