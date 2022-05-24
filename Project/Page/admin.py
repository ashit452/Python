from django.contrib import admin
from Page.models import page
from Language.models import language
from PageTranslation.models import pageTranslation

class ContentInline(admin.StackedInline):
    model = pageTranslation
    extra = 1
    max_num = language.objects.count()
    list_display = ['language','page','title','content']


class PageAdmin(admin.ModelAdmin):
    inlines = [ContentInline,]
    list_display = ['slug','status','sortOrder',]
    


admin.site.register(page,PageAdmin)
