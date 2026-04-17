from django.shortcuts import render
from .forms import SearchForm
from .plastid_search_function import initiate_search
from .models import SearchResult, SearchHistory
from datetime import datetime

def index(request):
    return render(request, 'index.html')

def search(request):
    if request.method == 'POST':
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
            result = SearchResult.objects.create(
                accession=record['Accession'],
                title=record['Title'],
                bp_length=record['BP Length'],
                updated=datetime.strptime(record['Updated'], '%Y/%m/%d') if record['Updated'] else None,
                created=datetime.strptime(record['Created'], '%Y/%m/%d') if record['Created'] else None,
            )
            result_instances.append(result)

        #Save history.
        history_record.results.set(result_instances)

        return render(request, 'search_function/results.html', {
            'search_term': search_term,
            'results': search_dict,
            'total_records': total_records
        })

    return render(request, 'index.html')

def history(request):
    return render(request, 'search_function/history.html')