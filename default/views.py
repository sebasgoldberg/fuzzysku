from django.shortcuts import render

from .models import *


def dashboard_secao(request):
    secao = Secao.objects.get(cod_secao=request.GET['cod_secao'])
    return render(request, 'default/dashboard_secao.html', {'secao': secao})

