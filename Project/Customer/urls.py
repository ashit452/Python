from django.urls import path,include
from . import views


urlpatterns = [
    
    path('',views.home,name="home"),
    path('getcitiesajax/', views.getcitiesajax, name="getcitiesajax"),
    path('delete/',views.delete,name='delete'),
    path('edit/',views.edit,name='edit'),
    path('verifyemail/',views.emailverify,name='verifyemail'),
]
