from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('doktor_giris/', views.doktor_giris, name='doktor_giris'),
    path('hasta_giris/', views.hasta_giris, name='hasta_giris'),
    path('yonetici_giris/', views.yonetici_giris, name='yonetici_giris'),
    path('hasta_ekle/', views.hasta_ekle, name='hasta_ekle'),
    path('hasta_listele/', views.hasta_listele, name='hasta_listele'),
    path('doktor_ekle/', views.doktor_ekle, name='doktor_ekle'),
    path('doktor_listele/', views.doktor_listele, name='doktor_listele'),
    path('doktor_sil/<str:id>', views.doktor_sil, name='doktor_sil'),
    path('hasta_sil/<str:id>', views.hasta_sil, name='hasta_sil'),
    path('randevu_al/', views.randevu_al, name='randevu_al'),
    path('randevu_ara/', views.randevu_ara, name='randevu_ara'),
    path('randevu_sec/', views.randevu_sec, name='randevu_sec'),
    path('randevu_listele/', views.randevu_listele, name='randevu_listele'),
    path('randevu_sil/', views.randevu_sil, name='randevu_sil'),
    path('doktor_hasta_listele/', views.doktor_hasta_listele, name='doktor_hasta_listele'),
    path('hasta_guncelle/', views.hasta_guncelle, name='hasta_guncelle'),
    path('doktor_duzenle/<int:id>/', views.doktor_duzenle, name='doktor_duzenle'),
    path('hasta_duzenle/<int:id>/', views.hasta_duzenle, name='hasta_duzenle'),
    path('randevu_duzenle/<int:randevu_id>/', views.randevu_duzenle, name='randevu_duzenle'),
    path('rapor_ekle/<int:hasta_id>/', views.rapor_ekle, name='rapor_ekle'),
    path('rapor_goruntule/', views.rapor_goruntule, name='rapor_goruntule'),
    path('rapor_sil/<int:rapor_id>/', views.rapor_sil, name='rapor_sil'),
    path('rapor_ekle/<int:hasta_id>/<int:rapor_id>/', views.rapor_sil, name='rapor_sil'),
    path('raporlar/<int:hasta_id>/', views.raporlar, name='raporlar'),
    path('rapor_sil/<int:rapor_id>/', views.rapor_sil, name='rapor_sil'),




]
