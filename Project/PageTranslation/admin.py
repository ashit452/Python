import re
from django.contrib import admin
from django.http import HttpResponseRedirect
from Language.models import language
from PageTranslation.forms import PageTranslationForm
from Page.models import page

from PageTranslation.models import pageTranslation

class PageTranslationAdmin(admin.ModelAdmin):
    list_display = ['title','language','page']

    def changeform_view(self, request,obj = None,form_url ='',context=None):
    
        languageData = language.objects.filter(status = "enabled")
        print(languageData)
        for i in languageData:
            print(i.title)
       
        context = context or {}
        context["language"]=languageData
        if request.method == 'POST':
            pageSlug = request.POST['page']
            title = request.POST['title']
            content = request.POST['content']
            lang = request.POST['lang']

            translation = pageTranslation(page=pageSlug,title=title,content=content,language=lang)
            translation.save()
        
        #     context["form"] = PageTranslationForm(request.POST)
        #
        #     if context["form"].is_valid():
        #         
                # # form = context['form'].save(commit=False)
                # context['form'].cleaned_data["language"]= language.objects.get(locale="cn")
                # print("hello",context['form'].data)
                # context['form'].save()
            return HttpResponseRedirect('/admin/PageTranslation/pagetranslation/')

        else:
                context['pages'] = page.objects.filter(status="enabled")
                print(context['pages'])
        

       
        return super(PageTranslationAdmin,self).changeform_view(request, obj ,form_url,context)

admin.site.register(pageTranslation,PageTranslationAdmin)