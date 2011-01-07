from django.template import RequestContext
from django.shortcuts import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from models import *
from datetime import datetime

def country_object_detail(request, country_id):
    end_year = datetime.now().year
    begin_year = end_year - 10
    country = get_object_or_404(Country, id=country_id.upper())
    datapoint_list = country.datapoint_set.filter(year__range=(begin_year, end_year)).order_by('indicator__id', '-year')
    
    paginator = Paginator(datapoint_list, 25)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
        
    try:
        datapoints = paginator.page(page)
    except (EmptyPage, InvalidPage):
        datapoints = paginator.page(paginator.num_pages)
    
    return render_to_response('country_object_detail.html', {'country': country, 'datapoints': datapoints}, context_instance=RequestContext(request))

def countries_list(request):
    countries = Country.objects.all()
    indicators = Indicator.objects.all()
    return render_to_response('countries_list.html', {'countries': countries, 'indicators': indicators}, context_instance=RequestContext(request))


def country_indicator_list(request, country_id, indicator_id):
    # country = get_object_or_404(Country, id=country_id.upper())
    # indicator = get_object_or_404(Indicator, id=indicator_id.upper())
    datapoints = get_list_or_404(DataPoint, country=country_id, indicator=indicator_id)
    return render_to_response('country_indicator_list.html', {'datapoints': datapoints}, context_instance=RequestContext(request))
    

def indicator_object_detail(request, indicator_id):
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
    
    return render_to_response('indicator_datapoint_list.html', {'indicator': indicator, 'datapoints': datapoints}, context_instance=RequestContext(request))
