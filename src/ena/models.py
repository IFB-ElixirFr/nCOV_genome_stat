from django.db import models
import datetime

class Sample(models.Model):
    sampleId = models.CharField(max_length=255, help_text="Biosample accession ID in original database (ENA) (e.g. SRS6007144)", blank=False)
    sampleType = models.CharField(max_length=255, help_text="Anatomical origin of biosample (e.g. Bronchoalveolar lavage fluid)", blank=True)
    collectionDate = models.DateField( default=datetime.date.today, help_text="Date of biosample collection. Iso format : 2021-01-15")
    country = models.CharField(max_length=255,help_text="Country submitter")

    def __str__(self):
        return self.sampleId


