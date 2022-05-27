from django.db import models

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
     
