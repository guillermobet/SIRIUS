from django.core.management.base import BaseCommand
from index.models import MetaHeuristic, MetaCriteria

# THIS STILL NEED WORK
class Command(BaseCommand):
	args = 'foo bar..'
	help = 'help string'
	
	def _clean_db(self):
		MetaCriteria.objects.all().delete()
		MetaHeuristic.objects.all().delete()
	
	def _populate_db(self):
		heuritic_aspectos_generales = MetaHeuristic.objects.create(
			name = 'Aspectos Generales',
			acronym = 'AG',
			comment = ''
		)
		
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Objetivos del sitio web concretos y bien definidos',
			acronym = 'AG1',
			metric = '',
			atribute = 'quantitative',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Contenidos y servicios ofrecidos precisos y completos',
			acronym = 'AG2',
			metric = '',
			atribute = 'quantitative',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Estructura general del sitio web orientada al usuario',
			acronym = 'AG3',
			metric = '',
			atribute = 'quantitative',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Look&Feel corresponde con los objetivos, características, contenidos y servicios del sitio web',
			acronym = 'AG4',
			metric = '',
			atribute = 'quantitative',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Diseño general del sitio web reconocible',
			acronym = 'AG5',
			metric = '',
			atribute = 'quantitative',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Diseño general del sitio web coherente',
			acronym = 'AG6',
			metric = '',
			atribute = 'quantitative',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Se utiliza el idioma del usuario',
			acronym = 'AG7',
			metric = '',
			atribute = 'qualitative',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Se da soporte a otro/s idioma/s',
			acronym = 'AG8',
			metric = '',
			atribute = 'qualitative',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Traducción del sitio completa y correcta',
			acronym = 'AG9',
			metric = '',
			atribute = 'qualitative',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Sitio web actualizado periódicamente',
			acronym = 'AG0',
			metric = '',
			atribute = 'qualitative',
			comment = ''
		)
		
	def handle(self, *args, **options):
		self._clean_db()
		self._populate_db()
