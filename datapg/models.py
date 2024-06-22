from django.db import models

class MydataPg(models.Model):
    Assistant = models.FloatField(null=True, blank=True)
    TMission = models.CharField(max_length=100)
    CMission = models.CharField(max_length=100)
    Raison_sociale = models.CharField(max_length=100)
    Description = models.CharField(max_length=1000)
    Client = models.CharField(max_length=100)
    Manager = models.FloatField(null=True, blank=True)
    Date = models.DateField()
    Libellé = models.CharField(max_length=100)
    Nbre_heures = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.TMission} - {self.Raison_sociale}"
