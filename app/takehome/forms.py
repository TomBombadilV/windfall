from django import forms
from django.db import models
from django.forms import ModelForm

from .models import Subreddit

class FollowSubredditForm(ModelForm):
    """ A form for creating a new Subreddit object to indicate
        that that subreddit is now being followed by user.
    """
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'AskReddit'}), label='')
    class Meta:
        model = Subreddit
        fields = ['name']