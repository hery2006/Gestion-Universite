from django.shortcuts import render,redirect
from django.http import JsonResponse
from typing import *
from .Utilitaire import VideVerificator,ValidatorClass
from God.models import GodRegisterTable
from django.db.models import Q
from django.contrib.auth import login

# Enregistrement de User principales main site
def EnregistrementGodUser(request):
    if request.method == "POST":
        Nom = request.POST.get('Nom_Input','')
        Prenom = request.POST.get('Prenom_Input','')
        Email = request.POST.get("Email_Input",'')
        Mdp = request.POST.get("Mot_de_Passe_Input",'')
        Mdp_Confirmations = request.POST.get("Confirmation_Input",'')
        Sexe:List[str] = [str(request.POST.get('Homme','')),str(request.POST.get("Femme",'')),str(request.POST.get("Autre",''))]

        # verification de que tous les variable la sont pas vide
        NameListe:list = ['Nom_Input','Prenom_Input','Sexe','Email_Input','Mot_de_Passe_Input','Confirmation_Input']
        ListeItems:list = [Nom,Prenom,Sexe,Email,Mdp,Mdp_Confirmations]
        DictVideValidator:dict = {}
        for m,i in enumerate(ListeItems):
            if not isinstance(i,str) and not isinstance(i,list):
                i = str(i)
            if isinstance(i,str):
                DictVideValidator[NameListe[m]] = VideVerificator(i)   
            if isinstance(i,list):
                DictVideValidator[NameListe[m]] = VideVerificator('',ListeVariable = i)
        session:dict = {}
        for items in DictVideValidator.keys():
            if DictVideValidator[items] == False:
                ErrorMessages:str = f' Pas de vide'
                session[f"{items}"] = ErrorMessages
            if items == 'Confirmation_Input' and len(session) != 0:
                print('session ==>',session)
                return JsonResponse({"errors": session})
            
        # verification de sexe :
        RealSexe:List[str] = []
        for i in Sexe:
            if i != '':
                RealSexe.append(i)

        if len(RealSexe) > 1:
            ErrorMessages:str = f"Choisis juste une seule sexe"
            session["Sexe"] = ErrorMessages
            return JsonResponse({"errors": session})
        
        # verification 
        Dictionnaire:dict = {
            'Email_Input':{
                'Email':f'{Email}'
            },
            'Mot_de_Passe_Input':{
                'Mot_de_Passe':f'{Mdp}',
            }
        }
        EmailValid:dict = ValidatorClass(Dictionnaire).MainLaunchFonctions(True,False)
        if not EmailValid['Email_Input'][0]:
            ErrorMessages:str = f'Email non valide veuiller verifier s\'il vous plait'
            session["Email_Input"] = ErrorMessages
            return JsonResponse({"errors": session})
        
        # Verification solidite du mot de passe
        MdpValid:dict = ValidatorClass(Dictionnaire).MainLaunchFonctions(False,True)
        if not MdpValid['Mot_de_Passe_Input'][0]:
            ErrorMessages:str = MdpValid['Mot_de_Passe_Input'][1]
            session["Mot_de_Passe_Input"] = ErrorMessages
            return JsonResponse({"errors": session})
        
        #  Verification de la validite du mot de passe
        if Mdp != Mdp_Confirmations:
            session['Confirmation_Input'] = 'Il y une difference'
            session['Mot_de_Passe_Input'] = 'Il y une difference'
            print(session)
            return JsonResponse({'errors':session})
        
        # Verification des erreurs de doublons
        if GodRegisterTable.objects.filter(Q(Nom=Nom) & Q(Prenom=Prenom)).exists():
            ErrorMessages:str = f'Utilisateur existant'
            session["Nom_Input"] = ErrorMessages
            session['Prenom_Input'] = ErrorMessages
            return JsonResponse({"errors": session})
        if GodRegisterTable.objects.filter(email=Email).exists():
            ErrorMessages:str = f'Email dejas utiliser !'
            session["Email_Input"] = ErrorMessages
            return JsonResponse({"errors": session})
        
        # Enregistrement
        GodUser = GodRegisterTable.objects.create_user(password=MdpValid['Mot_de_Passe_Input'][1],username=Nom,first_name=Prenom,Nom=Nom,Prenom=Prenom,Mot_de_Passe=MdpValid['Mot_de_Passe_Input'][1],email=Email,Image = '/',Sexe=RealSexe[0]) 
        login(request,GodUser)
        return JsonResponse({'success':True,
                             "redirect_url":"/"})

            
