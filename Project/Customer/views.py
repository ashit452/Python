import re
from django.shortcuts import render,redirect
from .models import city, customer, customerAddress
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime, timedelta
from django.utils import timezone
# Create your views here.
data ={}

def home(request):
    return render(request,"home.html")

def getcitiesajax(request):
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
    
    i = customerAddress.objects.get(customerAddressId = id[:-1])
    i.delete()
    return JsonResponse("sucess", safe = False) 

def edit(request):
    id = request.GET.get('id')
    
    try:            
        custaddr = customerAddress.objects.all().filter(customerAddressId=id[:-1])
    except Exception:
        data['error_message'] = 'error'
        return JsonResponse(data)
    return JsonResponse(list(custaddr.values()), safe = False)
    
def emailverify(request):
    code=request.GET.get("code")
    isData=customer.objects.filter(code=code)
    
    present = datetime.now()
    
    if request.method =="POST":
        verified=request.POST.get('verified',None)

        
        if isData.count()>0 and verified == 'yes':
            verifiedDate = datetime.now()
            customer.objects.filter(code=code).update(emailVarificationDate = verifiedDate,code="000000")
            messages.add_message(request, messages.SUCCESS, 'Your email verification Done sucessfully')
            return redirect("/customer")
        else:
            customer.objects.filter(code=code).update(code="000000")
            messages.add_message(request, messages.ERROR, 'Not verified you as our customer')
            return redirect("/customer")
    

        
    if isData.count()>0:
        expiry = isData[0].emailSentOn.replace(tzinfo=None) + timedelta(minutes=10)
    
        if present < expiry:
            return render(request, 'emailVerification.html',{"code":code})
    
        else:
            messages.add_message(request, messages.ERROR, 'Verification link is expired')
            return redirect("/customer")
    
    else:
        messages.add_message(request, messages.ERROR, 'Verification link is expired')
        return redirect("/customer")