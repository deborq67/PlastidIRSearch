from django.db import models

class SearchResult(models.Model):
    accession_number = models.CharField(max_length=200)



class SearchHistory(models.Model):
    search_result = models.ForeignKey(SearchResult, on_delete=models.CASCADE)
