from django import forms
from . models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image',
        ]

        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Title here'}),
            'content' : forms.Textarea(attrs={'class':'form-control','placeholder':'Enter your Content here'}),
            'image' : forms.ClearableFileInput(attrs={'class':'form-control'})
        }

# forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
