from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils.translation import ugettext_lazy as _


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

	def __str__(self):
		return self.user

class Website(models.Model):
	id = models.AutoField(primary_key=True)
	url = models.URLField()
	name = models.CharField(max_length=100)
	description = models.TextField()

class Review(models.Model):
	id = models.AutoField(primary_key=True)
	website_id = models.ForeignKey("Website", to_field="id", on_delete=models.CASCADE)
	username_id = models.ForeignKey("User", to_field="user", on_delete=models.CASCADE)
	review = models.TextField(default=None) #temporal

	class Meta:
		unique_together = ("website_id", "username_id")