from datetime import date

from django.db import models

# Create your models here.
from django.db.models import CASCADE


class Catalog(models.Model):
    id = models.AutoField(primary_key=True)
    short_title = models.CharField('Короткое название', max_length=100)
    full_title = models.CharField('Полное название', max_length=200)
    description = models.TextField('Описание', blank=True, null=True,)
    version = models.CharField('Версия', max_length=100, blank=False, null=False, )
    start_date = models.DateField('Дата начала действия справочника', default=date.today)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("full_title", "version"), name="unique_catalog_version")]

    def __str__(self):
        return f'{self.full_title} ver {self.version}'


class Element(models.Model):
    id = models.AutoField(primary_key=True)
    catalog = models.ForeignKey(Catalog, on_delete=CASCADE, related_name="elements")
    parent_id = models.IntegerField('Родительский идентификатор', blank=True, null=True)
    code = models.CharField('Код элемента', max_length=50, blank=False, null=False)
    value = models.CharField('Значение элемента', max_length=500, blank=False, null=False)

