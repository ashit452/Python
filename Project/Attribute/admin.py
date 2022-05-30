from django.contrib import admin
from Attribute.models import attribute
from Option.models import option
from AttributeTranslation.models import attributeTranslation
from OptionTranslation.models import optionTranslation
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
    def changeform_view(self, request,obj ,form_url,context=None):
        context = context or {}
        languageData = language.objects.filter(status = "enabled")
        context["language"]=languageData
        print(context["language"])

        
        return super(AttributeAdmin,self).changeform_view(request, obj ,form_url,context)

admin.site.register(attribute,AttributeAdmin)

