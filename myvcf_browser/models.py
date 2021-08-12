# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Mark(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    chrom = models.TextField(db_column='CHROM')  # Field name made lowercase.
    pos = models.IntegerField(db_column='POS')  # Field name made lowercase.
    rs_id = models.TextField(db_column='RS_ID', blank=True, null=True)  # Field name made lowercase.
    ref = models.TextField(db_column='REF')  # Field name made lowercase.
    alt = models.TextField(db_column='ALT', blank=True, null=True)  # Field name made lowercase.
    qual = models.FloatField(db_column='QUAL', blank=True, null=True)  # Field name made lowercase.
    filter = models.TextField(db_column='FILTER', blank=True, null=True)  # Field name made lowercase.
    end = models.IntegerField(db_column='END', blank=True, null=True)  # Field name made lowercase.
    allele = models.TextField(db_column='Allele', blank=True, null=True)  # Field name made lowercase.
    annotation = models.TextField(db_column='Annotation', blank=True, null=True)  # Field name made lowercase.
    annotation_impact = models.TextField(db_column='Annotation_Impact', blank=True, null=True)  # Field name made lowercase.
    gene_name = models.TextField(db_column='Gene_Name', blank=True, null=True)  # Field name made lowercase.
    gene_id = models.TextField(db_column='Gene_ID', blank=True, null=True)  # Field name made lowercase.
    feature_type = models.TextField(db_column='Feature_Type', blank=True, null=True)  # Field name made lowercase.
    feature_id = models.TextField(db_column='Feature_ID', blank=True, null=True)  # Field name made lowercase.
    transcript_biotype = models.TextField(db_column='Transcript_BioType', blank=True, null=True)  # Field name made lowercase.
    rank = models.TextField(db_column='Rank', blank=True, null=True)  # Field name made lowercase.
    hgvs_c = models.TextField(db_column='HGVS.c', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hgvs_p = models.TextField(db_column='HGVS.p', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cdna_pos_cdna_length = models.TextField(db_column='cDNA.pos / cDNA.length', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cds_pos_cds_length = models.TextField(db_column='CDS.pos / CDS.length', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    aa_pos_aa_length = models.TextField(db_column='AA.pos / AA.length', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    distance = models.TextField(db_column='Distance', blank=True, null=True)  # Field name made lowercase.
    lof = models.TextField(db_column='LOF', blank=True, null=True)  # Field name made lowercase.
    nmd = models.TextField(db_column='NMD', blank=True, null=True)  # Field name made lowercase.
    dbsnpbuildid = models.IntegerField(db_column='dbSNPBuildID', blank=True, null=True)  # Field name made lowercase.
    nsf = models.IntegerField(db_column='NSF', blank=True, null=True)  # Field name made lowercase.
    r3 = models.IntegerField(db_column='R3', blank=True, null=True)  # Field name made lowercase.
    r5 = models.IntegerField(db_column='R5', blank=True, null=True)  # Field name made lowercase.
    clnsig = models.TextField(db_column='CLNSIG', blank=True, null=True)  # Field name made lowercase.
    nsn = models.IntegerField(db_column='NSN', blank=True, null=True)  # Field name made lowercase.
    nsm = models.IntegerField(db_column='NSM', blank=True, null=True)  # Field name made lowercase.
    clnorigin = models.TextField(db_column='CLNORIGIN', blank=True, null=True)  # Field name made lowercase.
    clnrevstat = models.TextField(db_column='CLNREVSTAT', blank=True, null=True)  # Field name made lowercase.
    common = models.IntegerField(db_column='COMMON', blank=True, null=True)  # Field name made lowercase.
    rs = models.IntegerField(db_column='RS', blank=True, null=True)  # Field name made lowercase.
    gno = models.IntegerField(db_column='GNO', blank=True, null=True)  # Field name made lowercase.
    freq = models.TextField(db_column='FREQ', blank=True, null=True)  # Field name made lowercase.
    ass = models.IntegerField(db_column='ASS', blank=True, null=True)  # Field name made lowercase.
    u3 = models.IntegerField(db_column='U3', blank=True, null=True)  # Field name made lowercase.
    u5 = models.IntegerField(db_column='U5', blank=True, null=True)  # Field name made lowercase.
    clnacc = models.TextField(db_column='CLNACC', blank=True, null=True)  # Field name made lowercase.
    clndn = models.TextField(db_column='CLNDN', blank=True, null=True)  # Field name made lowercase.
    dss = models.IntegerField(db_column='DSS', blank=True, null=True)  # Field name made lowercase.
    syn = models.IntegerField(db_column='SYN', blank=True, null=True)  # Field name made lowercase.
    clnvi = models.TextField(db_column='CLNVI', blank=True, null=True)  # Field name made lowercase.
    vc = models.TextField(db_column='VC', blank=True, null=True)  # Field name made lowercase.
    sao = models.IntegerField(db_column='SAO', blank=True, null=True)  # Field name made lowercase.
    pseudogeneinfo = models.TextField(db_column='PSEUDOGENEINFO', blank=True, null=True)  # Field name made lowercase.
    clndisdb = models.TextField(db_column='CLNDISDB', blank=True, null=True)  # Field name made lowercase.
    geneinfo = models.TextField(db_column='GENEINFO', blank=True, null=True)  # Field name made lowercase.
    int = models.IntegerField(db_column='INT', blank=True, null=True)  # Field name made lowercase.
    pub = models.IntegerField(db_column='PUB', blank=True, null=True)  # Field name made lowercase.
    clnhgvs = models.TextField(db_column='CLNHGVS', blank=True, null=True)  # Field name made lowercase.
    ssr = models.IntegerField(db_column='SSR', blank=True, null=True)  # Field name made lowercase.
    pm = models.IntegerField(db_column='PM', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_clinvar_var_source = models.TextField(db_column='dbNSFP_clinvar_var_source', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_hg19_pos_1_based_field = models.IntegerField(db_column='dbNSFP_hg19_pos_1_based_', blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    dbnsfp_clinvar_review = models.TextField(db_column='dbNSFP_clinvar_review', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_polyphen2_hvar_score = models.FloatField(db_column='dbNSFP_Polyphen2_HVAR_score', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_clinvar_medgen_id = models.TextField(db_column='dbNSFP_clinvar_MedGen_id', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_gnomad_genomes_ac = models.IntegerField(db_column='dbNSFP_gnomAD_genomes_AC', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_clinvar_omim_id = models.TextField(db_column='dbNSFP_clinvar_OMIM_id', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_gnomad_genomes_af = models.FloatField(db_column='dbNSFP_gnomAD_genomes_AF', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_clinvar_hgvs = models.TextField(db_column='dbNSFP_clinvar_hgvs', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_sift4g_converted_rankscore = models.FloatField(db_column='dbNSFP_SIFT4G_converted_rankscore', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_sift_converted_rankscore = models.FloatField(db_column='dbNSFP_SIFT_converted_rankscore', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_sift4g_score = models.FloatField(db_column='dbNSFP_SIFT4G_score', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_hg19_chr = models.IntegerField(db_column='dbNSFP_hg19_chr', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_sift4g_pred = models.TextField(db_column='dbNSFP_SIFT4G_pred', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_gnomad_exomes_af = models.FloatField(db_column='dbNSFP_gnomAD_exomes_AF', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_polyphen2_hdiv_rankscore = models.FloatField(db_column='dbNSFP_Polyphen2_HDIV_rankscore', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_polyphen2_hvar_rankscore = models.FloatField(db_column='dbNSFP_Polyphen2_HVAR_rankscore', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_gnomad_exomes_ac = models.IntegerField(db_column='dbNSFP_gnomAD_exomes_AC', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_sift_score = models.FloatField(db_column='dbNSFP_SIFT_score', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_polyphen2_hdiv_score = models.FloatField(db_column='dbNSFP_Polyphen2_HDIV_score', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_polyphen2_hdiv_pred = models.TextField(db_column='dbNSFP_Polyphen2_HDIV_pred', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_clinvar_clnsig = models.TextField(db_column='dbNSFP_clinvar_clnsig', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_gnomad_genomes_an = models.IntegerField(db_column='dbNSFP_gnomAD_genomes_AN', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_clinvar_id = models.TextField(db_column='dbNSFP_clinvar_id', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_clinvar_trait = models.TextField(db_column='dbNSFP_clinvar_trait', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_polyphen2_hvar_pred = models.TextField(db_column='dbNSFP_Polyphen2_HVAR_pred', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_gnomad_exomes_an = models.IntegerField(db_column='dbNSFP_gnomAD_exomes_AN', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_sift_pred = models.TextField(db_column='dbNSFP_SIFT_pred', blank=True, null=True)  # Field name made lowercase.
    dbnsfp_clinvar_orphanet_id = models.TextField(db_column='dbNSFP_clinvar_Orphanet_id', blank=True, null=True)  # Field name made lowercase.
    mark = models.TextField(db_column='Mark', blank=True, null=True)  # Field name made lowercase.

    class Meta:
                db_table = 'Mark'
