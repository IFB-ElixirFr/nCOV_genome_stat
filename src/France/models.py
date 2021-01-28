import datetime
from django.db import models


class regionsFrance(models.Model):
    code = models.CharField(max_length=10, help_text="Code région exemple :REG-01 ")
    nom = models.CharField(max_length=50, help_text="Nom de la région : Corse", blank=False)
    features = models.JSONField()

    def __str__(self):
        return '{} ({})'.format(self.nom, self.code)


class vaccinFrance(models.Model):
    date = models.DateField(default= datetime.date.today, help_text="Date")
    region = models.ForeignKey("regionsFrance", related_name='vaccins',
                             on_delete=models.CASCADE)
    totalVaccines = models.IntegerField(default=0, help_text="Nombre de vaccins cumulés")

    def __str__(self):
        return '{} {} {}'.format(self.date, self.region, self.totalVaccines)


class hospitIncidReg(models.Model):
    date = models.DateField(default= datetime.date.today, help_text="Date of notice")
    region = models.ForeignKey("regionsFrance", related_name='hospitIncid',
                             on_delete=models.CASCADE)
    incid_rea = models.IntegerField(default=0, help_text="Number of new intensive care admissions in the last 24 hours")

    def __str__(self):
        return '{} {} {}'.format(self.date, self.region, self.incid_rea)


