# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Route'
        db.create_table(u'ride_route', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_latitude', self.gf('django.db.models.fields.FloatField')()),
            ('start_longitude', self.gf('django.db.models.fields.FloatField')()),
            ('start_radius', self.gf('django.db.models.fields.FloatField')(default=4)),
            ('start_address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('end_latitude', self.gf('django.db.models.fields.FloatField')()),
            ('end_longitude', self.gf('django.db.models.fields.FloatField')()),
            ('end_radius', self.gf('django.db.models.fields.FloatField')(default=4)),
            ('end_address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'ride', ['Route'])

        # Adding model 'Schedule'
        db.create_table(u'ride_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_recurring', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('byweekday', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=16, null=True, blank=True)),
        ))
        db.send_create_signal(u'ride', ['Schedule'])

        # Adding model 'Vehicle'
        db.create_table(u'ride_vehicle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brand', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('year', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=4, blank=True)),
            ('seat_capacity', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=3)),
        ))
        db.send_create_signal(u'ride', ['Vehicle'])

        # Adding model 'RideAdvert'
        db.create_table(u'ride_rideadvert', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('route', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ride.Route'], unique=True)),
            ('schedule', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ride.Schedule'], unique=True)),
            ('driver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('vehicle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ride.Vehicle'])),
            ('offerred_seats', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=3)),
            ('offerred_price', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'ride', ['RideAdvert'])

        # Adding model 'Ride'
        db.create_table(u'ride_ride', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('advert', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ride.RideAdvert'], unique=True)),
            ('route', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ride.Route'], unique=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('driver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('vehicle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ride.Vehicle'])),
            ('offerred_seats', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=3)),
            ('price', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('currency', self.gf('django.db.models.fields.CharField')(default='TRY', max_length=10)),
            ('state', self.gf('django.db.models.fields.CharField')(default='PENDING', max_length=23)),
        ))
        db.send_create_signal(u'ride', ['Ride'])

        # Adding model 'RideRequest'
        db.create_table(u'ride_riderequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('ride', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requests', to=orm['ride.Ride'])),
            ('passenger', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='PENDING', max_length=8)),
            ('passenger_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('driver_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'ride', ['RideRequest'])

        # Adding model 'RideExperience'
        db.create_table(u'ride_rideexperience', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('ride', self.gf('django.db.models.fields.related.ForeignKey')(related_name='experiences', to=orm['ride.Ride'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'ride', ['RideExperience'])


    def backwards(self, orm):
        # Deleting model 'Route'
        db.delete_table(u'ride_route')

        # Deleting model 'Schedule'
        db.delete_table(u'ride_schedule')

        # Deleting model 'Vehicle'
        db.delete_table(u'ride_vehicle')

        # Deleting model 'RideAdvert'
        db.delete_table(u'ride_rideadvert')

        # Deleting model 'Ride'
        db.delete_table(u'ride_ride')

        # Deleting model 'RideRequest'
        db.delete_table(u'ride_riderequest')

        # Deleting model 'RideExperience'
        db.delete_table(u'ride_rideexperience')


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
            'price': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'route': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ride.Route']", 'unique': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '23'}),
            'vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ride.Vehicle']"})
        },
        u'ride.rideadvert': {
            'Meta': {'object_name': 'RideAdvert'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'driver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'offerred_price': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'offerred_seats': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
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
            'state': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
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
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '8'})
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