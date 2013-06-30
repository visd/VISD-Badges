from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer, SkillsetSerializer, ChallengesSerializer
from badges.models import Skillset, Challenges

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

class ChallengesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Challenges to be viewed or edited.
    """
    queryset = Challenges.objects.all()
    serializer_class = ChallengesSerializer