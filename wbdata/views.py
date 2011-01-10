from django.template import RequestContext
from django.shortcuts import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Max
from models import *
from datetime import datetime

def country_object_detail(request, country_id, template_name='wbdata/country_object_detail.html'):
    max_year = DataPoint.objects.all().aggregate(Max('year'))
    end_year = max_year['year__max']
    begin_year = end_year - 10
    country = get_object_or_404(Country, id=country_id.upper())
    # datapoint_list = country.datapoint_set.filter(year__range=(begin_year, end_year)).order_by('indicator__id', '-year')
    datapoints = country.datapoint_set.filter(year=end_year).order_by('indicator__id')
    
    return render_to_response(template_name, {'country': country, 'datapoints': datapoints, 'year': end_year}, context_instance=RequestContext(request))

def countries_list(request, template_name='wbdata/countries_list.html'):
    countries = Country.objects.all()
    indicators = Indicator.objects.all()
    return render_to_response(template_name, {'countries': countries, 'indicators': indicators}, context_instance=RequestContext(request))


def country_indicator_list(request, country_id, indicator_id, template_name='wbdata/country_indicator_list.html'):
    country = get_object_or_404(Country, id=country_id.upper())
    indicator = get_object_or_404(Indicator, id=indicator_id.upper())
    datapoints = get_list_or_404(DataPoint.objects.order_by('-year'), country=country_id, indicator=indicator_id)
    return render_to_response(template_name, {'datapoints': datapoints, 'country': country, 'indicator': indicator}, context_instance=RequestContext(request))
    

def indicator_object_detail(request, indicator_id, template_name='wbdata/indicator_datapoint_list.html'):
    indicator = get_object_or_404(Indicator, id=indicator_id)
    datapoint_list = indicator.datapoint_set.order_by('country__id', '-year')
    
    paginator = Paginator(datapoint_list, 25)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
        
    try:
        datapoints = paginator.page(page)
    except (EmptyPage, InvalidPage):
        datapoints = paginator.page(paginator.num_pages)
    
    return render_to_response(template_name, {'indicator': indicator, 'datapoints': datapoints}, context_instance=RequestContext(request))
