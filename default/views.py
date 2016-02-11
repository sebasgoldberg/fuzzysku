from django.shortcuts import render

import json

from .models import *

def get_dashboard_config():

    es = Elasticsearch()

    res = es.get(index=".kibana", doc_type='dashboard', id='Familias-SKUs-familiasskus')

    panelsJSON = json.loads(res['_source']['panelsJSON'])

    panels = []
    for panel in panelsJSON:
        attrs = []
        for key in panel:
            attrs.append(u'%s:%s' % (key,panel[key]))
        panels.append(u'(%s)' % u','.join(attrs))


    panels = u'(%s)' % u','.join(panels)
    return {'panels': panels}

def dashboard_secao(request):
    secao = Secao.objects.get(cod_secao=request.GET['cod_secao'])
    context = get_dashboard_config()
    context['secao'] = secao
    return render(request, 'default/dashboard_secao.html', context)

def dashboard(request):

    return render(request, 'default/dashboard.html', get_dashboard_config() )
