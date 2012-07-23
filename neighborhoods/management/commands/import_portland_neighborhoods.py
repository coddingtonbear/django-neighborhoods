import logging
import urllib2

from django.contrib.gis.gdal import CoordTransform, SpatialReference
from django.core.management.base import BaseCommand
from django.template.defaultfilters import title

from neighborhoods.models import Neighborhood, NeighborhoodSource
from neighborhoods.importer import NeighborhoodShapefileImporter, \
        NeighborhoodShapefileImporterException

logger = logging.getLogger('neighborhoods.management.commands.import_portland_neighborhoods')
logging.basicConfig(level=logging.INFO)

class PortlandNeighborhoodShapefileImporter(NeighborhoodShapefileImporter):
    def transform_geometry(self, geometry):
        transformer = CoordTransform(
                SpatialReference('2913'),
                SpatialReference('WGS84'),
                )
        geometry.transform(transformer)
        return geometry

    def get_neighborhood(self, row, geometry):
        place = Neighborhood()
        place.source, created = NeighborhoodSource.objects.get_or_create(
                name='City of Portland, Oregon',
                slug='city-of-portland-oregon',
                priority=5
                )
        place.state = 'OR'
        place.city = 'Portland'
        place.name = title(row.get('NAME'))
        place.region_id = row.get('NBO_ID')
        place.geog = geometry.wkt
        return place

class Command(BaseCommand):
    args = '<\'Two-letter state abbreviation\'|\'all\'>' 
    help = 'Downloads and imports neighborhood boundaries supplied by Zillow.'

    URL = 'ftp://ftp02.portlandoregon.gov/CivicApps/Neighborhoods_pdx.zip'

    def handle(self, *args, **options):
        try:
            logger.info("Downloading data from \"%s\"" % (self.URL))
            importer = PortlandNeighborhoodShapefileImporter(self.URL)
            importer.process()
        except NeighborhoodShapefileImporterException as e:
            logger.exception(e)
        except urllib2.HTTPError:
            logger.error("Unable to download data!  Did the City of Portland change the URL?")
