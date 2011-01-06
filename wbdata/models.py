from django.db import models

class Indicator(models.Model):
    """Describes a particular World Bank data indicator"""
    id = models.CharField('Indicator Code', primary_key=True, max_length=100)
    name = models.CharField(blank=True, max_length=200)
    source_note = models.TextField(blank=True, null=True)
    source_organization = models.CharField(blank=True, max_length=140)

    class Meta:
        ordering = ['name']
        
    def __unicode__(self):
        if self.name:
            return self.name
        return self.id


class Country(models.Model):
    """Describes a country in terms of World Bank data"""
    id = models.CharField('Country Code', primary_key=True, max_length=3)
    name = models.CharField(blank=True, max_length=100)
    source_note = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "countries"
        ordering = ['name']

    def __unicode__(self):
        if self.name:
            return self.name
        return self.id


class DataPoint(models.Model):
    """Data for a particular indicator, country, and year"""
    indicator = models.ForeignKey(Indicator)
    country = models.ForeignKey(Country)
    year = models.PositiveIntegerField(db_index=True)
    value = models.DecimalField(max_digits=128, decimal_places=14)
    
    class Meta:
        order_with_respect_to = 'indicator'
        ordering = ['year', 'country']
    
    class Meta:
        unique_together = ("indicator", "country", "year")

    def __unicode__(self):
        return u"%s, %s %s" % (self.indicator, self.country, self.year)

