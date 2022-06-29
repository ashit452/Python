from django.urls import path,include
from . import views


urlpatterns = [
    
    
    path('getcitiesajax/', views.getcitiesajax, name="getcitiesajax"),
    path('delete/',views.delete,name='delete'),
    path('edit/',views.edit,name='edit'),
]
