# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PurchaseDetail'
        db.create_table(u'partal_purchasedetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['partal.PurchaseInvoice'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['partal.Product'])),
            ('weight', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('bharti', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=2)),
            ('rate', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=5)),
            ('bags', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'partal', ['PurchaseDetail'])

        # Deleting field 'PurchaseInvoice.bags'
        db.delete_column(u'partal_purchaseinvoice', 'bags')

        # Deleting field 'PurchaseInvoice.product'
        db.delete_column(u'partal_purchaseinvoice', 'product_id')

        # Deleting field 'PurchaseInvoice.weight'
        db.delete_column(u'partal_purchaseinvoice', 'weight')

        # Deleting field 'PurchaseInvoice.bharti'
        db.delete_column(u'partal_purchaseinvoice', 'bharti')

        # Deleting field 'PurchaseInvoice.rate'
        db.delete_column(u'partal_purchaseinvoice', 'rate')

        # Adding field 'PurchaseInvoice.seller_invoice_no'
        db.add_column(u'partal_purchaseinvoice', 'seller_invoice_no',
                      self.gf('django.db.models.fields.CharField')(default='None', max_length=10),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'PurchaseDetail'
        db.delete_table(u'partal_purchasedetail')

        # Adding field 'PurchaseInvoice.bags'
        db.add_column(u'partal_purchaseinvoice', 'bags',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'PurchaseInvoice.product'
        db.add_column(u'partal_purchaseinvoice', 'product',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['partal.Product']),
                      keep_default=False)

        # Adding field 'PurchaseInvoice.weight'
        db.add_column(u'partal_purchaseinvoice', 'weight',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'PurchaseInvoice.bharti'
        db.add_column(u'partal_purchaseinvoice', 'bharti',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=2),
                      keep_default=False)

        # Adding field 'PurchaseInvoice.rate'
        db.add_column(u'partal_purchaseinvoice', 'rate',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=5),
                      keep_default=False)

        # Deleting field 'PurchaseInvoice.seller_invoice_no'
        db.delete_column(u'partal_purchaseinvoice', 'seller_invoice_no')


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
        u'partal.commodity': {
            'Meta': {'object_name': 'Commodity'},
            'bags_processed': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'bags_raw': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'daily_purchase': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 3, 28, 0, 0)'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'primary_key': 'True'}),
            'net_stock_processed': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'net_stock_raw': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'total_purchase': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'partal.firm': {
            'Meta': {'object_name': 'Firm'},
            'PAN': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'TIN': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'address': ('django.db.models.fields.TextField', [], {}),
            'contact_number': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'primary_key': 'True'}),
            'net_commission': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'net_purchase_amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'net_purchase_weight': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'partal.product': {
            'Meta': {'object_name': 'Product'},
            'bags_processed': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'bags_raw': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'commodity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['partal.Commodity']"}),
            'daily_purchase': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 3, 28, 0, 0)'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'primary_key': 'True'}),
            'net_stock_processed': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'net_stock_raw': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'total_purchase': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'partal.purchasedetail': {
            'Meta': {'object_name': 'PurchaseDetail'},
            'bags': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'bharti': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['partal.PurchaseInvoice']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['partal.Product']"}),
            'rate': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '5'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'partal.purchaseinvoice': {
            'Meta': {'object_name': 'PurchaseInvoice'},
            'TDS': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'VAT': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'association_charges': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'commission': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 3, 28, 0, 0)'}),
            'dharmada': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandi_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'muddat': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['partal.Firm']"}),
            'seller_invoice_no': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '10'})
        },
        u'partal.ratedetail': {
            'Meta': {'object_name': 'RateDetail'},
            'TDS': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'VAT': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'association_charges': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'}),
            'commission': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'}),
            'dharmada': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandi_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'}),
            'muddat': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'})
        },
        u'partal.user': {
            'Meta': {'object_name': 'User'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['partal']