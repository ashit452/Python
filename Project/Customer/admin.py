from datetime import datetime
from django.contrib import admin,messages
from django.http import HttpResponse, HttpResponseRedirect

from .apps import CustomerConfig
from .models import customer, customerGroup, customerAddress, city, state
from django.utils.html import format_html
from django.db import  IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from querystring_parser import parser
from dateutil import parser as dateparser
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string 
from django.utils.html import strip_tags
import random
from django.contrib import messages
from django.conf import settings
from hashlib import md5
import re
from django.shortcuts import render


# Register your models here.
class CustomerGroupAdmin(admin.ModelAdmin):
    list_display = ['customerGroupName','isDefault','createdAt','updatedAt',]

# image size validation
def validate_file_size(value):
        filesize= value.size
        
        if filesize > 8000000:
            return False
        else:
            return True

# password validation
def validate_password(value):
        password = value
        pattern_password = "(?=^.{8,}$)(?=.*\d)(?=.*[!@#$%^&*]+)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$"
        if len(password) < 8:
            return False
        elif not (re.fullmatch(pattern_password,password)):
            return False
        else:
            return True

# postalcode validation
def validate_postalcode(value):
    # err = ""
    if value == "":
        return False
    elif len(value) != 6:
        return False
    else:
        return True


class CustomerAdmin(admin.ModelAdmin):
    change_form_template = 'change_form.html'
    
    list_display = ['name','email','profile','customerGroup','verified','created','updated',]

    def profile(self,obj):
        return format_html(f'<img src ="/media/{obj.profileImage}" style="height:30; width:30px;">')

    def name(self,obj):
        return obj.firstName + " " + obj.lastName

    def verified(self,obj):
        if obj.emailVarificationDate == None:
            return "No"
        else:
            return "Yes"

    def created(self,obj):
        return obj.createdAt.strftime(CustomerConfig.date_format)

    def updated(self,obj):
        return obj.updatedAt.strftime(CustomerConfig.date_format)

    
            

    

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
        print(CustomerConfig.date_format)
         
        # add customer and address
        if obj is None:
            
            if request.method == 'POST':
                post_dict = parser.parse(request.POST.urlencode())
               
                fname= post_dict['firstName']
                lname = post_dict['lastName']
                mobile = post_dict['mobile']
                email = post_dict['email']
                profile = request.FILES['profile']
                
                password = post_dict['password']
                confirmPassword = post_dict['confirmpassword']
                custGrp = post_dict['customerGroup']
                verified = post_dict.get('verified',None)

                if validate_password(password):
                    if password == confirmPassword:
                        password = md5(password.encode()).hexdigest()
                        
                    else:
                        messages.error(request,"Exception: Enter Password and Confirmpassword same")
                        return HttpResponseRedirect('/admin/Customer/customer/add/')
                else:
                    messages.error(request,"Exception: Enter valid Password with 8 latters with numbers and ahlphabates")
                    return HttpResponseRedirect('/admin/Customer/customer/add/')

                

                try:
                    custgrpValue = customerGroup.objects.get(customerGroupId=custGrp)
                    
                except ObjectDoesNotExist:
                    messages.error(request,"Exception: Error occurs while adding Customer")
                    return HttpResponseRedirect('/admin/Customer/customer/add/')
                

                if validate_file_size(profile) and profile.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        if verified == 'on':
                            verifiedDate = datetime.now()
                            cust = customer(firstName = fname, lastName = lname, mobileNumber = mobile, email = email,profileImage = profile, password = password,customerGroup = custgrpValue,emailVarificationDate = verifiedDate)
                            cust.save()
                        else:
                            verifiedDate = None
                            cust = customer(firstName = fname, lastName = lname, mobileNumber = mobile, email = email,profileImage = profile, password = password,customerGroup = custgrpValue,emailVarificationDate = verifiedDate)
                            cust.save()
                            code=random.randint(000000,999999)    
                            html_content = render_to_string("resetEmail.html",{'uname':fname+" "+lname,"code":code})
                            text_content = strip_tags(html_content)
                            mail = EmailMultiAlternatives(
                            "Email Verification Link",
                            text_content,
                            settings.EMAIL_HOST_USER,
                            [email],
                            )
                            mail.attach_alternative(html_content,"text/html")
                            mail.send()
                            
                            
                            customer.objects.filter(email = email).update(code=code,emailSentOn = datetime.now())

                        
                    except ValueError or IntegrityError:
                        messages.error(request,"Exception: Error occurs while adding Customer")
                        return HttpResponseRedirect('/admin/Customer/customer/add/')
                else:
                        messages.error(request,"Exception: Enter Image file like(.png, .jpg, .jpeg) and size Under 8 MB")
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

                    if name != '' and building != '' and street != '' and landmark != '' and postalcode != '' and cityid != '' and state != '':

                        if default == 'on':
                            default = True
                        else:
                            default = False

                    
                        cityValue = city.objects.get(cityId=cityid)
                        
                        stateValue = state.objects.get(stateId=stateid)
                        latestCustomer = customer.objects.latest("customerId")
                        
                        customerobj = customer.objects.get(customerId=latestCustomer.customerId)

                        # if validate_postalcode(postalcode):
                        #     addr = customerAddress(addressName = name, building = building, street = street, postalCode =postalcode, city = cityValue,state = stateValue, landMark =landmark, customer = customerobj,isDefault = default)
                        #     addr.save()
                        # else:
                        #     context['postal_err'] = "Please enter 6 digits for postalcode"
                        #     return super(CustomerAdmin,self).changeform_view(request, obj ,form_url,context)
                        addr = customerAddress(addressName = name, building = building, street = street, postalCode =postalcode, city = cityValue,state = stateValue, landMark =landmark, customer = customerobj,isDefault = default)
                        addr.save()
                        
                    


                messages.success(request,fname+" added successfully")
                return HttpResponseRedirect('/admin/Customer/customer')

        else:
            customerDetails = customer.objects.raw("select * from customer_customer c where c.customerId='"+obj+"'")
            context["customerDetails"] = customerDetails
            oldemail = customerDetails[0].email
            customerAddressDetails = customerAddress.objects.raw("select * from customer_customerAddress where customer_id='"+obj+"'")
            context["customerAddressDetails"] = customerAddressDetails


           # update customer and address 
            if request.method == 'POST':
                post_dict = parser.parse(request.POST.urlencode())
                print(post_dict,request.FILES)
                cid = post_dict['cid']
                fname= post_dict['firstName']
                lname = post_dict['lastName']
                mobile = post_dict['mobile']
                email = post_dict['email']
                profile = request.FILES.get('profile',None)
                
                password = post_dict['password']
                confirmPassword = post_dict['confirmpassword']
                custGrp = post_dict['customerGroup']
                verified = post_dict.get('verified',None)
                verificationdate = post_dict.get('verificationdate',None)


                

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
                

                
                try:
                    if profile != None:
                        if validate_file_size(profile) and profile.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                            cust = customer.objects.get(customerId=cid)
                            cust.profileImage.delete()
                            cust.profileImage = profile
                            cust.save()
                        else:
                            messages.error(request,"Exception: Enter Image file like(.png, .jpg, .jpeg) and size Under 8 MB")
                            return HttpResponseRedirect('/admin/Customer/customer/')

                    if password == '':
                        custupdt = customer.objects.filter(customerId=cid).update(firstName = fname, lastName = lname, mobileNumber = mobile, email = email,customerGroup = custgrpValue,emailVarificationDate = verifiedDate)
                    elif validate_password(password):
                        if password == confirmPassword:
                            password = md5(password.encode()).hexdigest()
                            
                            custupdt = customer.objects.filter(customerId=cid).update(firstName = fname, lastName = lname, mobileNumber = mobile, email = email,password = password,customerGroup = custgrpValue,emailVarificationDate = verifiedDate)
                        else:
                            messages.error(request,"Exception: Enter Password and Confirmpassword same")
                            return HttpResponseRedirect('/admin/Customer/customer')
                    else:
                        messages.error(request,"Exception: please enter strong password(1 Uppercase, 1 Lowercase, 1 Symbol, 1 Number) with minimum 8 latters")
                        return HttpResponseRedirect('/admin/Customer/customer')

                    if oldemail != email:
                        code=random.randint(000000,999999)    
                        html_content = render_to_string("resetEmail.html",{'uname':fname+" "+lname,"code":code})
                        text_content = strip_tags(html_content)
                        mail = EmailMultiAlternatives(
                        "Email Verification Link",
                        text_content,
                        settings.EMAIL_HOST_USER,
                        [email],
                        )
                        mail.attach_alternative(html_content,"text/html")
                        mail.send()
                        
                        customer.objects.filter(customerId = cid).update(code=code,emailVarificationDate = None,emailSentOn = datetime.now())

                    
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

                    if ((addrid == '' or addrid == None) and (cityid != '' or cityid == None) and stateid != '' and name != '' and building !='' and street != '' and landmark != '' and postalcode != ''): 
                        if default == 'on':
                            default = True
                        else:
                            default = False

                    
                        cityValue = city.objects.get(cityId=cityid)
                        
                        stateValue = state.objects.get(stateId=stateid)
                        
                        customerobj = customer.objects.get(customerId=obj)
                        
                        addr = customerAddress(addressName = name, building = building, street = street, postalCode =postalcode, city = cityValue,state = stateValue, landMark =landmark, customer = customerobj,isDefault = default)
                        addr.save()
                    
                    
                    elif(addrid != '' and addrid != None):
                        

                    
                        cityValue = city.objects.get(cityId=cityid)
                        
                        stateValue = state.objects.get(stateId=stateid)
                        if default == 'on':
                            default = True
                            customerAddress.objects.filter(isDefault=True).filter(customer=obj).update(isDefault=False)
                            addr = customerAddress.objects.filter(customerAddressId = addrid).update(addressName = name, building = building, street = street, postalCode =postalcode, city = cityValue,state = stateValue, landMark =landmark,isDefault = default)
                        
                        else:
                            default = False
                            addr = customerAddress.objects.filter(customerAddressId = addrid).update(addressName = name, building = building, street = street, postalCode =postalcode, city = cityValue,state = stateValue, landMark =landmark,isDefault = default)
                    
                    else:
                        messages.success(request,fname+" updated successfully")
                        return HttpResponseRedirect('/admin/Customer/customer')
                        
                       
                    
                            
                        
                            
                    
                messages.success(request,fname+" updated successfully")
                return HttpResponseRedirect('/admin/Customer/customer')
            
        return super(CustomerAdmin,self).changeform_view(request, obj ,form_url,context)


admin.site.register(customerGroup,CustomerGroupAdmin)
admin.site.register(customer,CustomerAdmin)


