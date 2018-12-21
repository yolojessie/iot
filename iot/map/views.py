from django.shortcuts import render
from map.models import Light
from django.http.response import HttpResponse
import json
from django.utils import timezone
from datetime import date

from django.contrib.auth.decorators import login_required

@login_required
def map(request):
    '''
    Show map in the map page
    '''
    lights = Light.objects.all()
    
    context = {'lights':lights}
    return render(request, 'map/indexShowAddress.html', context)

@login_required
def getAddress(request):
    lights = Light.objects.all()
    lightAddresses = lights.values('address').order_by('address').distinct('address')
    lightAddresses = list(lightAddresses)
    lightAddressList = []
    for address in lightAddresses:
        lightAddressList.append(address['address'])

    return HttpResponse(json.dumps({'lightAddresses':lightAddressList}), content_type='application/json')

@login_required
def getData(request):
    address = request.GET.get('address').strip()
    #address = '中興大學'
    if not address:
        return HttpResponse('')
    lights = Light.objects.filter(address__icontains=address)
    lightAddresses = lights.values('value', 'time', 'address').order_by('time')
    lightAddresses = list(lightAddresses)   
    
    for light in lightAddresses:
        light['time'] = date.strftime(timezone.localtime(light['time']), '%Y-%m-%d %H:%M:%S')  # 為了移除秒數(因為丟到form會顯示秒數) 
    
    return HttpResponse(json.dumps({'lightAddresses':lightAddresses}), content_type='application/json')

