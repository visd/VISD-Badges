from django.contrib.contenttypes.models import ContentType

from events import models


def register_event(model_instance, event_type, given_user=None, save=True):
    """ Accepts an event_type slug', a user instance, and a model instance.
    
    The event-type and user instances pass through. The model instance needs to be
    decomposed into content_type and pk and those sent along.

    Returns an event instance on completion.
    """

    instance_content_type = ContentType.objects.get_for_model(model_instance)
    model_pk = model_instance.pk

    e = models.Event(type=event_type,
                     user=given_user,
                     content_type=instance_content_type,
                     object_id=model_pk)
    if save:
        e.save()
    return e
