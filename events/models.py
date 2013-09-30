from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template import Template, Context
from django.forms.models import model_to_dict
from django.conf import settings

from badges.models import NestedGroup

from badges.models import Tag


class Event(models.Model):
    """ A record of something happening in the system.

    Records the model instance in question, a slug for the type, and the user in question.

    The type_info method looks up the information needed to render the event into human-readable form.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tags')
    group = models.ForeignKey(NestedGroup, related_name='tags')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=32)
    
    # The following fields locate the model instance serving as the predicate of this Event.
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    level = models.CharField(max_length=16)

    # Note these are not the tags returned in the get_dict method.
    # These tags leave open the option that we can tag events just as we can challenges, entries, etc.
    tags = models.ManyToManyField(Tag, related_name='events')


    def save(self, *args, **kwargs):
        self.level = self.type_info()['level'] # the event level is retrieved from our dictionary.
        super(Event, self).save(*args, **kwargs)

    def type_info(self):
        """ Returns the dictionary for the current type.

        This is done as a lookup against a Python object because:

        - we'll be calling this with every request;
        - it isn't really dynamic. (It only changes when admins reconfigure, not in normal operations).

        And the base assumption: a lookup against an object is much faster than a db lookup.
        """
        from event_types import EVENT_TYPES
        return EVENT_TYPES[self.type] # gives type_info the dictionary for our given type.
    
    def as_html(self):
        """ Renders the model instance against the matching template to produce a human-readable string.
        """
        t = Template(self.type_info()['eventstring'])
        context_dict = {'object':model_to_dict(self.content_object)}
        # when we have our user model, change this so it returns a sub-dictionary on the related User instance.
        if self.user is not None:
            context_dict['user'] = self.user
        c = Context(context_dict)
        return t.render(c)

    def get_dict(self):
        context = {'eventstring':self.as_html()}
        context['tags'] = self.type_info()['tags']
        context['tags'].append(self.level)
        context['created'] = self.created
        return context

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return 'Type: %s, modified %s' % (self.type, self.modified.strftime('%B %d %Y'))



# class EventType(models.Model):
#     """ A type of event in the system.

#     The template field contains a string, in Django template format, which renders contexts into
#     human-readable format.
#     """
#     EVENT_LEVELS = (
#         ('public','Public: Every visitor sees.'),
#         ('user','User: Logged-in users see.'),
#         ('staff','Staff: System events for staff members to see.'),
#         ('admin','Every event.'),
#         ('debug','The full log of activity.'),
#     )  

#     name = models.CharField(db_index=True, max_length=35, primary_key=True)
#     template = models.TextField()
#     event_level = models.CharField(max_length=8, 
#                                    choices=EVENT_LEVELS)

#     def get_template(self):
#         """Converts the template field into a Template.
#         """
#         return Template(self.template)
