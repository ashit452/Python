from django.contrib import admin
from Attribute.models import attribute,attributeTranslation,option,optionTranslation
from django.http import HttpResponseRedirect
from Language.models import language

from django.contrib import messages
from django.template.defaulttags import register
...
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Register your models here.
class AttributeAdmin(admin.ModelAdmin):
    def changeform_view(self, request, obj, form_url, context=None):
        context = context or {}
        languageData = language.objects.filter(status = "enabled")
        context["language"]=languageData
        
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
                for i in range(10):
                    customOption = request.POST['option['+str(i)+'][customoption]']
                    print(customOption)
            #     order = request.POST['order']
            #     default = request.POST['default']
            #     if default == 'on':
            #         default = True
            #     else:
            #         default = False

            #     opt = option(customOption=customOption,sortOrder=order,isDefault=default,attribute=attrId)
            #     opt.save()

            #     optId = option.objects.get(customOption=customOption)

            #     for i in languageData:
            #         optName = request.POST[i.locale+'opname']
            #         optLang = request.POST[i.locale+'oplanguage']
            #         optLangId = language.objects.get(locale=optLang)

            #         optTrans = optionTranslation(name=optName,language=optLangId,option=optId)
            #         optTrans.save()

            # messages.success(request,code+" added successfully")
            return HttpResponseRedirect('/admin/Attribute/attribute/')


        
        return super(AttributeAdmin,self).changeform_view(request, obj ,form_url,context)

admin.site.register(attribute,AttributeAdmin)
admin.site.register(option)
admin.site.register(optionTranslation)

