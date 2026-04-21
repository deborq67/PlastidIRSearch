from django.db import models
from search_function.models import SearchResult

class IR_Identification(models.Model):
    accession = models.CharField(max_length=50, unique=True)
    irs_found = models.CharField(max_length=50)
    ira_reported = models.CharField(max_length=50)
    ira_reported_start = models.IntegerField(null=True)
    ira_reported_end = models.IntegerField(null=True)
    ira_reported_length = models.IntegerField(null=True)
    irb_reported = models.CharField(max_length=50)
    irb_reported_start = models.IntegerField(null=True)
    irb_reported_end = models.IntegerField(null=True)
    irb_reported_length = models.IntegerField(null=True)

    class Meta:
        verbose_name = "IR Identification"