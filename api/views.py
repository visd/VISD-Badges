from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import *
from badges.models import *

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class SkillsetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Skillsets to be viewed or edited.
    """
    queryset = Skillset.objects.all()
    serializer_class = SkillsetSerializer


class ChallengeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Challenges to be viewed or edited.
    """
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer

class EntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Entries to be viewed or edited.
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


class ResourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Resource to be viewed or edited.
    """
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class ToolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Tool to be viewed or edited.
    """
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Tag to be viewed or edited.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer