Fixit Local - Django Web Projesi
================================

Bu proje, yerel kullanıcıların şehirde karşılaştıkları sorunları (altyapı arızası, çevre kirliliği vb.) konum bazlı olarak harita üzerinden bildirmelerini, diğer kullanıcıların bu raporları değerlendirmelerini ve herkesin ortak sorun bilincine katkı sağlamasını hedefleyen bir web uygulamasıdır.

TEKNOLOJİLER
------------
- Python 3.13
- Django (Backend)
- HTML5 + Bootstrap (Frontend)
- Leaflet.js (Harita API)
- OpenStreetMap & Nominatim (Koordinattan adres çevirme)
- SQLite (varsayılan veritabanı)

YAPISAL ÖZET
------------
Ana uygulama adı: **rapor**

Uygulama bileşenleri:
- `models.py`: Rapor, Uye, RaporDegerlendirme
- `forms.py`: UyeForm, GirisForm
- `views.py`: Tüm sayfa fonksiyonları (anasayfa, giriş, üyelik, rapor gönderme, filtreleme vb.)
- `templates/`: Tüm HTML sayfaları
- `static/`: Harita scriptleri, JS entegrasyonu (Leaflet)
- `urls.py`: Sayfa yönlendirmeleri

ÖZELLİKLER
----------

1. ÜYE OLMA / GİRİŞ / ÇIKIŞ SİSTEMİ
------------------------------------
- Kullanıcılar isim + 5 haneli TC Kimlik ile kayıt olabilir.
- Aynı bilgilerle giriş yapabilir.
- Session üzerinden oturum tutulur.
- Giriş yapan kullanıcının adı sağ üstte görünür.
- “Çıkış Yap” ile session sıfırlanır.

2. RAPOR OLUŞTURMA (ANA SAYFA)
-------------------------------
- Harita üzerinden konum seçilir (İstanbul sınırı zorunlu).
- Olay türü seçilir (elektrik kesintisi, yaralı hayvan, vs).
- Olay tarihi ve açıklama girilir.
- "Diğer" seçilirse özel açıklama alanı görünür.
- Rapor başarılı şekilde veritabanına kaydedilir.
- Kullanıcıya başarı/eksiklik mesajları popup ile gösterilir.

3. RAPORLARIM SAYFASI
----------------------
- Kullanıcının daha önce gönderdiği tüm raporları listeler.
- Her raporun altında:
  - Olay tarihi, açıklama, konum (adres dönüşümlü)
  - Diğer kullanıcıların bu raporla ilgili yaptığı değerlendirme sayıları
- Filtreleme: Olay türüne göre filtreleme yapılabilir.

4. SON KAYDEDİLEN RAPORLAR (GENEL LİSTE)
-----------------------------------------
- Tüm kullanıcıların gönderdiği raporlar görünür.
- Her rapor:
  - Ad, olay, tarih, adres, açıklama ile listelenir.
  - Değerlendirme yapılabilir (dropdown: doğru, eksik, yanıltıcı, alakasız).
- Kullanıcılar bir rapor hakkında görüş bildirebilir.
- Filtreleme: Olay türüne göre filtre yapılabilir.

5. ADRES DÖNÜŞÜMÜ (Koordinat → Açık Adres)
------------------------------------------
- Leaflet haritası ile konum seçilir (latitude + longitude)
- OpenStreetMap Nominatim servisi ile JS üzerinden açık adres otomatik getirilir
- Sayfa yüklendiğinde tüm adresler arka planda yüklenir

YAKLAŞAN / GELECEK GELİŞTİRMELER
-------------------------------
- Profil sayfası düzenleme (aktif değil, kaldırıldı)
- Rapor düzenleme / silme yetkisi
- Admin panelden rapor onay/reddet sistemi
- İstatistik panosu (rapor yoğunluğu, grafikler)
- Harita üzerinde bölgesel ısı haritası
- E-posta doğrulama / Şifreli giriş sistemi

KULLANIM
--------
1. Sanal ortamı aktive edin:
   `source venv/bin/activate`

2. Gerekirse veritabanını oluşturun:
   `python manage.py makemigrations && python manage.py migrate`

3. Uygulamayı başlatın:
   `python manage.py runserver`

4. Tarayıcıdan erişim:
   `http://127.0.0.1:8000/`

---

Bu proje, topluluk katkılarına açık olarak tasarlanmıştır.
Kodlarda sade yapı, işlevsel modüller ve kullanıcı deneyimi ön planda tutulmuştur.
