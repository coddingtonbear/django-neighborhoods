import logging

from django.contrib.gis.db import models

logger = logging.getLogger('neighborhoods.models')

class Neighborhood(models.Model):
    state = models.CharField(
            max_length=2,
            db_index=True,
            )
    county = models.CharField(
            max_length=90,
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
        boundary = cls.objects.get(
                geog__covers=point
                )
        logger.debug("Found geometry %s covering %s" % (
                boundary,
                point,
                )
            )
        return boundary

    class Meta:
        unique_together = (
                'state',
                'city',
                'name',
                )
        ordering = ['name', ]
