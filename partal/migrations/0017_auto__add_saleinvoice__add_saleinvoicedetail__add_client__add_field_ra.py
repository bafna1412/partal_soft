# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SaleInvoice'
        db.create_table(u'partal_saleinvoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2015, 4, 5, 0, 0))),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['partal.Client'])),
            ('invoice_no', self.gf('django.db.models.fields.CharField')(default='None', unique=True, max_length=10)),
            ('family', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['partal.Commodity'])),
            ('weight', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('bags', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('VAT', self.gf('django.db.models.fields.FloatField')()),
            ('insurance', self.gf('django.db.models.fields.FloatField')()),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'partal', ['SaleInvoice'])

        # Adding model 'SaleInvoiceDetail'
        db.create_table(u'partal_saleinvoicedetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['partal.SaleInvoice'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['partal.Product'])),
            ('weight', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('bharti', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=2)),
            ('rate', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=5)),
            ('bags', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'partal', ['SaleInvoiceDetail'])

        # Adding model 'Client'
        db.create_table(u'partal_client', (
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, primary_key=True)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('contact_number', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('PAN', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('TIN', self.gf('django.db.models.fields.CharField')(unique=True, max_length=11)),
            ('net_sale_weight', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('net_sale_amount', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'partal', ['Client'])

        # Adding field 'RateDetail.insurance'
        db.add_column(u'partal_ratedetail', 'insurance',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'ProcessEntry.process'
        db.add_column(u'partal_processentry', 'process',
                      self.gf('django.db.models.fields.CharField')(default='None', max_length=100),
                      keep_default=False)

        # Adding field 'ProcessEntry.storage'
        db.add_column(u'partal_processentry', 'storage',
                      self.gf('django.db.models.fields.CharField')(default='None', max_length=25),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'SaleInvoice'
        db.delete_table(u'partal_saleinvoice')

        # Deleting model 'SaleInvoiceDetail'
        db.delete_table(u'partal_saleinvoicedetail')

        # Deleting model 'Client'
        db.delete_table(u'partal_client')

        # Deleting field 'RateDetail.insurance'
        db.delete_column(u'partal_ratedetail', 'insurance')

        # Deleting field 'ProcessEntry.process'
        db.delete_column(u'partal_processentry', 'process')

        # Deleting field 'ProcessEntry.storage'
        db.delete_column(u'partal_processentry', 'storage')


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
        u'partal.client': {
            'Meta': {'object_name': 'Client'},
            'PAN': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'TIN': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'}),
            'address': ('django.db.models.fields.TextField', [], {}),
            'contact_number': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'primary_key': 'True'}),
            'net_sale_amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'net_sale_weight': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'partal.commodity': {
            'Meta': {'object_name': 'Commodity'},
            'avg_price_processed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'avg_price_raw': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bags_cold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bags_processed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bags_raw': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'primary_key': 'True'}),
            'net_stock_processed': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'net_stock_raw': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'stock_cold': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'partal.dailypurchase': {
            'Meta': {'object_name': 'DailyPurchase'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 4, 5, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['partal.Product']"}),
            'product_bags': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'product_weight': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'total_purchase_amount': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'partal.firm': {
            'Meta': {'object_name': 'Firm'},
            'PAN': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'TIN': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'}),
            'address': ('django.db.models.fields.TextField', [], {}),
            'contact_number': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'monthly_tds': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'primary_key': 'True'}),
            'net_commission': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'net_purchase_amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'net_purchase_weight': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'partal.processentry': {
            'Meta': {'object_name': 'ProcessEntry'},
            'bags_in': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bags_out': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 4, 5, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'process': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '100'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['partal.Product']"}),
            'storage': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '25'}),
            'weight_in': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'weight_out': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'partal.product': {
            'Meta': {'object_name': 'Product'},
            'avg_price_processed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'avg_price_raw': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bags_cold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bags_processed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bags_raw': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'commodity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['partal.Commodity']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'primary_key': 'True'}),
            'net_stock_processed': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'net_stock_raw': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'stock_cold': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'partal.purchaseinvoice': {
            'Meta': {'object_name': 'PurchaseInvoice'},
            'TDS': ('django.db.models.fields.FloatField', [], {}),
            'VAT': ('django.db.models.fields.FloatField', [], {}),
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'association_charges': ('django.db.models.fields.FloatField', [], {}),
            'bags': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'commission': ('django.db.models.fields.FloatField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 4, 5, 0, 0)'}),
            'dharmada': ('django.db.models.fields.FloatField', [], {}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['partal.Commodity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandi_tax': ('django.db.models.fields.FloatField', [], {}),
            'muddat': ('django.db.models.fields.FloatField', [], {}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['partal.Firm']"}),
            'seller_invoice_no': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '10'}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'partal.purchaseinvoicedetail': {
            'Meta': {'object_name': 'PurchaseInvoiceDetail'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'bags': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bharti': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['partal.PurchaseInvoice']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['partal.Product']"}),
            'rate': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '5'}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'partal.ratedetail': {
            'Meta': {'object_name': 'RateDetail'},
            'TDS': ('django.db.models.fields.FloatField', [], {}),
            'VAT': ('django.db.models.fields.FloatField', [], {}),
            'association_charges': ('django.db.models.fields.FloatField', [], {}),
            'commission': ('django.db.models.fields.FloatField', [], {}),
            'dharmada': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insurance': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'mandi_tax': ('django.db.models.fields.FloatField', [], {}),
            'muddat': ('django.db.models.fields.FloatField', [], {})
        },
        u'partal.saleinvoice': {
            'Meta': {'object_name': 'SaleInvoice'},
            'VAT': ('django.db.models.fields.FloatField', [], {}),
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'bags': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['partal.Client']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 4, 5, 0, 0)'}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['partal.Commodity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insurance': ('django.db.models.fields.FloatField', [], {}),
            'invoice_no': ('django.db.models.fields.CharField', [], {'default': "'None'", 'unique': 'True', 'max_length': '10'}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'partal.saleinvoicedetail': {
            'Meta': {'object_name': 'SaleInvoiceDetail'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'bags': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bharti': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['partal.SaleInvoice']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['partal.Product']"}),
            'rate': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '5'}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'partal.user': {
            'Meta': {'object_name': 'User'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['partal']