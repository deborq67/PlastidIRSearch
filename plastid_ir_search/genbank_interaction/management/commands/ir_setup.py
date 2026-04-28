import os
import polars as pl
from django.core.management.base import BaseCommand
from multiprocessing import Pool
from django.conf import settings

#Separate function for parsing needed for multiprocessing to work.

def parse_file(filepath):
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plastid_ir_search.settings')
    django.setup()
    from genbank_interaction.ir_operations import IROperations
    try:
        return IROperations(filepath).info
    except Exception as e:
        print(f"FAILED {filepath}: {e}")
        return None


class Command(BaseCommand):
    help = 'Processes all GB files and saves IR Identification.'

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            "--ignore",
            "-i",
            action="store_true",
            help="Ignore duplicate entries instead of updating them.",
        )

    def handle(self, *args, **options):

        from genbank_interaction.models import IR_Identification
        file_list = [
            file.path
            for file in os.scandir(os.path.join(settings.BASE_DIR, "genbank_files"))
            if file.name.endswith(".gb")
        ]

        if not file_list:
            self.stdout.write('The "genbank_files" directory can not be found. Make sure it is on the same level as manage.py.')
            return

        #Ignore duplicates rather than updating them.

        if options["ignore"]:
            current_records = set(IR_Identification.objects.values_list('accession', flat=True))
            file_list = [
                f for f in file_list
                if os.path.splitext(os.path.basename(f))[0] not in current_records
            ]
            if not file_list:
                self.stdout.write("No new files to process.")
                return
            self.stdout.write(f"{len(file_list)} new files to process.")

        self.stdout.write(f"Processing {len(file_list)} files...")

        with Pool() as pool:
            results = pool.map(parse_file, file_list)

        processed_results = [file_result for file_result in results if file_result is not None]

        if not processed_results:
            self.stdout.write('\n No new files to process.')
            return

        df = pl.concat(processed_results)

        df_dict = df.to_dicts()

        genbank_records = [
            IR_Identification(
                accession=row['ACCESSION'],
                title=row['TITLE'],
                ir_reported=row['IR_REPORTED'],
                ira_reported=row['IRa_REPORTED'],
                ira_reported_start=row['IRa_REPORTED_START'],
                ira_reported_end=row['IRa_REPORTED_END'],
                ira_reported_length=row['IRa_REPORTED_LENGTH'],
                irb_reported=row['IRb_REPORTED'],
                irb_reported_start=row['IRb_REPORTED_START'],
                irb_reported_end=row['IRb_REPORTED_END'],
                irb_reported_length=row['IRb_REPORTED_LENGTH'],
                )
            for row in df_dict
            ]

        if options["ignore"]:
            IR_Identification.objects.bulk_create(
                genbank_records,
                batch_size=1000,
                ignore_conflicts=True
                )
            self.stdout.write(f'Ignored duplicate entries and wrote {len(genbank_records)} files.')

        else:
            IR_Identification.objects.bulk_create(
                genbank_records,
                batch_size=1000,
                update_conflicts=True,
                unique_fields=['accession'],
                update_fields=[
                    'title', 'ir_reported', 'ira_reported', 'ira_reported_start',
                    'ira_reported_end', 'ira_reported_length',
                    'irb_reported', 'irb_reported_start',
                    'irb_reported_end', 'irb_reported_length'
                ]
                )


        self.stdout.write(f'Folder successfully processed {len(genbank_records)} files.')