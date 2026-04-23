from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import IR_Identification

@admin.register(IR_Identification)
class IRCalculationAdmin(ModelAdmin):
    exclude = ["irb_reported"]
    conditional_fields = {
        "ira_reported_start": "ira_reported == 'yes' || ira_reported == 'exception' ",
        "ira_reported_end": "ira_reported == 'yes' || ira_reported == 'exception'",
        "ira_reported_length": "ira_reported == 'yes' || ira_reported == 'exception'",
        "irb_reported_start": "ira_reported == 'yes'",
        "irb_reported_end": "ira_reported == 'yes'",
        "irb_reported_length": "ira_reported == 'yes'",
    }
    search_fields = ["accession", "title"]
    pass