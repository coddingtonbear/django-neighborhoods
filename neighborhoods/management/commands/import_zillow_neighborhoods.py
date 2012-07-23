import logging
import urllib2

from django.contrib.localflavor.us.us_states import STATE_CHOICES
from django.core.management.base import BaseCommand, CommandError

from neighborhoods.models import Neighborhood, NeighborhoodSource
from neighborhoods.importer import NeighborhoodShapefileImporter, \
        NeighborhoodShapefileImporterException

logger = logging.getLogger('neighborhoods.management.commands.import_zillow_neighborhoods')
logging.basicConfig(level=logging.INFO)

class ZillowNeighborhoodShapefileImporter(NeighborhoodShapefileImporter):
    def get_neighborhood(self, row, geometry):
        place = Neighborhood()
        place.source, created = NeighborhoodSource.objects.get_or_create(
                name='Zillow',
                slug='zillow',
                priority=10
                )
        place.state = row.get('STATE')
        place.city = row.get('CITY')
        place.name = row.get('NAME')
        place.region_id = row.get('REGIONID')
        place.geog = geometry.wkt
        return place

class Command(BaseCommand):
    args = '<\'Two-letter state abbreviation\'|\'all\'>' 
    help = 'Downloads and imports neighborhood boundaries supplied by Zillow.'

    URL_PATTERN = "http://www.zillow.com/static/shp/ZillowNeighborhoods-%(state_abbreviation)s.zip"

    def handle(self, *args, **options):
        try:
            arg = args[0]
        except IndexError:
            raise CommandError(
                "You must supply an argument of a two-letter state abbreviation "
                "or the word 'all'."
                )
        if arg.lower() == 'all':
            return self.import_all_states()
        else:
            return self.import_single_state(arg)

    def import_all_states(self):
        for state_info in STATE_CHOICES:
            self.import_single_state(state_info[0])

    def import_single_state(self, arg):
        url = self._get_url_from_arg(arg)
        logger.info("Downloading data for \"%s\" from %s" % (arg, url))

        try:
            importer = ZillowNeighborhoodShapefileImporter(url)
            importer.process()
        except NeighborhoodShapefileImporterException as e:
            logger.exception(e)
        except urllib2.HTTPError:
            logger.warning("No data available for \"%s\"." % arg)

    def _get_url_from_arg(self, arg):
        state = None
        if len(arg) == 2:
            state = arg.upper()
        else:
            for choice in STATE_CHOICES:
                if choice[2].upper() == arg:
                    state = choice[1].upper()

        return self.URL_PATTERN % {'state_abbreviation': state}
