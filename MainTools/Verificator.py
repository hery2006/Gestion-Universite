__autor__ = 'Le Grand Herimanjato'
"""
=========================================================
Creaton de class manipulation de tous la systeme CRUD
=========================================================
"""
import re,hashlib,difflib,unicodedata,unicodedata,os
from typing import *

class Verificator:
    def __init__(self,Donnee:Dict):
        super().__init__()
        """
            Traitement de chaque verification possible via dict
            le key doit etre la meme que le name des inputs ou autre 
            le Value reste  une donne
        """
        self.Donnee:Dict = Donnee

    def NullVerificator(self):
        ErrorSession:dict = {}
        NullBD:dict = self.Donnee
        ErrorTxt:str = 'Pas de vide pour '
        for key,value in NullBD.items():
            k:bool = self.SpaceNotValidator(value)
            if k:
                ErrorSession[key] = ErrorTxt + self.TakeOnlyTheLastWord(key)
        if len(ErrorSession) !=0:
            return True,ErrorSession
        return False,ErrorSession
    
    def NumberVerificator(self):
        session:dict = {}
        NumberBD:dict = self.Donnee
        for key,Value in NumberBD.items():
            if key == 'int' or key == 'number':
                for k , v in Value.items():
                    b,i = self.NumberType(v)
                    if b:
                        session[k] = i
        if len(session) != 0:
            return True,session
        return False,session

    def EmailVerificator(self) -> str :
        try:
            # take Email in DB
            ErrorSession:dict = {}
            EmailDB:dict = self.Donnee
            EmailKey:list = []
            for key,value in EmailDB:
                if 'email' in self.Normalisation(key):
                    EmailKey.append(key)
            Error_n1:str = 'Adresse Email non valide veillee le verifier . Merci !'
            t:str = EmailDB[EmailKey[0]].lower()
            FirstContraints:bool = True if int(t.find('@')) < 0 else False
            if FirstContraints or t.count('@') != 1:
                ErrorSession[EmailKey[0]] = Error_n1
                return True,ErrorSession 
            # la deuscieme contrainte
            if t.count('.') > 2:
                ErrorSession[EmailKey[0]] = Error_n1
                return True,ErrorSession
            PointPosition:int = t.find('.')
            if t.count('.') > 1:
                t = t[PointPosition + 1:len(t)]
                SecondPointPosition:int = t.find('.')
                if SecondPointPosition <= 3:
                    ErrorSession[EmailKey[0]] = Error_n1
                    return True,ErrorSession
            return False,ErrorSession
        except Exception as e:
            print(f"{e}\n====> il n'y a pas de email dans le donne que vous nous avez donne. \nverifiez l'ecriture ou le dictionnaire en question")

    def PassWordVerificator(self,t:str):
        ErrorSession:dict = {}
        Name:list = []
        for j , k in self.Donnee:
            if k == t:
                Name.append(j) 
        if len(t) < 8:
            ErrorSession[Name[0]] = 'Mot de passe trop court'
            return True,ErrorSession
        Error:str = 'Mot de passe pas assez robuste'
        t = t.lower()
        t = re.sub(r"[a-z\s]","",t)
        print(t)
        if len(t) == 0:
            ErrorSession[Name[0]] = Error
            return True,ErrorSession
        return False,ErrorSession
    
    def ImageCreator(self,request,Name:str,HtmlName:str,UrlsPath:str) -> str :
        if HtmlName in request.FILES:
            fichier = request.FILES[HtmlName]
            lien = os.path.splitext(fichier.name)
            if len(str(lien)) > 0:
                NewName:str = f'{Name}{lien[1]}'
                Emplacement:str = os.path.join(f'{UrlsPath}',NewName)
                TrueLien = f'/{UrlsPath}/{NewName}'

                with open(Emplacement,'wb') as destination:
                    for d in fichier.chunks():
                        destination.write(d)
                return TrueLien
            return ''

    # =======================
    # Les mini outils du class
    # =======================
    
    def SpaceNotValidator(self,f):
        if not isinstance(f,str):
            return False
        l = self.Normalisation(t=f)
        l = re.sub(r'[\s]','',f)
        if len(l) == 0:
            return True
        return False

    def Normalisation(self,t:str)-> str:
        t = t.lower()
        t = unicodedata.normalize('NFKD',t)
        t = re.sub(r'[^a-z0-9\s]','',t)
        return t
    
    def TakeOnlyTheLastWord(self,t:str) -> str:
        try:
            t = re.search(r'[A-Z][a-z]+$',t).group()
            return t
        except Exception as e:
            print(f'{e} ==> il faut au mois avoir une lettre en majuscule dans {t}')

    def NumberType(self,i: str | int | float) -> tuple[bool,str]:
        # traitement pour savoir si c'est vraiment un number ou non
        if isinstance(i,str):
            u = self.Normalisation(i)
            u = re.sub(r'[a-z]','',u)
            if len(u) == 0 and len(i) > 0:
                return True,'Ce formulaire prends juste les nombres'
            if len(u) != len(i):
                return True,'Pas de text juste des nombres'
            if '.' in u or ',' in u:
                I = float(u)
                if I < 0:
                    return True,'Pas de numbre inferieur a 0'
                return False,''
            I = int(u)
            if I < 0:
                return True,'Pas de numbre inferieur a 0'
            return False,''
        if isinstance(i,int):
            if i < 0:
                return True,'Pas de numbre inferieur a 0'
            return False,''   
        if isinstance(i,float):
            if i < 0 :
                return True,'Pas de numbre inferieur a 0'
            return False,''
        
if __name__ == '__main__':
    Verificator()