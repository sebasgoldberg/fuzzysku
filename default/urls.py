from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^dashboard_secao$', views.dashboard_secao, name='dashboard_secao'),
    ]
