from django.conf.urls import patterns, url

urlpatterns = patterns("",
    url(r'^(?:(?P<parent>\w+)/(?P<parent_id>\w+)/)?(?P<resource>\w+)(?:/(?P<resource_id>\w+))?$',
        'newviews.views.handler',
        name="parsed-url"),
)
