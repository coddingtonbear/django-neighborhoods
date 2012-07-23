# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Neighborhood.county'
        db.delete_column('neighborhoods_neighborhood', 'county')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Neighborhood.county'
        raise RuntimeError("Cannot reverse this migration. 'Neighborhood.county' and its values cannot be restored.")

    models = {
        'neighborhoods.neighborhood': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('source', 'state', 'city', 'name'),)", 'object_name': 'Neighborhood'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'geography': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'region_id': ('django.db.models.fields.FloatField', [], {}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['neighborhoods.NeighborhoodSource']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'})
        },
        'neighborhoods.neighborhoodsource': {
            'Meta': {'object_name': 'NeighborhoodSource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['neighborhoods']