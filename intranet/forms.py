from django import forms
from .models import *
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class Posting(forms.ModelForm):
    class Meta:
        model=Updates
        exclude=['user','time_stamp']



class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Updates
        exclude = ['user', 'time_stamp','status']
        widgets = {
            'update': SummernoteWidget(),
        }
        

        
class CommentForm(forms.ModelForm):
    class Meta:
        
        model = Comments
        fields = ['comment']
        widgets = {
            'comment': forms.TextInput(attrs={'placeholder':'Write a comment...'})
        }