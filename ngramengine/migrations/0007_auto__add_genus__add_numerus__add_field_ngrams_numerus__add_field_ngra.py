# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Genus'
        db.create_table('ngramengine_genus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('ngramengine', ['Genus'])

        # Adding model 'Numerus'
        db.create_table('ngramengine_numerus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('ngramengine', ['Numerus'])

        # Adding field 'NGrams.numerus'
        db.add_column('ngramengine_ngrams', 'numerus',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ngramengine.Numerus'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'NGrams.genus'
        db.add_column('ngramengine_ngrams', 'genus',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ngramengine.Genus'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Genus'
        db.delete_table('ngramengine_genus')

        # Deleting model 'Numerus'
        db.delete_table('ngramengine_numerus')

        # Deleting field 'NGrams.numerus'
        db.delete_column('ngramengine_ngrams', 'numerus_id')

        # Deleting field 'NGrams.genus'
        db.delete_column('ngramengine_ngrams', 'genus_id')


    models = {
        'ngramengine.antonyms': {
            'Meta': {'object_name': 'Antonyms'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'antonym'", 'to': "orm['ngramengine.NGrams']"}),
            't_rated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'antonym_of'", 'to': "orm['ngramengine.NGrams']"})
        },
        'ngramengine.associations': {
            'Meta': {'object_name': 'Associations'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'power': ('django.db.models.fields.FloatField', [], {}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'association_outbound'", 'to': "orm['ngramengine.NGrams']"}),
            't_associated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'association_inbound'", 'to': "orm['ngramengine.NGrams']"})
        },
        'ngramengine.cooccurrences': {
            'Meta': {'object_name': 'CoOccurrences'},
            'dirty': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mean_position': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'positions': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10000'}),
            'power': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coocurrence_outbound'", 'to': "orm['ngramengine.NGrams']"}),
            't_cooccured': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coocurrence_inbound'", 'to': "orm['ngramengine.NGrams']"})
        },
        'ngramengine.genus': {
            'Meta': {'ordering': "['type']", 'object_name': 'Genus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'ngramengine.inputstack': {
            'Meta': {'object_name': 'InputStack'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ngramengine.languages': {
            'Meta': {'ordering': "['language']", 'object_name': 'Languages'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'ngram_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'ngrams': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'language'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['ngramengine.NGrams']"})
        },
        'ngramengine.ngrams': {
            'Meta': {'ordering': "['token']", 'object_name': 'NGrams'},
            'dirty': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'genus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ngramengine.Genus']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numerus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ngramengine.Numerus']", 'null': 'True', 'blank': 'True'}),
            'qualified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'semantic_meaningless': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            't_occurred': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'wordstem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ngramengine.WordStems']", 'null': 'True', 'blank': 'True'})
        },
        'ngramengine.numerus': {
            'Meta': {'ordering': "['type']", 'object_name': 'Numerus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'ngramengine.partofspeech': {
            'Meta': {'ordering': "['type']", 'object_name': 'PartOfSpeech'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ngram_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'ngrams': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'partofspeech'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['ngramengine.NGrams']"}),
            'semantic_meaningless': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'ngramengine.subcategory': {
            'Meta': {'object_name': 'SubCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subcategory'", 'to': "orm['ngramengine.NGrams']"}),
            't_rated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subcategory_of'", 'to': "orm['ngramengine.NGrams']"})
        },
        'ngramengine.supercategory': {
            'Meta': {'object_name': 'SuperCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercategory'", 'to': "orm['ngramengine.NGrams']"}),
            't_rated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercategory_of'", 'to': "orm['ngramengine.NGrams']"})
        },
        'ngramengine.synonyms': {
            'Meta': {'object_name': 'Synonyms'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'synonyms'", 'to': "orm['ngramengine.NGrams']"}),
            't_rated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'synonym_of'", 'to': "orm['ngramengine.NGrams']"})
        },
        'ngramengine.wordstems': {
            'Meta': {'ordering': "['stem']", 'object_name': 'WordStems'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stem': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['ngramengine']