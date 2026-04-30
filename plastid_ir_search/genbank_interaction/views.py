import sys
from django.shortcuts import render
import os

from django_pandas.io import read_frame

from .ir_operations import *
from .models import IR_Identification
from search_function.models import SearchResult
import pandas as pd
import polars as pl
import plotly.express as px
import django_pandas

def ir_info(request, accession):

    '''
    ir_setup already sets up the model for us so all we need to really do is associate SearchResult's
    Accession # with the IR_Identification model's Accession #.
    '''

    search_result = SearchResult.objects.filter(accession=accession).first()
    ir_result = IR_Identification.objects.filter(accession=accession).first()

    return render(request, 'genbank_interaction/info.html', {
        'ir_result': ir_result,
        'search_result': search_result,
        'accession': accession,
    })

def time_stats(request, accession):
    histogram_qs = IR_Identification.objects.all()
    histogram_df = read_frame(histogram_qs, fieldnames=['updated','accession','ir_reported'])
    histogram_df = pl.from_pandas(histogram_df)

    #Filter out rows with no date annotated and those with IRs reported.

    histogram_df = histogram_df.filter(pl.col("updated").is_not_null())
    histogram_df = histogram_df.filter(pl.col("ir_reported") == "yes")
    histogram_df = histogram_df.drop('ir_reported')

    histogram_df = histogram_df.with_columns(pl.col("updated").str.to_date(format="%Y"))
    histogram_df = histogram_df.rename({"accession": "Accession IDs", "updated": "Last Update"})

    plastid_histogram = px.histogram(histogram_df, x="Last Update",
                       title="Total Annotated Plastid Records Uploaded to GenBank by Year")

    plastid_histogram = plastid_histogram.to_html()


    return render(request, "index.html", {"plastid_histogram": plastid_histogram})









