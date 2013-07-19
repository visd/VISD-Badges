"""
The management command for populating the database with phony, but hopefully well-structured, data.

"""
import pprint

from django.core.management.base import LabelCommand, CommandError
from optparse import make_option

from provisioner import populate

class Command(LabelCommand):
    args = '<manifest>'
    help = "Load data into an app using the specified manifest."

    option_list = LabelCommand.option_list + (
        make_option('-r', 
            '--reset-data', 
            action="store_const", 
            const=True, 
            dest="reset",
            default=False,
            help= "Begin from an empty database and set of objects."),
        # make_option('-v',
        #     '--verbose',
        #     action="store_const",
        #     const=True,
        #     dest="verbose",
        #     default=False,
        #     help="Get a full printout of results.")
        )


    def handle(self, *args, **options):
        pp = pprint.PrettyPrinter(indent=4)

        try:
            result = populate.install_fixtures(choice=args[0], reset=options['reset'])
            if options['verbosity'] == '2':
                print pp.pprint(result)
            else:
                print "Lots of instances created."
        except CommandError:
            print "You have supplied an invalid option."
        except IndexError:
            print "You must supply the name of a manifest list.\nUse ./manage.py manifest_list to show what we have."