"""
Lists the manifests available

"""

from django.core.management.base import NoArgsCommand, CommandError
from optparse import make_option

from build import populate

class Command(NoArgsCommand):
    help = "Lists available manifests."

    def handle(self, *args, **options):
        for manifest in populate.list_manifests():
            print str(manifest['title']).ljust(10) + manifest['description']