from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import HastaForm
from django.db import connection
from .forms import DoktorForm
from .forms import HastaGirisForm
from .forms import RandevuDuzenleForm

def home(request):
    return render(request, 'home.html')

def doktor_giris(request):
    if request.method == 'POST':
        doktor_id = request.POST.get('DoktorID')
        ad = request.POST.get('Ad')
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM doktorlar
                WHERE DoktorID = %s AND Ad = %s
            """, [doktor_id, ad])
            doktor = cursor.fetchone()
        if doktor is not None:
            request.session['doktor_id'] = doktor_id
            return redirect('doktor_hasta_listele')
        else:
            return render(request, 'doktor_giris.html', {'error': 'Doktor ID veya Ad hatalı.'})
    else:
        return render(request, 'doktor_giris.html')


def hasta_giris(request):
    if request.method == 'POST':
        form = HastaGirisForm(request.POST)
        if form.is_valid():
            HastaID = form.cleaned_data['HastaID']
            Ad = form.cleaned_data['Ad']
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM hastalar WHERE HastaID = %s AND Ad = %s", [HastaID, Ad])
                hasta = cursor.fetchone()
            if hasta is not None:
                request.session['hasta_id'] = HastaID  # Hasta ID'sini oturuma ekleriz
                return redirect('randevu_al')
            else:
                return render(request, 'hasta_giris.html', {'form': form, 'error': 'Geçersiz bilgi'})
    else:
        form = HastaGirisForm()
    return render(request, 'hasta_giris.html', {'form': form})

def yonetici_giris(request):
    return render(request, 'yonetici_giris.html')

def hasta_ekle(request):
    hata = None
    basarili = False  # Başarı durumunu takip etmek için bir değişken ekleyin
    if request.method == 'POST':
        form = HastaForm(request.POST)
        if form.is_valid():
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO hastalar (HastaID, Ad, Soyad, DogumTarihi, Cinsiyet, TelefonNumarasi, Adres)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, [form.cleaned_data['HastaID'], form.cleaned_data['Ad'], form.cleaned_data['Soyad'], form.cleaned_data['DogumTarihi'], form.cleaned_data['Cinsiyet'], form.cleaned_data['TelefonNumarasi'], form.cleaned_data['Adres']])
                basarili = True  # İşlem başarılı olduğunda 'basarili' değişkenini True olarak ayarlayın
            except Exception as e:
                print("An error occurred: ", e)
                if 'Violation of PRIMARY KEY constraint' in str(e):
                    hata = "Bu ID zaten var"
                else:
                    hata = str(e)
    else:
        form = HastaForm()
    return render(request, 'hasta_ekle.html', {'form': form, 'hata': hata, 'basarili': basarili})  # 'basarili' değişkenini şablona ekleyin

def hasta_sil(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM hastalar WHERE HastaID = %s", [id])
    return redirect('hasta_listele')


 
from django.db import connection

from django.contrib import messages

def doktor_ekle(request):
    hata = None
    basarili = False  # Başarı durumunu takip etmek için bir değişken ekleyin
    if request.method == 'POST': 
        form = DoktorForm(request.POST)
        if form.is_valid():
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO doktorlar (DoktorID, Ad, Soyad, UzmanlikAlani, CalistigiHastane)
                        VALUES (%s, %s, %s, %s, %s)
                    """, [form.cleaned_data['DoktorID'], form.cleaned_data['Ad'], form.cleaned_data['Soyad'], form.cleaned_data['UzmanlikAlani'], form.cleaned_data['CalistigiHastane']])  
                connection.commit()
                basarili = True  # İşlem başarılı olduğunda 'basarili' değişkenini True olarak ayarlayın
            except Exception as e:
                print("An error occurred: ", e)
                if 'Violation of PRIMARY KEY constraint' in str(e):
                    hata = "Bu ID zaten var"
                else:
                    hata = str(e)
    else:
        form = DoktorForm()
    return render(request, 'doktor_ekle.html', {'form': form, 'hata': hata, 'basarili': basarili})  # 'basarili' değişkenini şablona ekleyin

from django.contrib import messages

def doktor_sil(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM doktorlar WHERE DoktorID = %s", [id])
    messages.success(request, 'Doktor başarıyla silindi.')
    return redirect('doktor_listele')

def rapor_ekle(request):
    return render(request, 'rapor_ekle.html')

def rapor_sil(request):
    return render(request, 'rapor_sil.html')

def hasta_listele(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT HastaID, Ad, Soyad, DogumTarihi, Cinsiyet, TelefonNumarasi, Adres FROM hastalar")
        hastalar = cursor.fetchall()
    return render(request, 'hasta_listele.html', {'hastalar': hastalar})

def doktor_listele(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT DoktorID, Ad, Soyad, UzmanlikAlani, CalistigiHastane FROM doktorlar")
        doktorlar = cursor.fetchall()
    return render(request, 'doktor_listele.html', {'doktorlar': doktorlar})

def randevu_al(request):
    return render(request, 'randevu_al.html')

def randevu_ara(request):
    if request.method == 'POST':
        doktor_adi = request.POST.get('doktor_adi', '')
        uzmanlik_alani = request.POST.get('uzmanlik_alani', '')
        hastane_adi = request.POST.get('hastane_adi', '')
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT d.DoktorID, d.Ad, d.Soyad, d.UzmanlikAlani, d.CalistigiHastane
                FROM doktorlar d
                WHERE d.Ad LIKE %s AND d.UzmanlikAlani LIKE %s AND d.CalistigiHastane LIKE %s
            """, ['%' + doktor_adi + '%', '%' + uzmanlik_alani + '%', '%' + hastane_adi + '%'])
            randevular = cursor.fetchall()
        if not randevular:
            return render(request, 'randevu_ara.html', {'error': 'Arama sonucunuzla eşleşen randevu yok.'})
        else:
            return render(request, 'randevu_ara.html', {'randevular': randevular})
    else:
        return render(request, 'randevu_ara.html')

import datetime

def randevu_sec(request):
    if request.method == 'POST':
        doktor_id = request.POST.get('doktor_id')  # 'doktor_id' isimli alanı arıyoruz
        if not doktor_id:
            # doktor_id değeri None veya boşsa, bir hata mesajı döndürün
            return render(request, 'hata.html', {'hata': 'Doktor ID alınamadı.'})
        hasta_id = request.session.get('hasta_id')  # Hasta ID'sini oturumdan alırız
        with connection.cursor() as cursor:
            # RandevuId'yi otomatik olarak artan bir sayı olarak atayabiliriz
            cursor.execute("SELECT MAX(RandevuId) FROM randevular")
            max_id = cursor.fetchone()[0]
            yeni_randevu_id = max_id + 1 if max_id is not None else 1

            # RandevuTarihi ve RandevuSaati bilgileri, randevunun alındığı anın tarih ve saati olarak atanabilir
            randevu_tarihi = request.POST.get('randevu_tarihi')
            randevu_saati = request.POST.get('randevu_saati')

            # Aynı doktordan ve aynı saatte başka bir hasta randevu alamaz
            cursor.execute("""
                SELECT COUNT(*)
                FROM randevular
                WHERE DoktorId = %s AND RandevuTarihi = %s AND RandevuSaati = %s
            """, [doktor_id, randevu_tarihi, randevu_saati])
            varolan_randevu_sayisi = cursor.fetchone()[0]
            if varolan_randevu_sayisi > 0:
                return render(request, 'hata.html', {'hata': 'Bu saatte başka bir hasta zaten randevu aldı.'})

            cursor.execute("""
                INSERT INTO randevular (RandevuId, RandevuTarihi, RandevuSaati, HastaId, DoktorId)
                VALUES (%s, %s, %s, %s, %s)
            """, [yeni_randevu_id, randevu_tarihi, randevu_saati, hasta_id, doktor_id])
        # Başarı mesajını göstermek için yeni bir template render ediyoruz
        return render(request, 'basarili.html', {'mesaj': 'Randevunuz başarıyla oluşturuldu.'})
    else:
        return redirect('randevu_ara')
    

def randevu_listele(request):
    hasta_id = request.session.get('hasta_id')  # Hasta ID'sini oturumdan alırız
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.RandevuID, r.RandevuTarihi, r.RandevuSaati, d.Ad, d.Soyad, d.UzmanlikAlani, d.CalistigiHastane
            FROM randevular r
            JOIN doktorlar d ON r.DoktorID = d.DoktorID
            WHERE r.HastaID = %s
        """, [hasta_id])
        randevular = cursor.fetchall()
    return render(request, 'randevu_listele.html', {'randevular': randevular})

def randevu_sil(request):
    if request.method == 'POST':
        randevu_id = request.POST.get('randevu_id')
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM randevular
                WHERE RandevuID = %s
            """, [randevu_id])
        return redirect('randevu_listele')
    else:
        return redirect('randevu_listele')


def doktor_hasta_listele(request):
    doktor_id = request.session.get('doktor_id')
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT h.* FROM hastalar h
            JOIN randevular r ON h.HastaID = r.HastaID
            WHERE r.DoktorID = %s
        """, [doktor_id])
        hastalar = cursor.fetchall()
    return render(request, 'doktor_hasta_listele.html', {'hastalar': hastalar})


def hasta_guncelle(request):
    if request.method == 'POST':
        hasta_id = request.session.get('hasta_id')  # Hasta ID'sini oturumdan alırız
        ad = request.POST.get('Ad')
        soyad = request.POST.get('Soyad')
        dogum_tarihi = request.POST.get('DogumTarihi')
        cinsiyet = request.POST.get('Cinsiyet')
        telefon_numarasi = request.POST.get('TelefonNumarasi')
        adres = request.POST.get('Adres')
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE hastalar2
                SET Ad = %s, Soyad = %s, DogumTarihi = %s, Cinsiyet = %s, TelefonNumarasi = %s, Adres = %s
                WHERE HastaID = %s
            """, [ad, soyad, dogum_tarihi, cinsiyet, telefon_numarasi, adres, hasta_id])
        return render(request, 'basarili.html', {'mesaj': 'Bilgiler başarıyla güncellendi.'})
    else:
        hasta_id = request.session.get('hasta_id')  # Hasta ID'sini oturumdan alırız
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM hastalar2 WHERE HastaID = %s", [hasta_id])
            hasta = cursor.fetchone()
        return render(request, 'hasta_guncelle.html', {'hasta': hasta})


def doktor_duzenle(request, id):
    mesaj = ''
    if request.method == 'POST':
        ad = request.POST.get('ad')
        soyad = request.POST.get('soyad')
        uzmanlik_alani = request.POST.get('uzmanlik_alani')
        calistigi_hastane = request.POST.get('calistigi_hastane')
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE doktorlar
                SET Ad = %s, Soyad = %s, UzmanlikAlani = %s, CalistigiHastane = %s
                WHERE DoktorID = %s
            """, [ad, soyad, uzmanlik_alani, calistigi_hastane, id])
        mesaj = 'Doktor bilgileri başarıyla güncellendi.'

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM doktorlar WHERE DoktorID = %s", [id])
        doktor = cursor.fetchone()

    return render(request, 'doktor_duzenle.html', {'doktor': doktor, 'mesaj': mesaj})

def hasta_duzenle(request, id):
    if request.method == 'POST':
        ad = request.POST.get('ad')
        soyad = request.POST.get('soyad')
        dogum_tarihi = request.POST.get('dogum_tarihi')
        telefon_numarasi = request.POST.get('telefon_numarasi')
        adres = request.POST.get('adres')
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE hastalar
                SET Ad = %s, Soyad = %s, DogumTarihi = %s, TelefonNumarasi = %s, Adres = %s
                WHERE HastaID = %s
            """, [ad, soyad, dogum_tarihi, telefon_numarasi, adres, id])
        return redirect('home')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM hastalar WHERE HastaID = %s", [id])
            hasta = cursor.fetchone()
        return render(request, 'hasta_duzenle.html', {'hasta': hasta})


def randevu_duzenle(request, randevu_id):
    mesaj = ''
    if request.method == 'POST':
        yeni_tarih = request.POST.get('yeni_tarih')
        yeni_saat = request.POST.get('yeni_saat')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE randevular
                SET RandevuTarihi = %s, RandevuSaati = %s
                WHERE RandevuID = %s
            """, [yeni_tarih, yeni_saat, randevu_id])

        mesaj = 'Randevu başarıyla güncellendi.'

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM randevular WHERE RandevuID = %s
        """, [randevu_id])
        randevu = cursor.fetchone()

    return render(request, 'randevu_duzenle.html', {'randevu': randevu, 'mesaj': mesaj})


from django.shortcuts import render, redirect
from django.db import connection


def rapor_goruntule(request):
    if request.method == 'GET':
        hasta_id = request.session.get('hasta_id')  # HastaID'yi oturumdan alın
        with connection.cursor() as cursor:
            # HastaID'ye göre tüm raporları alın
            cursor.execute("SELECT GörüntüURL FROM HASTANE.dbo.TibbiRaporlar WHERE HastaID = %s", [hasta_id])
            raporlar = cursor.fetchall()
        return render(request, 'rapor_goruntule.html', {'raporlar': raporlar})


def raporlar(request, hasta_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM HASTANE.dbo.TibbiRaporlar WHERE HastaID = %s", [hasta_id])
        raporlar = cursor.fetchall()
    return render(request, 'raporlar.html', {'raporlar': raporlar, 'hasta_id': hasta_id})

from django.http import JsonResponse


def rapor_sil(request, rapor_id):
    if request.method == 'POST':
        hasta_id = request.session.get('hasta_id')  # HastaID'yi oturumdan alın
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM HASTANE.dbo.TibbiRaporlar WHERE RaporID = %s", [rapor_id])
        return redirect('rapor_ekle', hasta_id=hasta_id)


import datetime

def rapor_ekle(request, hasta_id):
    if request.method == 'POST':
        rapor_url = request.POST.get('rapor_url')
        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(RaporID) FROM HASTANE.dbo.TibbiRaporlar")
            max_rapor_id = cursor.fetchone()[0]
            yeni_rapor_id = max_rapor_id + 1 if max_rapor_id else 1
            bugunun_tarihi = datetime.datetime.now()  # Bugünün tarihini al
            cursor.execute("INSERT INTO HASTANE.dbo.TibbiRaporlar (RaporID, GörüntüURL, HastaID, RaporTarihi) VALUES (%s, %s, %s, %s)", [yeni_rapor_id, rapor_url, hasta_id, bugunun_tarihi])
        return redirect('rapor_ekle', hasta_id=hasta_id)
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM HASTANE.dbo.TibbiRaporlar WHERE HastaID = %s", [hasta_id])
            raporlar = cursor.fetchall()
        return render(request, 'rapor_ekle.html', {'hasta_id': hasta_id, 'raporlar': raporlar})
