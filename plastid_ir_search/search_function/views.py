from django.shortcuts import render
from .plastid_search_function import initiate_search
from .models import SearchResult, SearchHistory
from genbank_interaction.models import IR_Identification
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
                bp_length=record['BP_Length'],
                updated=datetime.strptime(record['Updated'], '%Y/%m/%d') if record['Updated'] else None,
                created=datetime.strptime(record['Created'], '%Y/%m/%d') if record['Created'] else None,
            )
            result_instances.append(result)
            ir_result = IR_Identification.objects.filter(accession=record['Accession']).first()
            if ir_result:
                record['ira_reported'] = ir_result.ira_reported
                record['irb_reported'] = ir_result.irb_reported

        #Save history.
        history_record.results.set(result_instances)

        #Clear the SearchResult model to keep it from being too bloated. It's only meant to
        #link to SearchHistory anyway, which is persistent.

        # SearchResult.objects.all().delete()

        return render(request, 'search_function/results.html', {
            'search_term': search_term,
            'results': search_dict,
            'total_records': total_records,
        })

    return render(request, 'index.html')

def history(request):
    history_records = SearchHistory.objects.filter(
        session_key=request.session.session_key
    ).values('search_term', 'total_records', 'searched_at').order_by('-searched_at')
    return render(request, 'search_function/history.html', {"history_records": history_records})