# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'RideAdvert.offerred_price'
        db.delete_column(u'ride_rideadvert', 'offerred_price')

        # Adding field 'RideAdvert.price'
        db.add_column(u'ride_rideadvert', 'price',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0),
                      keep_default=False)

        # Adding M2M table for field passengers on 'Ride'
        m2m_table_name = db.shorten_name(u'ride_ride_passengers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ride', models.ForeignKey(orm[u'ride.ride'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ride_id', 'user_id'])


    def backwards(self, orm):
        # Adding field 'RideAdvert.offerred_price'
        db.add_column(u'ride_rideadvert', 'offerred_price',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=3),
                      keep_default=False)

        # Deleting field 'RideAdvert.price'
        db.delete_column(u'ride_rideadvert', 'price')

        # Removing M2M table for field passengers on 'Ride'
        db.delete_table(db.shorten_name(u'ride_ride_passengers'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ride.ride': {
            'Meta': {'object_name': 'Ride'},
            'advert': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ride.RideAdvert']", 'unique': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'TRY'", 'max_length': '10'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'driver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'offerred_seats': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'passengers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'passenger_rides'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'price': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'route': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ride.Route']", 'unique': 'True'}),
            'state': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ride.Vehicle']"})
        },
        u'ride.rideadvert': {
            'Meta': {'object_name': 'RideAdvert'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'TRY'", 'max_length': '10'}),
            'driver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'offerred_seats': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'price': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'route': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ride.Route']", 'unique': 'True'}),
            'schedule': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ride.Schedule']", 'unique': 'True'}),
            'vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ride.Vehicle']"})
        },
        u'ride.rideexperience': {
            'Meta': {'object_name': 'RideExperience'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ride': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'experiences'", 'to': u"orm['ride.Ride']"}),
            'state': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'ride.riderequest': {
            'Meta': {'object_name': 'RideRequest'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'driver_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'passenger': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'passenger_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ride': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requests'", 'to': u"orm['ride.Ride']"}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'})
        },
        u'ride.route': {
            'Meta': {'object_name': 'Route'},
            'end_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'end_latitude': ('django.db.models.fields.FloatField', [], {}),
            'end_longitude': ('django.db.models.fields.FloatField', [], {}),
            'end_radius': ('django.db.models.fields.FloatField', [], {'default': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'start_latitude': ('django.db.models.fields.FloatField', [], {}),
            'start_longitude': ('django.db.models.fields.FloatField', [], {}),
            'start_radius': ('django.db.models.fields.FloatField', [], {'default': '4'})
        },
        u'ride.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'byweekday': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_recurring': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'ride.vehicle': {
            'Meta': {'object_name': 'Vehicle'},
            'brand': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'seat_capacity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '4', 'blank': 'True'})
        }
    }

    complete_apps = ['ride']