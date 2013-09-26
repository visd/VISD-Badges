from django.conf.urls import patterns, url, include
# from rest_framework import routers
# from api import views as api_views

# router = routers.DefaultRouter()
# router.register(r'user', api_views.UserViewSet)
# router.register(r'group', api_views.GroupViewSet)
# router.register(r'skillset', api_views.SkillsetViewSet)
# router.register(r'tool', api_views.ToolViewSet)
# router.register(r'entry', api_views.EntryViewSet)
# router.register(r'tag', api_views.TagViewSet)
# router.register(r'challenge', api_views.ChallengeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    # url(r'^api/', include(router.urls)),
    # url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^', include('newviews.urls', namespace='newviews'))
)
