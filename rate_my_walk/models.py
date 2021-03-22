from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

# This model is for walks. It's similar to the Page model, I was just 
# making this to test the templates.
class Walk(models.Model):
	NAME_MAX_LENGTH = 128
	
	name = models.CharField(max_length=128, unique=True)
	desc = models.CharField(max_length=128, unique=True)
	start = models.CharField(max_length=128, unique=True)
	end = models.CharField(max_length=128, unique=True)
	slug = models.SlugField(unique=True)

	enjoyment = models.IntegerField(default=0)
	duration = models.IntegerField(default=0)
	difficulty = models.IntegerField(default=0)

	date = models.DateField(default=timezone.now())
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Walk, self).save(*args, **kwargs)
	
	class Meta:
		verbose_name_plural = 'Walks'
	
	def __str__(self):
		return self.name

class Category(models.Model):
	NAME_MAX_LENGTH = 128
	
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)
	
	class Meta:
		verbose_name_plural = 'Categories'
	
	def __str__(self):
		return self.name

class Page(models.Model):
	TITLE_MAX_LENGTH = 128
	URL_MAX_LENGTH = 200

	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)
	picture = models.ImageField(upload_to='page_image', blank=True)
	startPoint = models.CharField(max_length=32)
	endPoint = models.CharField(max_length=32)
	
	def __str__(self):
		return self.title
		
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	picture = models.ImageField(upload_to='profile_images', blank=True)
	
	def __str__(self):
		return self.user.username
		
		
class Comment(models.Model):
	TITLE_MAX_LENGTH = 128
	URL_MAX_LENGTH = 200

	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)
	comment = models.CharField(max_length=128)
	owner = models.CharField(max_length=128)
	date = models.DateField()
		
	def __str__(self):
		return self.title
		
class Rating(models.Model):
	TITLE_MAX_LENGTH = 128
	URL_MAX_LENGTH = 200

	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)
	length = models.IntegerField(default=0)
	duration = models.IntegerField(default=0)
	difficulty = models.IntegerField(default=0)
	enjoyment = models.IntegerField(default=0)
	
	def __str__(self):
		return self.title
		
class Photo(models.Model):
	TITLE_MAX_LENGTH = 128
	URL_MAX_LENGTH = 200
	
	date = models.DateField()
	owner = models.CharField(max_length=128)
	picture = models.ImageField(upload_to='page_image', blank=True)