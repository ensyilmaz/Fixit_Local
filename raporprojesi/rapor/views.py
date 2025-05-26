from django.shortcuts import render, redirect
from .models import Rapor, Uye, RaporDegerlendirme
from .forms import UyeForm, GirisForm
from geopy.geocoders import Nominatim  # Adres çözümleme
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

# Sabit İstanbul ilçeleri listesi
ILCELER = [
    "Adalar", "Arnavutköy", "Ataşehir", "Avcılar", "Bağcılar", "Bahçelievler", "Bakırköy",
    "Başakşehir", "Bayrampaşa", "Beşiktaş", "Beykoz", "Beylikdüzü", "Beyoğlu", "Büyükçekmece",
    "Çatalca", "Çekmeköy", "Esenler", "Esenyurt", "Eyüpsultan", "Fatih", "Gaziosmanpaşa",
    "Güngören", "Kadıköy", "Kağıthane", "Kartal", "Küçükçekmece", "Maltepe", "Pendik",
    "Sancaktepe", "Sarıyer", "Silivri", "Sultanbeyli", "Sultangazi", "Şile", "Şişli",
    "Tuzla", "Ümraniye", "Üsküdar", "Zeytinburnu"
]

# Adres çözüm fonksiyonu
def koordinat_to_adres(enlem, boylam):
    try:
        geolocator = Nominatim(user_agent="fixit-local")
        location = geolocator.reverse((enlem, boylam), exactly_one=True, timeout=10)
        return location.address if location else "Adres alınamadı"
    except (GeocoderTimedOut, GeocoderUnavailable):
        return "Adres alınamadı"

def uye_ol(request):
    if request.method == 'POST':
        form = UyeForm(request.POST)
        if form.is_valid():
            uye = form.save()
            request.session['uye_id'] = uye.id
            return redirect('anasayfa')
    else:
        form = UyeForm()
    return render(request, 'rapor/uye_ol.html', {'form': form})

def giris_yap(request):
    if request.method == 'POST':
        form = GirisForm(request.POST)
        if form.is_valid():
            isim = form.cleaned_data['isim']
            tc_kimlik = form.cleaned_data['tc_kimlik']
            try:
                uye = Uye.objects.get(isim=isim, tc_kimlik=tc_kimlik)
                request.session['uye_id'] = uye.id
                return redirect('anasayfa')
            except Uye.DoesNotExist:
                form.add_error(None, "Bilgiler eşleşmedi.")
    else:
        form = GirisForm()
    return render(request, 'rapor/giris.html', {'form': form})

def cikis_yap(request):
    request.session.flush()
    return redirect('anasayfa')

def anasayfa(request):
    uye = None
    if 'uye_id' in request.session:
        try:
            uye = Uye.objects.get(id=request.session['uye_id'])
        except Uye.DoesNotExist:
            del request.session['uye_id']

    if request.method == 'POST':
        isim = request.POST.get('isim')
        olay = request.POST.get('olay')
        tarih = request.POST.get('tarih')
        enlem = request.POST.get('enlem')
        boylam = request.POST.get('boylam')
        diger_aciklama = request.POST.get('diger_aciklama', '') if olay == 'Diğer' else ''

        if not (isim and olay and tarih and enlem and boylam):
            return redirect('/anasayfa/?error=1')

        adres = koordinat_to_adres(enlem, boylam)

        rapor = Rapor(
            isim=isim,
            olay=olay,
            tarih=tarih,
            enlem=enlem,
            boylam=boylam,
            diger_aciklama=diger_aciklama,
            uye=uye,
            adres=adres
        )
        rapor.save()
        return redirect('/anasayfa/?success=1')

    raporlar = Rapor.objects.all().order_by('-id')[:3]
    return render(request, 'rapor/anasayfa.html', {'uye': uye, 'raporlar': raporlar})

def raporlar(request):
    if request.method == "POST":
        rapor_id = request.POST.get('rapor_id')
        secim = request.POST.get('secim')
        if rapor_id and secim:
            try:
                rapor = Rapor.objects.get(id=rapor_id)
                RaporDegerlendirme.objects.create(rapor=rapor, secim=secim)
            except Rapor.DoesNotExist:
                pass
        return redirect('raporlar')

    secili_olay = request.GET.get('olay', '')
    secili_ilce = request.GET.get('ilce', '')
    raporlar = Rapor.objects.all().order_by('-id')

    if secili_olay:
        raporlar = raporlar.filter(olay=secili_olay)
    if secili_ilce:
        raporlar = raporlar.filter(adres__icontains=secili_ilce)

    for rapor in raporlar:
        gosterim = ""
        for secenek, secenek_adi in RaporDegerlendirme.DEGER_SECENEKLERI:
            adet = rapor.degerlendirmeler.filter(secim=secenek).count()
            gosterim += f"{secenek_adi}: {adet}<br>"
        rapor.gosterim_metni = gosterim

    olay_turleri = Rapor.objects.values_list('olay', flat=True).distinct()

    uye = None
    if 'uye_id' in request.session:
        try:
            uye = Uye.objects.get(id=request.session['uye_id'])
        except Uye.DoesNotExist:
            pass

    return render(request, 'rapor/raporlar.html', {
        'raporlar': raporlar,
        'uye': uye,
        'olay_turleri': olay_turleri,
        'secili_olay': secili_olay,
        'ilceler': ILCELER,
        'secili_ilce': secili_ilce,
    })

def raporlarim(request):
    if 'uye_id' not in request.session:
        return redirect('giris')

    try:
        uye = Uye.objects.get(id=request.session['uye_id'])
    except Uye.DoesNotExist:
        return redirect('giris')

    secili_olay = request.GET.get('olay', '')
    secili_ilce = request.GET.get('ilce', '')
    raporlar = Rapor.objects.filter(isim=uye.isim)

    if secili_olay:
        raporlar = raporlar.filter(olay=secili_olay)
    if secili_ilce:
        raporlar = raporlar.filter(adres__icontains=secili_ilce)

    for rapor in raporlar:
        gosterim = ""
        for secenek, secenek_adi in RaporDegerlendirme.DEGER_SECENEKLERI:
            adet = rapor.degerlendirmeler.filter(secim=secenek).count()
            gosterim += f"{secenek_adi}: {adet}<br>"
        rapor.gosterim_metni = gosterim

    olay_turleri = raporlar.values_list('olay', flat=True).distinct()

    return render(request, 'rapor/raporlarim.html', {
        'raporlar': raporlar,
        'uye': uye,
        'olay_turleri': olay_turleri,
        'secili_olay': secili_olay,
        'ilceler': ILCELER,
        'secili_ilce': secili_ilce,
    })
