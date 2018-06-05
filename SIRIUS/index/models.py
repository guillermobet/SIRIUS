from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils.translation import ugettext_lazy as _
import datetime

class UserManager(BaseUserManager):

	use_in_migrations = True
	def create_user(self,user,email,full_name,telephone,password):
		user = self.model(user=user,email=email,full_name=full_name, telephone=telephone, password= password)
		user.set_password(password)
		user.is_staff = True
		user.is_superuser = False
		user.save(using=self._db)
		return user
	def create_superuser(self,user,email,full_name,telephone,password):
		user = self.model(user=user,email=email,full_name=full_name, telephone=telephone, password= password)
		user.set_password(password)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user
	def get_by_natural_key(self,user_):
		print(user_)
		return self.get(user=user_)

class User(AbstractBaseUser, PermissionsMixin):

	user = models.CharField(_('Usuario'),max_length=40,unique=True)
	email = models.EmailField(_('Correo electronico'),blank=True)
	full_name = models.CharField(_('Nombre completo'), max_length=100, blank=True)
	telephone = models.CharField(_('Telefono'),max_length=11, blank = True)
	is_staff = models.BooleanField(_('staff'),default=False)
	is_superuser = models.BooleanField(_('superuser'),default=False)
	USERNAME_FIELD = 'user'
	REQUIRED_FIELDS = ['email','full_name','telephone']

	objects= UserManager()

	def get_short_name(self):
		return self.user

	def natural_key(self):
		return self.user
		
	def is_tester(self):
		return self.is_staff
		
	def is_admin(self):
		return self.is_superuser

	def __str__(self):
		return self.user

class Website(models.Model):

	id = models.AutoField(primary_key=True)
	url = models.URLField(unique=True)
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField()
	type = models.IntegerField(default = 1)

class Review(models.Model):

	id = models.AutoField(primary_key=True)
	website = models.ForeignKey("Website", to_field="id", on_delete=models.CASCADE)
	username = models.ForeignKey("User", to_field="user", on_delete=models.CASCADE)
	browser = models.CharField(max_length=20)
	browser_version = models.CharField(max_length=10)
	date = models.DateField(default = datetime.date.today)
	UP = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0.0)
	comment = models.TextField()

	class Meta:
		unique_together = ("website", "username")
		
class MetaHeuristic(models.Model):

	id = models.AutoField(primary_key=True)
	#review = models.ForeignKey("Review", to_field="id", on_delete=models.CASCADE)
	name = models.CharField(max_length=100, unique=True)
	acronym = models.CharField(max_length=2, unique=True)
	relevance = models.CharField(max_length = 35, default = '4_4_4_4_4_4_4_4_4_4_4_4_4_4_4_4_4')
	comment = models.TextField()
	
	def get_relevance_list(self):
		relevance_list = self.relevance.split('_')
		for i in range(0, len(relevance_list)):
			relevance_list[i] = int(relevance_list[i])
			
		return relevance_list
	
	def __str__(self):
		return self.name
	
class MetaCriteria(models.Model):

	id = models.AutoField(primary_key=True)
	#heuristic = models.ForeignKey("Heuristic", to_field="id", on_delete=models.CASCADE)
	heuristic = models.ForeignKey("MetaHeuristic", to_field="id", on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	acronym = models.CharField(max_length=4, unique=True)
	relevance = models.CharField(max_length = 55, default = 'CR CR CR CR CR CR CR CR CR CR CR CR CR CR CR CR CR')
	metric = models.CharField(max_length=12)
	atribute = models.CharField(max_length=12)
	comment = models.TextField()

	def get_relevance_list(self):
		relevance_list = self.relevance.split()
		#for i in range(0, len(relevance_list)):
		#	relevance_list[i] = int(relevance_list[i])
			
		return relevance_list
		

class Criteria(models.Model):
	id = models.AutoField(primary_key=True)
	#heuristic = models.ForeignKey("Heuristic", to_field="id", on_delete=models.CASCADE)
	review = models.ForeignKey("Review", to_field="id", on_delete=models.CASCADE)
	meta_criteria = models.ForeignKey("MetaCriteria", to_field="id", on_delete=models.CASCADE)
	value = models.CharField(max_length=12)
	
	def get_numeric_value(self):
		qualitative_mapping = {
			'NTS' : 0,
			'NEP' : 2.5,
			'NPP' : 5,
			'NPI' : 7.5,
			'S' : 10,
			}
		if(self.meta_criteria.atribute == 'cualitativo'):
			value = qualitative_mapping[self.value]
		else:
			value = float(self.value)
			
		return value
