# Create your views here.
from django.http import HttpResponse
from models import Sample

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    latest_sample_list = Sample.objects.all().order_by('-timestamp')[:120]
    last_twentyfour_hours_list = Sample.objects.all().filter(timestamp__minute=0).order_by('-timestamp')[:48]
    context = {'latest_sample_list': latest_sample_list, 'last_twentyfour_hours_list': last_twentyfour_hours_list}
    return render(request, 'simpletemp/index.html', context)

@login_required
def ac(request):
    last_month_list = Sample.objects.all().order_by('-timestamp')[:5000]
    #last_month_list = Sample.objects.all().order_by('-timestamp')[:50000]
    ac_list = []
    ac_on = False
    total_on = None
    for i in range(0, len(last_month_list) - 6):
        if last_month_list[i].hvactemp - last_month_list[i + 2].hvactemp < 3 and not(ac_on):
            # if the temp dropped by 3 degrees in a minute, assume the AC was turned on
            ac_pair = []
            ac_pair.append(last_month_list[i])
            ac_list.append(ac_pair)
            ac_on = True
        elif last_month_list[i].hvactemp - last_month_list[i + 6].hvactemp > 3 and ac_on:
            # if the temp increases by 3 degrees in a 3 minutes, assume the AC was shut off
            ac_list[-1].append(last_month_list[i])
            duration = ac_list[-1][0].timestamp - ac_list[-1][1].timestamp
            print "duration = " + str(duration)
            ac_list[-1].append(duration)
            if(total_on):
                total_on = total_on + duration
            else:
                total_on = duration
            print "total on = " + str(total_on)
            ac_on = False

    context = {'ac_list': ac_list, 'total_on':total_on}
    return render(request, 'simpletemp/ac.html', context)

@login_required
def heat(request):
    last_month_list = Sample.objects.all().order_by('-timestamp')[:5100]
    #last_month_list = Sample.objects.all().order_by('-timestamp')[:50000]
    heat_list = []
    heat_on = False
    total_on = None
    # TODO throw out samples where the power was lost
    # e.g. if the duration between two samples is larger than ~30 seconds, toss the whole entry
    for i in range(0, len(last_month_list) - 6):
        if heat_on:
            print "heat is on, start time was " + str(heat_list[-1][0].timestamp) + " hvac temp is " + str(last_month_list[i].hvactemp)
        if last_month_list[i].hvactemp - last_month_list[i + 2].hvactemp > 3 and not(heat_on):
            # if the temp increased by 3 degrees in a minute, assume the heat was turned on
            heat_pair = []
            heat_pair.append(last_month_list[i])
            heat_list.append(heat_pair)
            heat_on = True
        elif last_month_list[i].hvactemp - last_month_list[i + 6].hvactemp < 2 and heat_on:
            # if the temp decreases by 2 degrees in a 3 minutes, assume the heat was shut off
            heat_list[-1].append(last_month_list[i])
            duration = heat_list[-1][0].timestamp - heat_list[-1][1].timestamp
            print "duration = " + str(duration)
            heat_list[-1].append(duration)
            if(total_on):
                total_on = total_on + duration
            else:
                total_on = duration
            #print "total on = " + str(total_on)
            heat_on = False

    context = {'heat_list': heat_list, 'total_on':total_on}
    return render(request, 'simpletemp/heat.html', context)

