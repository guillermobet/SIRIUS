from django import template
register = template.Library()

@register.filter(name='addcssclass')
def addcss(field, cssclass):
   return field.as_widget(attrs={"class":cssclass})
