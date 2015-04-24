from django.db import models

class DrugsAndSNP(models.Model):
    drug = models.CharField(max_length = 30, unique = True)
    snp = models.CharField(max_length = 30)

    def __unicode__(self):
        return self.drug