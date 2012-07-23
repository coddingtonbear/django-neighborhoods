import logging
import os.path
import shutil
import tempfile
import urllib2
import zipfile

from django.contrib.gis.gdal import DataSource, OGRGeometry, OGRGeomType
from django.db import transaction
from django.db.utils import IntegrityError

logger = logging.getLogger('neighborhoods.importer')

class NeighborhoodShapefileImporterException(Exception):
    pass

class NeighborhoodShapefileImporter(object):
    def __init__(self, url):
        self.url = url

    @transaction.commit_on_success
    def process(self):
        shapefile_dir = self._get_temporary_shapefile_dir_from_url(self.url)
        self._insert_from_shapefile(shapefile_dir)
        shutil.rmtree(shapefile_dir)

    def _cleanup_temporary_directory(self, directory):
        shutil.rmtree(directory)

    def _get_multipolygon_geometry_from_row(self, row):
        if row.geom_type.django == 'PolygonField':
            geom = OGRGeometry(OGRGeomType('MultiPolygon'))
            geom.add(row.geom)
            geom.coord_dim = 2
            return geom
        elif row.geom_type.django == 'MultiPolygonField':
            return geom

    def transform_geometry(self, geom):
        return geom

    def _insert_from_shapefile(self, shapefile_dir):
        shapefile_path = self._get_shapefile_path_from_directory(shapefile_dir)
        source = DataSource(shapefile_path)

        for row in source[0]:
            geom = self._get_multipolygon_geometry_from_row(row)
            geom = self.transform_geometry(geom)
            if not geom:
                logger.warning(
                        "Unable to convert row %s %s into MultiPolygon" % (
                            row.fid,
                            repr(row)
                            )
                        )
                continue
            place = self.get_neighborhood(row, geom)
            sid = transaction.savepoint()
            try:
                place.save()
                transaction.savepoint_commit(sid)
                logger.info(
                        "(%s) %s, %s, %s Imported Successfully" % (
                            row.fid,
                            place.name,
                            place.city,
                            place.state,
                            )
                        )
            except IntegrityError:
                transaction.savepoint_rollback(sid)
                logger.warning(
                        "(%s) %s, %s, %s Already Exists" % (
                            row.fid,
                            place.name,
                            place.city,
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
            raise NeighborhoodShapefileImporterException(
                "No shapefile was found in the data extracted!"
                )

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
