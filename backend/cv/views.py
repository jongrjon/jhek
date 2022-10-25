from django.shortcuts import render
from .models import Person, CVItem, Skill, Reccommendor, ItemPoint
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .headers import *

# Create your views here.
def index(request):
    person = Person.objects.all()
    template = loader.get_template('index.html')
    education =[]
    jobs = []
    seminars = []
    for i in CVItem.objects.all().order_by('-start'):
        item = {'item':i, 'points': ItemPoint.objects.filter(item = i)}
        if i.item_type =="ED":
            education.append(item)
        if i.item_type =="JO":
            jobs.append(item)
        if i.item_type =="SE":
            seminars.append(item)
    skills = []
    for s in Skill.objects.all():
        skill = {'skill_name_is':s.skill_name_is, 'skill_level': (s.skill_level/5)*100}
        skills.append(skill)
    reccommendors = Reccommendor.objects.all()
    context = {
        'person' : person,
        'jobs' : jobs,
        'education': education,
        'seminars': seminars,
        'skills' : skills,
        'reccommendors' : reccommendors,
        'headers':headers
    }
    return HttpResponse(template.render(context,request))