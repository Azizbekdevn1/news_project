from django import forms
from .models import Contact,News,Comment
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class ContactForm(forms.ModelForm):

    class Meta:
        model=Contact
        fields="__all__"


class NewsForm(forms.ModelForm):
    class Meta:
        model=News
        fields = ('title', 'image', 'category', 'body', 'status',)
        labels = {
            'title': 'Title',
            'image': 'Image',
            'category': 'Category',
            'body': 'Body',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            #'status': forms.Select(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields =["body"]

        labels={
            'body':'Comment',
        }

        widgets = {
            'body': forms.TextInput(attrs={'class': 'form-control'})
        }