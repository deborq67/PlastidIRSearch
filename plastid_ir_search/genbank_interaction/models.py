from django.db import models
from search_function.models import SearchResult

class IR_Identification(models.Model):
    accession = models.ForeignKey(SearchResult, on_delete=models.CASCADE, related_name="ir_identifications", null=True)
    gb_file = models.FileField(upload_to="gb_files/")
    irs_found = models.CharField(max_length=50)
    ira_reported = models.CharField(max_length=50)
    ira_reported_start = models.IntegerField(null=True)
    ira_reported_end = models.IntegerField(null=True)
    ira_reported_length = models.IntegerField(null=True)
    irb_reported = models.CharField(max_length=50)
    irb_reported_start = models.IntegerField(null=True)
    irb_reported_end = models.IntegerField(null=True)
    irb_reported_length = models.IntegerField(null=True)