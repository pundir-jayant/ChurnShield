from django.core.management.base import BaseCommand
from backend.ml.training import train_and_select

class Command(BaseCommand):
    help = "Train churn models, compare metrics, and save the best model artifact."

    def add_arguments(self, parser):
        parser.add_argument("--dataset", required=True)

    def handle(self, *args, **options):
        result = train_and_select(options["dataset"])
        self.stdout.write(self.style.SUCCESS(f"Best model: {result['best_model']}"))

