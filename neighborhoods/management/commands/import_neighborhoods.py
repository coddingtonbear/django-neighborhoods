from __future__ import with_statement

import logging
import os.path
import shutil
import tempfile
import urllib2
import zipfile

from django.contrib.gis.gdal import DataSource, OGRGeometry, OGRGeomType
from django.contrib.localflavor.us.us_states import STATE_CHOICES
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from neighborhoods.models import Neighborhood

logger = logging.getLogger('neighborhoods.management.commands.import_neighborhoods')
logging.basicConfig(level=logging.INFO)

class Command(BaseCommand):
    args = '<\'Two-letter state abbreviation\'|\'all\'>' 
    help = 'Downloads and imports neighborhood boundaries supplied by Zillow.'

    URL_PATTERN = "http://www.zillow.com/static/shp/ZillowNeighborhoods-%(state_abbreviation)s.zip"

    @transaction.commit_on_success
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
            shapefile_dir = self._get_temporary_shapefile_dir_from_url(url)
            self._insert_from_shapefile(shapefile_dir)
            shutil.rmtree(shapefile_dir)
        except urllib2.HTTPError:
            logger.warning("No data available for \"%s\"." % arg)

    def _cleanup_temporary_directory(self, directory):
        shutil.rmtree(directory)

    def _get_multipolygon_geometry_from_row(self, row):
        if row.geom_type.django == 'PolygonField':
            geom = OGRGeometry(OGRGeomType('MultiPolygon'))
            geom.add(row.geom)
            return geom
        elif row.geom_type.django == 'MultiPolygonField':
            return geom

    def _insert_from_shapefile(self, shapefile_dir):
        shapefile_path = self._get_shapefile_path_from_directory(shapefile_dir)
        source = DataSource(shapefile_path)

        for row in source[0]:
            geom = self._get_multipolygon_geometry_from_row(row)
            if not geom:
                logger.warning(
                        "Unable to convert row %s %s into MultiPolygon" % (
                            row.fid,
                            repr(row)
                            )
                        )
                continue
            place = Neighborhood()
            place.state = row.get('STATE')
            place.county = row.get('COUNTY')
            place.city = row.get('CITY')
            place.name = row.get('NAME')
            place.region_id = row.get('REGIONID')
            place.geog = geom.wkt
            place.save()
            logger.info(
                    "Imported (%s) %s, %s, %s, %s" % (
                        row.fid,
                        place.name,
                        place.city,
                        place.county,
                        place.state,
                        )
                    )

    def _get_shapefile_path_from_directory(self, directory):
        shapefile_path = None
        for path in os.listdir(directory):
            basename, extension = os.path.splitext(path)
            if extension == '.shp':
                shapefile_path = os.path.join(
                        directory,
                        path
                        )

        if not shapefile_path:
            raise CommandError("No shapefile was found in the data extracted!")

        return shapefile_path

    def _get_temporary_shapefile_dir_from_url(self, url):
        temporary_directory = tempfile.mkdtemp()
        with tempfile.TemporaryFile() as temporary_file:
            zip_file_stream = urllib2.urlopen(url)
            temporary_file.write(
                    zip_file_stream.read()
                    )
            zip_file_stream.close()
            archive = zipfile.ZipFile(temporary_file, 'r')
            archive.extractall(temporary_directory)
        return temporary_directory

    def _get_url_from_arg(self, arg):
        state = None
        if len(arg) == 2:
            state = arg.upper()
        else:
            for choice in STATE_CHOICES:
                if choice[2].upper() == arg:
                    state = choice[1].upper()

        return self.URL_PATTERN % {'state_abbreviation': state}
