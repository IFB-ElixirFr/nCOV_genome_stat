import json

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from France.models import vaccinFrance, regionsFrance, hospitIncidReg
from django.db.models import Sum, Count, Max, Prefetch, Avg


def vaccins(request):
    return render(request, "France/index.html")


def stats_region(request, codeRegion):
    try:
        test = regionsFrance.objects.get(code=codeRegion)
    except (test.DoesNotExist, test.EmptyResultSet) as e:
        return HttpResponse(status=404)

    vaccinFrance.objects.filter(region__code__exact=codeRegion)
    dataValue = []
    labels = []

    result = vaccinFrance.objects.values('date').annotate(totalVaccines=Sum('totalVaccines')).order_by('date')
    for v in result:
        dataValue.append(v['totalVaccines'])
        labels.append(v['date'].strftime("%Y-%m-%d"))

    speRegion = regionsFrance.objects.get(code=codeRegion).nom
    map = regionsFrance.objects.get(code=codeRegion).features

    return render(request, "France/region.html", context={"dataValue": dataValue,
                                                          "labels": labels,
                                                          "region": speRegion,
                                                          "codeRegion": codeRegion,
                                                          "map": map})


def stats_all_regions(request):
    dataValue_vaccin, labels_vaccin = vaccins()
    dataValue_hospitInci_date, labels_hospitInci_date = hospitInci_date()

    map = generate_map()
    dateUpdate = vaccinFrance.objects.aggregate(Max('date'))['date__max']

    all_vaccins = sum(list(vaccinFrance.objects.filter(date=dateUpdate).values_list('totalVaccines', flat=True)))
    all_rea = sum(list(hospitIncidReg.objects.filter(date=dateUpdate).values_list('incid_rea', flat=True)))

    evolDate_vaccin_data, evolDate_vaccin_labels = evolDate_vaccin()
    evolDate_hospiInci_data, evolDate_hospiInci_labels = evolDate_hospiInci()

    return render(request, "France/regions.html", context={"dataValue_vaccin": dataValue_vaccin,
                                                           "labels_vaccin": labels_vaccin,
                                                           "dataValue_hospitInci_date": dataValue_hospitInci_date,
                                                           "labels_hospitInci_date": labels_hospitInci_date,
                                                           "dateUpdate": dateUpdate,
                                                           "evolDate_vaccin_data": evolDate_vaccin_data,
                                                           "evolDate_vaccin_labels": evolDate_vaccin_labels,
                                                           "evolDate_hospiInci_data": evolDate_hospiInci_data,
                                                           "evolDate_hospiInci_labels": evolDate_hospiInci_labels,
                                                           "map": map,
                                                           "all_vaccins": all_vaccins,
                                                           "all_rea":all_rea
                                                           })


def generate_map():
    map = []
    regions = regionsFrance.objects.all()
    for r in regions:
        latest_dates = vaccinFrance.objects.filter(region__pk=r.pk).latest('date').date
        r.features['properties']['Total_vac'] = \
        vaccinFrance.objects.filter(region__pk=r.pk).filter(date=latest_dates).values('region__nom').annotate(
            total_vac=Sum('totalVaccines')).order_by('total_vac').first()['total_vac']
        latest_dates = hospitIncidReg.objects.filter(region__pk=r.pk).latest('date').date
        r.features['properties']['Total_hospiIncid'] = \
        hospitIncidReg.objects.filter(region__pk=r.pk).filter(date=latest_dates).values('region__nom').annotate(
            total_hospiIncid=Sum('incid_rea')).order_by('total_hospiIncid').first()['total_hospiIncid']
        map.append(r.features)

    return map


def vaccins(code=None):
    if code:
        latest_dates = vaccinFrance.objects.filter(region__code=code).values('region__nom').annotate(date=Max('date'))
        qs = vaccinFrance.objects.filter(region__code=code).filter(date__in=latest_dates.values('date')).order_by(
            'totalVaccines').values(
            'region__nom', 'totalVaccines', 'region__features')
    else:
        latest_dates = vaccinFrance.objects.values('region__nom').annotate(date=Max('date'))
        qs = vaccinFrance.objects.filter(date__in=latest_dates.values('date')).order_by('totalVaccines').values(
            'region__nom', 'totalVaccines', 'region__features')

    dataValue = []
    labels = []

    for q in qs:
        labels.append(q['region__nom'])
        dataValue.append(q['totalVaccines'])

    return dataValue, labels


def hospitInci_date(Date=None):
    if Date:
        qs = hospitIncidReg.objects.filter(date__in=Date).order_by('incid_rea').values(
            'region__nom', 'incid_rea', 'region__features')
    else:
        latest_dates = hospitIncidReg.objects.values('region__nom').annotate(date=Max('date'))
        qs = hospitIncidReg.objects.filter(date__in=latest_dates.values('date')).order_by('incid_rea').values(
            'region__nom', 'incid_rea', 'region__features')

    dataValue = []
    labels = []

    for q in qs:
        labels.append(q['region__nom'])
        dataValue.append(q['incid_rea'])

    return dataValue, labels


def evolDate_vaccin():
    evolDate = vaccinFrance.objects.values('date').annotate(total_vac=Sum('totalVaccines')).order_by('date')
    evolDate_data = []
    evolDate_labels = []

    for ed in evolDate:
        evolDate_data.append(ed['total_vac'])
        evolDate_labels.append(ed['date'].strftime("%Y-%m-%d"))

    return evolDate_data, evolDate_labels


def evolDate_hospiInci():
    evolDate = hospitIncidReg.objects.values('date').annotate(incid_rea=Sum('incid_rea')).order_by('date')
    evolDate_data = []
    evolDate_labels = []

    for ed in evolDate:
        evolDate_data.append(ed['incid_rea'])
        evolDate_labels.append(ed['date'].strftime("%Y-%m-%d"))

    return evolDate_data, evolDate_labels



def request_asJson_France(request):
    dataFrance = []
    regions = list(regionsFrance.objects.values_list('pk', flat=True))

    for r in regions:
        inter = dict()
        inter["region"] = regionsFrance.objects.get(pk=r).nom
        inter["code"] = regionsFrance.objects.get(pk=r).code
        inter["Total_vac"] = vaccinFrance.objects.filter(region__pk=r).values('region__nom').annotate(
            total_vac=Sum('totalVaccines')).order_by('total_vac').first()['total_vac']
        inter["Total_hospiIncid"] = hospitIncidReg.objects.filter(region__pk=r).values('region__nom').annotate(
            total_hospiIncid=Sum('incid_rea')).order_by('total_hospiIncid').first()['total_hospiIncid']
        dataFrance.append(inter)

    for df in dataFrance:
        df["region"] = "<a href='" + reverse('focusRegion_code', args=(df['code'],)) + "'>" + df['region'] + "</a>"

    structure = json.dumps(list(dataFrance), cls=DjangoJSONEncoder)
    return HttpResponse(structure, content_type='application/json;charset=utf-8')


def request_asJson_Region(request, codeRegion):
    try:
        object_list = vaccinFrance.objects.filter(region__code__exact=codeRegion).values('date', 'totalVaccines')
    except object_list.DoesNotExist:
        return HttpResponse(status=404)

    structure = json.dumps(list(object_list), cls=DjangoJSONEncoder)
    return HttpResponse(structure, content_type='application/json;charset=utf-8')
