from django.conf.urls import patterns, url, include
from rest_framework import routers
from api import views as api_views
from badges import views as badge_views

router = routers.DefaultRouter()
router.register(r'user', api_views.UserViewSet)
router.register(r'group', api_views.GroupViewSet)
router.register(r'skillset', api_views.SkillsetViewSet)
router.register(r'tool', api_views.ToolViewSet)
router.register(r'entry', api_views.EntryViewSet)
router.register(r'tag', api_views.TagViewSet)
router.register(r'challenge', api_views.ChallengeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^skillsets$', badge_views.SkillsetsList.as_view(), name='skillsets-index'),
    url(r'^skillsets$/?P<id>\w+$', badge_views.SkillsetsDetail.as_view(), name='skillsets-detail'),
    url(r'^challenges/?P<id>\w+$', badge_views.challenges_detail, name='challenges-detail'),
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework'))
)