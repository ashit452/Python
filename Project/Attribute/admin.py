from django.contrib import admin
from Attribute.models import attribute
from Option.models import option
from AttributeTranslation.models import attributeTranslation
from OptionTranslation.models import optionTranslation
# Register your models here.
admin.site.register(attribute)
admin.site.register(option)
admin.site.register(attributeTranslation)
admin.site.register(optionTranslation)
