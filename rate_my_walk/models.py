from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

# This model is for walks. It's similar to the Page model, I was just 
# making this to test the templates.

class WalkPage(models.Model):
	NAME_MAX_LENGTH = 128
	
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User', null=True)
	name = models.CharField(max_length=128, unique=True)
	desc = models.CharField(max_length=2048)
	start = models.CharField(max_length=128)
	end = models.CharField(max_length=128)
	slug = models.SlugField(unique=True)

	cover = models.ImageField(upload_to='page_image', default='default.jpg')

	enjoyment = models.IntegerField(default=5)
	duration = models.IntegerField(default=5)
	difficulty = models.IntegerField(default=5)

	date = models.DateField(default=timezone.now)
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(WalkPage, self).save(*args, **kwargs)
	
	class Meta:
		verbose_name_plural = 'Walks'
	
	def __str__(self):
		return self.name		
		
class Comment(models.Model):
	TITLE_MAX_LENGTH = 128
	URL_MAX_LENGTH = 128
    
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Owner', null=True)
	walk = models.ForeignKey(WalkPage, on_delete=models.CASCADE, default=None)
	title = models.CharField(max_length=128)
	comment = models.CharField(max_length=128)
	date = models.DateField(default=timezone.now)
		
	def __str__(self):
		return self.title

class Rating(models.Model):

	walk = models.ForeignKey(WalkPage, on_delete=models.CASCADE, default=None)
	rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Rater', null=True)
	duration = models.IntegerField(default=0)
	difficulty = models.IntegerField(default=0)
	enjoyment = models.IntegerField(default=0)
	
	def __str__(self):
		return str(self.rater) + ": " + str(self.walk)

class Photo(models.Model):
	TITLE_MAX_LENGTH = 128
	URL_MAX_LENGTH = 128
	
	walk = models.ForeignKey(WalkPage, on_delete=models.CASCADE, default=None)
	date = models.DateField(default=timezone.now)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Uploader', null=True)
	picture = models.ImageField(upload_to='more_page_image', default='default.jpg')


class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    website = models.URLField(blank=True, default='https://google.com')
    picture = models.ImageField(upload_to='profile_images',blank=True, default='profile_images/default.jpg')
    
    def __str__(self):
        return self.user.username