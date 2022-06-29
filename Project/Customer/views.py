from django.shortcuts import render,redirect
from .models import city, customerAddress
from django.http import JsonResponse

# Create your views here.
data ={}
def getcitiesajax(request):
    print("hello")
    if request.method == "POST":
        stateName = request.POST['statename']
        try:            
            cities = city.objects.all().filter(stateName=stateName)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(cities.values('cityId', 'cityName')), safe = False)  

def delete(request):
    id = request.GET.get('id')
    print(id)
    i = customerAddress.objects.get(customerAddressId = id[:-1])
    i.delete()
    return JsonResponse("sucess", safe = False) 

def edit(request):
    id = request.GET.get('id')
    print(id)
    try:            
        custaddr = customerAddress.objects.all().filter(customerAddressId=id[:-1])
    except Exception:
        data['error_message'] = 'error'
        return JsonResponse(data)
    return JsonResponse(list(custaddr.values()), safe = False)
    
    
    