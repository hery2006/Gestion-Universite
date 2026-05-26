# verification vide str/liste
from typing import *
import re,hashlib
Alphabet:str = 'qwertyuiopasdfghjklzxcvbnm'
def VideVerificator(Variable:str = '',ListeVariable:list = []) -> bool:
    if not isinstance(Variable,str) :
        Variable = str(Variable)
    if not isinstance(ListeVariable,list):
        return False
    if Variable == '' and len(ListeVariable) == 0:
        return False
    # verification liste    
    if len(ListeVariable) != 0:
        ValidItem:List = []
        for i in ListeVariable:
            if str(i) != '':
                ValidItem.append('True')
        if len(ValidItem) > 1:
            return True
        if len(ValidItem) == 0:
            return False
    return True

#  verification des conditionnement valide
class ValidatorClass:
    def __init__(self,Dictionnaire:Dict= {}):
        super().__init__()
        self.Dictionnaire = Dictionnaire

    def MainLaunchFonctions(self,Email:bool = False,Diff_Mdp:bool = False) -> dict:
        self.Answer:Dict = {}
        if Email:
            self.DictTraitor('email',self.EmailVerification)
        if Diff_Mdp:
            self.DictTraitor('mot_de_passe',self.MotDePasseSolidity)
        return self.Answer  
    
    def DictTraitor(self,Research:str,FonctionPropre:callable) -> Dict:
        for i in self.Dictionnaire.keys():
            if isinstance(self.Dictionnaire[i],dict):
                KeyListe:str = ' '.join(str(x) for x in self.Dictionnaire[i].keys())
                if KeyListe.lower().find(Research) >= 0:
                    Point:int = KeyListe.lower().find(Research) + 1 if KeyListe.lower().find(Research) != 0 else KeyListe.lower().find(Research)
                    KeyTake:str = KeyListe[Point:len(Research)]
                    Text:str = self.Dictionnaire[i][KeyTake]
                    self.Answer[i] = FonctionPropre(Text)
            else:
                if i.lower() == Research:
                    self.Answer[i] = FonctionPropre(self.Dictionnaire[i])


    def EmailVerification(self,EmailText:str) -> str :
        Error_n1:str = 'Adresse Email non valide veillee le verifier . Merci !'
        t:str = EmailText.lower()
        
        FirstContraints:bool = True if int(t.find('@')) < 0 else False
        if FirstContraints or t.count('@') != 1:
            return [False , Error_n1]
        
        # la deuscieme contrainte
        if t.count('.') > 2:
                return [False,Error_n1]
        
        PointPosition:int = t.find('.')
        if t.count('.') > 1:
            t = t[PointPosition + 1:len(t)]
            SecondPointPosition:int = t.find('.')
            if SecondPointPosition <= 3:
                return [False,Error_n1]
        
        return [True,EmailText]
    
    def MotDePasseSolidity(self,Mot:str) -> list:
        # verification d'un mot de passe assez puissant
        if len(Mot) < 8:
            return [False,'Mot de passe trop courts']
        
        Error:str = 'Mot de passe pas assez robuste'

        t = Mot.lower()
        t = re.sub(r"[a-z\s]","",t)
        print(t)
        if len(t) == 0:
            return [False,Error]
    
        return [True,self.HMPD(Mot)]
    
    def HMPD(self,mdp:str) ->str:
        Mot_de_passe_Hashed = hashlib.sha224()
        Mot_de_passe_Hashed.update(mdp.encode("utf-8"))
        return str(Mot_de_passe_Hashed.hexdigest())[0:25]