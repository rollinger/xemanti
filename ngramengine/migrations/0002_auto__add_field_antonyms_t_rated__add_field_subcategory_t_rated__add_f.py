# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Antonyms.t_rated'
        db.add_column('ngramengine_antonyms', 't_rated',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'SubCategory.t_rated'
        db.add_column('ngramengine_subcategory', 't_rated',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'SuperCategory.t_rated'
        db.add_column('ngramengine_supercategory', 't_rated',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Synonyms.t_rated'
        db.add_column('ngramengine_synonyms', 't_rated',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Antonyms.t_rated'
        db.delete_column('ngramengine_antonyms', 't_rated')

        # Deleting field 'SubCategory.t_rated'
        db.delete_column('ngramengine_subcategory', 't_rated')

        # Deleting field 'SuperCategory.t_rated'
        db.delete_column('ngramengine_supercategory', 't_rated')

        # Deleting field 'Synonyms.t_rated'
        db.delete_column('ngramengine_synonyms', 't_rated')


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
        'ngramengine.inputstack': {
            'Meta': {'object_name': 'InputStack'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ngramengine.languages': {
            'Meta': {'ordering': "['language']", 'object_name': 'Languages'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'ngrams': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'language'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['ngramengine.NGrams']"})
        },
        'ngramengine.ngrams': {
            'Meta': {'ordering': "['token']", 'object_name': 'NGrams'},
            'dirty': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            't_occurred': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'wordstem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ngramengine.WordStems']", 'null': 'True', 'blank': 'True'})
        },
        'ngramengine.partofspeech': {
            'Meta': {'ordering': "['type']", 'object_name': 'PartOfSpeech'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicates_semantic_meaninglessness': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ngrams': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'partofspeech'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['ngramengine.NGrams']"}),
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