# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        zillow = orm['neighborhoods.NeighborhoodSource']()
        zillow.name = 'Zillow'
        zillow.slug = 'zillow'
        zillow.priority = 10
        zillow.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'neighborhoods.neighborhood': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('state', 'city', 'name'),)", 'object_name': 'Neighborhood'},
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
    symmetrical = True
