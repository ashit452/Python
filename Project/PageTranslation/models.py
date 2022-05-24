from django.db import models
from tinymce import models as tinymce_models
from Language.models import language
from Page.models import page


# Create your models here.
def get_language():
    return language.objects.get(isDefault=True)

class pageTranslation(models.Model):
    language = models.ForeignKey(language,on_delete = models.CASCADE,null=False,default=get_language)
    page = models.ForeignKey(page,on_delete = models.CASCADE,null=False)
    contentId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = tinymce_models.HTMLField()

    class Meta:
        verbose_name = "Page Translation"
        unique_together = ('language', 'page',)

    def __str__(self):
        return str(self.title)   