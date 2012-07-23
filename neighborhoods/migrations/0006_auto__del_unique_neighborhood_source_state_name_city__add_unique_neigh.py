# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Neighborhood', fields ['source', 'state', 'name', 'city']
        db.delete_unique('neighborhoods_neighborhood', ['source_id', 'state', 'name', 'city'])

        # Adding unique constraint on 'Neighborhood', fields ['region_id', 'source', 'state', 'name', 'city']
        db.create_unique('neighborhoods_neighborhood', ['region_id', 'source_id', 'state', 'name', 'city'])


    def backwards(self, orm):
        # Removing unique constraint on 'Neighborhood', fields ['region_id', 'source', 'state', 'name', 'city']
        db.delete_unique('neighborhoods_neighborhood', ['region_id', 'source_id', 'state', 'name', 'city'])

        # Adding unique constraint on 'Neighborhood', fields ['source', 'state', 'name', 'city']
        db.create_unique('neighborhoods_neighborhood', ['source_id', 'state', 'name', 'city'])


    models = {
        'neighborhoods.neighborhood': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('source', 'state', 'city', 'name', 'region_id'),)", 'object_name': 'Neighborhood'},
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