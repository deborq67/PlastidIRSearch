from Bio import Entrez
import pandas as pd
import time
from django.core.cache import cache

'''
Purpose: This script only fetches basic information on an organism from Genbank.
It will work in conjunction with a local Genbank database to parse using said information.
'''


def initiate_search(search_term):
    # Email is a requirement by NCBI, the API provider.

    Entrez.email = "johnsmith@example.com"

    query = (f'"{search_term}"[Organism]' +
             ' AND ((chloroplast[filter] OR plastid[filter]) AND "complete genome"[Title])'
             )

    # Cache the result to save on speed.

    cached = cache.get(search_term)
    if cached:
        return cached

    # Entrez.esearch fetches IDs necessary to get record title and DNA sequence.

    handle = Entrez.esearch(db="nuccore", term=query, retmax=10000)
    record = Entrez.read(handle)
    handle.close()

    total_records = int(record['Count'])

    # Get IDs needed for look up records.

    id_list = record["IdList"]

    # Get records and place in a dataframe.


    records = []
    batch_size = 500
    for i in range(0, len(id_list), batch_size):
        batch = id_list[i:i + batch_size]
        handle = Entrez.esummary(db="nuccore", id=",".join(batch), retmax=batch_size)
        summaries = Entrez.read(handle)
        handle.close()
        time.sleep(0.34)
        for index, summary in enumerate(summaries):
            records.append({
                "Entry": i + index,
                "Accession": summary['AccessionVersion'],
                "Title": summary['Title'],
                "BP_Length": int(summary['Length']),
                "Updated": summary['UpdateDate'],
                "Created": summary['CreateDate'],
            })

    df = pd.DataFrame(records)
    return df, total_records