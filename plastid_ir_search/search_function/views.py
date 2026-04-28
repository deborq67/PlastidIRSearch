from django.shortcuts import render, redirect
from .plastid_search_function import initiate_search
from .models import SearchResult, SearchHistory
from genbank_interaction.models import IR_Identification
from datetime import datetime
import polars as pl
import pandas as pd
from django.http import HttpResponse
from django_pandas.io import read_frame
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)


def index(request):
    return render(request, 'index.html')


def search(request):
    if request.method == 'POST':
        if SearchResult.objects.exists():
            ''' Clear the SearchResult model at the beginning of each new search to
             keep it from being too bloated. It's only meant to
            link to SearchHistory anyway, which is persistent.'''
            SearchResult.objects.all().delete()

        # Take out white space if user makes a search. Convert to dictionary for model conversion.
        search_term = request.POST.get('search_term', '').strip()
        search_query, total_records = initiate_search(search_term)
        search_dict = search_query.to_dicts()

        #Generate a session if not one yet made.

        if not request.session.session_key:
            request.session.create()

        #Put the search term,into history.

        history_record = SearchHistory.objects.create(
            session_key=request.session.session_key,
            search_term=search_term,
            total_records=total_records,
            search_accessions=','.join([record['Accession'] for record in search_dict])
        )

        #Make a dictionary of dictionaries

        result_instances = []

        for record in search_dict:
            ir_result = IR_Identification.objects.filter(accession=record['Accession']).first()
            result = SearchResult.objects.create(
                accession=record['Accession'],
                title=record['Title'],
                bp_length=record['BP_Length'],
                updated=datetime.strptime(record['Updated'], '%Y/%m/%d') if record['Updated'] else None,
                created=datetime.strptime(record['Created'], '%Y/%m/%d') if record['Created'] else None,
                ir_info=ir_result,
            )
            result_instances.append(result)
            if ir_result:
                record['ir_reported'] = ir_result.ir_reported
            else:
                record['ir_reported'] = 'n/a'

        #Save history.
        history_record.save()

        request.session['search_dict'] = search_dict
        request.session['search_term'] = search_term
        request.session['total_records'] = total_records

        return redirect('/results/')

    search_dict = request.session.get('search_dict', [])
    search_term = request.session.get('search_term', '')
    total_records = request.session.get('total_records', 0)

    default_page = 1
    page = request.GET.get('page', default_page)
    paginator = Paginator(search_dict, 20)
    try:
        results_page = paginator.page(page)
    except PageNotAnInteger:
        results_page = paginator.page(default_page)
    except EmptyPage:
        results_page = paginator.page(paginator.num_pages)

    return render(request, 'search_function/results.html', {
        'search_term': search_term,
        'results': results_page,
        'total_records': total_records,
    })


#This loads the history into a table.

def history(request):
    history_records = SearchHistory.objects.filter(
        session_key=request.session.session_key
    ).values('id', 'search_term', 'total_records', 'searched_at').order_by('-searched_at')
    default_page = 1
    page = request.GET.get('page', default_page)
    paginator = Paginator(history_records, 20)
    try:
        results_page = paginator.page(page)
    except PageNotAnInteger:
        results_page = paginator.page(default_page)
    except EmptyPage:
        results_page = paginator.page(paginator.num_pages)

    return render(request, 'search_function/history.html', {"history_records": results_page})


#This extracts a list of Accession numbers for a separate page.

def accession_list(request):
    id = request.GET.get('id')
    history_accessions = SearchHistory.objects.get(
        id=id, session_key=request.session.session_key
    ).search_accessions.split(',')
    history_accessions.sort()
    return render(request, 'search_function/accessions.html', {"history_accessions": history_accessions})


def download_results(request):

    '''Django-Pandas is great at turning the df into a Pandas df since there isn't a really good
    polars equivalent. From there I can convert to Polars and do the following.'''
    searchresult_qs = SearchResult.objects.all()
    df = read_frame(searchresult_qs,
                    fieldnames=['accession', 'title', 'bp_length', 'updated', 'created', 'ir_info__ir_reported'])
    df = pl.from_pandas(df)
    df = df.with_columns(pl.col('updated').dt.strftime('%Y-%m-%d'))
    df = df.with_columns(pl.col('created').dt.strftime('%Y-%m-%d'))
    df = df.rename({"accession": "Accession",
                        "title": "Title",
                        "bp_length": "Base_Pair_Length",
                        "updated": "Updated",
                        "created": "Created",
                        "ir_info__ir_reported": "IRs_Reported"})
    response = HttpResponse(df.write_csv(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="plastid_ir_search_results.csv"'
    return response

def download_history(request):

    #Same logic as download_results, but for the history page.

    searchhistory_qs = SearchHistory.objects.all()
    df = read_frame(searchhistory_qs, fieldnames=['search_term', 'total_records', 'searched_at'])
    df = pl.from_pandas(df)
    df = df.with_columns(pl.col('searched_at').dt.strftime('%Y-%m-%d %H:%M:%S'))
    df = df.rename({"search_term": "Search_Term",
                        "total_records": "Records_Found",
                        "searched_at": "Timestamp"})
    response = HttpResponse(df.write_csv(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="plastid_ir_search_history.csv"'
    return response

def download_accessions(request):

    #Same logic as download_results, but for the history page.

    searchhistory_qs = SearchHistory.objects.all()
    history_accession_df = read_frame( searchhistory_qs ,fieldnames=['id','accession'])
    history_accession_df = pl.from_pandas(history_accession_df)

    ir_info_qs = IR_Identification.objects.all()
    ir_info_df = read_frame(ir_info_qs, fieldnames=['accession', 'ir_reported'])
    ir_info_df = pl.from_pandas(ir_info_df)

    df = df.with_columns(pl.col('searched_at').dt.strftime('%Y-%m-%d %H:%M:%S'))
    df = df.rename({"search_term": "Search_Term",
                        "total_records": "Records_Found",
                        "searched_at": "Timestamp"})
    response = HttpResponse(df.write_csv(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="plastid_ir_search_history.csv"'
    return response
