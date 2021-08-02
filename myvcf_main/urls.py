from django.conf.urls import include, url
from django.conf import settings
from django.views.static import serve
from myvcf_main import views as myVCF_view
from myvcf_browser import urls as myVCF_urls

urlpatterns = [
    url(r'^$', myVCF_view.main_page),
    url(r'^login/$', myVCF_view.user_login, name='login'),
    url(r'^logout/$', myVCF_view.user_logout, name='logout'),
    url(r'^delete_db/$', myVCF_view.delete_db),
    url(r'^upload/$', myVCF_view.upload_project),
    url(r'^upload/preprocessing_vcf/$', myVCF_view.preprocessing_vcf),
    url(r'^upload/select_vcf/$', myVCF_view.select_vcf),
    url(r'^upload/submit_vcf/$', myVCF_view.submit_vcf),
    url(r'^upload/check_project_name/$', myVCF_view.check_project_name),
    url(r'^myvcf_browser/', include(myVCF_urls, namespace="myvcf_browser")),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

