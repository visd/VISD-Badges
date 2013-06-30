from rest_framework import serializers
from django.contrib.auth.models import User, Group
from badges.models import Skillset, Challenges

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class SkillsetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skillset
        fields = ('url', 'title', 'short_description', 'long_description', 'challenges_list')


class ChallengesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Challenges
        fields = ('url', 'title', 'short_description', 'long_description', 'tags')