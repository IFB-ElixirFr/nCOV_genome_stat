import urllib, json

from django.core.management.base import BaseCommand

from home.models import countries


class Command(BaseCommand):
    help = 'Reload regions data'

    def handle(self, *args, **kwargs):

        with open("Home/static/data/countries.geojson") as f:
            data = json.load(f)

        countries.objects.all().delete()

        for d in data['features']:
            v = countries(ADMIN=d['properties']['ADMIN'],
                        ISO_A3= d['properties']['ISO_A3'],
                        ISO_A2=d['properties']['ISO_A2'],
                        geometry=d)
            v.save()

        self.stdout.write("Done")
