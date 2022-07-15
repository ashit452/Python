from django.shortcuts import render,redirect
from Page.models import page,pageTranslation
from Language.models import language
from django.http import JsonResponse

# Create your views here.
def home(request):
    pages = page.objects.filter(status="enabled").order_by('sortOrder')
    return render(request, 'index.html',{'pages':pages})


def page_list():
    pages = page.objects.filter(status="enabled").order_by('sortOrder')
    for i in pages:
        print(i.slug)
    languages = language.objects.filter(status="enabled")
    
    return pages,languages

def page_details(request,slug):
    
    languages = language.objects.filter(status="enabled")

    if request.method == 'POST':
        locale=request.POST.get('lang')
        request.session['defaultLanguage'] = locale
        msg={
            "Tag":"Success",
        }
        return JsonResponse(msg)

    if "defaultLanguage" in request.session:
        pagelist = pageTranslation.objects.raw("select * from page_pagetranslation as c inner join language_language as l on c.language_id=l.locale inner join page_page as p on c.page_id=p.pageId where l.locale= '"+request.session['defaultLanguage']+"'")
        pageDetails = pageTranslation.objects.raw("select * from page_pagetranslation as c inner join language_language as l on c.language_id=l.locale inner join page_page as p on c.page_id=p.pageId where p.slug='"+slug+"' and l.locale= '"+request.session['defaultLanguage']+"'")
        pageData = pageTranslation.objects.raw("select * from page_pagetranslation as c inner join language_language as l on c.language_id=l.locale where l.locale= '"+request.session['defaultLanguage']+"'")
        
    else:
        pagelist = pageTranslation.objects.raw("select * from page_pagetranslation as c inner join language_language as l on c.language_id=l.locale inner join page_page as p on c.page_id=p.pageId where l.locale= '"+request.session['defaultLanguage']+"'")
        pageDetails = pageTranslation.objects.raw("select * from page_pagetranslation as c inner join language_language as l on c.language_id=l.locale inner join page_page as p on c.page_id=p.pageId where p.slug='"+slug+"' and l.isDefault= 1")
        pageData = pageTranslation.objects.raw("select * from page_pagetranslation as c inner join language_language as l on c.language_id=l.locale where l.isDefault= 1")
        
    for i in pageDetails:
        request.session["defaultLanguage"]=i.locale
    
    
    
       

    print(request.session['defaultLanguage'])
    return render(request,'slugpage.html',{'page':pageDetails,'pageData':pageData,'pages':pagelist,'languages':languages,'languageSession':request.session['defaultLanguage']})
