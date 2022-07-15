from django.db import models
from tinymce import models as tinymce_models
from Language.models import language

class block(models.Model):
    blockId = models.AutoField(primary_key=True)
    slug = models.CharField(max_length=100,unique=True,default=None)
    statusChoice = (
        ('enabled','Enabled'),
        ('disabled','Disabled'),
    )
    status = models.CharField(max_length=10,choices=statusChoice,default='enabled')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug) 

def get_language():
    return language.objects.get(isDefault=True)

class blockTranslation(models.Model):
    language = models.ForeignKey(language,on_delete = models.CASCADE,null=False,default=get_language)
    block = models.ForeignKey(block,on_delete = models.CASCADE,null=False)
    blockTranslationId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = tinymce_models.HTMLField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Block Translation"
        unique_together = ('language', 'block',)

    def __str__(self):
        return str(self.title)  