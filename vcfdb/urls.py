from django.conf.urls import url
from django.contrib.auth import views as auth_views
from vcfdb import views as myapp_views

app_name = 'vcfdb'

cache = {}
urlpatterns = [
    url(r'^(?P<project_name>\w+)/$', myapp_views.project_homepage, name='index'),
    url(r'^(?P<project_name>\w+)/search/$', myapp_views.search, name='search'),
    url(r'^(?P<project_name>\w+)/not_found/(?P<q>\w+)$', myapp_views.not_found, name='not_found'),
    url(r'^(?P<project_name>\w+)/gene/(?P<gene_ensgene>ENSG[0-9]+)/$', myapp_views.display_gene_results, name='gene_list'),
    url(r'^(?P<project_name>\w+)/gene/(?P<gene_ensgene>ENSG[0-9]+)/plink_gene/$', myapp_views.plink_gene, name='plink_g'),
    url(r'^(?P<project_name>\w+)/region/(?P<region>(chr)?[0-9XY]{1,2}-[0-9]+-[0-9]+)/$',
        myapp_views.display_region_results, name='region'),
    url(r'^(?P<project_name>\w+)/region/(?P<region>(chr)?[0-9XY]{1,2}-[0-9]+-[0-9]+)/plink_region/$',
        myapp_views.plink_region, name='plink_r'),
    url(r'^(?P<project_name>\w+)/variant/(?P<variant>(chr)?[0-9XY]{1,2}-[0-9]+-[0-9]+-[Aa,Tt,Gg,Cc]+-[Aa,Tt,Gg,Cc]+)/$',
        myapp_views.display_variant_results, name='variant'),
    url(r'^(?P<project_name>\w+)/variant/(?P<variant>(chr)?[0-9XY]{1,2}-[0-9]+-[0-9]+-[Aa,Tt,Gg,Cc]+-[Aa,Tt,Gg,Cc]+)/get_insilico_pred/$',
        myapp_views.get_insilico_pred, name='insilico' ),
    url(r'^(?P<project_name>\w+)/variant/(?P<variant>(chr)?[0-9XY]{1,2}-[0-9]+-[0-9]+-[Aa,Tt,Gg,Cc]+-[Aa,Tt,Gg,Cc]+)/get_exac_data/$',
        myapp_views.get_exac_data, name='exac'),
    url(r'^(?P<project_name>\w+)/variant/(?P<variant>(chr)?[0-9XY]{1,2}-[0-9]+-[0-9]+-[Aa,Tt,Gg,Cc]+-[Aa,Tt,Gg,Cc]+)/get_esp_data/$',
        myapp_views.get_esp_data, name='esp'),
    url(r'^(?P<project_name>\w+)/variant/(?P<variant>(chr)?[0-9XY]{1,2}-[0-9]+-[0-9]+-[Aa,Tt,Gg,Cc]+-[Aa,Tt,Gg,Cc]+)/get_1000g_data/$',
        myapp_views.get_1000g_data, name='1000g'),
    url(r'^(?P<project_name>\w+)/settings/$', myapp_views.settings, name='settings'),
    url(r'^(?P<project_name>\w+)/settings/get_col_list/$', myapp_views.get_col_list, name='get_col_list'),
    url(r'^(?P<project_name>\w+)/settings/get_sample_list/$', myapp_views.get_sample_list, name='get_sample_list'),
    url(r'^(?P<project_name>\w+)/settings/delete_group/$', myapp_views.delete_group, name='delete_group'),
    url(r'^(?P<project_name>\w+)/settings/save_preferences/$', myapp_views.save_preferences, name='save_preferences'),
    url(r'^(?P<project_name>\w+)/settings/save_groups/$', myapp_views.save_groups, name='save_groups'),
    url(r'^(?P<project_name>\w+)/settings/check_group_name/$', myapp_views.check_group_name, name='check_group_name'),
    url(r'^(?P<project_name>\w+)/summary_statistics/$', myapp_views.summary_statistics, name='summary_statistics'),
    url(r'^(?P<project_name>\w+)/summary_statistics/get_qual_vcf/$', myapp_views.get_qual_vcf, {'cache': cache} ),
    url(r'^(?P<project_name>\w+)/summary_statistics/get_mean_variations/$', myapp_views.get_mean_variations, {'cache': cache} ),
    url(r'^(?P<project_name>\w+)/summary_statistics/get_exonictype_variations/$', myapp_views.get_exonictype_variations, {'cache': cache} ),
    url(r'^(?P<project_name>\w+)/summary_statistics/get_biotype_variations/$', myapp_views.get_biotype_variations, {'cache': cache} ),
    url(r'^(?P<project_name>\w+)/summary_statistics/get_chr_variations/$', myapp_views.get_chr_variations, {'cache': cache} ),
    url(r'^(?P<project_name>\w+)/summary_statistics/get_top_genes/$', myapp_views.get_top_genes, {'cache': cache} ),
]

handler404 = myapp_views.error404
handler500 = myapp_views.error500
