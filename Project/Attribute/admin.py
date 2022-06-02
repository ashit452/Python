from django.contrib import admin
from Attribute.models import attribute,attributeTranslation,option,optionTranslation
from django.http import HttpResponseRedirect
from Language.models import language
import re

from django.contrib import messages
from django.template.defaulttags import register
...
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Register your models here.
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['code','inputType','isRequired']
    def changeform_view(self, request, obj, form_url, context=None):
        context = context or {}
        languageData = language.objects.filter(status = "enabled")
        context["language"]=languageData

        if obj is None:
        
            if request.method == 'POST':
                code= request.POST['code']
                input = request.POST['inputtype']
                required = request.POST['required']

                attr = attribute(code=code,inputType=input,isRequired=required)
                attr.save()

                attrId = attribute.objects.get(code=code)

                for i in languageData:
                    name = request.POST[i.locale+'name']
                    lang = request.POST[i.locale+'language']
                    langId = language.objects.get(locale=lang)

                    attrTrans = attributeTranslation(name=name,language=langId,attribute=attrId)
                    attrTrans.save()
                
                if input in ['radio','checkbox','select','multiselect']:
                    reObj = re.compile('option')
                    ls = []
                    for key in request.POST.keys():
                        if(reObj.match(key)):
                            ls.append(key)

                    div = (language.objects.count() * 2) + 3
                    print(div)
                            
                    for i in range(round(len(ls)/div)):
                        print(i)
                        customOption = request.POST['option['+str(i)+'][customoption]']
                        order = request.POST['option['+str(i)+'][order]']
                        default = request.POST['option['+str(i)+'][default]']
                        if default == 'on':
                            default = True
                        else:
                            default = False

                        opt = option(customOption=customOption,sortOrder=order,isDefault=default,attribute=attrId)
                        opt.save()

                        optId = option.objects.get(customOption=customOption)

                        for lang in languageData:
                            optName = request.POST['option'+lang.locale+'['+str(i)+'][opname]']
                            optLang = request.POST['option'+lang.locale+'['+str(i)+'][oplanguage]']
                            optLangId = language.objects.get(locale=optLang)

                            optTrans = optionTranslation(name=optName,language=optLangId,option=optId)
                            optTrans.save()

                    messages.success(request,code+" added successfully")
                return HttpResponseRedirect('/admin/Attribute/attribute/')

        else:
            attributeDetails = attribute.objects.filter(attributeId=obj)
            print("details",attributeDetails)
            context['attributeDetails'] = attributeDetails

            optionDetails = option.objects.raw("select * from attribute_option as o where o.attribute_id ='"+obj+"'")
            print("details",optionDetails)
            context['optionDetails'] = optionDetails

            attributeNames = {}
            attributeTranslationDetails = attributeTranslation.objects.raw("select * from attribute_attributetranslation as at inner join language_language l on at.language_id = l.locale where at.attribute_id='"+obj+"'")

            for lang in languageData:
                for i in attributeTranslationDetails:
                    if lang.locale == i.locale:
                        print(i.name)
                        attributeNames[lang.locale] = {"language":i.locale,'name':i.name,"attributeTranslationId":i.attributeTranslationId}
                print("attribute",attributeNames[lang.locale])

            context['attributeNames'] = attributeNames

            optionNames = {}
            optionTranslationDetails = optionTranslation.objects.raw("select * from attribute_optiontranslation as ot inner join language_language l on ot.language_id = l.locale inner join attribute_option as o on o.optionId=ot.option_id where o.attribute_id='"+obj+"'")
            context['optionTranslationDetails'] = optionTranslationDetails

            for lang in languageData:
                optionNames[lang.locale] = {}
                for i in optionTranslationDetails:
                    if i.locale == lang.locale:
                        optionNames[lang.locale][i.customOption]= {"language":i.locale,'name':i.name,"optionTranslationId":i.optionTranslationId}
            # for j in attributeDetails:
            #     for i in optionTranslationDetails:
            #         optionNames[i.customOption] ={}
            #         optionNames[i.customOption][i.locale] = {"language":i.locale,'name':i.name,"optionTranslationId":i.optionTranslationId}
            print("option",optionNames)

            context['optionNames'] = optionNames

        
        return super(AttributeAdmin,self).changeform_view(request, obj ,form_url,context)

admin.site.register(attribute,AttributeAdmin)

