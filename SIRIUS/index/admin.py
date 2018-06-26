from django.contrib import admin
from django.apps import apps
# Register your models here.
from .models import User, MetaHeuristic, MetaCriteria, Criteria, Website, Review

admin.site.register(User)
admin.site.register(MetaHeuristic)
admin.site.register(MetaCriteria)
admin.site.register(Criteria)
admin.site.register(Website)
admin.site.register(Review)
