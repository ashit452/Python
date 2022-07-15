from django.shortcuts import render
from .models import block, blockTranslation
# Create your views here.
def home(request):
    blockData = block.objects.all()
    for i in blockData:
        blockTranslationData = blockTranslation.objects.filter(block_id = i.blockId)
        print(i.blockId)
        for j in blockTranslationData:
            print(j)
        
    return render(request,"block.html",{"blockdata" : blockData,"blocktranslation":blockTranslationData})