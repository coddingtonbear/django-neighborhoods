# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Neighborhood'
        db.create_table('neighborhoods_neighborhood', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, db_index=True)),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('geog', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(geography=True)),
            ('region_id', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('neighborhoods', ['Neighborhood'])


    def backwards(self, orm):
        # Deleting model 'Neighborhood'
        db.delete_table('neighborhoods_neighborhood')


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
        }
    }

    complete_apps = ['neighborhoods']