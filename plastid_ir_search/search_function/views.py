from django.shortcuts import render, redirect
from .plastid_search_function import initiate_search
from .models import SearchResult, SearchHistory
from genbank_interaction.models import IR_Identification
from datetime import datetime
import pandas as pd
import csv
from django.http import HttpResponse
from django_pandas.io import read_frame

from genbank_interaction.ir_operations import IROperations

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
        search_dict = search_query.to_dict('records')

        #Generate a session if not one yet made.

        if not request.session.session_key:
            request.session.create()

        history_record = SearchHistory.objects.create(
            session_key=request.session.session_key,
            search_term=search_term,
            total_records=total_records,
        )

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
                record['ira_reported'] = ir_result.ira_reported
                record['irb_reported'] = ir_result.irb_reported
            else:
                record['ira_reported'] = 'n/a'
                record['irb_reported'] = 'n/a'

        #Save history.
        history_record.results.set(result_instances)

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

def history(request):
    history_records = SearchHistory.objects.filter(
        session_key=request.session.session_key
    ).values('search_term', 'total_records', 'searched_at').order_by('-searched_at')
    return render(request, 'search_function/history.html', {"history_records": history_records})

def download_results(request):
    if request.GET.get('download'):
        #Django-Pandas handles the CSV Exports. A great improvement from the last export code.
        searchresult_qs = SearchResult.objects.all()
        df = read_frame(searchresult_qs, fieldnames=['accession', 'title', 'bp_length', 'updated', 'created', 'ira_info__ira_reported'])
        df['updated'] = pd.to_datetime(df['updated']).dt.strftime('%Y-%m-%d')
        df['created'] = pd.to_datetime(df['created']).dt.strftime('%Y-%m-%d')
        df = df.rename(columns={"accession": "Accession",
                                "title": "Title",
                                "bp_length": "Base_Pair_Length",
                                "updated": "Updated",
                                "created": "Created",
                                "ira_info__ira_reported": "IRs_Reported"})
        response = HttpResponse(df.to_csv(index=False), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="plastid_ir_search_results.csv"'
        return response
    return render(request, "search_function/download.html")


def download_history(request):
    if request.GET.get('download'):
        searchhistory_qs = SearchHistory.objects.all()
        df = read_frame(searchhistory_qs, fieldnames=['search_term', 'total_records', 'searched_at'])
        df['searched_at'] = pd.to_datetime(df['searched_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
        df = df.rename(columns={"search_term": "Search_Term",
                                "total_records": "Records_Found",
                                "searched_at": "Timestamp"})
        response = HttpResponse(df.to_csv(index=False), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="plastid_ir_search_history.csv"'
        return response
    return render(request, "search_function/download.html")