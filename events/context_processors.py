from events.models import Event

def return_latest_events(level="guest", count="20"):
    """ Returns a list of the latest :count events, with a dictionary for each.

    We register this with TEMPLATE_CONTEXT_PROCESSORS so the latest events are included with every request object.
    """
    events = []
    for event in Event.objects.all()[:count]:
        events.append(event.get_dict())
    return {'events': events}