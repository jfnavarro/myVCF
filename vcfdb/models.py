# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Test(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    chrom = models.TextField(db_column='CHROM')  # Field name made lowercase.
    pos = models.IntegerField(db_column='POS')  # Field name made lowercase.
    rs_id = models.TextField(db_column='RS_ID', blank=True, null=True)  # Field name made lowercase.
    ref = models.TextField(db_column='REF')  # Field name made lowercase.
    alt = models.TextField(db_column='ALT', blank=True, null=True)  # Field name made lowercase.
    qual = models.FloatField(db_column='QUAL', blank=True, null=True)  # Field name made lowercase.
    filter = models.TextField(db_column='FILTER', blank=True, null=True)  # Field name made lowercase.
    ac = models.IntegerField(db_column='AC', blank=True, null=True)  # Field name made lowercase.
    af = models.FloatField(db_column='AF', blank=True, null=True)  # Field name made lowercase.
    an = models.IntegerField(db_column='AN', blank=True, null=True)  # Field name made lowercase.
    baseqranksum = models.FloatField(db_column='BaseQRankSum', blank=True, null=True)  # Field name made lowercase.
    ccc = models.IntegerField(db_column='CCC', blank=True, null=True)  # Field name made lowercase.
    clippingranksum = models.FloatField(db_column='ClippingRankSum', blank=True, null=True)  # Field name made lowercase.
    db = models.IntegerField(db_column='DB', blank=True, null=True)  # Field name made lowercase.
    dp = models.IntegerField(db_column='DP', blank=True, null=True)  # Field name made lowercase.
    ds = models.IntegerField(db_column='DS', blank=True, null=True)  # Field name made lowercase.
    end = models.IntegerField(db_column='END', blank=True, null=True)  # Field name made lowercase.
    fs = models.FloatField(db_column='FS', blank=True, null=True)  # Field name made lowercase.
    gq_mean = models.FloatField(db_column='GQ_MEAN', blank=True, null=True)  # Field name made lowercase.
    gq_stddev = models.FloatField(db_column='GQ_STDDEV', blank=True, null=True)  # Field name made lowercase.
    hwp = models.FloatField(db_column='HWP', blank=True, null=True)  # Field name made lowercase.
    haplotypescore = models.FloatField(db_column='HaplotypeScore', blank=True, null=True)  # Field name made lowercase.
    inbreedingcoeff = models.FloatField(db_column='InbreedingCoeff', blank=True, null=True)  # Field name made lowercase.
    mleac = models.IntegerField(db_column='MLEAC', blank=True, null=True)  # Field name made lowercase.
    mleaf = models.FloatField(db_column='MLEAF', blank=True, null=True)  # Field name made lowercase.
    mq = models.FloatField(db_column='MQ', blank=True, null=True)  # Field name made lowercase.
    mq0 = models.IntegerField(db_column='MQ0', blank=True, null=True)  # Field name made lowercase.
    mqranksum = models.FloatField(db_column='MQRankSum', blank=True, null=True)  # Field name made lowercase.
    ncc = models.IntegerField(db_column='NCC', blank=True, null=True)  # Field name made lowercase.
    negative_train_site = models.IntegerField(db_column='NEGATIVE_TRAIN_SITE', blank=True, null=True)  # Field name made lowercase.
    positive_train_site = models.IntegerField(db_column='POSITIVE_TRAIN_SITE', blank=True, null=True)  # Field name made lowercase.
    qd = models.FloatField(db_column='QD', blank=True, null=True)  # Field name made lowercase.
    readposranksum = models.FloatField(db_column='ReadPosRankSum', blank=True, null=True)  # Field name made lowercase.
    sor = models.FloatField(db_column='SOR', blank=True, null=True)  # Field name made lowercase.
    vqslod = models.FloatField(db_column='VQSLOD', blank=True, null=True)  # Field name made lowercase.
    culprit = models.TextField(blank=True, null=True)
    allele = models.TextField(db_column='Allele', blank=True, null=True)  # Field name made lowercase.
    consequence = models.TextField(db_column='Consequence', blank=True, null=True)  # Field name made lowercase.
    impact = models.TextField(db_column='IMPACT', blank=True, null=True)  # Field name made lowercase.
    symbol = models.TextField(db_column='SYMBOL', blank=True, null=True)  # Field name made lowercase.
    gene = models.TextField(db_column='Gene', blank=True, null=True)  # Field name made lowercase.
    feature_type = models.TextField(db_column='Feature_type', blank=True, null=True)  # Field name made lowercase.
    feature = models.TextField(db_column='Feature', blank=True, null=True)  # Field name made lowercase.
    biotype = models.TextField(db_column='BIOTYPE', blank=True, null=True)  # Field name made lowercase.
    exon = models.TextField(db_column='EXON', blank=True, null=True)  # Field name made lowercase.
    intron = models.TextField(db_column='INTRON', blank=True, null=True)  # Field name made lowercase.
    hgvsc = models.TextField(db_column='HGVSc', blank=True, null=True)  # Field name made lowercase.
    hgvsp = models.TextField(db_column='HGVSp', blank=True, null=True)  # Field name made lowercase.
    cdna_position = models.TextField(db_column='cDNA_position', blank=True, null=True)  # Field name made lowercase.
    cds_position = models.TextField(db_column='CDS_position', blank=True, null=True)  # Field name made lowercase.
    protein_position = models.TextField(db_column='Protein_position', blank=True, null=True)  # Field name made lowercase.
    amino_acids = models.TextField(db_column='Amino_acids', blank=True, null=True)  # Field name made lowercase.
    codons = models.TextField(db_column='Codons', blank=True, null=True)  # Field name made lowercase.
    existing_variation = models.TextField(db_column='Existing_variation', blank=True, null=True)  # Field name made lowercase.
    distance = models.TextField(db_column='DISTANCE', blank=True, null=True)  # Field name made lowercase.
    strand = models.TextField(db_column='STRAND', blank=True, null=True)  # Field name made lowercase.
    variant_class = models.TextField(db_column='VARIANT_CLASS', blank=True, null=True)  # Field name made lowercase.
    symbol_source = models.TextField(db_column='SYMBOL_SOURCE', blank=True, null=True)  # Field name made lowercase.
    hgnc_id = models.TextField(db_column='HGNC_ID', blank=True, null=True)  # Field name made lowercase.
    canonical = models.TextField(db_column='CANONICAL', blank=True, null=True)  # Field name made lowercase.
    tsl = models.TextField(db_column='TSL', blank=True, null=True)  # Field name made lowercase.
    appris = models.TextField(db_column='APPRIS', blank=True, null=True)  # Field name made lowercase.
    ccds = models.TextField(db_column='CCDS', blank=True, null=True)  # Field name made lowercase.
    ensp = models.TextField(db_column='ENSP', blank=True, null=True)  # Field name made lowercase.
    swissprot = models.TextField(db_column='SWISSPROT', blank=True, null=True)  # Field name made lowercase.
    trembl = models.TextField(db_column='TREMBL', blank=True, null=True)  # Field name made lowercase.
    uniparc = models.TextField(db_column='UNIPARC', blank=True, null=True)  # Field name made lowercase.
    gene_pheno = models.TextField(db_column='GENE_PHENO', blank=True, null=True)  # Field name made lowercase.
    sift = models.TextField(db_column='SIFT', blank=True, null=True)  # Field name made lowercase.
    polyphen = models.TextField(db_column='PolyPhen', blank=True, null=True)  # Field name made lowercase.
    domains = models.TextField(db_column='DOMAINS', blank=True, null=True)  # Field name made lowercase.
    hgvs_offset = models.TextField(db_column='HGVS_OFFSET', blank=True, null=True)  # Field name made lowercase.
    gmaf = models.TextField(db_column='GMAF', blank=True, null=True)  # Field name made lowercase.
    afr_maf = models.TextField(db_column='AFR_MAF', blank=True, null=True)  # Field name made lowercase.
    amr_maf = models.TextField(db_column='AMR_MAF', blank=True, null=True)  # Field name made lowercase.
    eas_maf = models.TextField(db_column='EAS_MAF', blank=True, null=True)  # Field name made lowercase.
    eur_maf = models.TextField(db_column='EUR_MAF', blank=True, null=True)  # Field name made lowercase.
    sas_maf = models.TextField(db_column='SAS_MAF', blank=True, null=True)  # Field name made lowercase.
    aa_maf = models.TextField(db_column='AA_MAF', blank=True, null=True)  # Field name made lowercase.
    ea_maf = models.TextField(db_column='EA_MAF', blank=True, null=True)  # Field name made lowercase.
    exac_maf = models.TextField(db_column='ExAC_MAF', blank=True, null=True)  # Field name made lowercase.
    exac_adj_maf = models.TextField(db_column='ExAC_Adj_MAF', blank=True, null=True)  # Field name made lowercase.
    exac_afr_maf = models.TextField(db_column='ExAC_AFR_MAF', blank=True, null=True)  # Field name made lowercase.
    exac_amr_maf = models.TextField(db_column='ExAC_AMR_MAF', blank=True, null=True)  # Field name made lowercase.
    exac_eas_maf = models.TextField(db_column='ExAC_EAS_MAF', blank=True, null=True)  # Field name made lowercase.
    exac_fin_maf = models.TextField(db_column='ExAC_FIN_MAF', blank=True, null=True)  # Field name made lowercase.
    exac_nfe_maf = models.TextField(db_column='ExAC_NFE_MAF', blank=True, null=True)  # Field name made lowercase.
    exac_oth_maf = models.TextField(db_column='ExAC_OTH_MAF', blank=True, null=True)  # Field name made lowercase.
    exac_sas_maf = models.TextField(db_column='ExAC_SAS_MAF', blank=True, null=True)  # Field name made lowercase.
    clin_sig = models.TextField(db_column='CLIN_SIG', blank=True, null=True)  # Field name made lowercase.
    somatic = models.TextField(db_column='SOMATIC', blank=True, null=True)  # Field name made lowercase.
    pheno = models.TextField(db_column='PHENO', blank=True, null=True)  # Field name made lowercase.
    pubmed = models.TextField(db_column='PUBMED', blank=True, null=True)  # Field name made lowercase.
    motif_name = models.TextField(db_column='MOTIF_NAME', blank=True, null=True)  # Field name made lowercase.
    motif_pos = models.TextField(db_column='MOTIF_POS', blank=True, null=True)  # Field name made lowercase.
    high_inf_pos = models.TextField(db_column='HIGH_INF_POS', blank=True, null=True)  # Field name made lowercase.
    motif_score_change = models.TextField(db_column='MOTIF_SCORE_CHANGE', blank=True, null=True)  # Field name made lowercase.
    c1 = models.TextField(db_column='C1', blank=True, null=True)  # Field name made lowercase.
    c10 = models.TextField(db_column='C10', blank=True, null=True)  # Field name made lowercase.
    c11 = models.TextField(db_column='C11', blank=True, null=True)  # Field name made lowercase.
    c12 = models.TextField(db_column='C12', blank=True, null=True)  # Field name made lowercase.
    c13 = models.TextField(db_column='C13', blank=True, null=True)  # Field name made lowercase.
    c14 = models.TextField(db_column='C14', blank=True, null=True)  # Field name made lowercase.
    c15 = models.TextField(db_column='C15', blank=True, null=True)  # Field name made lowercase.
    c16 = models.TextField(db_column='C16', blank=True, null=True)  # Field name made lowercase.
    c17 = models.TextField(db_column='C17', blank=True, null=True)  # Field name made lowercase.
    c2 = models.TextField(db_column='C2', blank=True, null=True)  # Field name made lowercase.
    c3 = models.TextField(db_column='C3', blank=True, null=True)  # Field name made lowercase.
    c4 = models.TextField(db_column='C4', blank=True, null=True)  # Field name made lowercase.
    c5 = models.TextField(db_column='C5', blank=True, null=True)  # Field name made lowercase.
    c6 = models.TextField(db_column='C6', blank=True, null=True)  # Field name made lowercase.
    c7 = models.TextField(db_column='C7', blank=True, null=True)  # Field name made lowercase.
    c8 = models.TextField(db_column='C8', blank=True, null=True)  # Field name made lowercase.
    c9 = models.TextField(db_column='C9', blank=True, null=True)  # Field name made lowercase.
    d1 = models.TextField(db_column='D1', blank=True, null=True)  # Field name made lowercase.
    d10 = models.TextField(db_column='D10', blank=True, null=True)  # Field name made lowercase.
    d11 = models.TextField(db_column='D11', blank=True, null=True)  # Field name made lowercase.
    d12 = models.TextField(db_column='D12', blank=True, null=True)  # Field name made lowercase.
    d13 = models.TextField(db_column='D13', blank=True, null=True)  # Field name made lowercase.
    d14 = models.TextField(db_column='D14', blank=True, null=True)  # Field name made lowercase.
    d15 = models.TextField(db_column='D15', blank=True, null=True)  # Field name made lowercase.
    d16 = models.TextField(db_column='D16', blank=True, null=True)  # Field name made lowercase.
    d17 = models.TextField(db_column='D17', blank=True, null=True)  # Field name made lowercase.
    d18 = models.TextField(db_column='D18', blank=True, null=True)  # Field name made lowercase.
    d19 = models.TextField(db_column='D19', blank=True, null=True)  # Field name made lowercase.
    d2 = models.TextField(db_column='D2', blank=True, null=True)  # Field name made lowercase.
    d20 = models.TextField(db_column='D20', blank=True, null=True)  # Field name made lowercase.
    d21 = models.TextField(db_column='D21', blank=True, null=True)  # Field name made lowercase.
    d22 = models.TextField(db_column='D22', blank=True, null=True)  # Field name made lowercase.
    d23 = models.TextField(db_column='D23', blank=True, null=True)  # Field name made lowercase.
    d24 = models.TextField(db_column='D24', blank=True, null=True)  # Field name made lowercase.
    d25 = models.TextField(db_column='D25', blank=True, null=True)  # Field name made lowercase.
    d26 = models.TextField(db_column='D26', blank=True, null=True)  # Field name made lowercase.
    d27 = models.TextField(db_column='D27', blank=True, null=True)  # Field name made lowercase.
    d28 = models.TextField(db_column='D28', blank=True, null=True)  # Field name made lowercase.
    d29 = models.TextField(db_column='D29', blank=True, null=True)  # Field name made lowercase.
    d3 = models.TextField(db_column='D3', blank=True, null=True)  # Field name made lowercase.
    d30 = models.TextField(db_column='D30', blank=True, null=True)  # Field name made lowercase.
    d31 = models.TextField(db_column='D31', blank=True, null=True)  # Field name made lowercase.
    d4 = models.TextField(db_column='D4', blank=True, null=True)  # Field name made lowercase.
    d5 = models.TextField(db_column='D5', blank=True, null=True)  # Field name made lowercase.
    d6 = models.TextField(db_column='D6', blank=True, null=True)  # Field name made lowercase.
    d7 = models.TextField(db_column='D7', blank=True, null=True)  # Field name made lowercase.
    d8 = models.TextField(db_column='D8', blank=True, null=True)  # Field name made lowercase.
    d9 = models.TextField(db_column='D9', blank=True, null=True)  # Field name made lowercase.
    h1 = models.TextField(db_column='H1', blank=True, null=True)  # Field name made lowercase.
    h10 = models.TextField(db_column='H10', blank=True, null=True)  # Field name made lowercase.
    h11 = models.TextField(db_column='H11', blank=True, null=True)  # Field name made lowercase.
    h12 = models.TextField(db_column='H12', blank=True, null=True)  # Field name made lowercase.
    h13 = models.TextField(db_column='H13', blank=True, null=True)  # Field name made lowercase.
    h14 = models.TextField(db_column='H14', blank=True, null=True)  # Field name made lowercase.
    h15 = models.TextField(db_column='H15', blank=True, null=True)  # Field name made lowercase.
    h16 = models.TextField(db_column='H16', blank=True, null=True)  # Field name made lowercase.
    h17 = models.TextField(db_column='H17', blank=True, null=True)  # Field name made lowercase.
    h18 = models.TextField(db_column='H18', blank=True, null=True)  # Field name made lowercase.
    h19 = models.TextField(db_column='H19', blank=True, null=True)  # Field name made lowercase.
    h2 = models.TextField(db_column='H2', blank=True, null=True)  # Field name made lowercase.
    h20 = models.TextField(db_column='H20', blank=True, null=True)  # Field name made lowercase.
    h21 = models.TextField(db_column='H21', blank=True, null=True)  # Field name made lowercase.
    h22 = models.TextField(db_column='H22', blank=True, null=True)  # Field name made lowercase.
    h23 = models.TextField(db_column='H23', blank=True, null=True)  # Field name made lowercase.
    h24 = models.TextField(db_column='H24', blank=True, null=True)  # Field name made lowercase.
    h25 = models.TextField(db_column='H25', blank=True, null=True)  # Field name made lowercase.
    h26 = models.TextField(db_column='H26', blank=True, null=True)  # Field name made lowercase.
    h27 = models.TextField(db_column='H27', blank=True, null=True)  # Field name made lowercase.
    h28 = models.TextField(db_column='H28', blank=True, null=True)  # Field name made lowercase.
    h29 = models.TextField(db_column='H29', blank=True, null=True)  # Field name made lowercase.
    h3 = models.TextField(db_column='H3', blank=True, null=True)  # Field name made lowercase.
    h30 = models.TextField(db_column='H30', blank=True, null=True)  # Field name made lowercase.
    h31 = models.TextField(db_column='H31', blank=True, null=True)  # Field name made lowercase.
    h32 = models.TextField(db_column='H32', blank=True, null=True)  # Field name made lowercase.
    h4 = models.TextField(db_column='H4', blank=True, null=True)  # Field name made lowercase.
    h5 = models.TextField(db_column='H5', blank=True, null=True)  # Field name made lowercase.
    h6 = models.TextField(db_column='H6', blank=True, null=True)  # Field name made lowercase.
    h7 = models.TextField(db_column='H7', blank=True, null=True)  # Field name made lowercase.
    h8 = models.TextField(db_column='H8', blank=True, null=True)  # Field name made lowercase.
    h9 = models.TextField(db_column='H9', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'test'


class Test2(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    chrom = models.TextField(db_column='CHROM')  # Field name made lowercase.
    pos = models.IntegerField(db_column='POS')  # Field name made lowercase.
    rs_id = models.TextField(db_column='RS_ID', blank=True, null=True)  # Field name made lowercase.
    ref = models.TextField(db_column='REF')  # Field name made lowercase.
    alt = models.TextField(db_column='ALT', blank=True, null=True)  # Field name made lowercase.
    qual = models.FloatField(db_column='QUAL', blank=True, null=True)  # Field name made lowercase.
    filter = models.TextField(db_column='FILTER', blank=True, null=True)  # Field name made lowercase.
    ac = models.IntegerField(db_column='AC', blank=True, null=True)  # Field name made lowercase.
    af = models.FloatField(db_column='AF', blank=True, null=True)  # Field name made lowercase.
    an = models.IntegerField(db_column='AN', blank=True, null=True)  # Field name made lowercase.
    baseqranksum = models.FloatField(db_column='BaseQRankSum', blank=True, null=True)  # Field name made lowercase.
    ccc = models.IntegerField(db_column='CCC', blank=True, null=True)  # Field name made lowercase.
    clippingranksum = models.FloatField(db_column='ClippingRankSum', blank=True, null=True)  # Field name made lowercase.
    db = models.IntegerField(db_column='DB', blank=True, null=True)  # Field name made lowercase.
    dp = models.IntegerField(db_column='DP', blank=True, null=True)  # Field name made lowercase.
    ds = models.IntegerField(db_column='DS', blank=True, null=True)  # Field name made lowercase.
    end = models.IntegerField(db_column='END', blank=True, null=True)  # Field name made lowercase.
    fs = models.FloatField(db_column='FS', blank=True, null=True)  # Field name made lowercase.
    gq_mean = models.FloatField(db_column='GQ_MEAN', blank=True, null=True)  # Field name made lowercase.
    gq_stddev = models.FloatField(db_column='GQ_STDDEV', blank=True, null=True)  # Field name made lowercase.
    hwp = models.FloatField(db_column='HWP', blank=True, null=True)  # Field name made lowercase.
    haplotypescore = models.FloatField(db_column='HaplotypeScore', blank=True, null=True)  # Field name made lowercase.
    inbreedingcoeff = models.FloatField(db_column='InbreedingCoeff', blank=True, null=True)  # Field name made lowercase.
    mleac = models.IntegerField(db_column='MLEAC', blank=True, null=True)  # Field name made lowercase.
    mleaf = models.FloatField(db_column='MLEAF', blank=True, null=True)  # Field name made lowercase.
    mq = models.FloatField(db_column='MQ', blank=True, null=True)  # Field name made lowercase.
    mq0 = models.IntegerField(db_column='MQ0', blank=True, null=True)  # Field name made lowercase.
    mqranksum = models.FloatField(db_column='MQRankSum', blank=True, null=True)  # Field name made lowercase.
    ncc = models.IntegerField(db_column='NCC', blank=True, null=True)  # Field name made lowercase.
    negative_train_site = models.IntegerField(db_column='NEGATIVE_TRAIN_SITE', blank=True, null=True)  # Field name made lowercase.
    positive_train_site = models.IntegerField(db_column='POSITIVE_TRAIN_SITE', blank=True, null=True)  # Field name made lowercase.
    qd = models.FloatField(db_column='QD', blank=True, null=True)  # Field name made lowercase.
    readposranksum = models.FloatField(db_column='ReadPosRankSum', blank=True, null=True)  # Field name made lowercase.
    sor = models.FloatField(db_column='SOR', blank=True, null=True)  # Field name made lowercase.
    vqslod = models.FloatField(db_column='VQSLOD', blank=True, null=True)  # Field name made lowercase.
    culprit = models.TextField(blank=True, null=True)
    annovar_date = models.TextField(db_column='ANNOVAR_DATE', blank=True, null=True)  # Field name made lowercase.
    func_refgene = models.TextField(db_column='Func_refGene', blank=True, null=True)  # Field name made lowercase.
    gene_refgene = models.TextField(db_column='Gene_refGene', blank=True, null=True)  # Field name made lowercase.
    genedetail_refgene = models.TextField(db_column='GeneDetail_refGene', blank=True, null=True)  # Field name made lowercase.
    exonicfunc_refgene = models.TextField(db_column='ExonicFunc_refGene', blank=True, null=True)  # Field name made lowercase.
    aachange_refgene = models.TextField(db_column='AAChange_refGene', blank=True, null=True)  # Field name made lowercase.
    func_ensgene = models.TextField(db_column='Func_ensGene', blank=True, null=True)  # Field name made lowercase.
    gene_ensgene = models.TextField(db_column='Gene_ensGene', blank=True, null=True)  # Field name made lowercase.
    genedetail_ensgene = models.TextField(db_column='GeneDetail_ensGene', blank=True, null=True)  # Field name made lowercase.
    exonicfunc_ensgene = models.TextField(db_column='ExonicFunc_ensGene', blank=True, null=True)  # Field name made lowercase.
    aachange_ensgene = models.TextField(db_column='AAChange_ensGene', blank=True, null=True)  # Field name made lowercase.
    avsnp142 = models.TextField(blank=True, null=True)
    popfreqmax = models.TextField(db_column='PopFreqMax', blank=True, null=True)  # Field name made lowercase.
    esp6500siv2_all = models.FloatField(blank=True, null=True)
    esp6500siv2_ea = models.FloatField(blank=True, null=True)
    u1000g2014oct_all = models.FloatField(blank=True, null=True)
    u1000g2014oct_eur = models.FloatField(blank=True, null=True)
    exac_all = models.TextField(db_column='ExAC_ALL', blank=True, null=True)  # Field name made lowercase.
    exac_afr = models.TextField(db_column='ExAC_AFR', blank=True, null=True)  # Field name made lowercase.
    exac_amr = models.TextField(db_column='ExAC_AMR', blank=True, null=True)  # Field name made lowercase.
    exac_eas = models.TextField(db_column='ExAC_EAS', blank=True, null=True)  # Field name made lowercase.
    exac_fin = models.TextField(db_column='ExAC_FIN', blank=True, null=True)  # Field name made lowercase.
    exac_nfe = models.TextField(db_column='ExAC_NFE', blank=True, null=True)  # Field name made lowercase.
    exac_oth = models.TextField(db_column='ExAC_OTH', blank=True, null=True)  # Field name made lowercase.
    exac_sas = models.TextField(db_column='ExAC_SAS', blank=True, null=True)  # Field name made lowercase.
    kaviar_af = models.TextField(db_column='Kaviar_AF', blank=True, null=True)  # Field name made lowercase.
    kaviar_ac = models.TextField(db_column='Kaviar_AC', blank=True, null=True)  # Field name made lowercase.
    kaviar_an = models.TextField(db_column='Kaviar_AN', blank=True, null=True)  # Field name made lowercase.
    dbscsnv_ada_score = models.TextField(db_column='dbscSNV_ADA_SCORE', blank=True, null=True)  # Field name made lowercase.
    dbscsnv_rf_score = models.TextField(db_column='dbscSNV_RF_SCORE', blank=True, null=True)  # Field name made lowercase.
    hrc_af = models.TextField(db_column='HRC_AF', blank=True, null=True)  # Field name made lowercase.
    hrc_ac = models.TextField(db_column='HRC_AC', blank=True, null=True)  # Field name made lowercase.
    hrc_an = models.TextField(db_column='HRC_AN', blank=True, null=True)  # Field name made lowercase.
    hrc_non1000g_af = models.TextField(db_column='HRC_non1000G_AF', blank=True, null=True)  # Field name made lowercase.
    hrc_non1000g_ac = models.TextField(db_column='HRC_non1000G_AC', blank=True, null=True)  # Field name made lowercase.
    hrc_non1000g_an = models.TextField(db_column='HRC_non1000G_AN', blank=True, null=True)  # Field name made lowercase.
    cosmic70 = models.TextField(blank=True, null=True)
    clinvar_20150629 = models.TextField(blank=True, null=True)
    sift_score = models.TextField(db_column='SIFT_score', blank=True, null=True)  # Field name made lowercase.
    sift_pred = models.TextField(db_column='SIFT_pred', blank=True, null=True)  # Field name made lowercase.
    polyphen2_hdiv_score = models.TextField(db_column='Polyphen2_HDIV_score', blank=True, null=True)  # Field name made lowercase.
    polyphen2_hdiv_pred = models.TextField(db_column='Polyphen2_HDIV_pred', blank=True, null=True)  # Field name made lowercase.
    polyphen2_hvar_score = models.TextField(db_column='Polyphen2_HVAR_score', blank=True, null=True)  # Field name made lowercase.
    polyphen2_hvar_pred = models.TextField(db_column='Polyphen2_HVAR_pred', blank=True, null=True)  # Field name made lowercase.
    lrt_score = models.TextField(db_column='LRT_score', blank=True, null=True)  # Field name made lowercase.
    lrt_pred = models.TextField(db_column='LRT_pred', blank=True, null=True)  # Field name made lowercase.
    mutationtaster_score = models.TextField(db_column='MutationTaster_score', blank=True, null=True)  # Field name made lowercase.
    mutationtaster_pred = models.TextField(db_column='MutationTaster_pred', blank=True, null=True)  # Field name made lowercase.
    mutationassessor_score = models.TextField(db_column='MutationAssessor_score', blank=True, null=True)  # Field name made lowercase.
    mutationassessor_pred = models.TextField(db_column='MutationAssessor_pred', blank=True, null=True)  # Field name made lowercase.
    fathmm_score = models.TextField(db_column='FATHMM_score', blank=True, null=True)  # Field name made lowercase.
    fathmm_pred = models.TextField(db_column='FATHMM_pred', blank=True, null=True)  # Field name made lowercase.
    provean_score = models.TextField(db_column='PROVEAN_score', blank=True, null=True)  # Field name made lowercase.
    provean_pred = models.TextField(db_column='PROVEAN_pred', blank=True, null=True)  # Field name made lowercase.
    vest3_score = models.TextField(db_column='VEST3_score', blank=True, null=True)  # Field name made lowercase.
    cadd_raw = models.TextField(db_column='CADD_raw', blank=True, null=True)  # Field name made lowercase.
    cadd_phred = models.TextField(db_column='CADD_phred', blank=True, null=True)  # Field name made lowercase.
    dann_score = models.TextField(db_column='DANN_score', blank=True, null=True)  # Field name made lowercase.
    fathmm_mkl_coding_score = models.TextField(db_column='fathmm_MKL_coding_score', blank=True, null=True)  # Field name made lowercase.
    fathmm_mkl_coding_pred = models.TextField(db_column='fathmm_MKL_coding_pred', blank=True, null=True)  # Field name made lowercase.
    metasvm_score = models.TextField(db_column='MetaSVM_score', blank=True, null=True)  # Field name made lowercase.
    metasvm_pred = models.TextField(db_column='MetaSVM_pred', blank=True, null=True)  # Field name made lowercase.
    metalr_score = models.TextField(db_column='MetaLR_score', blank=True, null=True)  # Field name made lowercase.
    metalr_pred = models.TextField(db_column='MetaLR_pred', blank=True, null=True)  # Field name made lowercase.
    integrated_fitcons_score = models.TextField(db_column='integrated_fitCons_score', blank=True, null=True)  # Field name made lowercase.
    integrated_confidence_value = models.TextField(blank=True, null=True)
    gerp_rs = models.TextField(db_column='GERP_RS', blank=True, null=True)  # Field name made lowercase.
    phylop7way_vertebrate = models.TextField(db_column='phyloP7way_vertebrate', blank=True, null=True)  # Field name made lowercase.
    phylop20way_mammalian = models.TextField(db_column='phyloP20way_mammalian', blank=True, null=True)  # Field name made lowercase.
    phastcons7way_vertebrate = models.TextField(db_column='phastCons7way_vertebrate', blank=True, null=True)  # Field name made lowercase.
    phastcons20way_mammalian = models.TextField(db_column='phastCons20way_mammalian', blank=True, null=True)  # Field name made lowercase.
    siphy_29way_logodds = models.TextField(db_column='SiPhy_29way_logOdds', blank=True, null=True)  # Field name made lowercase.
    interpro_domain = models.TextField(db_column='Interpro_domain', blank=True, null=True)  # Field name made lowercase.
    allele_end = models.IntegerField(db_column='ALLELE_END', blank=True, null=True)  # Field name made lowercase.
    c1 = models.TextField(db_column='C1', blank=True, null=True)  # Field name made lowercase.
    c10 = models.TextField(db_column='C10', blank=True, null=True)  # Field name made lowercase.
    c11 = models.TextField(db_column='C11', blank=True, null=True)  # Field name made lowercase.
    c12 = models.TextField(db_column='C12', blank=True, null=True)  # Field name made lowercase.
    c13 = models.TextField(db_column='C13', blank=True, null=True)  # Field name made lowercase.
    c14 = models.TextField(db_column='C14', blank=True, null=True)  # Field name made lowercase.
    c15 = models.TextField(db_column='C15', blank=True, null=True)  # Field name made lowercase.
    c16 = models.TextField(db_column='C16', blank=True, null=True)  # Field name made lowercase.
    c17 = models.TextField(db_column='C17', blank=True, null=True)  # Field name made lowercase.
    c2 = models.TextField(db_column='C2', blank=True, null=True)  # Field name made lowercase.
    c3 = models.TextField(db_column='C3', blank=True, null=True)  # Field name made lowercase.
    c4 = models.TextField(db_column='C4', blank=True, null=True)  # Field name made lowercase.
    c5 = models.TextField(db_column='C5', blank=True, null=True)  # Field name made lowercase.
    c6 = models.TextField(db_column='C6', blank=True, null=True)  # Field name made lowercase.
    c7 = models.TextField(db_column='C7', blank=True, null=True)  # Field name made lowercase.
    c8 = models.TextField(db_column='C8', blank=True, null=True)  # Field name made lowercase.
    c9 = models.TextField(db_column='C9', blank=True, null=True)  # Field name made lowercase.
    d1 = models.TextField(db_column='D1', blank=True, null=True)  # Field name made lowercase.
    d10 = models.TextField(db_column='D10', blank=True, null=True)  # Field name made lowercase.
    d11 = models.TextField(db_column='D11', blank=True, null=True)  # Field name made lowercase.
    d12 = models.TextField(db_column='D12', blank=True, null=True)  # Field name made lowercase.
    d13 = models.TextField(db_column='D13', blank=True, null=True)  # Field name made lowercase.
    d14 = models.TextField(db_column='D14', blank=True, null=True)  # Field name made lowercase.
    d15 = models.TextField(db_column='D15', blank=True, null=True)  # Field name made lowercase.
    d16 = models.TextField(db_column='D16', blank=True, null=True)  # Field name made lowercase.
    d17 = models.TextField(db_column='D17', blank=True, null=True)  # Field name made lowercase.
    d18 = models.TextField(db_column='D18', blank=True, null=True)  # Field name made lowercase.
    d19 = models.TextField(db_column='D19', blank=True, null=True)  # Field name made lowercase.
    d2 = models.TextField(db_column='D2', blank=True, null=True)  # Field name made lowercase.
    d20 = models.TextField(db_column='D20', blank=True, null=True)  # Field name made lowercase.
    d21 = models.TextField(db_column='D21', blank=True, null=True)  # Field name made lowercase.
    d22 = models.TextField(db_column='D22', blank=True, null=True)  # Field name made lowercase.
    d23 = models.TextField(db_column='D23', blank=True, null=True)  # Field name made lowercase.
    d24 = models.TextField(db_column='D24', blank=True, null=True)  # Field name made lowercase.
    d25 = models.TextField(db_column='D25', blank=True, null=True)  # Field name made lowercase.
    d26 = models.TextField(db_column='D26', blank=True, null=True)  # Field name made lowercase.
    d27 = models.TextField(db_column='D27', blank=True, null=True)  # Field name made lowercase.
    d28 = models.TextField(db_column='D28', blank=True, null=True)  # Field name made lowercase.
    d29 = models.TextField(db_column='D29', blank=True, null=True)  # Field name made lowercase.
    d3 = models.TextField(db_column='D3', blank=True, null=True)  # Field name made lowercase.
    d30 = models.TextField(db_column='D30', blank=True, null=True)  # Field name made lowercase.
    d31 = models.TextField(db_column='D31', blank=True, null=True)  # Field name made lowercase.
    d4 = models.TextField(db_column='D4', blank=True, null=True)  # Field name made lowercase.
    d5 = models.TextField(db_column='D5', blank=True, null=True)  # Field name made lowercase.
    d6 = models.TextField(db_column='D6', blank=True, null=True)  # Field name made lowercase.
    d7 = models.TextField(db_column='D7', blank=True, null=True)  # Field name made lowercase.
    d8 = models.TextField(db_column='D8', blank=True, null=True)  # Field name made lowercase.
    d9 = models.TextField(db_column='D9', blank=True, null=True)  # Field name made lowercase.
    h1 = models.TextField(db_column='H1', blank=True, null=True)  # Field name made lowercase.
    h10 = models.TextField(db_column='H10', blank=True, null=True)  # Field name made lowercase.
    h11 = models.TextField(db_column='H11', blank=True, null=True)  # Field name made lowercase.
    h12 = models.TextField(db_column='H12', blank=True, null=True)  # Field name made lowercase.
    h13 = models.TextField(db_column='H13', blank=True, null=True)  # Field name made lowercase.
    h14 = models.TextField(db_column='H14', blank=True, null=True)  # Field name made lowercase.
    h15 = models.TextField(db_column='H15', blank=True, null=True)  # Field name made lowercase.
    h16 = models.TextField(db_column='H16', blank=True, null=True)  # Field name made lowercase.
    h17 = models.TextField(db_column='H17', blank=True, null=True)  # Field name made lowercase.
    h18 = models.TextField(db_column='H18', blank=True, null=True)  # Field name made lowercase.
    h19 = models.TextField(db_column='H19', blank=True, null=True)  # Field name made lowercase.
    h2 = models.TextField(db_column='H2', blank=True, null=True)  # Field name made lowercase.
    h20 = models.TextField(db_column='H20', blank=True, null=True)  # Field name made lowercase.
    h21 = models.TextField(db_column='H21', blank=True, null=True)  # Field name made lowercase.
    h22 = models.TextField(db_column='H22', blank=True, null=True)  # Field name made lowercase.
    h23 = models.TextField(db_column='H23', blank=True, null=True)  # Field name made lowercase.
    h24 = models.TextField(db_column='H24', blank=True, null=True)  # Field name made lowercase.
    h25 = models.TextField(db_column='H25', blank=True, null=True)  # Field name made lowercase.
    h26 = models.TextField(db_column='H26', blank=True, null=True)  # Field name made lowercase.
    h27 = models.TextField(db_column='H27', blank=True, null=True)  # Field name made lowercase.
    h28 = models.TextField(db_column='H28', blank=True, null=True)  # Field name made lowercase.
    h29 = models.TextField(db_column='H29', blank=True, null=True)  # Field name made lowercase.
    h3 = models.TextField(db_column='H3', blank=True, null=True)  # Field name made lowercase.
    h30 = models.TextField(db_column='H30', blank=True, null=True)  # Field name made lowercase.
    h31 = models.TextField(db_column='H31', blank=True, null=True)  # Field name made lowercase.
    h32 = models.TextField(db_column='H32', blank=True, null=True)  # Field name made lowercase.
    h4 = models.TextField(db_column='H4', blank=True, null=True)  # Field name made lowercase.
    h5 = models.TextField(db_column='H5', blank=True, null=True)  # Field name made lowercase.
    h6 = models.TextField(db_column='H6', blank=True, null=True)  # Field name made lowercase.
    h7 = models.TextField(db_column='H7', blank=True, null=True)  # Field name made lowercase.
    h8 = models.TextField(db_column='H8', blank=True, null=True)  # Field name made lowercase.
    h9 = models.TextField(db_column='H9', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'test2'
