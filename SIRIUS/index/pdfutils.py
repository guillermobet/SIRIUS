import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa

def link_callback(uri, rel):
	"""
	Convert HTML URIs to absolute system paths so xhtml2pdf can access those
	resources
	"""
	# use short variable names
	sUrl = settings.STATIC_URL      # Typically /static/
	sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
	mUrl = settings.MEDIA_URL       # Typically /static/media/
	mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

	# convert URIs to absolute system paths
	if uri.startswith(mUrl):
		path = os.path.join(mRoot, uri.replace(mUrl, ""))
	elif uri.startswith(sUrl):
		path = os.path.join(sRoot, uri.replace(sUrl, ""))
	else:
		return uri  # handle absolute uri (ie: http://some.tld/foo.png)

	# make sure that file exists
	if not os.path.isfile(path):
			raise Exception(
				'media URI must start with %s or %s' % (sUrl, mUrl)
			)
	return path
	
def render_pdf_view(request, template_path, context, file_name):
	# Create a Django response object, and specify content_type as pdf
	template_path = os.path.realpath(os.path.dirname(__file__))+'/templates/'+template_path
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(file_name)
	
	# find the template and render it.
	template = get_template(template_path)
	html = template.render(context)

	# create a pdf
	pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
	   
	# if error then show some funy view
	if pisaStatus.err:
	   return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response
