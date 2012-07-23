# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Neighborhood', fields ['city', 'state', 'name']
        db.delete_unique('neighborhoods_neighborhood', ['city', 'state', 'name'])

        # Adding field 'Neighborhood.source'
        db.add_column('neighborhoods_neighborhood', 'source',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['neighborhoods.NeighborhoodSource']),
                      keep_default=False)

        # Adding unique constraint on 'Neighborhood', fields ['source', 'state', 'name', 'city']
        db.create_unique('neighborhoods_neighborhood', ['source_id', 'state', 'name', 'city'])


    def backwards(self, orm):
        # Removing unique constraint on 'Neighborhood', fields ['source', 'state', 'name', 'city']
        db.delete_unique('neighborhoods_neighborhood', ['source_id', 'state', 'name', 'city'])

        # Deleting field 'Neighborhood.source'
        db.delete_column('neighborhoods_neighborhood', 'source_id')

        # Adding unique constraint on 'Neighborhood', fields ['city', 'state', 'name']
        db.create_unique('neighborhoods_neighborhood', ['city', 'state', 'name'])


    models = {
        'neighborhoods.neighborhood': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('source', 'state', 'city', 'name'),)", 'object_name': 'Neighborhood'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
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