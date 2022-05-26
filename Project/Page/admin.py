from django.contrib import admin
from django.http import HttpResponseRedirect
from Page.models import page
from Language.models import language
from PageTranslation.models import pageTranslation
from PageTranslation.forms import PageTranslationForm

    
class PageAdmin(admin.ModelAdmin):
    # inlines = [ContentInline,]
    list_display = ['slug','status','sortOrder',]
    def changeform_view(self, request,obj ,form_url,context=None):
        context = context or {}
        languageData = language.objects.filter(status = "enabled")
        context["language"]=languageData

        if obj is None:
            
            if request.method == 'POST':
                slug = request.POST['slug']
                status = request.POST['status']
                sortOrder = request.POST['order']

                pageObj = page(slug=slug,status=status,sortOrder=sortOrder)
                pageObj.save()

                for i in languageData:
                
                    title = request.POST[i.locale+'title']
                    content = request.POST[i.locale+'content']
                    print("title",title,content)
                    langcode = request.POST[i.locale+'lang']
                
                    lang = language.objects.get(locale = langcode)
                    

                    

                    pg = page.objects.get(slug=slug)
                    
                    translation = pageTranslation(page=pg,title=title,content=content,language=lang)
                    translation.save()
            
            
                return HttpResponseRedirect('/admin/Page/page/')

            else:
                    
                    context['pages'] = page.objects.filter(status="enabled")
                    print(context['pages'])
        
        else:
            pageDetails = page.objects.filter(slug=obj)
            context['pageDetails'] = pageDetails
            pageTranslationDetails = pageTranslation.objects.filter(page=obj)
            context['pageTranslationDetails'] = pageTranslationDetails
            for i in pageTranslationDetails:
                print("page",i.language)

            if request.method == 'POST':
                slug = request.POST['slug']
                status = request.POST['status']
                sortOrder = request.POST['order']

                pageObj = page.objects.filter(slug=slug).update(status=status,sortOrder=sortOrder)
                

                for i in languageData:
                    contentId = request.POST[i.locale+'contentId']
                    title = request.POST[i.locale+'title']
                    content = request.POST[i.locale+'content']
                    print("title",title,content)
                    langcode = request.POST[i.locale+'lang']
                
                    lang = language.objects.get(locale = langcode)
                    

                    

                    pg = page.objects.get(slug=slug)
                    
                    translation = pageTranslation.objects.filter(contentId=contentId).update(page=pg,title=title,content=content,language=lang)
                    
            
            
                return HttpResponseRedirect('/admin/Page/page/')
        

       
        return super(PageAdmin,self).changeform_view(request, obj ,form_url,context)

admin.site.register(page,PageAdmin)
