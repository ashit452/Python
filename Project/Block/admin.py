from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import block,blockTranslation
from Language.models import language
from django.contrib import messages
from django.template.defaulttags import register
...
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


    
class BlockAdmin(admin.ModelAdmin):
    # inlines = [ContentInline,]
    list_display = ['slug','status','createdAt','updatedAt',]

        
    def changeform_view(self, request,obj ,form_url,context=None):
        context = context or {}
        languageData = language.objects.filter(status = "enabled")
        context["language"]=languageData

        if obj is None:
            
            if request.method == 'POST':
                slug = request.POST['slug']
                status = request.POST['status']
                
                blockObj = block(slug=slug,status=status)
                blockObj.save()

                for i in languageData:
                
                    title = request.POST[i.locale+'title']
                    content = request.POST[i.locale+'content']
                    print("title",title,content)
                    langcode = request.POST[i.locale+'lang']
                
                    lang = language.objects.get(locale = langcode)
                    
 
                    latestBlock = block.objects.latest("blockId")
                    blockid = block.objects.get(blockId=latestBlock.blockId)
                    
                    translation = blockTranslation(block=blockid,title=title,content=content,language=lang)
                    translation.save()
            
                messages.success(request,slug+" added successfully")
                return HttpResponseRedirect('/admin/Block/block/')

            else:
                    
                context['blocks'] = block.objects.filter(status="enabled")
                print(context['blocks'])
        
        else:
            blockDetails = block.objects.filter(blockId=obj)
            context['blockDetails'] = blockDetails
            print("context",context['blockDetails'][0].slug)
            # pageTranslationDetails = pageTranslation.objects.filter(page=obj)
            # context['pageTranslationDetails'] = pageTranslationDetails
            blockList = {}
            blockTranslationDetails = blockTranslation.objects.raw("select * from block_blocktranslation as bt inner join language_language l on bt.language_id = l.locale where bt.block_id='"+obj+"'")

            for lang in languageData:
                for i in blockTranslationDetails:
                    if i.locale == lang.locale:
                        blockList[lang.locale] = {"language":i.locale,'title':i.title,"content":i.content,"contentId":i.blockTranslationId}
            print(blockList)
            context['blockList'] = blockList

            

            if request.method == 'POST':
                slug = request.POST['slug']
                status = request.POST['status']
                blockid = request.POST['blockid']

                bid = block.objects.get(blockId=blockid)
                blockObj = block.objects.filter(blockId=blockid).update(slug=slug,status=status)
                

                for i in languageData:
                    contentId = request.POST[i.locale+'contentId']
                    title = request.POST[i.locale+'title']
                    content = request.POST[i.locale+'content']
                    print("title",title,content)
                    langcode = request.POST[i.locale+'lang']
                
                    lang = language.objects.get(locale = langcode)
                    

                    

                    # pgid = page.objects.get(page=slug)
                    
                    translation = blockTranslation.objects.filter(blockTranslationId=contentId).update(block=bid,title=title,content=content,language=lang)
                    
            
                messages.success(request,slug+" updated successfully")
                return HttpResponseRedirect('/admin/Block/block/')
        

       
        return super(BlockAdmin,self).changeform_view(request, obj ,form_url,context)

admin.site.register(block,BlockAdmin)
