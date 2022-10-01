from . import views
from django.urls import path


#only necessary when you have multiple apps
#app_name = 'MongoBnB'
urlpatterns = [
    path('', views.index, name='index'),
    path('/listing/<str:id>', views.listing, name='listing'),
    path('/confirmation/<str:id>', views.confirmation, name='confirmation'),
]