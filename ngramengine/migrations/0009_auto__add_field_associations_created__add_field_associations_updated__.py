# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Associations.created'
        db.add_column('ngramengine_associations', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Associations.updated'
        db.add_column('ngramengine_associations', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'WordStems.created'
        db.add_column('ngramengine_wordstems', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'WordStems.updated'
        db.add_column('ngramengine_wordstems', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'NGrams.created'
        db.add_column('ngramengine_ngrams', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'NGrams.updated'
        db.add_column('ngramengine_ngrams', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'PartOfSpeech.created'
        db.add_column('ngramengine_partofspeech', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'PartOfSpeech.updated'
        db.add_column('ngramengine_partofspeech', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Genus.created'
        db.add_column('ngramengine_genus', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Genus.updated'
        db.add_column('ngramengine_genus', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'SubCategory.created'
        db.add_column('ngramengine_subcategory', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'SubCategory.updated'
        db.add_column('ngramengine_subcategory', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Languages.created'
        db.add_column('ngramengine_languages', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Languages.updated'
        db.add_column('ngramengine_languages', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'SuperCategory.created'
        db.add_column('ngramengine_supercategory', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'SuperCategory.updated'
        db.add_column('ngramengine_supercategory', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Antonyms.created'
        db.add_column('ngramengine_antonyms', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Antonyms.updated'
        db.add_column('ngramengine_antonyms', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Numerus.created'
        db.add_column('ngramengine_numerus', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Numerus.updated'
        db.add_column('ngramengine_numerus', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'CoOccurrences.created'
        db.add_column('ngramengine_cooccurrences', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'CoOccurrences.updated'
        db.add_column('ngramengine_cooccurrences', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Synonyms.created'
        db.add_column('ngramengine_synonyms', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Synonyms.updated'
        db.add_column('ngramengine_synonyms', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'InputStack.created'
        db.add_column('ngramengine_inputstack', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'InputStack.updated'
        db.add_column('ngramengine_inputstack', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 7, 13, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Associations.created'
        db.delete_column('ngramengine_associations', 'created')

        # Deleting field 'Associations.updated'
        db.delete_column('ngramengine_associations', 'updated')

        # Deleting field 'WordStems.created'
        db.delete_column('ngramengine_wordstems', 'created')

        # Deleting field 'WordStems.updated'
        db.delete_column('ngramengine_wordstems', 'updated')

        # Deleting field 'NGrams.created'
        db.delete_column('ngramengine_ngrams', 'created')

        # Deleting field 'NGrams.updated'
        db.delete_column('ngramengine_ngrams', 'updated')

        # Deleting field 'PartOfSpeech.created'
        db.delete_column('ngramengine_partofspeech', 'created')

        # Deleting field 'PartOfSpeech.updated'
        db.delete_column('ngramengine_partofspeech', 'updated')

        # Deleting field 'Genus.created'
        db.delete_column('ngramengine_genus', 'created')

        # Deleting field 'Genus.updated'
        db.delete_column('ngramengine_genus', 'updated')

        # Deleting field 'SubCategory.created'
        db.delete_column('ngramengine_subcategory', 'created')

        # Deleting field 'SubCategory.updated'
        db.delete_column('ngramengine_subcategory', 'updated')

        # Deleting field 'Languages.created'
        db.delete_column('ngramengine_languages', 'created')

        # Deleting field 'Languages.updated'
        db.delete_column('ngramengine_languages', 'updated')

        # Deleting field 'SuperCategory.created'
        db.delete_column('ngramengine_supercategory', 'created')

        # Deleting field 'SuperCategory.updated'
        db.delete_column('ngramengine_supercategory', 'updated')

        # Deleting field 'Antonyms.created'
        db.delete_column('ngramengine_antonyms', 'created')

        # Deleting field 'Antonyms.updated'
        db.delete_column('ngramengine_antonyms', 'updated')

        # Deleting field 'Numerus.created'
        db.delete_column('ngramengine_numerus', 'created')

        # Deleting field 'Numerus.updated'
        db.delete_column('ngramengine_numerus', 'updated')

        # Deleting field 'CoOccurrences.created'
        db.delete_column('ngramengine_cooccurrences', 'created')

        # Deleting field 'CoOccurrences.updated'
        db.delete_column('ngramengine_cooccurrences', 'updated')

        # Deleting field 'Synonyms.created'
        db.delete_column('ngramengine_synonyms', 'created')

        # Deleting field 'Synonyms.updated'
        db.delete_column('ngramengine_synonyms', 'updated')

        # Deleting field 'InputStack.created'
        db.delete_column('ngramengine_inputstack', 'created')

        # Deleting field 'InputStack.updated'
        db.delete_column('ngramengine_inputstack', 'updated')


    models = {
        'ngramengine.antonyms': {
            'Meta': {'object_name': 'Antonyms'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'antonym'", 'to': "orm['ngramengine.NGrams']"}),
            't_rated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'antonym_of'", 'to': "orm['ngramengine.NGrams']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'ngramengine.associations': {
            'Meta': {'object_name': 'Associations'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'power': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'association_outbound'", 'to': "orm['ngramengine.NGrams']"}),
            't_associated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'association_inbound'", 'to': "orm['ngramengine.NGrams']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'ngramengine.cooccurrences': {
            'Meta': {'object_name': 'CoOccurrences'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dirty': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mean_position': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'positions': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '10000'}),
            'power': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coocurrence_outbound'", 'to': "orm['ngramengine.NGrams']"}),
            't_cooccured': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coocurrence_inbound'", 'to': "orm['ngramengine.NGrams']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'ngramengine.genus': {
            'Meta': {'ordering': "['type']", 'object_name': 'Genus'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'ngramengine.inputstack': {
            'Meta': {'object_name': 'InputStack'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'ngramengine.languages': {
            'Meta': {'ordering': "['language']", 'object_name': 'Languages'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'ngram_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'ngrams': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'language'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['ngramengine.NGrams']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'ngramengine.ngrams': {
            'Meta': {'ordering': "['token']", 'object_name': 'NGrams'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dirty': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'genus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ngramengine.Genus']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numerus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ngramengine.Numerus']", 'null': 'True', 'blank': 'True'}),
            'qualified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'semantic_meaningless': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            't_occurred': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            't_rated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'wordstem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ngramengine.WordStems']", 'null': 'True', 'blank': 'True'})
        },
        'ngramengine.numerus': {
            'Meta': {'ordering': "['type']", 'object_name': 'Numerus'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'ngramengine.partofspeech': {
            'Meta': {'ordering': "['type']", 'object_name': 'PartOfSpeech'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ngram_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'ngrams': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'partofspeech'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['ngramengine.NGrams']"}),
            'semantic_meaningless': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'ngramengine.subcategory': {
            'Meta': {'object_name': 'SubCategory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subcategory'", 'to': "orm['ngramengine.NGrams']"}),
            't_rated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subcategory_of'", 'to': "orm['ngramengine.NGrams']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'ngramengine.supercategory': {
            'Meta': {'object_name': 'SuperCategory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercategory'", 'to': "orm['ngramengine.NGrams']"}),
            't_rated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercategory_of'", 'to': "orm['ngramengine.NGrams']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'ngramengine.synonyms': {
            'Meta': {'object_name': 'Synonyms'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'synonyms'", 'to': "orm['ngramengine.NGrams']"}),
            't_rated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'synonym_of'", 'to': "orm['ngramengine.NGrams']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'ngramengine.wordstems': {
            'Meta': {'ordering': "['stem']", 'object_name': 'WordStems'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stem': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ngramengine']