from django.core.management.base import BaseCommand
from index.models import MetaHeuristic, MetaCriteria

def add_search_relevance(relevance_string):
	aux = relevance_string.split()
	output = []
	
	for i in range(0, len(aux)):
		if(i == 4):
			output.append('CR')
		output.append(aux[i])
		
	output = " ".join(output)
	return output
	
# THIS STILL NEED WORK
class Command(BaseCommand):
	args = 'foo bar..'
	help = 'help string'
	
	def _clean_db(self):
		MetaCriteria.objects.all().delete()
		MetaHeuristic.objects.all().delete()
	
	def _populate_db(self):
		try:
			f = open('static/baseMetaScheme.txt', 'r')
		except FileNotFound:
			print('File baseMetaScheme.txt not in static folder')
			exit()
			
		# read from file and create evrything
		line = None
		while(line != '--EOF--'):
			
			# Read MetaHeuristic
			heuristic_name = f.readline()[:-1]
			heuristic_acronym = f.readline()[:-1]
			heuristic_relevance = f.readline()[:-1]
			# Create MetaHeuristic
			heuristic = MetaHeuristic.objects.create(
				name = heuristic_name,
				acronym = heuristic_acronym,
				#relevance = heuristic_relevance,
				comment = ''
			)
			line = f.readline()
			line = f.readline()
			while(line != '' and line != '--EOF--'):
				# Read MetaCriterion
				line = line.split(': ')
				criterion_name = line[1]
				criterion_acronym = line[0]
				criterion_relevance = f.readline()[:-1]
				criterion_attribute = f.readline()[:-1]
				
				# Create MetaCriterion
				MetaCriteria.objects.create(
					heuristic = heuristic,
					name = criterion_name,
					acronym = criterion_acronym,
					#relevance = add_search_relevance(criterion_relevance),
					metric = '',
					atribute = criterion_attribute,
					comment = ''
				)
				
				line = f.readline()[:-1]
				
		"""				
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
			atribute = 'cuantitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Contenidos y servicios ofrecidos precisos y completos',
			acronym = 'AG2',
			metric = '',
			atribute = 'cuantitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Estructura general del sitio web orientada al usuario',
			acronym = 'AG3',
			metric = '',
			atribute = 'cuantitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Look&Feel corresponde con los objetivos, características, contenidos y servicios del sitio web',
			acronym = 'AG4',
			metric = '',
			atribute = 'cuantitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Diseño general del sitio web reconocible',
			acronym = 'AG5',
			metric = '',
			atribute = 'cuantitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Diseño general del sitio web coherente',
			acronym = 'AG6',
			metric = '',
			atribute = 'cuantitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Se utiliza el idioma del usuario',
			acronym = 'AG7',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Se da soporte a otro/s idioma/s',
			acronym = 'AG8',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Traducción del sitio completa y correcta',
			acronym = 'AG9',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Sitio web actualizado periódicamente',
			acronym = 'AG0',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		
		heuritic_identidad_e_informacion = MetaHeuristic.objects.create(
			name = 'Identidad e Información',
			acronym = 'II',
			comment = ''
		)
		
		MetaCriteria.objects.create(
			heuristic = heuritic_identidad_e_informacion,
			name = 'IIdentidad o logotipo significativo, identificable y suficientemente visible',
			acronym = 'II1',
			metric = '',
			atribute = 'cuantitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_identidad_e_informacion,
			name = 'Identidad del sitio en todas las páginas',
			acronym = 'II2',
			metric = '',
			atribute = 'cuanlitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_identidad_e_informacion,
			name = 'Eslogan o tagline adecuado al objetivo del sitio',
			acronym = 'II3',
			metric = '',
			atribute = 'cuantitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_identidad_e_informacion,
			name = 'Se ofrece información sobre el sitio web, empresa',
			acronym = 'II4',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_identidad_e_informacion,
			name = 'Existen mecanismos de contacto',
			acronym = 'II5',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_identidad_e_informacion,
			name = 'Se ofrece información sobre la protección de datos personales o der/autor del contenido en el sitio',
			acronym = 'II6',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_identidad_e_informacion,
			name = 'Se ofrece información sobre el autor, fuentes y fechas de creación y revisión en el contenido web',
			acronym = 'II7',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		
		heuritic_estructura_y_navegacion = MetaHeuristic.objects.create(
			name = 'Estructura y Navegación',
			acronym = 'EN',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_estructura_y_navegacion,
			name = 'Se ha evitado pantalla de bienvenida',
			acronym = 'EN1',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_estructura_y_navegacion,
			name = 'Estructura de organización y navegación adecuada',
			acronym = 'EN2',
			metric = '',
			atribute = 'cuantitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_estructura_y_navegacion,
			name = 'Organización de elementos consistente con las convenciones',
			acronym = 'EN3',
			metric = '',
			atribute = 'cuantitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_estructura_y_navegacion,
			name = 'Control del número de elementos y de términos por elemento en los menús de navegación',
			acronym = 'EN4',
			metric = '',
			atribute = 'cuantitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_estructura_y_navegacion,
			name = 'Equilibrio entre profundidad y anchura en el caso de estructura jerárquica',
			acronym = 'EN5',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_estructura_y_navegacion,
			name = 'Enlaces fácilmente reconocibles como tales',
			acronym = 'EN6',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_estructura_y_navegacion,
			name = 'La caracterización de los enlaces indica su estado (visitados, activos)',
			acronym = 'EN7',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_estructura_y_navegacion,
			name = 'No hay redundancia de enlaces',
			acronym = 'EN8',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_estructura_y_navegacion,
			name = 'No hay enlaces rotos',
			acronym = 'EN9',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_estructura_y_navegacion,
			name = 'No hay enlaces que lleven a la misma página que se está visualizando',
			acronym = 'EN10',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_estructura_y_navegacion,
			name = 'En las imágenes de enlace se indica el contenido al que se va a acceder',
			acronym = 'EN11',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_estructura_y_navegacion,
			name = 'Existe un enlace para volver al inicio en cada página',
			acronym = 'EN12',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_estructura_y_navegacion,
			name = 'Existen elementos de navegación que orienten al usuario acerca de dónde está y como volver',
			acronym = 'EN13',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_estructura_y_navegacion,
			name = 'Existe mapa del sitio para acceder directamente a los contenidos sin navegar',
			acronym = 'EN14',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		"""
		
	def handle(self, *args, **options):
		self._clean_db()
		self._populate_db()
