from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    ctg = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': "form-control", 'style': 'max-width: 40em; border-color: black'}), label='Kategoriya')
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': "form-control", 'style': 'max-width: 40em; border-color: black'}), label='Rasm')
    name = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 40em; border-color: black'}), label='Nomi')
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 40em; border-color: black'}), label='Malumot')
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control", 'style': 'max-width: 40em; border-color: black'}), label='Narxi')

    class Meta:
        model = Product
        fields = ('ctg', 'image', 'name', 'description', 'price')


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 40em; border-color: black'}), label='Nomi')

    class Meta:
        model = Category
        fields = '__all__'


class MessageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': "form-control", 'style': 'max-width: 40em; border-color: black'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 40em; border-color: black'}))

    class Meta:
        model = Messages
        fields = '__all__'


class OrderForm(forms.ModelForm):

    class Meta:
        model = Orders
        fields = '__all__'
