from django.core.management.base import BaseCommand, CommandError

from main.models import WikiCategory, SeedWikiWebsite, Website, STATUS_WORKING, STATUS_WAITING


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        WikiCategory.objects.filter(status=STATUS_WORKING).update(status=STATUS_WAITING)
        SeedWikiWebsite.objects.filter(status=STATUS_WORKING).update(status=STATUS_WAITING)
        Website.objects.filter(status=STATUS_WORKING).update(status=STATUS_WAITING)

        self.stdout.write(self.style.SUCCESS('Successfully cleaned db'))
