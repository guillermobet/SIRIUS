from django import template
register = template.Library()

@register.filter(name='addclassandid')
def addclassandid(field, class_id):
	args = class_id.split('_')
	attrs = { 'class': args[0], 'id' : field.auto_id+args[1] }
	
	return field.as_widget(attrs=attrs)
