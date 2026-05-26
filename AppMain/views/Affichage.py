from django.shortcuts import render
from AppTools.models import FormationsModels
def AffichePages(request):
    return render(request,'MainCountainers.html')

def LoginPages(request):
    return render(request,'LoginPages.html')

def FormationsPages(request):
    session:dict = {}
    # request.session["F_Filter"]
    DBTAKE = FormationsModels.objects.all() if 'F_Filter' not in request.session else FormationsModels.objects.filter(**request.session["F_Filter"]).all()
    session['Formations'] = [x for x in DBTAKE]
    return render(request,'Formations/Formations.html',session)