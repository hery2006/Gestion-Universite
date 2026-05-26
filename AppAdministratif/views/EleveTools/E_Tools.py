from AppAdministratif.models import EleveAjout
import re,os,difflib,hashlib,shutil
import unicodedata
from typing import *
from django.utils import timezone
from django.db.models import Q

class Recherche:
    def __init__(self,Phrase:str = 'je veux pas prendre le Prenom herimanjato avec un sexe homme',DataBase = EleveAjout):
        super().__init__()
        self.Phrase = self.Normalisation(Phrase)
        self.Data = DataBase
        self.TakeName:dict = {}

        self.DatabaseName:List[str] = self.TakeNameFormDataBase()
        self.NegatifForm = ['non','pas']
        for D in self.DatabaseName:
            self.TakeName[D] = D.lower()
        self.MainStructure()

    def MainStructure(self) -> Dict[str,str]:
        Answer:dict = {}
        t = self.Phrase
        self.Name,self.tPosition = self.TreatementList()
        for k in self.Name:
            Pre_answer = self.AnswerTreatment(k)
            Answer[[f for f in Pre_answer.keys()][0]] = [f for f in Pre_answer.values()][0]
        print(Answer)
        return 
    def AnswerTreatment(self,Name:str) -> dict:
        Data:dict = self.tPosition[Name]
        t = self.Phrase
        Answer:dict = {}
        for j,k in Data.items():
            Sentence:str = t[int(k):int(j)]
            SentenceTr:dict = self.SentenceTreatement(Sentence,Name)
            if len(SentenceTr) > 0:
                for l,y in SentenceTr.items():
                    Answer[l] = y
        return Answer
    
    def SentenceTreatement(self,txt:str,name) -> dict:
        U:dict = {}
        name1 = [ str(x) for x in name]
        name1[0] = name1[0].upper()
        Name = ''.join(n for n in name1)
        NAME = Name + '__iexact'
        ArrTxt:list = txt.split()
        for t in ArrTxt:
            rec:dict = {NAME:t}
            if self.Data.objects.filter(Q(**rec)).exists():
                obj = self.Data.objects.filter(Q(**rec)).first()
                U[Name] = getattr(obj,Name)

        return U

    
    def TreatementList (self) -> tuple[list,dict]:
        t = self.Phrase
        FindKeys:Dict[str:str] = {}
        id_phrase:int = 0
        for j in self.DatabaseName:
            VldName = t.find(j.lower())
            if VldName > 0 and t[VldName - 1:VldName] == ' ':
                FindKeys[str(VldName)] = j.lower()
                id_phrase += 1
        
        NameFind:dict = {}
        ArrKeys:list = self.RearragedList([int(x) for x in FindKeys.keys()])
        for k,v in enumerate(ArrKeys):
            NameFind[str(k)] = {}
            NameFind[str(k)][str(v)] = FindKeys[str(v)]
        SeparatedSentence:dict = {}
        Name:list = []
        PossibilitySentence:int = int(len(NameFind) + len(NameFind))
        ChangeName:int = int(PossibilitySentence / int(len(NameFind)))
        Name_id = 0
        for j in range(len(NameFind)):
            nom:str = [str(j) for j in NameFind[str(j)].values()][0]
            Name.append(nom)

        lastid:int = len(t)
        Takeable:List[int] = self.AlgorithmTest(len(NameFind))
        for i in range(PossibilitySentence):
            firstSentence:int = [int(o) for o in NameFind[str(Takeable[i])].keys()][0]
            if i == PossibilitySentence - 1:
                firstSentence = 0
            if int(i) == int(ChangeName):
                Name_id += 1
                lastid = [int(o) for o in NameFind[f'{Takeable[i] - 1}'].keys()][0]
                # print(lastid)
                firstSentence:int = [int(o) for o in NameFind[str(Takeable[i])].keys()][0]
                ChangeName += 2
            SeparatedSentence.setdefault(Name[Name_id],{})

            SeparatedSentence[str(Name[Name_id])][str(lastid)] = firstSentence
            lastid = firstSentence
            
        return Name,SeparatedSentence

    def TakeNameFormDataBase(self):
        return [field.name for field in self.Data._meta.fields]
    
    def Normalisation(self,txt:str) -> str :
        t = txt.lower()
        t = unicodedata.normalize('NFKD',t)
        t = re.sub(r'[^a-z0-9\s]','',t)
        return t
    
    def AlgorithmTest(self,k:int) -> list:
        Bouclage:int = k + k
        Addable:int = 0
        resultat:list = []
        while len(resultat) < Bouclage:
            resultat.append(Addable)
            if resultat.count(Addable) > 1 and Addable != 0 and int(Addable + 1) != k:
                Addable += 1
            if Addable == 0 and k != 1:
                Addable += 1
        return resultat
    
    def RearragedList(self,l:list) -> list :
        k = l.copy()
        Answer:list = []
        Val:list = []
        p:list = [int(y) for y in l]
        a:int = 0
        while len(Answer) < len(l):
            Val.clear()
            if a > len(l):
                a = 0
                print(a)
            for x in k:
                if p[a] > int(x):
                    Val.append('True')
            if len(Val) == int(len(k) - 1):
                k.remove(p[a])
                Answer.append(p[a])
                a = -1
            a += 1
        return Answer

