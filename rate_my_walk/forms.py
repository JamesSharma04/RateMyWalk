from django import forms
from rate_my_walk.models import WalkPage, Comment, Rating, Photo
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
    
    #how to deal with uploaded pictures in forms?
    cover = forms.ImageField(upload_to='page_image', blank=True)
    
    enjoyment = forms.IntegerField(initial = 0)
    duration = forms.IntegerField(initial = 0)
    difficulty = forms.IntegerField(initial = 0)
    
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    #how to deal with date fields in forms?
    #shoud be hidden and it takes current date when creating the object anyways?
    date = forms.DateField(default=timezone.now())
    
    class Meta:
        model = WalkPage
        fields = ('name', 'desc', 'start', 'end', 'cover', 'enjoyment', 'duration', 'difficulty', )
        #slug not needed but date?

class RatingForm(forms.ModelForm):
    duration = forms.IntegerField(help_text="Duration", initial = 0)
    difficulty = forms.IntegerField(help_text="Difficulty", initial = 0)
    enjoyment = forms.IntegerField(help_text="Enjoyment", initial = 0)

    class Meta:
        model = Rating
        exclude = ('walk',)

class PhotoForm(forms.ModelForm):
    	
	date = forms.DateField()
	owner = forms.CharField(max_length=128)
	picture = forms.ImageField(upload_to='page_image', blank=True)

	class Meta:
		model = Photo
		exclude = ('WalkPage',)

class CommentForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text = "Please enter the title of your comment")
    comment = forms.CharField(max_length=128,
                              help_text = "Write your comment here")
    #owner should be pulled automatically somehow
    owner = forms.CharField(max_length=128)
    #date also should be automatic
    date = forms.DateField()
    #do we need these?
    url = forms.URLField()
    views = forms.IntegerField(default=0)
    
    class Meta:
        model = Comment
