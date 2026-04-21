from ...models import IR_Identification
import os
import pandas as pd
from django.core.management.base import BaseCommand
from ...ir_operations import IROperations
from django.conf import settings


class Command(BaseCommand):
    help = 'Processes all GB files and saves IR Identification.'

    def handle(self, *args, **kwargs):
        df_final = []

        for file in os.scandir(os.path.join(settings.BASE_DIR, "genbank_files")):
            if file.name.endswith(".gb"):
                try:
                    df_row = IROperations(file.path).info
                    df_final.append(df_row)
                    self.stdout.write(f"Processed: {file.name}")
                except Exception as e:
                    self.stdout.write(f"SKIPPED {file.name}: {e}")

        if df_final:
            df = pd.concat(df_final)
            df_dict = df.to_dict('records')

            for record in df_dict:
                IR_Identification.objects.get_or_create(
                    accession=record['ACCESSION'],
                    defaults={
                        'ira_reported': record['IRa_REPORTED'],
                        'ira_reported_start': record['IRa_REPORTED_START'],
                        'ira_reported_end': record['IRa_REPORTED_END'],
                        'ira_reported_length': record['IRa_REPORTED_LENGTH'],
                        'irb_reported': record['IRb_REPORTED'],
                        'irb_reported_start': record['IRb_REPORTED_START'],
                        'irb_reported_end': record['IRb_REPORTED_END'],
                        'irb_reported_length': record['IRb_REPORTED_LENGTH'],
                    }
                )
                self.stdout.write(f"Saved: {record['ACCESSION']}")

            self.stdout.write('Folder successfully processed.')
        else:
            self.stdout.write('No GB files found.')