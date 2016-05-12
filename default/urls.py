from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^dashboard_secao$', views.dashboard_secao, name='dashboard_secao'),
    url(r'^expfm$', views.expfm, name='expfm'),
    ]
