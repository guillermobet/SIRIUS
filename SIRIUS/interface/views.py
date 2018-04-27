from django.shortcuts import render
from .forms import TestForm

def index(request):
	
	form = TestForm()
	context = {'form' : form }
	
	return render(request, 'interface/index.html', context)
