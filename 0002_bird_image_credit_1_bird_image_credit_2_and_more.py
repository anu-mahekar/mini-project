# birds/management/commands/import_birds.py
from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
import pandas as pd
from birds.models import Bird

class Command(BaseCommand):
    help = "Import birds from a metadata CSV with columns: file_id,genus,species,english_cname,..."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to metadata CSV")

    def handle(self, *args, **opts):
        csv_path = Path(opts["csv_path"])
        if not csv_path.exists():
            raise CommandError(f"CSV not found: {csv_path}")

        df = pd.read_csv(csv_path)
        required = {"genus", "species", "english_cname"}
        missing = required - set(df.columns)
        if missing:
            raise CommandError(f"Missing columns: {missing}")

        df["genus"] = df["genus"].astype(str).str.strip()
        df["species"] = df["species"].astype(str).str.strip()
        df["english_cname"] = df["english_cname"].astype(str).str.strip()
        df["binomial"] = df["genus"] + " " + df["species"]

        created, updated = 0, 0
        for _, r in df.drop_duplicates(subset=["binomial"]).iterrows():
            obj, is_created = Bird.objects.update_or_create(
                binomial=r["binomial"],
                defaults={
                    "genus": r["genus"],
                    "species": r["species"],
                    "english_cname": r.get("english_cname", ""),
                    # Optionally seed some text from CSV columns if you have them:
                    # "habitat": ...,
                    # "diet": ...,
                }
            )
            created += int(is_created)
            updated += int(not is_created)

        self.stdout.write(self.style.SUCCESS(f"Imported: created={created}, updated={updated}"))
