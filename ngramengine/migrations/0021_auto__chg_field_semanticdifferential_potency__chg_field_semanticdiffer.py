# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SemanticDifferential.potency'
        db.alter_column(u'ngramengine_semanticdifferential', 'potency', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'SemanticDifferential.activity'
        db.alter_column(u'ngramengine_semanticdifferential', 'activity', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'SemanticDifferential.evaluation'
        db.alter_column(u'ngramengine_semanticdifferential', 'evaluation', self.gf('django.db.models.fields.FloatField')())

    def backwards(self, orm):

        # Changing field 'SemanticDifferential.potency'
        db.alter_column(u'ngramengine_semanticdifferential', 'potency', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=3))

        # Changing field 'SemanticDifferential.activity'
        db.alter_column(u'ngramengine_semanticdifferential', 'activity', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=3))

        # Changing field 'SemanticDifferential.evaluation'
        db.alter_column(u'ngramengine_semanticdifferential', 'evaluation', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=3))

    models = {
        u'ngramengine.antonyms': {
            'Meta': {'object_name': 'Antonyms'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'power': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'antonyms'", 'to': u"orm['ngramengine.NGrams']"}),
            't_rated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'antonym_of'", 'to': u"orm['ngramengine.NGrams']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ngramengine.associations': {
            'Meta': {'object_name': 'Associations'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dirty': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'power': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'association_outbound'", 'to': u"orm['ngramengine.NGrams']"}),
            't_associated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'association_inbound'", 'to': u"orm['ngramengine.NGrams']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ngramengine.cooccurrences': {
            'Meta': {'object_name': 'CoOccurrences'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dirty': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mean_position': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'positions': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10000'}),
            'power': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coocurrence_outbound'", 'to': u"orm['ngramengine.NGrams']"}),
            't_cooccured': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coocurrence_inbound'", 'to': u"orm['ngramengine.NGrams']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ngramengine.genus': {
            'Meta': {'ordering': "['type']", 'object_name': 'Genus'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ngramengine.languages': {
            'Meta': {'ordering': "['language']", 'object_name': 'Languages'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'ngram_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'ngrams': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'language'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['ngramengine.NGrams']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ngramengine.ngrams': {
            'Meta': {'ordering': "['token']", 'object_name': 'NGrams'},
            'coocurrence_relevancy': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dirty': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'genus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ngramengine.Genus']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numerus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ngramengine.Numerus']", 'null': 'True', 'blank': 'True'}),
            'qualified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            't_occurred': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            't_rated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'wordstem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ngramengine.WordStems']", 'null': 'True', 'blank': 'True'})
        },
        u'ngramengine.notrelated': {
            'Meta': {'object_name': 'NotRelated'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'power': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'not_related_to'", 'to': u"orm['ngramengine.NGrams']"}),
            't_rated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'not_related_from'", 'to': u"orm['ngramengine.NGrams']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ngramengine.numerus': {
            'Meta': {'ordering': "['type']", 'object_name': 'Numerus'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ngramengine.partofspeech': {
            'Meta': {'ordering': "['type']", 'object_name': 'PartOfSpeech'},
            'coocurrence_relevancy': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ngram_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'ngrams': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'partofspeech'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['ngramengine.NGrams']"}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ngramengine.semanticdifferential': {
            'Meta': {'object_name': 'SemanticDifferential'},
            'activity': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'evaluation': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ngram': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ngramengine.NGrams']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'potency': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ngramengine.subcategory': {
            'Meta': {'object_name': 'SubCategory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'power': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subcategories'", 'to': u"orm['ngramengine.NGrams']"}),
            't_rated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subcategory_of'", 'to': u"orm['ngramengine.NGrams']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ngramengine.supercategory': {
            'Meta': {'object_name': 'SuperCategory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'power': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercategories'", 'to': u"orm['ngramengine.NGrams']"}),
            't_rated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercategory_of'", 'to': u"orm['ngramengine.NGrams']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ngramengine.synonyms': {
            'Meta': {'object_name': 'Synonyms'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'power': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'synonyms'", 'to': u"orm['ngramengine.NGrams']"}),
            't_rated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'synonym_of'", 'to': u"orm['ngramengine.NGrams']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ngramengine.wordstems': {
            'Meta': {'ordering': "['stem']", 'object_name': 'WordStems'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stem': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ngramengine']