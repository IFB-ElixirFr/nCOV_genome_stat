import csv
import requests
import io


from django.core.management.base import BaseCommand

from France.models import hospitIncidReg, regionsFrance


class Command(BaseCommand):
    help = 'Reload regions data'

    def handle(self, *args, **kwargs):
        response = requests.get("https://www.data.gouv.fr/fr/datasets/r/a1466f7f-4ece-4158-a373-f5d4db167eb0")
        if not response:
            self.stdout.write("Error. Not update")
        else:
            hospitIncidReg.objects.all().delete()
            csv_bytes = response.content
            str_file = io.StringIO(csv_bytes.decode('latin-1'), newline='\n')

            reader = csv.reader(str_file)
            next(reader, None)
            for row_list in reader:
                r = row_list[0].split(";")
                if len(r[2]) == 1 :
                    reg = "REG-0"+r[2]
                else:
                    reg = "REG-" + r[2]

                v = hospitIncidReg(date=row_list[0].split(";")[0],
                                   region=regionsFrance.objects.get(code=reg),
                                   incid_rea=r[3])
                v.save()

            str_file.close()
            self.stdout.write("Done")