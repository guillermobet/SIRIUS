from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
	path("", views.index, name="index"),
	path("login/", auth_views.login, name="login"),
	path("logout/", auth_views.logout, name="logout"),
	path("register/", views.register, name="register"),
	path("home/", views.home, name="home"),
	#path("home/indicator", views.indicator, name="indicator"),
	#path("home/features", views.features, name="features"),
	#path("home/subfeatures", views.subfeatures, name="subfeatures"),
	#path("home/attributes", views.attributes, name="attributes"),
	path("home/metaheuristics", views.meta_heuristics, name="meta_heuristics"),
	path("home/delete-metaheuristic/<int:meta_heuristic_id>/", views.delete_meta_heuristics, name="delete_meta_heuristic"),
	path("home/metacriteria", views.meta_criteria, name="meta_criteria"),
	path("home/delete-metacriterion/<int:meta_criterion_id>/", views.delete_meta_criterion, name="delete_meta_criterion"),
	path("home/evaluate", views.evaluate, name="evaluate"),
	path("home/evaluate/items/<int:review_id>/", views.evaluate_items, name="evaluate_items"),
	path("home/reviews", views.reviews, name="reviews"),
	path("home/reviews/<int:review_id>/", views.reviews_edit, name="reviews_edit"),
]
