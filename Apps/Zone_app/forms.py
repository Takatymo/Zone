# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from .models import NomadUser, Mood, Tool, Category, Contact, PlacePoint


class UserForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'required': 'true'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': 'true'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'required': 'true',
                                                            'pattern': '^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)?$'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 7, 'max': 99}))

    class Meta:
        model = NomadUser
        fields = ('username', 'password', 'email', 'age', 'gender', 'job', 'icon')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class NarrowDownForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(Category.objects.all(), widget=forms.CheckboxSelectMultiple(),
                                                required=False, label='Select Category')
    moods = forms.ModelMultipleChoiceField(Mood.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False,
                                           label='Select Mood')
    tools = forms.ModelMultipleChoiceField(Tool.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False,
                                           label='Select Tool')


class MoodForm(forms.Form):
    moods = forms.ModelMultipleChoiceField(Mood.objects.all(), required=True, widget=forms.CheckboxSelectMultiple(),
                                           label='Select Mood')


class PlacePointForm(ModelForm):
    point = forms.IntegerField(max_value=100, min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = PlacePoint
        fields = ('place', 'nomad', 'point')
        widgets = {
            'place': forms.HiddenInput(),
            'nomad': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super(PlacePointForm, self).clean()
        point = cleaned_data.get('point')
        nomad = cleaned_data.get('nomad')
        if nomad.point < point:
            raise forms.ValidationError(
                "%(value)s ポイント以下で入力してください。",
                params={'value': str(nomad.point)},
            )



class ContactForm(ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'required': 'true', 'placeholder': 'Name', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'required': 'true', 'placeholder': 'Email', 'class': 'form-control',
               'pattern': '^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)?$'}))
    message = forms.CharField(
        widget=forms.Textarea(attrs={'required': 'true', 'placeholder': 'Message', 'class': 'form-control'}))

    class Meta:
        model = Contact
        fields = ('name', 'email', 'message')


class UserEditForm(ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'pattern': '^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)?$'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 7, 'max': 99}))

    class Meta:
        model = NomadUser
        fields = ('email', 'age', 'gender', 'job', 'icon')
