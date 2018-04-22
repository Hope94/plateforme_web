from django.db import models


# Create your models here.
class Dataset (models.Model):
    name = models.CharField (max_length=30, unique=True)

    def __str__(self):
        return self.name


class Apk (models.Model):
    name = models.TextField ()
    malignity = models.IntegerField ()
    package = models.TextField ()
    developer = models.TextField ()  # company name
    displayed_version = models.TextField ()
    added_on = models.DateField (auto_now_add=True)  # date d'ajout à la base de données
    size = models.PositiveIntegerField ()
    md5 = models.TextField (unique=True)
    sha1 = models.TextField (unique=True)
    sha256 = models.TextField (unique=True)
    datasets = models.ManyToManyField (Dataset)

    def __str__(self):
        return self.name


class Feature (models.Model):
    name = models.TextField ()
    type = models.TextField ()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'type',)


class Extract (models.Model):
    apk = models.ForeignKey ('Apk', on_delete=models.CASCADE,related_name='extractions')
    feature = models.ForeignKey ('Feature', on_delete=models.CASCADE,related_name='extractions')
    nb_feature = models.PositiveIntegerField ()  # nombre de caractéristiques
    extracted_on = models.DateField (auto_now_add=True)  # date d'extraction des caractéristiques

    def __str__(self):
        return "{0} - {1}".format (self.apk.name, self.feature.name)

    class Meta:
        unique_together = ('apk', 'feature',)



class SuspiciousAPI (models.Model):
    api = models.TextField (unique=True)

    def __str__(self):
        return self.api


class PermissionAPI (models.Model):
    api = models.TextField ()
    permission = models.TextField ()

    def __str__(self):
        return self.api + ' ' + self.permission

    class Meta:
        unique_together = ('api', 'permission',)
