from codecs import StreamWriter
from datetime import datetime
from django.contrib import admin,messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import customer, customerGroup, customerAddress, city, state
from django.utils.html import format_html
from django.db import  IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from querystring_parser import parser
from dateutil import parser as dateparser



# Register your models here.
class CustomerGroupAdmin(admin.ModelAdmin):
    list_display = ['customerGroupName','isDefault','createdAt','updatedAt',]

def validate_file_size(value):
        filesize= value.size
        
        if filesize > 8000000:
            return False
        else:
            return True


class CustomerAdmin(admin.ModelAdmin):
    change_form_template = 'change_form.html'
    
    list_display = ['name','email','profile','customerGroup','verified','createdAt','updatedAt',]

    def profile(self,obj):
        return format_html(f'<img src ="/media/{obj.profileImage}" style="height:30; width:30px;">')

    def name(self,obj):
        return obj.firstName + " " + obj.lastName

    def verified(self,obj):
        if obj.emailVarificationDate == None:
            return "No"
        else:
            return "Yes"

    

    def changeform_view(self, request,obj ,form_url,context=None):
        context = context or {}
        customerData = customer.objects.all()
        context['customerData'] = customerData
        custGroup = customerGroup.objects.all()
        context["customerGroup"]=custGroup
        st = state.objects.all()
        context["state"]=st
        ct = city.objects.all()
        context["city"]=ct

         
        # add customer and address
        if obj is None:
            
            if request.method == 'POST':
                post_dict = parser.parse(request.POST.urlencode())
                print(post_dict)
                fname= post_dict['firstName']
                lname = post_dict['lastName']
                mobile = post_dict['mobile']
                email = post_dict['email']
                profile = request.FILES['profile']
                print(profile)
                password = post_dict['password']
                confirmPassword = post_dict['confirmpassword']
                custGrp = post_dict['customerGroup']
                verified = post_dict.get('verified',None)

                if password == confirmPassword:
                    password = password
                else:
                    messages.error(request,"Exception: Enter Password and Confirmpassword same")
                    return HttpResponseRedirect('/admin/Customer/customer/add/')

                if verified == 'on':
                    verifiedDate = datetime.now()
                else:
                    verifiedDate = None

                try:
                    custgrpValue = customerGroup.objects.get(customerGroupId=custGrp)
                    
                except ObjectDoesNotExist:
                    messages.error(request,"Exception: Error occurs while adding Customer")
                    return HttpResponseRedirect('/admin/Customer/customer/add/')
                

                if validate_file_size(profile):
                    try:
                        cust = customer(firstName = fname, lastName = lname, mobileNumber = mobile, email = email,profileImage = profile, password = password,customerGroup = custgrpValue,emailVarificationDate = verifiedDate)
                        cust.save()
                        
                    except ValueError or IntegrityError:
                        messages.error(request,"Exception: Error occurs while adding Customer")
                        return HttpResponseRedirect('/admin/Customer/customer/add/')
                else:
                        messages.error(request,"Exception: Enter Image Under 8 MB")
                        return HttpResponseRedirect('/admin/Customer/customer/add/')

                for i in post_dict['address']:
                    name = post_dict['address'][i]['name']
                    building = post_dict['address'][i]['building']
                    street = post_dict['address'][i]['street']
                    landmark = post_dict['address'][i]['landmark']
                    postalcode = post_dict['address'][i]['postalcode']
                    cityid = post_dict['address'][i]['city']
                    stateid = post_dict['address'][i]['state']
                    default = post_dict['address'][i].get('defaultaddr',None)

                    

                    if default == 'on':
                        default = True
                    else:
                        default = False

                
                    cityValue = city.objects.get(cityId=cityid)
                    print(cityValue)
                    stateValue = state.objects.get(stateId=stateid)
                    latestCustomer = customer.objects.latest("customerId")
                    print(latestCustomer.customerId)
                    customerobj = customer.objects.get(customerId=latestCustomer.customerId)
                    print("obj", customerobj)
                    addr = customerAddress(addressName = name, building = building, street = street, postalCode =postalcode, city = cityValue,state = stateValue, landMark =landmark, customer = customerobj,isDefault = default)
                    addr.save()
                        
                    


                messages.success(request,fname+" added successfully")
                return HttpResponseRedirect('/admin/Customer/customer')

        else:
            customerDetails = customer.objects.raw("select * from customer_customer c where c.customerId='"+obj+"'")
            context["customerDetails"] = customerDetails
            customerAddressDetails = customerAddress.objects.raw("select * from customer_customerAddress where customer_id='"+obj+"'")
            context["customerAddressDetails"] = customerAddressDetails


            #update customer and address
            if request.method == 'POST':
                post_dict = parser.parse(request.POST.urlencode())
                print(post_dict)
                # print(request.POST,"..",request.FILES)
                cid = post_dict['cid']
                fname= post_dict['firstName']
                lname = post_dict['lastName']
                mobile = post_dict['mobile']
                email = post_dict['email']
                profile = request.FILES['profile']
                print(profile)
                password = post_dict['password']
                confirmPassword = post_dict['confirmpassword']
                custGrp = post_dict['customerGroup']
                verified = post_dict.get('verified',None)
                verificationdate = post_dict.get('verificationdate',None)


                if password == confirmPassword:
                    password = password
                else:
                    messages.error(request,"Exception: Enter Password and Confirmpassword same")
                    return HttpResponseRedirect('/admin/Customer/customer/add/')

                if verified == 'on':
                    verifiedDate = datetime.now()
                elif verificationdate != None:
                    verifiedDate = dateparser.parse(verificationdate)
                else:
                    verifiedDate = None

                
                try:
                    custgrpValue = customerGroup.objects.get(customerGroupId=custGrp)
                    
                except ObjectDoesNotExist:
                    messages.error(request,"Exception: Error occurs while adding Customer")
                    return HttpResponseRedirect('/admin/Customer/customer/add/')
                

                if validate_file_size(profile):
                    try:
                        cust = customer.objects.get(customerId=cid)
                        cust.profileImage.delete()
                        cust.profileImage = profile
                        cust.save()
                        
                        custupdt = customer.objects.filter(customerId=cid).update(firstName = fname, lastName = lname, mobileNumber = mobile, email = email,password = password,customerGroup = custgrpValue,emailVarificationDate = verifiedDate)
                        

                        
                    except ValueError or IntegrityError:
                        messages.error(request,"Exception: Error occurs while updating Customer")
                        return HttpResponseRedirect('/admin/Customer/customer')

                    for i in post_dict['address']:
                        
                        addrid = post_dict['address'][i].get('addrid',None)
                        name = post_dict['address'][i]['name']
                        building = post_dict['address'][i]['building']
                        street = post_dict['address'][i]['street']
                        landmark = post_dict['address'][i]['landmark']
                        postalcode = post_dict['address'][i]['postalcode']
                        cityid = post_dict['address'][i].get('city',None)
                        stateid = post_dict['address'][i]['state']
                        default = post_dict['address'][i].get('defaultaddr',None)

                        #update old customer address
                        if(addrid != '' and addrid != None):
                            if default == 'on':
                                default = True
                            else:
                                default = False

                        
                            cityValue = city.objects.get(cityId=cityid)
                            print(cityValue)
                            stateValue = state.objects.get(stateId=stateid)
                            
                            addr = customerAddress.objects.filter(customerAddressId = addrid).update(addressName = name, building = building, street = street, postalCode =postalcode, city = cityValue,state = stateValue, landMark =landmark,isDefault = default)

                        #update customer with new address    
                        elif (addrid == '' or addrid == None and cityid != '' or cityid == None and stateid != '' and name != '' and building !='' and street != '' and landmark != '' and postalcode != '' and default != '' or default != None): 
                            if default == 'on':
                                default = True
                            else:
                                default = False

                        
                            cityValue = city.objects.get(cityId=cityid)
                            print(cityValue)
                            stateValue = state.objects.get(stateId=stateid)
                            
                            customerobj = customer.objects.get(customerId=obj)
                            print("obj", customerobj)
                            addr = customerAddress(addressName = name, building = building, street = street, postalCode =postalcode, city = cityValue,state = stateValue, landMark =landmark, customer = customerobj,isDefault = default)
                            addr.save()
                            
                        
                            
                    
                messages.success(request,fname+" updated successfully")
                return HttpResponseRedirect('/admin/Customer/customer')
            
        return super(CustomerAdmin,self).changeform_view(request, obj ,form_url,context)


admin.site.register(customerGroup,CustomerGroupAdmin)
admin.site.register(customer,CustomerAdmin)
admin.site.register(customerAddress)

