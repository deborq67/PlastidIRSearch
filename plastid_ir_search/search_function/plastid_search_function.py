from Bio import Entrez, SeqIO
from io import StringIO
import pandas as pd
import time

'''
Purpose: This script calculates the ambiguity percentage (percent of non A, T, C, or G
values in a DNA sequence) and sorts by the records by those with the highest (in other
words the most error prone records are shown first.)
'''


def initiate_search(search_term):
    # Email is a requirement by NCBI, the API provider.

    Entrez.email = johnsmith@example.com

    query = (f'"{search_term}"[Organism]' +
             ' AND ((chloroplast[filter] OR plastid[filter]) AND "complete genome"[Title])'
             )

    # Entrez.esearch fetches IDs necessary to get record title and DNA sequence.

    handle = Entrez.esearch(db="nuccore", term=query, retmax=10000)
    record = Entrez.read(handle)
    handle.close()

    total_records = int(record['Count'])

    if total_records == 0:
        return pd.DataFrame(), 0

    # Get IDs needed for look up records.

    id_list = record["IdList"]

    # Get records and place in a dataframe.

    handle = Entrez.esummary(db="nuccore", id=",".join(id_list), retmax=500)
    summaries = Entrez.read(handle)
    handle.close()

    records = []
    for index, summary in enumerate(summaries):
        records.append({
            "Entry": index,
            "Accession": summary['AccessionVersion'],
            "Title": summary['Title'],
            "BP Length": int(summary['Length']),
            "Updated": summary['UpdateDate'],
            "Created": summary['CreateDate'],
        })

    df = pd.DataFrame(records)

    return df, total_records