from django.contrib import admin
from django.urls import path
from search_function.views import search, index, history

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('results/', search, name='search'),
    path('history/', history, name='history'),
]
