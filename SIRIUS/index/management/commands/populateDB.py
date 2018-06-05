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
			relevance = '4_4_4_4_4_4_4_4_4_4_4_4_4_4_4_4_4',
			comment = ''
		)
		
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Objetivos del sitio web concretos y bien definidos',
			acronym = 'AG1',
			relevance = 'MA MA MO CR MA ME MA ME MA MA MO ME ME MA MA MA ME',
			metric = '',
			atribute = 'cuantitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Contenidos y servicios ofrecidos precisos y completos',
			acronym = 'AG2',
			relevance = 'CR CR MO CR CR CR MA MA CR MA MO ME ME MA MA MA MA',
			metric = '',
			atribute = 'cuantitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Estructura general del sitio web orientada al usuario',
			acronym = 'AG3',
			relevance = 'MA MA ME CR MA MA MA MA MA MA MA ME ME MA ME MA MA',
			metric = '',
			atribute = 'cuantitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Look&Feel corresponde con los objetivos, características, contenidos y servicios del sitio web',
			acronym = 'AG4',
			relevance = 'MA MA MO CR ME MA ME MO ME ME ME ME ME ME ME ME MA',
			metric = '',
			atribute = 'cuantitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Diseño general del sitio web reconocible',
			acronym = 'AG5',
			relevance = 'MA MA ME CR MA ME ME ME ME ME ME ME ME MA MO ME MA',
			metric = '',
			atribute = 'cuantitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Diseño general del sitio web coherente',
			acronym = 'AG6',
			relevance = 'CR MA ME CR MA MA ME ME MA ME ME ME ME MA MA ME MA',
			metric = '',
			atribute = 'cuantitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Se utiliza el idioma del usuario',
			acronym = 'AG7',
			relevance = 'MA MA MA CR MA MA MA MO MA MA MA ME MO MA ME ME ME',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Se da soporte a otro/s idioma/s',
			acronym = 'AG8',
			relevance = 'MA MA MO CR MA MA MA MO ME MO MO MO MO ME MO ME ME',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Traducción del sitio completa y correcta',
			acronym = 'AG9',
			relevance = 'MA MA ME CR MA MA ME MO ME ME ME MO ME ME MO ME ME',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		MetaCriteria.objects.create(
			heuristic = heuritic_aspectos_generales,
			name = 'Sitio web actualizado periódicamente',
			acronym = 'AG0',
			relevance = 'MA ME CR CR MA CR ME MA ME MA MA MA ME MA MA MA CR',
			metric = '',
			atribute = 'cualitativo',
			comment = ''
		)
		
		"""
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
