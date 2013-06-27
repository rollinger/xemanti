# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WordStems'
        db.create_table('ngramengine_wordstems', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stem', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('ngramengine', ['WordStems'])

        # Adding model 'PartOfSpeech'
        db.create_table('ngramengine_partofspeech', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('indicates_semantic_meaninglessness', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ngramengine', ['PartOfSpeech'])

        # Adding M2M table for field ngrams on 'PartOfSpeech'
        db.create_table('ngramengine_partofspeech_ngrams', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partofspeech', models.ForeignKey(orm['ngramengine.partofspeech'], null=False)),
            ('ngrams', models.ForeignKey(orm['ngramengine.ngrams'], null=False))
        ))
        db.create_unique('ngramengine_partofspeech_ngrams', ['partofspeech_id', 'ngrams_id'])

        # Adding model 'Languages'
        db.create_table('ngramengine_languages', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('ngramengine', ['Languages'])

        # Adding M2M table for field ngrams on 'Languages'
        db.create_table('ngramengine_languages_ngrams', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('languages', models.ForeignKey(orm['ngramengine.languages'], null=False)),
            ('ngrams', models.ForeignKey(orm['ngramengine.ngrams'], null=False))
        ))
        db.create_unique('ngramengine_languages_ngrams', ['languages_id', 'ngrams_id'])

        # Adding model 'Synonyms'
        db.create_table('ngramengine_synonyms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='synonyms', to=orm['ngramengine.NGrams'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='synonym_of', to=orm['ngramengine.NGrams'])),
        ))
        db.send_create_signal('ngramengine', ['Synonyms'])

        # Adding model 'Antonyms'
        db.create_table('ngramengine_antonyms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='antonym', to=orm['ngramengine.NGrams'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='antonym_of', to=orm['ngramengine.NGrams'])),
        ))
        db.send_create_signal('ngramengine', ['Antonyms'])

        # Adding model 'SuperCategory'
        db.create_table('ngramengine_supercategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='supercategory', to=orm['ngramengine.NGrams'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='supercategory_of', to=orm['ngramengine.NGrams'])),
        ))
        db.send_create_signal('ngramengine', ['SuperCategory'])

        # Adding model 'SubCategory'
        db.create_table('ngramengine_subcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subcategory', to=orm['ngramengine.NGrams'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subcategory_of', to=orm['ngramengine.NGrams'])),
        ))
        db.send_create_signal('ngramengine', ['SubCategory'])

        # Adding model 'NGrams'
        db.create_table('ngramengine_ngrams', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('t_occurred', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('wordstem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ngramengine.WordStems'], null=True, blank=True)),
            ('dirty', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('ngramengine', ['NGrams'])

        # Adding model 'CoOccurrences'
        db.create_table('ngramengine_cooccurrences', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='coocurrence_outbound', to=orm['ngramengine.NGrams'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='coocurrence_inbound', to=orm['ngramengine.NGrams'])),
            ('t_cooccured', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('positions', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=10000)),
            ('mean_position', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('power', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('dirty', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('ngramengine', ['CoOccurrences'])

        # Adding model 'Associations'
        db.create_table('ngramengine_associations', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='association_outbound', to=orm['ngramengine.NGrams'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='association_inbound', to=orm['ngramengine.NGrams'])),
            ('t_associated', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('power', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('ngramengine', ['Associations'])

        # Adding model 'InputStack'
        db.create_table('ngramengine_inputstack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=2000)),
        ))
        db.send_create_signal('ngramengine', ['InputStack'])


    def backwards(self, orm):
        # Deleting model 'WordStems'
        db.delete_table('ngramengine_wordstems')

        # Deleting model 'PartOfSpeech'
        db.delete_table('ngramengine_partofspeech')

        # Removing M2M table for field ngrams on 'PartOfSpeech'
        db.delete_table('ngramengine_partofspeech_ngrams')

        # Deleting model 'Languages'
        db.delete_table('ngramengine_languages')

        # Removing M2M table for field ngrams on 'Languages'
        db.delete_table('ngramengine_languages_ngrams')

        # Deleting model 'Synonyms'
        db.delete_table('ngramengine_synonyms')

        # Deleting model 'Antonyms'
        db.delete_table('ngramengine_antonyms')

        # Deleting model 'SuperCategory'
        db.delete_table('ngramengine_supercategory')

        # Deleting model 'SubCategory'
        db.delete_table('ngramengine_subcategory')

        # Deleting model 'NGrams'
        db.delete_table('ngramengine_ngrams')

        # Deleting model 'CoOccurrences'
        db.delete_table('ngramengine_cooccurrences')

        # Deleting model 'Associations'
        db.delete_table('ngramengine_associations')

        # Deleting model 'InputStack'
        db.delete_table('ngramengine_inputstack')


    models = {
        'ngramengine.antonyms': {
            'Meta': {'object_name': 'Antonyms'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'antonym'", 'to': "orm['ngramengine.NGrams']"}),
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
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subcategory_of'", 'to': "orm['ngramengine.NGrams']"})
        },
        'ngramengine.supercategory': {
            'Meta': {'object_name': 'SuperCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercategory'", 'to': "orm['ngramengine.NGrams']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supercategory_of'", 'to': "orm['ngramengine.NGrams']"})
        },
        'ngramengine.synonyms': {
            'Meta': {'object_name': 'Synonyms'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'synonyms'", 'to': "orm['ngramengine.NGrams']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'synonym_of'", 'to': "orm['ngramengine.NGrams']"})
        },
        'ngramengine.wordstems': {
            'Meta': {'ordering': "['stem']", 'object_name': 'WordStems'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stem': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['ngramengine']