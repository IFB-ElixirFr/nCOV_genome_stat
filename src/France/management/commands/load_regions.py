import urllib, json

from django.core.management.base import BaseCommand

from France.models import regionsFrance


class Command(BaseCommand):
    help = 'Reload regions data'

    def handle(self, *args, **kwargs):

        with open("France/static/data/regions-avec-outre-mer.geojson") as f:
            data = json.load(f)

        regionsFrance.objects.all().delete()

        for d in data['features']:
            v = regionsFrance(nom=d['properties']['nom'],
                        code= "REG-" + d['properties']['code'],
                        features=d)
            v.save()

        self.stdout.write("Done")
