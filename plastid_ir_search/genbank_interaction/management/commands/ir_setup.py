import os
import pandas as pd
import dask.bag as db
from django.core.management.base import BaseCommand
from django.conf import settings

def process_file(record):
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plastid_ir_search.settings')
    django.setup()
    from genbank_interaction.ir_operations import IROperations
    try:
        return IROperations(record).info.to_dict('records')[0]
    except Exception as e:
        print(f"FAILED {record}: {e}")
        return None

class Command(BaseCommand):
    help = 'Processes all GB files and saves IR Identification.'

    def handle(self, *args, **kwargs):
        from genbank_interaction.ir_operations import IROperations
        from genbank_interaction.models import IR_Identification

        genbank_dir = os.path.join(settings.BASE_DIR, "genbank_files")

        file_list = [
            os.path.join(genbank_dir, f)
            for f in os.listdir(genbank_dir)
            if f.endswith('.gb')
        ]

        if file_list:
            print(f"Found {len(file_list)} files")
            bag = db.from_sequence(file_list, npartitions=20)
            results = bag.map(process_file).filter(lambda x: x is not None).compute(scheduler='threads')
            print(f"Got {len(results)} results")

            instances = [
                IR_Identification(
                    accession=record['ACCESSION'],
                    title=record['TITLE'],
                    ira_reported=record['IRa_REPORTED'],
                    ira_reported_start=record['IRa_REPORTED_START'],
                    ira_reported_end=record['IRa_REPORTED_END'],
                    ira_reported_length=record['IRa_REPORTED_LENGTH'],
                    irb_reported=record['IRb_REPORTED'],
                    irb_reported_start=record['IRb_REPORTED_START'],
                    irb_reported_end=record['IRb_REPORTED_END'],
                    irb_reported_length=record['IRb_REPORTED_LENGTH'],
                )
                for record in results
            ]

            IR_Identification.objects.bulk_create(
                instances,
                update_conflicts=True,
                unique_fields=['accession'],
                update_fields=[
                    'title', 'ira_reported', 'ira_reported_start',
                    'ira_reported_end', 'ira_reported_length',
                    'irb_reported', 'irb_reported_start',
                    'irb_reported_end', 'irb_reported_length'
                ]
            )
            self.stdout.write(f'Saved {len(instances)} records.')
        else:
            self.stdout.write('No GB files found.')