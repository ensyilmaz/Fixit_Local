from django.urls import path
from . import views

urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('raporlar/', views.raporlar, name='raporlar'),
    path('raporlarim/', views.raporlarim, name='raporlarim'),
    path('uye-ol/', views.uye_ol, name='uye_ol'),
    path('giris/', views.giris_yap, name='giris'),
    path('cikis/', views.cikis_yap, name='cikis'),
    path('anasayfa/', views.anasayfa, name='anasayfa'),
]
