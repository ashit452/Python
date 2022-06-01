from django.db import models
from Language.models import language
from django.db import transaction

# Create your models here.

class attribute(models.Model):
    attributeId = models.AutoField(primary_key=True)
    code = models.CharField(("Code"),unique=True,max_length=50)
    inputChoice = (
        ('boolean','Boolean'),
        ('checkbox','Checkbox'),
        ('multiselect','Multi-select'),
        ('select','Select'),
        ('radio','Radio'),
        ('textbox','Textbox'),
        ('textarea','Textarea'),
    )
    inputType = models.CharField(("Input Type"),max_length=50,choices=inputChoice,default='text')
    requiredChoice = (
        ('yes','Yes'),
        ('no','No'),
    )
    isRequired = models.CharField(("Is Required"),max_length=10,choices=requiredChoice,default='yes')

class attributeTranslation(models.Model):
    attributeTranslationId = models.AutoField(primary_key=True)
    language = models.ForeignKey(language,on_delete = models.CASCADE,null=False)
    name = models.CharField(max_length=200)
    attribute = models.ForeignKey(attribute,on_delete=models.CASCADE,null=False)

class option(models.Model):
    optionId = models.AutoField(primary_key=True)
    attribute = models.ForeignKey(attribute,on_delete=models.CASCADE,null=False)
    customOption = models.CharField(("Custom Option"),max_length=100,unique=True)
    sortOrder = models.IntegerField(("Sort Order"),default=1)
    isDefault = models.BooleanField(("Is Default"),default=False)

    def save(self, *args, **kwargs):
        if not self.isDefault:
            return super(option, self).save(*args, **kwargs)
        with transaction.atomic():
            option.objects.filter(
                isDefault=True).update(isDefault=False)
            return super(option, self).save(*args, **kwargs)

class optionTranslation(models.Model):
    optionTranslationId = models.AutoField(primary_key=True)
    language = models.ForeignKey(language,on_delete = models.CASCADE,null=False)
    name = models.CharField(max_length=250)
    option = models.ForeignKey(option,on_delete=models.CASCADE,null=False)

     
