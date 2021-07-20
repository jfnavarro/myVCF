from __future__ import unicode_literals
from django.db import models
import datetime
from django.utils import timezone


class Gene75(models.Model):
    ensgene = models.TextField(db_column='Ensgene_ID', blank=False, null=False)
    genename = models.TextField(db_column='Gene_name', blank=True)
    description = models.TextField(db_column='Description', blank=True)

    def __unicode__(self):
        return self.ensgene


class Gene84(models.Model):
    ensgene = models.TextField(db_column='Ensgene_ID', blank=False, null=False)
    genename = models.TextField(db_column='Gene_name', blank=True)
    description = models.TextField(db_column='Description', blank=True)

    def __unicode__(self):
        return self.ensgene


class Log(models.Model):
    log_text = models.TextField()
    log_date = models.DateTimeField('log modified')

    def __unicode__(self):
        return self.log_text

    def was_modified_recently(self):
        return self.log_date >= timezone.now() - datetime.timedelta(days=3)

    def log_date_human(self):
        return self.log_date.strftime('%d %B %Y')

    def is_recent(self):
        is_recent_var = self.log_date >= timezone.now() - datetime.timedelta(days=3)
        return is_recent_var

    was_modified_recently.admin_order_field = 'log_date'
    was_modified_recently.boolean = True
    was_modified_recently.short_description = 'Modified recently?'


class DbInfo(models.Model):
    project_name = models.TextField()
    sw_annotation = models.TextField()
    gene_annotation = models.TextField()
    assembly_version = models.TextField()
    samples = models.TextField()
    samples_len = models.IntegerField()
    default_col = models.TextField()
    mutation_col = models.TextField()

    def __unicode__(self):
        return self.project_name

    def annotation_type(self):
        return self.gene_annotation

    def annotation_sw(self):
        return self.sw_annotation

    def get_samples(self):
        return self.samples

    def n_samples(self):
        return self.samples_len

    def default_col_list(self):
        return self.default_col

    def get_mutation_col(self):
        return self.mutation_col


class Groups(models.Model):
    p_id = models.IntegerField(db_column='p_id', blank=False, null=False)
    project_name = models.TextField()
    group_name = models.TextField()
    samples = models.TextField()

    def __unicode__(self):
        return self.group_name

    def n_samples(self):
        return len(self.samples)

    def get_samples(self):
        return self.samples