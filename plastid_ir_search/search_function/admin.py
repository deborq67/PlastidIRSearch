from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline
from .models import SearchResult, SearchHistory


@admin.register(SearchHistory)
class SearchHistoryAdmin(ModelAdmin):
    readonly_fields = ["session_key", "search_term", "total_records"]
    search_fields = ["search_term", "searched_at"]
    pass
