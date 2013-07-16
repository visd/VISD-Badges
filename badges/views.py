from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django import template
from django.shortcuts import render
from badges.models import *

def index(request, **kwargs):
    rendered = 'Hello'

    return render(request, 'base.html', {'user': 'Thane Gill',})


def get_events_list():
    pass 

def get_challenges_in_skill(skill):
    return challenges = Challenge.objects.filter(skill=skill)
