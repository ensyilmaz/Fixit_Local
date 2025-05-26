from django.contrib import admin
from .models import Uye, Rapor, RaporDegerlendirme


@admin.register(Uye)
class UyeAdmin(admin.ModelAdmin):
    list_display = ('isim', 'tc_kimlik')
    search_fields = ('isim', 'tc_kimlik')
    ordering = ('isim',)


@admin.register(Rapor)
class RaporAdmin(admin.ModelAdmin):
    list_display = ('isim', 'olay', 'tarih', 'uye', 'adres')
    search_fields = ('isim', 'olay', 'adres', 'uye__isim')
    list_filter = ('olay', 'tarih')
    date_hierarchy = 'tarih'
    ordering = ('-tarih',)


@admin.register(RaporDegerlendirme)
class RaporDegerlendirmeAdmin(admin.ModelAdmin):
    list_display = ('rapor', 'secim')
    list_filter = ('secim',)
    search_fields = ('rapor__isim', 'rapor__olay')