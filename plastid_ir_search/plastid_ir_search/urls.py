from django.contrib import admin
from django.urls import path
from search_function.views import search, index, history, download_history, download_results, accession_list
from genbank_interaction.views import ir_info
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('results/', search, name='search'),
    path('results/download/', download_results, name='download_results'),
    path('results/<str:accession>/', ir_info, name='ir_info'),
    path('history/', history, name='history'),
    path('history/accessions/', accession_list, name='accession_list'),
    path('history/download/', download_history, name='download_history'),
] + debug_toolbar_urls()
