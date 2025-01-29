

from django import forms

class HastaForm(forms.Form):
    HastaID = forms.CharField(max_length=100)
    Ad = forms.CharField(max_length=100)
    Soyad = forms.CharField(max_length=100)
    DogumTarihi = forms.DateField()
    Cinsiyet = forms.CharField(max_length=10)
    TelefonNumarasi = forms.CharField(max_length=15)
    Adres = forms.CharField(widget=forms.Textarea)

class DoktorForm(forms.Form):
    DoktorID = forms.CharField(max_length=100)
    Ad = forms.CharField(max_length=100)
    Soyad = forms.CharField(max_length=100)
    UzmanlikAlani = forms.CharField(max_length=100)
    CalistigiHastane = forms.CharField(max_length=100)


class HastaGirisForm(forms.Form):
    HastaID = forms.CharField(max_length=100)
    Ad = forms.CharField(max_length=100)

class RandevuDuzenleForm(forms.Form):
    RandevuTarihi = forms.DateField()
    RandevuSaati = forms.TimeField()
