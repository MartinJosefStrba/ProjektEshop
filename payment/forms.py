from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
	shipping_full_name = forms.CharField(label="Celé jméno", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Celé jméno'}), required=True)
	shipping_email = forms.CharField(label="Email", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}), required=True)
	shipping_address1 = forms.CharField(label="Adresa 1", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adresa1'}), required=True)
	shipping_address2 = forms.CharField(label="Adresa 2", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adresa2'}), required=False)
	shipping_city = forms.CharField(label="Město", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Město'}), required=True)
	shipping_state = forms.CharField(label="Stát", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Stát'}), required=False)
	shipping_zipcode = forms.CharField(label="PSČ", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'PSČ'}), required=False)
	shipping_country = forms.CharField(label="Země", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Země'}), required=True)

	class Meta:
		model = ShippingAddress
		fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country']

		exclude = ['user',]