from Bio.Phylo.PhyloXML import Accession
from django.db import models


class IR_Identification(models.Model):
    #search_result = models.ForeignKey(SearchResult, on_delete=models.CASCADE, related_name="ir_identifications")
    gb_file = models.FileField(upload_to="gb_files/")
    irs_found = models.CharField(max_length=50)
    ira_reported = models.CharField(max_length=50)
    ira_reported_start = models.IntegerField(null=True, blank=True)
    ira_reported_end = models.IntegerField(null=True, blank=True)
    ira_reported_length = models.IntegerField(null=True, blank=True)
    irb_reported = models.CharField(max_length=50)
    irb_reported_start = models.IntegerField(null=True, blank=True)
    irb_reported_end = models.IntegerField(null=True, blank=True)
    irb_reported_length = models.IntegerField(null=True, blank=True)