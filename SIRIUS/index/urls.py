from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
	path("", views.index, name="index"),
	path("login/", auth_views.login, name="login"),
	path("logout/", auth_views.logout, name="logout"),
	path("register/", views.register, name="register"),
	path("home/", views.home, name="home"),
	path("home/indicator", views.indicator, name="indicator"),
	path("home/features", views.features, name="features"),
	path("home/subfeatures", views.subfeatures, name="subfeatures"),
	path("home/attributes", views.attributes, name="attributes"),
	path("home/evaluate", views.evaluate, name="evaluate"),
	path("home/evaluate/1", views.evaluate1, name="evaluate1"),
]