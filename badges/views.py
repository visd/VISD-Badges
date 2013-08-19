from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django import template
from django.template import loader, RequestContext
from django.shortcuts import render

from helper_methods import retrieve


class models:
    from badges.models import Skillset, Challenge, Tag, Tool, Entry, Resource

def index(request, **kwargs):
    rendered = 'Hello'

    return render(request, 'base.html', {'user': 'Thane Gill', })



def skillset_objects():
    prefetch_list = ['challenges']
    return {'objects': [
         {'fields': retrieve('body', s), 
          'traversals': [models.Challenge.collection.url(s.pk)]} 
          for s in models.Skillset.objects.prefetch_related(*prefetch_list).all()
    ]
    }

def skillset_list(request, primary=True):
    if request.method == 'GET':
        result = skillset_objects()
        # for s in skillsets:
        #     result = retrieve
        # result['challenges'] = [retrieve('header',c) for c in s.challenge_set.all()]
        # Write something to determine
        #     skillset_list.append(result)
        if primary:
            template = loader.get_template('skillset_list.html')
            context = RequestContext(request, {
                'skillsets': skillset_list,
            })
            return HttpResponse(template.render(context))
        else:
            return result


def skillset_detail(request, primary=True):
    pass


def challenges_detail(request, primary=True):
    pass


def get_challenges_in_skill(skill):
    pass
    # return challenges = Challenge.objects.filter(skill=skill)
