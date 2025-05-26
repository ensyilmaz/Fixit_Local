from django.db import models

class Uye(models.Model):
    isim = models.CharField(max_length=100)
    tc_kimlik = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.isim

class Rapor(models.Model):
    isim = models.CharField(max_length=100)
    olay = models.CharField(max_length=100)
    tarih = models.DateField()
    enlem = models.FloatField()
    boylam = models.FloatField()
    adres = models.TextField(blank=True)  # ✅ adres boş olabilir ama otomatik doldurulacak
    diger_aciklama = models.TextField(blank=True, null=True)
    uye = models.ForeignKey(Uye, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.tarih} - {self.isim} - {self.olay}"

class RaporDegerlendirme(models.Model):
    SECENEK_DOGRU = 'dogru'
    SECENEK_EKSIK = 'eksik'
    SECENEK_YANILTICI = 'yaniltici'
    SECENEK_ALAKASIZ = 'alakasi_yok'

    DEGER_SECENEKLERI = [
        (SECENEK_DOGRU, 'Bilgi doğru'),
        (SECENEK_EKSIK, 'Eksik bilgi var'),
        (SECENEK_YANILTICI, 'Yanıltıcı bilgi'),
        (SECENEK_ALAKASIZ, 'Alakasız rapor'),
    ]

    rapor = models.ForeignKey(Rapor, on_delete=models.CASCADE, related_name='degerlendirmeler')
    secim = models.CharField(max_length=20, choices=DEGER_SECENEKLERI)
