from django import forms
from rate_my_walk.models import WalkPage, Comment, Photo, Rating
from django.utils import timezone

class WalkPageForm(forms.ModelForm):
    
    name = forms.CharField(max_length=128,
                           help_text = "Please enter the name of your walk")
    desc = forms.CharField(max_length=128,
                           help_text = "Please write the description of your walk here")
    start = forms.CharField(max_length=128,
                            help_text = "Enter start location of your walk")
    end = forms.CharField(max_length=128,
                          help_text = "Enter end location of your walk")
    
    cover = forms.ImageField(help_text = "Upload picture of your walk", required=False)
    
    enjoyment = forms.IntegerField(initial = 0,
                                   help_text = "Rate enjoyment (0-10)",
                                   max_value = 10,
                                   min_value = 0)
    duration = forms.IntegerField(initial = 0,
                                  help_text = "Rate duration (0-10)",
                                  max_value = 10,
                                  min_value = 0)
    difficulty = forms.IntegerField(initial = 0, help_text = "Rate difficulty (0-10)",
                                    max_value = 10,
                                    min_value = 0)
    
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    date = forms.DateField(widget=forms.HiddenInput, required=False)
    
    class Meta:
        model = WalkPage
        fields = ('name', 'desc', 'start', 'end', 'cover', 'enjoyment', 'duration', 'difficulty', )


class RatingForm(forms.ModelForm):
    duration = forms.IntegerField(help_text="Duration", initial = 0, max_value = 10, min_value = 0)
    difficulty = forms.IntegerField(help_text="Difficulty", initial = 0, max_value = 10, min_value = 0)
    enjoyment = forms.IntegerField(help_text="Enjoyment", initial = 0, max_value = 10, min_value = 0)

    class Meta:
        model = Rating
        exclude = ('walk',)

class PhotoForm(forms.ModelForm):
    	
	picture = forms.ImageField(help_text="If you also had a walk at this location you can upload a picture here")

	class Meta:
		model = Photo
		exclude = ('walk', 'owner', 'date')

class CommentForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text = "Please enter the title of your comment")
    comment = forms.CharField(max_length=128,
                              help_text = "Write your comment here")
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Comment
        exclude = ('owner', 'walk', )

class DeleteWalkForm(forms.ModelForm):
    slug = forms.SlugField(widget=forms.HiddenInput())
    
    class Meta:
        model = WalkPage
        fields = ('slug', )
