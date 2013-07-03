from rest_framework import serializers
from django.contrib.auth.models import User, Group
from badges.models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'first_name', 'last_name', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class SkillsetSerializer(serializers.HyperlinkedModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Skillset
        fields = ('url', 'title', 'slug' ,'short_description', 'long_description', 'created_at')


class ChallengeSerializer(serializers.HyperlinkedModelSerializer):
    skill = serializers.PrimaryKeyRelatedField()
    slug = serializers.SlugField(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True)
    tools = serializers.PrimaryKeyRelatedField(many=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Challenge
        fields = ('title', 'slug', 'skill', 'short_description', 'long_description', 'tags', 'resources', 'tools', 'created_at')


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    challenge = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Entry


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag


class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource


class ToolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tool