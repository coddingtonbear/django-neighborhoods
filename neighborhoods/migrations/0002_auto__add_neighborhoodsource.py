# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NeighborhoodSource'
        db.create_table('neighborhoods_neighborhoodsource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('priority', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('neighborhoods', ['NeighborhoodSource'])


    def backwards(self, orm):
        # Deleting model 'NeighborhoodSource'
        db.delete_table('neighborhoods_neighborhoodsource')


    models = {
        'neighborhoods.neighborhood': {
            'Meta': {'ordering': "['name']", 'object_name': 'Neighborhood'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'geography': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'region_id': ('django.db.models.fields.FloatField', [], {}),
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