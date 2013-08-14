from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django import template
from django.shortcuts import render
from django.views import generic

from badges.models import *

def index(request, **kwargs):
    rendered = 'Hello'

    return render(request, 'base.html', {'user': 'Thane Gill',})


def skillset_list(request, primary=True):
    skillsets = Skillset.objects.all()
    skillset_list =[]
    for s in skillsets:
        this_dict = model_to_dict(s)
        this_dict['challenges'] = s.challenge_set.all().values('id','title')
        skillset_list.append(this_dict)
    template = loader.get_template('skillsets_index.html')
    context = RequestContext(request, {
            'skillsets': skillset_list,
        })
    return HttpResponse(template.render(context)) and primary or context


class SkillsetsList(generic.ListView):
    
    model = Skillset
    template_name = 'skillset_list.html'
    
class SkillsetsDetail(generic.DetailView):

    model = Skillset

def challenges_detail(request, primary=True):
    pass

def get_challenges_in_skill(skill):
    pass
    # return challenges = Challenge.objects.filter(skill=skill)
