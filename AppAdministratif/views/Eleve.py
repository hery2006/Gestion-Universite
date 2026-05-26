from django.shortcuts import render,redirect
from AppTools.models import FormationsModels
from MainTools.Verificator import Verificator
from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse
from AppAdministratif.models import EleveAjout
from typing import *
from .EleveTools import Recherche

def EleveAffiche(request):
    return render(request,'Eleve/Eleve.html')


"""
===========================
    cote modification pages
===========================
"""
def Modification(request):
    session:dict = {}
    EleveDB  = EleveAjout.objects.all()
    session['EleveDB'] = EleveDB
    session['EleveCount'] = EleveDB.count()
    print(Recherche())
    return render(request,'Eleve/ModificationMainPages.html',session)


"""
========================================================================
    Cote AJOUT Eleves 
========================================================================
"""
from .EleveTools import *
def AjoutEleve(request,id:int):
    Session:dict = {}
    F_DB = FormationsModels.objects.all()
    Session['FormationsBd'] = F_DB
    if id == 0 and 'EleveID' in request.session and 'EleveUpload' in request.session:
        del request.session['EleveUpload']
        del request.session['EleveID']
    return render(request,'Eleve/EleveAjout.html',Session)

def AjoutSaves(request):
    if request.method == 'POST':
        Nom = request.POST.get('EA_Nom','')
        Prenom = request.POST.get('EA_Prenom','')
        Sexe = request.POST.get('EA_Sexe','')
        Dossier = request.POST.get('EA_Dossier','')
        Parcours = request.POST.get('EA_Parcours','')

        DictVerificator:dict = {
            'EA_Nom':Nom,
            'EA_Prenom':Prenom,
            'EA_Sexe':Sexe,
            'EA_Dossier':Dossier,
            'EA_Parcours':Parcours,
        }
        V_Main = Verificator(DictVerificator)
        NullBolean,Errorsession = V_Main.NullVerificator()
        Image:str = V_Main.ImageCreator(request=request,Name=Prenom,HtmlName='EA_Photo',UrlsPath='static/Images/DataImage')
        F_ForgeinKey = FormationsModels.objects.get(id=int(Parcours))
        
        if NullBolean:
            print(Errorsession)
            return JsonResponse({'errors':Errorsession})
        DBool,Value = Doublons(Prenom,Nom)

        if 'EleveUpload' in request.session:
            EleveChoiced = EleveAjout.objects.get(id = int(request.session['EleveID']))
            if EleveChoiced.Nom == Nom and EleveChoiced.Prenom == Prenom and EleveChoiced.Sexe == Sexe and EleveChoiced.Dossier == BooleanTransformation(Dossier) and EleveChoiced.Parcours.id == F_ForgeinKey.id and Image == None:
                if DBool:
                    return JsonResponse(Value)
            if EleveChoiced.Nom != Nom or EleveChoiced.Prenom != Prenom:
                if DBool:
                    return JsonResponse(Value)
                
            EleveChoiced.Nom = Nom
            EleveChoiced.Prenom = Prenom
            EleveChoiced.Sexe = Sexe
            EleveChoiced.Dossier = BooleanTransformation(Dossier)
            EleveChoiced.Parcours = F_ForgeinKey
            EleveChoiced.Image = Image 
            EleveChoiced.save()
            return JsonResponse({'success':True,
                                'redirect_url':f'{reverse('EModification')}'})

        if DBool:
            return JsonResponse(Value)
        
        EleveAjout.objects.create(Nom=Nom,Prenom=Prenom,Sexe=Sexe,Dossier=BooleanTransformation(Dossier),Parcours=F_ForgeinKey,Image=Image)
        return JsonResponse({'success':True,
                             'redirect_url':f'{reverse('EModification')}'})

def Doublons(Prenom:str,Nom:str) -> tuple[bool,dict]:
    ErrorExist:dict = {}
    if EleveAjout.objects.filter(**{'Prenom':Prenom}).exists():
        ErrorExist['EA_Prenom'] = 'le prenom existe dejas . change le!'
        if EleveAjout.objects.filter(Nom = Nom).exists():
            ErrorExist['EA_Nom'] = 'le nom existe dejas . change le!'
            return True,{'errors':ErrorExist}
        return True,{'errors':ErrorExist}
    return False,{'errors':ErrorExist}
"""
transformation de false js en False python
"""
def BooleanTransformation(B:str | bool) -> bool | str:
    if not isinstance(B,str):
        B = str(B)
    ListB:List[str] = [str(j) if k != 0 else j.upper() for k,j in enumerate(B)]
    return bool(''.join(i for i in ListB))
    


def IdPassEnter(request,id:int):
    if 'EleveID' not in request.session or 'EleveUpload' not in request.session :
        request.session['EleveUpload'] = True
        request.session['EleveID'] = id
    request.session['EleveID'] = id
    request.session['EleveUpload'] = True
    return redirect(reverse('EAjout',kwargs={'id':1}))

def SeeAjout(request) :
    DB_checkeble = EleveAjout.objects.get(id = int(request.session['EleveID']))
    DBELEVES:dict = {}
    if request.session['EleveID']:
        DBELEVES['EA_Nom'] = DB_checkeble.Nom
        DBELEVES['EA_Prenom'] = DB_checkeble.Prenom
        DBELEVES['EA_Sexe'] = DB_checkeble.Sexe
        DBELEVES['EA_Dossier'] = DB_checkeble.Dossier
        DBELEVES['EA_Parcours'] = DB_checkeble.Parcours.id
        DBELEVES['EA_Photo'] = str(DB_checkeble.Image)

    return JsonResponse({'EleveDB':DBELEVES}) 

def DeleteEleve(request,id:int) :
    if EleveAjout.objects.filter(id=id).exists():
        DBEleve = EleveAjout.objects.get(id=id)
        DBEleve.delete()
        return redirect(reverse('EModification'))
    return ''

def RechercheFonction(request):
    return JsonResponse({'success':True,
                         'redirect_url':reverse('EModification')})