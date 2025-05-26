from django import forms
from .models import Uye

class UyeForm(forms.ModelForm):
    class Meta:
        model = Uye
        fields = ['isim', 'tc_kimlik']
        widgets = {
            'isim': forms.TextInput(attrs={'placeholder': 'Ad Soyad', 'class': 'form-control'}),
            'tc_kimlik': forms.TextInput(attrs={'maxlength': 5, 'class': 'form-control'}),
        }

    def clean_tc_kimlik(self):
        tc = self.cleaned_data['tc_kimlik']
        if not tc.isdigit() or len(tc) != 5:
            raise forms.ValidationError("TC Kimlik numarası 5 haneli olmalıdır.")
        return tc

class GirisForm(forms.Form):
    isim = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Ad Soyad', 'class': 'form-control'}))
    tc_kimlik = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'maxlength': 5, 'class': 'form-control'}))
