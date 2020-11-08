from django.db import models

from django.contrib.auth.models import Permission, User
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator



class User(AbstractUser):
	is_client = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=True)
	
	email = models.EmailField(unique=True)
	image = models.ImageField(upload_to ='uploads/', null=True, blank=True, default = 'uploads/img_avatar.png') 
	disease = models.ForeignKey(Disease, null=True, blank=True, on_delete=models.CASCADE) 
	
class Hospital(models.Model):
	name   	= models.CharField(max_length=200)
	location   	= models.CharField(max_length=200, blank=True, null=True)
	phone   	= models.CharField(max_length=200,blank=True, null=True)
	description  = models.TextField(blank=True, null=True)
	images		= models.FileField(blank=True, null=True)
	
	website		= models.CharField(max_length=200, blank=True, null=True)


	def __str__(self):
		return self.name 

class Disease(models.Model):
	name   	= models.CharField(max_length=200)
	hospitals = models.ManyToManyField(Hospital,  blank=True)

	def __str__(self):
		return self.name 





class Patient(models.Model):
	name   	= models.CharField(max_length=200)
	age   	= models.CharField(max_length=200,blank=True, null=True,validators=[MaxValueValidator(100),MinValueValidator(1)])
	location   	= models.CharField(max_length=200, blank=True, null=True)
	contact = models.CharField(max_length=20, blank=True, null=True)
	blood_group		= models.CharField(max_length=200, blank=True, null=True)


	disease		= models.CharField(max_length=200, blank=True, null=True)

	inqury_date = models.DateTimeField(auto_now_add=True, null=True)

	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE) 


	def __str__(self):
		return self.name

class Rate(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE) 
	hospital = models.ForeignKey(Hospital, null=True, blank=True, on_delete=models.CASCADE)
	rating = models.FloatField(default=1,validators=[MaxValueValidator(5),MinValueValidator(0)])

	def __str__(self):
		return self.user.username
		

