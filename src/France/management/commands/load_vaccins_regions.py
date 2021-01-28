import urllib, json
import requests

from django.core.management.base import BaseCommand

from France.models import vaccinFrance, regionsFrance


class Command(BaseCommand):
    help = 'Reload regions data'

    def handle(self, *args, **kwargs):

        r = requests.get('https://www.data.gouv.fr/fr/datasets/r/16cb2df5-e9c7-46ec-9dbf-c902f834dab1')
        if not r and not r.json():
            self.stdout.write("Error. Not update")
        else:
            vaccinFrance.objects.all().delete()
            for d in r.json():

                v = vaccinFrance(date=d['date'],
                                 region= regionsFrance.objects.get(code=d['code']),
                                 totalVaccines=d['totalVaccines'])
                v.save()
            self.stdout.write("Done")