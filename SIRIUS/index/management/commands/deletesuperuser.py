#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError


class Command(BaseCommand):

	def add_arguments(self, parser):
		parser.add_argument('username', type=str)

	def handle(self, *args, **options):
		User = get_user_model()
		try:
			user = User.objects.get(user = options['username'], is_superuser=True)
		except User.DoesNotExist:
			raise CommandError("There is no superuser named {}".format(options['username']))

		self.stdout.write("-------------------")
		self.stdout.write("Deleting superuser {}".format(options.get('username')))
		user.delete()
		self.stdout.write("Done.")
