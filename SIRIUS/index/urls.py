from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
	path("", views.index, name="index"),
	path("login/", auth_views.login, name="login"),
	path("logout/", auth_views.logout, name="logout"),
	path("register/", views.register, name="register"),
	path("home/", views.home, name="home"),
	path("home/perfil", views.perfil, name="perfil"),
	
	# MetaHeuristics
	path("home/metaheuristics", views.meta_heuristics, name="meta_heuristics"),
	path("home/metaheuristics/<int:meta_heuristic_id>/", views.meta_heuristics, name="edit_meta_heuristic"),
	path("home/delete-metaheuristic/<int:meta_heuristic_id>/", views.delete_meta_heuristics, name="delete_meta_heuristic"),
	
	# MetaCriteria
	path("home/metacriteria", views.meta_criteria, name="meta_criteria"),
	path("home/metacriteria/<int:meta_criterion_id>/", views.meta_criteria, name="edit_meta_criterion"),
	#path("home/metacriteria/<int:meta_criterion_id>/", views.edit_meta_criterion, name="edit_meta_criterion"),
	path("home/delete-metacriterion/<int:meta_criterion_id>/", views.delete_meta_criterion, name="delete_meta_criterion"),
	path("home/filter_meta_criteria", views.filter_meta_criteria, name="filter_meta_criteria"),
	
	# Evaluate
	path("home/evaluate", views.evaluate, name="evaluate"),
	path("home/evaluate/items/<int:review_id>/", views.evaluate_items, name="evaluate_items"),
	
	# Reviews
	path("home/reviews", views.reviews, name="reviews"),
	path("home/reviews/<int:review_id>/", views.see_review, name="see_review"),
	path("home/edit_review/<int:review_id>/", views.edit_review, name="edit_review"),
	
	# Websites
	path("home/websites", views.websites, name="websites"),
	path("home/websites/<int:website_id>/", views.websites, name="edit_website"),
]
