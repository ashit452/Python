from django.db import models
from Attribute.models import attribute
from Language.models import language

# Create your models here.

class attributeTranslation(models.Model):
    attributeTranslationId = models.AutoField(primary_key=True)
    language = models.ForeignKey(language,on_delete = models.CASCADE,null=False)
    name = models.CharField(max_length=200)
    attribute = models.ForeignKey(attribute,on_delete=models.CASCADE,null=False)
