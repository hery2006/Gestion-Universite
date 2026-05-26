from django.shortcuts import render,redirect
from AppTools.models import FormationsModels,DiplomesModels
from django.http import JsonResponse
from .Utilitaire import Formations,Re_search_Formation
from django.urls import reverse 
from typing import *
import re
def FormationAjout(request,id:int):
    session:dict = {}
    DiplomeDon = DiplomesModels.objects.all()
    session['Diplome'] = [x for x in DiplomeDon]
    if id == 0 and 'FA_id' in request.session:
        del request.session['FA_id']
    return render(request,"Formations/AjoutFormations.html",session)

def Formations_Save(request):
    if request.method == 'POST':

        # les donnees a prendre
        Nom = request.POST.get('FA_Nom','')
        Categorie = request.POST.get('FA_Categorie','')
        Duree = request.POST.get('FA_Duree','')
        DiplomeNumber = request.POST.get('FA_Diplome','')
        Heure = request.POST.get('FA_RHeure','')
        # liste des nom pour le post
        NameListe:List[str] = ['FA_Nom','FA_Categorie','FA_Duree','FA_Diplome','FA_RHeure']
        # Traitement des donnees
        Fort = Formations(Nom=Nom,Categorie=Categorie,Duree=Duree,DiplomeNumber=DiplomeNumber,Heure=Heure,NameListe=NameListe)
        # vide verification
        Val, Answer  = Fort.VideVerificator()
        if not Val:
            return JsonResponse({'errors':Answer})
        
        # duree verification
        D_Val,D_Answer = Fort.DureeManipulations()
        if not D_Val:
            return JsonResponse({'errors':D_Answer})
        
        VDiplome,V_AnswerDisplome = Fort.DiplomeMainVerificator()
        if not VDiplome:
            return JsonResponse({'errors':V_AnswerDisplome})
        VHeure,V_AnswerHeure  = Fort.HeureMainVerificator()
        if not VHeure:
            return JsonResponse({'errors':V_AnswerHeure})
        
        # traitement des diplomes choices 
        NameValue:List[str] = [x for x in DiplomesModels.objects.all()]
        Value:Dict = {}
        for j in NameValue:
            r = request.POST.get(f'{j.Nom}','')
            if r != '':
                Value[j.Nom] = j.id
        
        if len(Value) != float(V_AnswerDisplome):
            session:dict = {}
            session['FA_Diplome'] = 'il y a une difference entre les diplomes selectionne et ne nombre de diplome'
            return JsonResponse({'errors':session})
        # evite les doublons avec le meme nom 
        if FormationsModels.objects.filter(Nom = Nom).exists():
            session:dict = {}
            session['FA_Nom'] = 'Cette formations existe dejas'
            return JsonResponse({'errors':session})
        
        SaveFormations = FormationsModels.objects.create(Nom=Nom,Categorie=Categorie,Duree=D_Answer,Nombre_Diplome=str(','.join(str(k) for k in Value.keys())),Nombre_Heure=V_AnswerHeure)

        return JsonResponse({'success':True,
                             'redirect_url':f'{reverse('Formations')}',
                             'FormationsNom':Nom})

# fonction entrer
def Id_EnterFormation(request,id):
    request.session['FA_id'] = int(id)
    return redirect(reverse('F_Ajout',kwargs={'id':1}))

def Enter_Formation(request):
    session:dict = {}
    if not request.session.get('FA_id'):
        return JsonResponse({'DB':session})
    
    DiplomeDB = FormationsModels.objects.filter(id=request.session.get('FA_id')).values().first()
    NameListe:List[str] = ['FA_Nom','FA_Categorie','FA_Duree','FA_Diplome','FA_RHeure']
    for j,i in enumerate(NameListe):
        session[str(i)] = DiplomeDB[SupprimationSTRUseless(str(i)) if j not in [3,4] else str(f"Nombre_{SupprimationSTRUseless(str(i))}")]
    
    return JsonResponse ({'DB':session})
    
def SupprimationSTRUseless(t:str) ->str:
    return str(re.search(r'[A-Z][a-z]+$',t).group())

# Fonction recherche
def F_RechercheFonction(request):
    if request.method == "POST":
        Mot:str = request.POST.get('FA_Recherche','')
        t = re.sub(r'[\s]','',Mot)
        if len(t) == 0:
            if "F_Filter" in request.session:
                del request.session['F_Filter']
            return JsonResponse({'success':True,
                                'redirect_url':f"{reverse('Formations')}"})
        Donnee:dict = Re_search_Formation(FormationsModels,Mot).MainTraitementDonne()
        request.session["F_Filter"] = Donnee
        return JsonResponse({'success':True,
                            'redirect_url':f"{reverse('Formations')}"})

def F_DeleteFonction(request,id:int):
    Nom:list = []
    Nom.append(FormationsModels.objects.get(id=id).Nom)
    DB_Formations = FormationsModels.objects.filter(id=id)
    if not DB_Formations.exists():
        return JsonResponse({'error':'Error id'})
    
    DB_Formations.delete()
    return JsonResponse({'success':True,
                        'successUrls':reverse('Formations'),
                        'FormationsNom':Nom[0]})