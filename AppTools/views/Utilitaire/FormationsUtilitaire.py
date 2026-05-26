import re,unicodedata
from typing import *
from datetime import datetime

class Formations:
    def __init__(self,Nom,Categorie,Duree,DiplomeNumber,Heure,NameListe:list):
        super().__init__()
        self.Nom = Nom
        self.Categorie = Categorie
        self.Duree = Duree
        self.DiplomeNumber = DiplomeNumber
        self.Heure = Heure
        self.NameListe = NameListe
        self.session:dict = {}

    def VideVerificator(self) :
        # verification Formation vide
        self.DonneeListe:list  = [self.Nom,self.Categorie,self.Duree,self.DiplomeNumber,self.Heure]
        for i,j in enumerate(self.DonneeListe):
            if self.SpaceVerificator(j) == '':
                self.session[self.NameListe[i]] = 'Pas de vide s\'il vous plait!'
        if len(self.session) > 0:
            return False,self.session
        return True,self.session
    
    def DureeManipulations(self)-> int:
        self.DatePossibility:Dict = {
            'ans':1,
            'mois':12,
            'jours':365,
        }
        # possibility
        self.Poss:dict = {
            'ans':['annees','an','annee','ans','anne'],
            'mois':['mois','moi'],
            'jours':['jours','jour']
        }
        # error Traitement
        Valid,Answer = self.DureeError(self.Duree)
        if not Valid:
            return False ,Answer

        Nbr,Date = self.DureeTraitement(Answer)
        KeyListe:list = [x for x in self.DatePossibility.keys()]
        TrueDate:list = []
        for x in KeyListe:
            if Date in self.Poss[str(x)]:
                TrueDate.append(x)
        return True ,float(Nbr/int(self.DatePossibility[TrueDate[0]]))

    def DureeTraitement(self,D) :
        if isinstance(D,str):
            t:list = D.split()
            if len(t) == 2 :
                return float(t[0]),t[-1]
            return float(t[0]),'ans'
        
    def DureeError(self,D):
        if not isinstance(D,str):
            D =str(D)
        t:list = D.split()
        KeyResearch:list = ['annee']
        for j in self.DatePossibility.keys():
            KeyResearch += self.Poss[str(j)]
        if len(t) > 1:

            for k,l in enumerate(t):
                if self.Normalisateur(l) in KeyResearch :
                    if len(re.sub(r"[0-9.]","",t[k - 1])) == 0:
                        return True,str(' '.join(x for x in[t[k - 1],t[k]]))
        if len(t) == 1 and len(re.sub(r"[0-9.]","",t[0])) == 0:
            return True,str(' '.join(x for x in[t[0],'ans']))

        if len(t) == 1 and len(re.sub(r"[0-9.]","",t[0])) != 0:
            if self.Normalisateur(t[0]) in KeyResearch:
                return True,str(' '.join(x for x in [str(t[0])[0:int(len(t[0]) - len(self.Normalisateur(t[0])))],str(t[0])[len(str(t[0])[0:int(len(t[0]) - len(self.Normalisateur(t[0])))]):len(t[0])] ]))
        self.session[self.NameListe[2]] = 'Duree non valide ![mois,jours et annnees]'    
        return False,self.session

    def DiplomeMainVerificator(self):
        MainErrors:str = 'Nombre de diplome doit contenir un nombre '
        # verification si nombre
        t:str = self.DiplomeNumber.lower()
        if re.search(r"[a-z]+",t):
            t =  re.search(r"[a-z]+",t).group()
            if len(t) > 0:
                self.session['FA_Diplome'] = MainErrors
                return False,self.session
        t = re.sub(r"[^0-9]",'',t)
        t = float(t)
        return True,t
    
    def HeureMainVerificator(self):
        MainErrors:str = 'Nombre d\'heure doit contenir un nombre '
        # verification si nombre
        t = self.Heure.lower()
        t =  re.sub(r"[^0-9\s]",'',t)
        if len(t) == 0:
            self.session['FA_Diplome'] = MainErrors
            return False,self.session
        
        t = float(t)
        return True,t

    def SpaceVerificator(self,text:str) -> str:
        t = re.sub(r"[ ]",'',str(text))
        return t
    
    def Normalisateur(self,text:str) -> str:
        t:str = text.lower()
        t = unicodedata.normalize('NFKD',t)
        t = re.sub(r"[1-9 ]",'',t)
        return t

class Re_search_Formation:
    def __init__(self,DBFormat,TextDonne):
        super().__init__()
        self.Data:Dict = DBFormat
        self.Text:str = TextDonne

    def TakeNameDB(self) -> List:
        t:dict = self.Data.objects.all().values().first()
        r:list = [str(i) for i in t.keys()]
        return r

    def MainTraitementDonne(self) -> Dict:
        Answer:dict = {}
        MainTextUsed:str = self.Normalisation(self.Text)
        DBcolName:list = self.TakeNameDB()
        DictDB:list = self.Data.objects.all().values().all()

        DBLength:int = len(DictDB)
        i:int = 0
        Centralisation:dict = {}
        while i < DBLength:
            Traitement:dict = DictDB[i]
            for j in DBcolName:
                if j not in Centralisation:
                    Centralisation[j] = []
                Centralisation[j].append(Traitement[j])
            i+= 1
        Re_search_list = self.ListTODict(MainTextUsed.split())
        l:int = 1
        while l < len(DBcolName):
            Name:str = DBcolName[l]
            DBAllByName:list = Centralisation[Name]
            for b in DBAllByName:
                k,o = self.MultipleMotTrue(str(b),Re_search_list)
                if k:
                    Answer[Name] = o
            l+= 1
        return Answer

    def ListTODict(self,ListeD:list) ->dict:
        Session:dict = {}
        for j,n in enumerate(ListeD):
            Val,k = self.TreatementFloat(n)
            if Val:
                print(k)
                Session[k] = j    
            if not Val:
                Session[n] = j
        return Session
    
    def MultipleMotTrue(self,Mot:str,MotDict:dict):
        y:list = Mot.lower().split() if ',' not in Mot else Mot.lower().split(',')
        valList:list = []
        for m in y:
            if m in MotDict:
                valList.append(m)
        if len(valList) > 0:
            return True,Mot
        return False,''


    def Normalisation(self,text:str) -> str:
        t = text.lower()
        t = unicodedata.normalize('NFKD',t)
        t = ''.join(c for c in t if not unicodedata.combining(c))
        t = re.sub(r'[^a-z0-9\s.]','',t)
        return t
    
    def TreatementFloat(self,Number:str) -> bool:
        Nbr:list = [x for x in Number]
        if len(Nbr) == 1:
            return True ,str(float(Number))
        if len(Nbr) > 1 and len(re.sub(r"[^0-9.]",'',Number)) == len(Number):
            return True,str(float(Number))

        return False,Number
    
