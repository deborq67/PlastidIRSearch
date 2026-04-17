from django.contrib import admin
from .models import SearchResult, SearchHistory

admin.site.register(SearchResult)
admin.site.register(SearchHistory)
