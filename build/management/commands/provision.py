"""
The management command for populating the database with phony, but hopefully well-structured, data.

"""
from django.core.management.base import LabelCommand, CommandError
from optparse import make_option

from build import populate


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
                    help="Begin from an empty database and set of objects."
                    ),
        make_option('-s',
                    '--save-data',
                    action="store_const",
                    const=True,
                    dest="save",
                    default=False,
                    help="Persist data to the database."
                    )
        )

    def handle(self, *args, **options):
        try:
            result = populate.install_fixtures(choice=args[0],
                                               reset=options['reset'],
                                               save=options['save']
                                               )
            if options['verbosity'] == '2':
                print result[1]
            print "%d instances created%s." % (len(result[0]),
                                               options['save'] and " and saved" or " but not saved"
                                               )
        except CommandError:
            print "You have supplied an invalid option."
        except IndexError:
            print "You must supply the name of a manifest list.\nUse ./manage.py manifest_list to show what we have."