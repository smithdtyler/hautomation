# Create your views here.
from django.http import HttpResponse
from models import Sample

from django.shortcuts import render

def index(request):
    latest_sample_list = Sample.objects.all().order_by('-timestamp')[:120]
    last_twentyfour_hours_list = Sample.objects.all().order_by('-timestamp')[:2880]
    context = {'latest_sample_list': latest_sample_list, 'last_twentyfour_hours_list': last_twentyfour_hours_list}
    return render(request, 'simpletemp/index.html', context)

