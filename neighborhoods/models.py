import logging

from django.contrib.gis.db import models

logger = logging.getLogger('neighborhoods.models')

class NeighborhoodSource(models.Model):
    name = models.CharField(
            max_length=255,
            )
    slug = models.SlugField()
    priority = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.name

class Neighborhood(models.Model):
    source = models.ForeignKey(NeighborhoodSource)
    state = models.CharField(
            max_length=2,
            db_index=True,
            )
    city = models.CharField(
            max_length=90,
            )
    name = models.CharField(
            max_length=90,
            )
    geog = models.MultiPolygonField(
            geography=True,
            spatial_index=True
            )
    region_id = models.FloatField()

    objects = models.GeoManager()

    @classmethod
    def get_containing(cls, point):
        try:
            boundary = cls.objects.filter(geog__covers=point)\
                    .order_by('source__priority')\
                    [0]
            logger.debug("Found geometry %s covering %s" % (
                    boundary,
                    point,
                    )
                )
            return boundary
        except IndexError:
            raise cls.DoesNotExist("A place covering %s does not exist." % point)

    def __unicode__(self):
        return "%s, %s, %s" % (
                self.name,
                self.city,
                self.state,
                )

    class Meta:
        unique_together = (
                'source',
                'state',
                'city',
                'name',
                'region_id',
                )
        ordering = ['name', ]
