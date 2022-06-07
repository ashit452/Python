from django.contrib import admin
from Attribute.models import attribute,attributeTranslation,option,optionTranslation
from django.http import HttpResponse, HttpResponseRedirect
from Language.models import language
from django.db import  IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from querystring_parser import parser


from django.contrib import messages
from django.template.defaulttags import register
...
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


class Error(Exception):
   pass


class FetchDataError(Error):
    pass

# Register your models here.
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['code','inputType','isRequired']
    def changeform_view(self, request, obj, form_url, context=None):
        context = context or {}
        languageData = language.objects.filter(status = "enabled")
        context["language"]=languageData

        if obj is None:
            
            if request.method == 'POST':
                post_dict = parser.parse(request.POST.urlencode())
                
                code= post_dict['code']
                input = post_dict['inputtype']
                required = post_dict['required']

                try:
                    attr = attribute(code=code,inputType=input,isRequired=required)
                    attr.save()
                except IntegrityError:
                    messages.error(request,"Exception: Error occurs while adding the attribute")
                    return HttpResponseRedirect('/admin/Attribute/attribute/add/')
                    # return HttpResponse("Exception: Error occurs while adding the attribute")

                try:
                    attrId = attribute.objects.get(code=code)
                except ObjectDoesNotExist:
                    return HttpResponse("Exception: Error occurs while fetching attribute id")

                for i in languageData:
                    
                    name = request.POST[i.locale+'name']
                    lang = request.POST[i.locale+'language']
                    langId = language.objects.get(locale=lang)

                    try:
                        attrTrans = attributeTranslation(name=name,language=langId,attribute=attrId)
                        attrTrans.save()
                    except ValueError or IntegrityError:
                        messages.error(request,"Exception: Error occurs while adding the attributeTranslation")
                        return HttpResponseRedirect('/admin/Attribute/attribute/add/')
                        # return HttpResponse("Exception: Error occurs while adding the attributeTranslation")
                
                if input in ['radio','checkbox','select','multiselect']:
                    
                    for i in post_dict['option']:
                        
                        customOption = post_dict['option'][i]['customoption']
                        order = post_dict['option'][i]['order']
                        default = post_dict['option'][i].get('default',None)
                        if default == 'on':
                            defaultval = True
                        else:
                            defaultval = False
                        

                        try:
                            opt = option(customOption=customOption,sortOrder=order,isDefault=defaultval,attribute=attrId)
                            opt.save()
                        except IntegrityError:
                            return HttpResponse("Exception: Error occurs while adding the options")

                        try:
                            optId = option.objects.get(customOption=customOption)
                        except ObjectDoesNotExist:
                            return HttpResponse("Exception: Error occurs while getting option id")

                        
                        for lang in languageData:
                            
                            optName = post_dict['option'+lang.locale][i]['opname']
                            optLang = post_dict['option'+lang.locale][i]['oplanguage']
                            optLangId = language.objects.get(locale=optLang)
                            
                            try:
                                optTrans = optionTranslation(name=optName,language=optLangId,option=optId)
                                optTrans.save()
                            except IntegrityError:
                                return HttpResponse("Exception: Error occurs while adding the optionTranslation")

                messages.success(request,code+" added successfully")
                return HttpResponseRedirect('/admin/Attribute/attribute/')
                

        else:
            attributeDetails = attribute.objects.filter(attributeId=obj)
           
            context['attributeDetails'] = attributeDetails

            optionDetails = option.objects.raw("select * from attribute_option as o where o.attribute_id ='"+obj+"'")
            
            context['optionDetails'] = optionDetails
            

            attributeNames = {}
            attributeTranslationDetails = attributeTranslation.objects.raw("select * from attribute_attributetranslation as at inner join language_language l on at.language_id = l.locale where at.attribute_id='"+obj+"'")

            for lang in languageData:
                for i in attributeTranslationDetails:
                    
                    if lang.locale == i.locale:
                        attributeNames["attributeTranslationId"] = i.attributeTranslationId
                        attributeNames[lang.locale] = {"language":i.locale,'name':i.name,'attributeTranslationId':i.attributeTranslationId}
            

            context['attributeNames'] = attributeNames

            optionNames = {}
            optionTranslationDetails = optionTranslation.objects.raw("select * from attribute_optiontranslation as ot inner join language_language l on ot.language_id = l.locale inner join attribute_option as o on o.optionId=ot.option_id where o.attribute_id='"+obj+"'")
            

            for lang in languageData:
                optionNames[lang.locale] = {}
                for i in optionTranslationDetails:
                    
                    if i.locale == lang.locale:
                        optionNames[lang.locale][i.customOption]= {"language":i.locale,'name':i.name,"optionTranslationId":i.optionTranslationId}
            
            
            context['optionNames'] = optionNames

            try:
                if context['attributeDetails'] is None or context['optionDetails'] is None or context['attributeNames'] is None or context['optionNames'] is None:
                    raise FetchDataError
            except FetchDataError:
                return HttpResponse("Exception: Error occurs while fetching attribute details")

            if request.method == 'POST':
                post_dict = parser.parse(request.POST.urlencode())
                

                if(post_dict.get('deletedata') is not None):
                    for dlt in post_dict['deletedata']:
                        option.objects.filter(optionId=post_dict['deletedata'][dlt]).delete() 

                attrId = post_dict['attributeid']
                code= post_dict['code']
                input = post_dict['inputtype']
                required = post_dict['required']

                attr = attribute.objects.filter(attributeId=attrId).update(code=code,inputType=input,isRequired=required)
               

                for i in languageData:
                    name = post_dict[i.locale+'name']
                    lang = post_dict[i.locale+'language']
                    langId = language.objects.get(locale=lang)
                    
                    attrTransId = request.POST[i.locale+'attributetranslationid']
                

                    attrTrans = attributeTranslation.objects.filter(attributeTranslationId=attrTransId).update(name=name,language=langId,attribute=attrId)
                
                if input in ['radio','checkbox','select','multiselect']:                  
                    for i in post_dict['option']:
                        
                        optId = post_dict['option'][i].get('optionid',None)
                        customOption = post_dict['option'][i]['customoption']
                        order = post_dict['option'][i]['order']
                        default = post_dict['option'][i].get('default',None)
                        
                        if default == 'on':
                            defaultval = True
                        else:
                            defaultval = False
                        
                        if optId == None:
                            try:
                                attribute_id = attribute.objects.get(attributeId=attrId)
                                opt = option(customOption=customOption,sortOrder=order,isDefault=defaultval,attribute=attribute_id)
                                opt.save()
                            except IntegrityError:
                                return HttpResponse("Exception: Error occurs while adding the options")
                        else:
                            opt = option.objects.filter(optionId=optId).update(customOption=customOption,sortOrder=order,isDefault=defaultval,attribute=attrId)

                        for lang in languageData:
                            optName = post_dict['option'+lang.locale][i]['opname']
                            optLang = post_dict['option'+lang.locale][i]['oplanguage']
                            optTransId = post_dict['option'+lang.locale][i].get('optiontranslationid',None)
                            optLangId = language.objects.get(locale=optLang)

                            if optTransId == None:
                                try:
                                    optId = option.objects.get(customOption=customOption)
                                    optTrans = optionTranslation(name=optName,language=optLangId,option=optId)
                                    optTrans.save()
                                except ObjectDoesNotExist or IntegrityError:
                                    return HttpResponse("Exception: Error occurs while adding optionTranslation")
                            else:
                                optTrans = optionTranslation.objects.filter(optionTranslationId=optTransId).update(name=optName,language=optLangId,option=optId)

                else:
                    option.objects.filter(attribute=attrId).delete() 
                messages.success(request,code+" updated successfully")
                return HttpResponseRedirect('/admin/Attribute/attribute/')

        
        return super(AttributeAdmin,self).changeform_view(request, obj ,form_url,context)

admin.site.register(attribute,AttributeAdmin)

