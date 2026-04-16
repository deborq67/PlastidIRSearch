from django.db import models
from django.conf import settings

# from genbank_interaction.models import  IRClassification

class SearchResult(models.Model):
    accession = models.CharField(max_length=50)
    title = models.TextField()
    bp_length = models.IntegerField()
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)

class SearchHistory(models.Model):
    class Meta:
        #Correcting spelling on admin page.
        verbose_name_plural = "Search Histories"
    session_key = models.CharField(max_length=50)
    search_term = models.CharField(max_length=255)
    total_records = models.IntegerField()
    searched_at = models.DateTimeField(auto_now_add=True)
    results = models.ManyToManyField(SearchResult)