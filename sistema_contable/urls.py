from django.urls import path
from . import views

urlpatterns=[
    path('', views.inicio, name='index'),

    path('registroTransaccion', views.registroTransaccion, name='registroTransaccion'),
    path('catalogoCuentas', views.catalogoCuentas, name='catalogoCuentas'),
    path('manoObra', views.manoObra, name='manoObra'),
    path('costos', views.costos, name='costos'),
    path('balanzaComprobacion', views.balanzaComprobacion, name='balanzaComprobacion'),
    path('hojaTrabajo', views.hojaTrabajo, name='hojaTrabajo'),
    path('cierraContable', views.cierraContable, name='cierraContable'),

]