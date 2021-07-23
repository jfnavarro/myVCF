from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.apps import apps
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

import ast
import json
import re
from collections import Counter
from collections import OrderedDict
from collections import defaultdict

import numpy as np
import requests

from vcfdb.base_models import DbInfo, Groups

app_label = "vcfdb"

# DB containing common data
actual_db = "default"

# DB containing mutations
project_db = "projects"


def error404(request, exception):
    context = {'test': "OK"}
    return render(request, '404.html', context)


def error500(request):
    context = {'test': "OK"}
    return render(request, '500.html', context)


def not_found(request, project_name, q):
    context = {'q': q, 'project_name': project_name}
    return render(request, 'not_found.html', context)


def project_homepage(request, project_name):
    # Get the information of DB selected
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()
    sw_annotation = dbinfo.sw_annotation
    gene_annotation = dbinfo.gene_annotation
    assembly_version = dbinfo.assembly_version
    context = {'project_name': project_name,
               'assembly_version': assembly_version,
               'sw_annotation': sw_annotation,
               'gene_annotation': gene_annotation}
    return render(request, 'index.html', context)


@login_required
def search(request, project_name):
    def is_region(query):
        res = len(re.findall(r"[:-]", query))
        return res == 2

    def split_region(region):
        # Get the numbers from string
        r = re.findall(r"\d+", region)
        # test for element length (CHR:start-end)
        return "%s-%s-%s" % (r[0], r[1], r[2]) if len(r) == 3 else 0

    def is_dbsnp(query):
        # Check correct rs number
        pattern = re.compile('^rs[1-9]+', re.IGNORECASE)
        return pattern.match(query)

    def is_variant(query):
        # Check correct rs number
        pattern = re.compile('^[0-9XY]{1,2}-[0-9]+-[0-9]+-[A,T,G,C]+-[A,T,G,C]+', re.IGNORECASE)
        return pattern.match(query)

    def get_dbsnp_record(query, model_project):
        return model_project.objects.using(project_db).filter(rs_id=query)

    # Parse request
    query = request.GET['q']
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()
    gene_annotation = dbinfo.gene_annotation
    sw_annotation = dbinfo.sw_annotation

    # Get the project model
    model_project = apps.get_model(app_label=app_label, model_name=project_name)

    # Define the query: Region or Gene?
    if is_region(query):
        region_query = split_region(query)
        return HttpResponseRedirect('/vcfdb/%s/region/%s' % (project_name, region_query))
    elif is_dbsnp(query):
        results = get_dbsnp_record(query, model_project)
        if sw_annotation == "vep":
            gene_symbol_col = "symbol"
            ensgene_id_col = "gene"
        else:
            gene_symbol_col = "gene_refgene"
            ensgene_id_col = "gene_ensgene"
        context = {'query': query,
                    'results': results,
                    'ensgene_id_col': ensgene_id_col,
                    'gene_symbol_col': gene_symbol_col,
                    'project_name': project_name}
        return render(request, 'search_variant.html', context)
    elif is_variant(query):
        # Remove whitespaces
        query = query.replace(" ", "")
        return HttpResponseRedirect('/vcfdb/%s/variant/%s' % (project_name, query))
    else:
        # Get the ENSEMBL model
        model_name_ensembl = "Gene" + gene_annotation
        model_ensembl = apps.get_model(app_label=app_label, model_name=model_name_ensembl)
        # TODO this may not work for Annovar
        results = model_ensembl.objects.filter(genename__icontains=query).values('ensgene', 
                                                                                 'genename',
                                                                                 'description').distinct()

        # Get mutation count for each ENSGENE
        # Build a new dictionary which contains EnsembleGeneID, description, Genename and mutation count
        # final_results is the merged dictionary
        final_results = []
        for res in results:
            ensgene_id = res['ensgene']
            if sw_annotation == "annovar":
                count = model_project.objects.using(project_db).filter(gene_ensgene__iexact=ensgene_id).count()
            else:
                count = model_project.objects.using(project_db).filter(gene__iexact=ensgene_id).count()
            res['mut_count'] = count
            final_results.append(res)

        # Send results back
        context = {'query': query,
                    'results': final_results,
                    'project_name': project_name}
        return render(request, 'search.html', context)


@login_required
def display_gene_results(request, gene_ensgene, project_name):

    # get the info of the project
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()
    sw_annotation = dbinfo.sw_annotation
    gene_annotation = dbinfo.gene_annotation
    samples = ast.literal_eval(dbinfo.samples)
    default_col = ast.literal_eval(dbinfo.default_col)
    mutation_col = dbinfo.mutation_col
    groups = Groups.objects.filter(project_name__iexact=project_name)
    type = "gene"

    # Get gene symbol from ensembl table
    model_name_ensembl = "Gene" + gene_annotation
    model_ensembl = apps.get_model(app_label=app_label, model_name=model_name_ensembl)
    gene_symbol = model_ensembl.objects.filter(ensgene__iexact=gene_ensgene).values('genename').distinct()[0]

    # Django converts characters
    samples = [sample.replace('-', '_') for sample in samples]
    model = apps.get_model(app_label=app_label, model_name=project_name)

    # Samples pattern matching
    samples_col = samples

    # Get fields
    all_fields = [f.name for f in model._meta.get_fields()]

    # Get the mutation data
    if sw_annotation == "annovar":
        # exact match
        mutations = model.objects.using(project_db).filter(gene_ensgene__iexact=gene_ensgene)
    else:
        # exact match
        mutations = model.objects.using(project_db).filter(gene__iexact=gene_ensgene)
    mutations_category = Counter([getattr(m, mutation_col).encode() for m in mutations])

    # Get mutation categories
    category = [key.decode('ascii', 'ignore') for key in mutations_category.keys()]
    context = {'samples_col': samples_col,
                'default_col': default_col,
                'all_fields': all_fields,
                'query': gene_ensgene,
                'gene_symbol': gene_symbol,
                'mutations': mutations,
                'category': category,
                'values': list(mutations_category.values()),
                'type': type,
                'groups': groups,
                'project_name': project_name}

    return render(request, 'gene_results.html', context)


@login_required
def display_region_results(request, region, project_name):

    # get the info of the project
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()
    sw_annotation = dbinfo.sw_annotation
    samples = ast.literal_eval(dbinfo.samples)
    default_col = ast.literal_eval(dbinfo.default_col)
    mutation_col = dbinfo.mutation_col
    groups = Groups.objects.filter(project_name__iexact=project_name)
    type = "region"

    # Django converts characters
    samples = [sample.replace('-', '_') for sample in samples]
    model = apps.get_model(app_label=app_label, model_name=project_name)

    # Get fields
    all_fields = [f.name for f in model._meta.get_fields()]

    # Get the mutation data
    # Split region in CHR, START, END
    chr, start, end = region.split("-")

    # Get the mutations and default_col of a region
    mutations = model.objects.using(project_db).filter(chrom=chr).filter(pos__range=[start, end])
    mutations_category = Counter([getattr(m, mutation_col).encode() for m in mutations])

    # Get mutation categories
    category = [key.decode('ascii', 'ignore') for key in mutations_category.keys()]

    context = {'samples_col': samples,
                'default_col': default_col,
                'all_fields': all_fields,
                'query': region,
                'gene_symbol': region,
                'mutations': mutations,
                'category': category,
                'values': list(mutations_category.values()),
                'type': type,
                'sw_annotation': sw_annotation,
                'groups': groups,
                'project_name': project_name}
    return render(request, 'gene_results.html', context)


@login_required
def display_variant_results(request, variant, project_name):

    # get the info of the project
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()
    sw_annotation = dbinfo.sw_annotation
    gene_annotation = dbinfo.gene_annotation
    samples = ast.literal_eval(dbinfo.samples)
    assembly_version = dbinfo.assembly_version
    mutation_col = dbinfo.mutation_col
    n_samples = dbinfo.n_samples()

    # Get mutations
    model = apps.get_model(app_label=app_label,model_name=project_name)
    split_v = variant.split("-")
    mutations = None
    try:
        mutations = model.objects.using(project_db).filter(chrom=split_v[0],
                                                            pos=split_v[1],
                                                            ref=split_v[3],
                                                            alt=split_v[4]).get()
    except:
        pass
    if mutations is None:
        context = {'q': variant, 'project_name': project_name}
        template = 'not_found.html'
    else:
        # Csq and gene
        # Get the gene field depending on annotation
        gene_field = "gene_ensgene" if sw_annotation == "annovar" else "gene"
        model_ensembl = apps.get_model(app_label=app_label, model_name="Gene" + gene_annotation)
        csq = getattr(mutations, mutation_col)
        ensgene_id = getattr(mutations, gene_field)
        gene = model_ensembl.objects.filter(ensgene=ensgene_id).values("genename", "description").distinct()

        # Coverage
        covered_samples = mutations.an / 2
        low_ac = 1 if mutations.an <= ((n_samples * 2) * 80 / 100) else 0

        # Zigosity
        zigosity_index = ["0", "1", "2"]
        zigosity_list = Counter([getattr(mutations, sample.lower()) for sample in samples])

        # Assembly label
        assembly_label = "GRCh37/hg19" if assembly_version == "hg19" else "GRCh38/hg38"

        context = {'mutations': mutations,
                    'low_ac': low_ac,
                    'n_samples': n_samples,
                    'covered_samples': covered_samples,
                    'csq': csq,
                    'ensgene_id': ensgene_id,
                    'gene': gene,
                    'zigosity_index': zigosity_index,
                    'zigosity_list': list(zigosity_list.values()),
                    'project_name': project_name,
                    'assembly_label': assembly_label,
                    'sw_annotation': sw_annotation,
                    'variant': variant}
        template = 'variant_results.html'

    return render(request, template, context)


def get_exac_data(request, variant, project_name):

    v_split = variant.split("-")

    # Get assembly version for the project
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()
    assembly_version = dbinfo.assembly_version

    res_data = []
    response = False
    if assembly_version == "hg19":
        # Format variant for EXAC REST
        v = "-".join([v_split[0], v_split[1], v_split[3], v_split[4]])
        url = "http://exac.hms.harvard.edu/rest/variant/variant/" + v
        r = requests.get(url)
        if r.ok:
            response = r.ok
            data = r.json()
            try:
                populations = data["pop_ans"].keys()
                for pop in populations:
                    tmp = {}
                    tmp["population"] = pop
                    tmp["pop_acs"] = data["pop_acs"][pop]
                    tmp["pop_ans"] = data["pop_ans"][pop]
                    tmp["pop_homs"] = data["pop_homs"][pop]
                    tmp["pop_af"] = float("{0:.6f}".format(data["pop_acs"][pop] / float(data["pop_ans"][pop])))
                    res_data.append(tmp)
            except KeyError:
                pass
    else:
        # Format variant for VEP REST
        v = v_split[0] + ':g.' + v_split[1] + v_split[3] + '>' + v_split[4]
        url = "http://rest.ensembl.org/vep/human/hgvs/" + v + "?content-type=application/json"
        r = requests.get(url)
        if r.ok:
            response = r.ok
            data = r.json()
            pop_dict = {"exac_nfe_maf": "European (Non-Finnish)",
                        "exac_fin_maf": "European (Finnish)",
                        "exac_afr_maf": "African",
                        "exac_eas_maf": "East Asian",
                        "exac_sas_maf": "South Asian",
                        "exac_amr_maf": "Latino",
                        "exac_oth_maf": "Other"}
            for pop, pop_value in pop_dict.items():
                tmp = {}
                tmp["population"] = pop_value
                tmp["pop_acs"] = "ND"
                tmp["pop_ans"] = "ND"
                tmp["pop_homs"] = "ND"
                try:
                    tmp["pop_af"] = data[0]['colocated_variants'][0][pop]
                except KeyError:
                    tmp["pop_af"] = None
                res_data.append(tmp)

    context = json.dumps({'response': response,
                          'data': res_data,
                          'url': url})
    return HttpResponse(context)


def get_esp_data(request, variant, project_name):
    # reformat position from:
    # CHR-POS-POS-REF-ALT to CHR:g.PosRef>ALT
    v_split = variant.split("-")
    v = v_split[0] + ':g.' + v_split[1] + v_split[3] + '>' + v_split[4]

    # Get assembly version for the project
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()
    assembly_version = dbinfo.assembly_version

    if assembly_version == "hg19":
        # ESP hg19
        url = "http://grch37.rest.ensembl.org/vep/human/hgvs/" + v + "?content-type=application/json"
    else:
        url = "http://rest.ensembl.org/vep/human/hgvs/" + v + "?content-type=application/json"

    r = requests.get(url)
    res_data = []
    response = False
    if r.ok:
        response = r.ok
        data = r.json()
        
        # EA
        tmp = {}
        try:
            tmp["population"] = "EA - European American"
            tmp["pop_af"] = data[0]['colocated_variants'][0]['ea_maf']
        except KeyError:
            pass
        res_data.append(tmp)

        # AA
        tmp = {}
        try:
            tmp["population"] = "AA - African American"
            tmp["pop_af"] = data[0]['colocated_variants'][0]['aa_maf']
        except KeyError:
            pass
        res_data.append(tmp)

    context = json.dumps({'response': response,
                          'data': res_data,
                          'url': url})
    return HttpResponse(context)


def get_1000g_data(request, variant, project_name):
    # reformat position from:
    # CHR-POS-POS-REF-ALT to CHR:g.PosRef>ALT
    v_split = variant.split("-")
    v = v_split[0] + ':g.' + v_split[1] + v_split[3] + '>' + v_split[4]

    # Get assembly version for the project
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()
    assembly_version = dbinfo.assembly_version

    if assembly_version == "hg19":
        # 1000G hg19
        url = "http://grch37.rest.ensembl.org/vep/human/hgvs/" + v + "?content-type=application/json"
    else:
        url = "http://rest.ensembl.org/vep/human/hgvs/" + v + "?content-type=application/json"

    r = requests.get(url)
    res_data = []
    response = False
    if r.ok:
        response = r.ok
        data = r.json()
        pop_dict = {"eur_maf": "European",
                    "afr_maf": "African",
                    "sas_maf": "South Asian",
                    "eas_maf": "East Asian",
                    "amr_maf": "American (Ad Mixed)"}
        for pop in pop_dict.keys():
            tmp = {}
            pop_value = pop_dict[pop]
            tmp["population"] = pop_value
            try:
                tmp["pop_af"] = data[0]['colocated_variants'][0][pop]
            except KeyError:
                tmp["pop_af"] = None
            res_data.append(tmp)

    context = json.dumps({'response': response,
                          'data': res_data,
                          'url': url})
    return HttpResponse(context)


def get_exac_data_hg38(request, variant, project_name):
    # reformat position from:
    # CHR-POS-POS-REF-ALT to CHR:g.PosRef>ALT
    v_split = variant.split("-")
    v = v_split[0] + ':g.' + v_split[1] + v_split[3] + '>' + v_split[4]

    # Get assembly version for the project
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()
    assembly_version = dbinfo.assembly_version

    if assembly_version == "hg19":
        # ExAC
        url = "http://grch37.rest.ensembl.org/vep/human/hgvs/" + v + "?content-type=application/json"
    else:
        url = "http://rest.ensembl.org/vep/human/hgvs/" + v + "?content-type=application/json"

    r = requests.get(url)
    response = False
    res_data = []
    if r.ok:
        response = r.ok
        data = r.json()
        pop_dict = {"exac_nfe_maf": "European (Non-Finnish)",
                    "exac_fin_maf": "European (Finnish)",
                    "exac_afr_maf": "African",
                    "exac_eas_maf": "East Asian",
                    "exac_sas_maf": "South Asian",
                    "exac_amr_maf": "Latino",
                    "exac_oth_maf": "Other",
                    "exac_maf": "Total"}
        for pop in pop_dict.keys():
            tmp = {}
            pop_value = pop_dict[pop]
            tmp["population"] = pop_value
            try:
                tmp["pop_af"] = data[0]['colocated_variants'][0][pop]
            except KeyError:
                tmp["pop_af"] = None
            res_data.append(tmp)

    context = json.dumps({'response': response,
                          'data': res_data,
                          'url': url})
    return HttpResponse(context)


def get_insilico_pred(request, variant, project_name):
    # reformat position from:
    # CHR-POS-POS-REF-ALT to CHR:g.PosRef>ALT
    v_split = variant.split('-')
    v = v_split[0] + '%3Ag.' + v_split[1] + v_split[3] + '>' + v_split[4]
    if not v_split[0].startswith("chr"):
        v = 'chr' + v

    # URL endpoint to get prediction
    url = "http://myvariant.info/v1/variant/" + v + "?fields=dbnsfp.polyphen2%2Cdbnsfp.sift"

    # Parse results
    r = requests.get(url)
    data = json.loads(r.content) if r.ok else {}
    return JsonResponse({'data': data}, status=200)


@login_required
def settings(request, project_name):
    msg_validate = "OK"
    groups = Groups.objects.filter(project_name__iexact=project_name)
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()
    sw_annotation = dbinfo.sw_annotation
    context = {'project_name': project_name,
               'groups': groups,
               'sw_annotation': sw_annotation,
               'msg_validate': msg_validate}
    return render(request, 'settings.html', context)


def get_col_list(request, project_name):
    # Get DB info
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()

    # Transform string into PYTHON LIST (ast.literal_eval)
    samples = ast.literal_eval(dbinfo.samples)
    default_cols = ast.literal_eval(dbinfo.default_col)
    mutation_col = dbinfo.mutation_col

    # Django converts caracters
    samples = [sample.replace('-', '_').lower() for sample in samples]

    # Get data model
    model = apps.get_model(app_label=app_label, model_name=project_name)

    # all fields
    all_cols = []
    # Not visible fields
    other_cols = []
    for f in model._meta.get_fields():
        all_cols.append(f.name)
        if f.name not in default_cols and f.name not in samples:
            other_cols.append(f.name)

    # Remove ID (autoincrement from results)
    all_cols.remove('id')
    other_cols.remove('id')
    sanity_check = "OK"
    context = json.dumps({'project_name': project_name,
                          'default_cols': default_cols,
                          'all_cols': all_cols,
                          'other_cols': other_cols,
                          'mutation_col': mutation_col,
                          'sanity_check': sanity_check})
    return HttpResponse(context)


def get_sample_list(request, project_name):
    # Get DB info
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()

    # Transform string into PYTHON LIST (ast.literal_eval)
    samples = ast.literal_eval(dbinfo.samples)

    # Django converts caracters
    samples = [sample.replace('-', '_').lower() for sample in samples]

    sanity_check = "OK"
    context = json.dumps({'project_name': project_name,
                          'sample_col': samples,
                          'sanity_check': sanity_check})
    return HttpResponse(context)


def check_group_name(request, project_name):
    # Get group name from the request
    group_name = request.POST['new_group_name']

    # __iexact is case-insensitive
    res = Groups.objects.filter(project_name__iexact=project_name)

    # check if given group if in list of groups
    isValid = group_name in [g.group_name for g in res]

    context = json.dumps({'valid': isValid})
    return HttpResponse(context)


def delete_group(request, project_name):
    # Get group name from the request
    group_name = request.POST['g_name']

    # Delete data
    Groups.objects.filter(project_name__iexact=project_name).filter(group_name=group_name).delete()

    msg_validate = "Group deleted"
    context = json.dumps({'project_name': project_name,
                          'msg_validate': msg_validate})
    return HttpResponse(context)


def save_preferences(request, project_name):
    # Get the user-defined cols
    cols = request.POST.getlist("cols")
    mutation_col = request.POST["mutation_col"]

    # Update the default_col field
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()
    dbinfo.default_col = cols

    # Update mutation_col field
    dbinfo.mutation_col = mutation_col

    # Save preferences
    dbinfo.save()

    msg_validate = "OK"
    context = json.dumps({'project_name': project_name,
                          'msg_validate': msg_validate,
                          'new_col': cols,
                          'mutation_col': mutation_col})
    return HttpResponse(context)


def save_groups(request, project_name):
    # Get the user-defined cols
    sample_list = request.POST.getlist("samples_list")
    group_name = request.POST["new_group_name"]

    # Get project_id
    project_id = DbInfo.objects.get(project_name=project_name).id

    # Add group
    g = Groups(p_id=project_id, project_name=project_name, 
               group_name=group_name, samples=sample_list)
    g.save()
    context = json.dumps({'r': group_name,
                          'p': project_id,
                          's': sample_list})
    return HttpResponse(context)


@login_required
def summary_statistics(request, project_name):

    # Get the project model
    model_project = apps.get_model(app_label=app_label,
                                   model_name=project_name)

    # Get DB INFO
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()

    # Annotation sw
    sw_annotation = dbinfo.sw_annotation

    # Number of samples
    n_samples = dbinfo.n_samples()

    # Get the number of mutation found
    n_mutations = model_project.objects.using(project_db).count()

    msg_validate = "OK"
    context = {'project_name': project_name,
               'n_samples': n_samples,
               'sw_annotation': sw_annotation,
               'n_mutations': n_mutations,
               'msg_validate': msg_validate}

    return render(request, 'summary_statistics.html', context)


def get_qual_vcf(request, project_name):
    # Get the project model
    model_project = apps.get_model(app_label=app_label, model_name=project_name)

    # Quality field
    qual_field = "qual"
    quals = model_project.objects.using(project_db).values_list(qual_field, flat=True)
    qual_mean = np.round(np.mean(quals), 3)
    quals = np.round(np.log10(quals), 3)

    # Get bin and values
    qual_data, qual_bins = np.histogram(quals, bins="auto")
    qual_bins = np.round(np.power(qual_bins, 10), 3)

    # Generate qual_data array
    data = list(zip(qual_bins.tolist(), qual_data.tolist()))
    
    return JsonResponse({'qual_data': data, 'qual_mean': qual_mean}, status=200)


def get_mean_variations(request, project_name):

    def is_outlier(value, p25, p75):
        """Check if value is an outlier
        """
        lower = p25 - 1.5 * (p75 - p25)
        upper = p75 + 1.5 * (p75 - p25)
        return value <= lower or value >= upper

    # Get the project model
    model_project = apps.get_model(app_label=app_label, model_name=project_name)

    # Get dbinfo
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()
    samples = ast.literal_eval(dbinfo.samples)
    samples = [sample.replace('-', '_').lower() for sample in samples]

    var_samples = []
    search_type = "icontains"
    for sample in samples:
        filter_string = sample + "__" + search_type
        value = model_project.objects.using(project_db).filter(**{filter_string: 1}).count()
        var_samples.append(value)

    # Since highchart DRAW only values without calculate anything:
    x = project_name
    mut_q1 = np.percentile(var_samples, 25)
    mut_q3 = np.percentile(var_samples, 75)

    # Add data to the boxplot and outlier_data array
    boxplot_values = []
    outlier_data = []
    for val in var_samples:
        if is_outlier(val, mut_q1, mut_q3):
            outlier = [0, val]
            outlier_data.append(outlier)
        else:
            boxplot_values.append(val)

    # Calculate statistics
    mut_min = min(boxplot_values)
    mut_max = max(boxplot_values)
    mut_median = np.median(var_samples)

    # Generate boxplot_data array
    boxplot_data = []
    boxplot_data.extend([x, mut_min, mut_q1, mut_median, mut_q3, mut_max])

    return JsonResponse({'boxplot_data': boxplot_data,
                         'outlier_data': outlier_data}, status=200)


def get_chr_variations(request, project_name):
    # Get the project model
    model_project = apps.get_model(app_label=app_label, model_name=project_name)

    # Get DB INFO
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()

    # Chromosome column
    chr_col = "chrom"

    # Consequence column
    mutation_col = dbinfo.get_mutation_col()

    # Get chrom list
    chromosomes = model_project.objects.using(project_db).values_list(chr_col, flat=True).distinct()

    # Get function list
    functions = model_project.objects.using(project_db).values_list(mutation_col, flat=True).distinct()

    # Get the summary count of the mutation by chr
    chr_summary = Counter(model_project.objects.using(project_db).values_list(chr_col, mutation_col))

    # The idea is to obtain a list of mutational counts for the top 15 effects for each chromosome
    # TODO this could be done in a much simpler and efficient way
    tmp_plot_data = defaultdict(list)
    for func in functions:
        for chr in chromosomes:
            data = chr_summary[(chr, func,)]
            tmp_plot_data[func].append(data)
    number_of_categories = 15
    top_funcs = [x[0] for x in sorted(tmp_plot_data.items(), key=lambda t: -sum(t[1]))[:number_of_categories]]
    plot_data = {func:tmp_plot_data[func] for func in top_funcs}

    return JsonResponse({'chromosomes': list(chromosomes),
                         'plot_data': plot_data}, status=200)



def get_biotype_variations(request, project_name):
    # Get the project model
    model_project = apps.get_model(app_label=app_label, model_name=project_name)

    # Get DB INFO
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()

    # Get sw annotation
    sw_annotation = dbinfo.sw_annotation

    # Biotype column
    biotype_col = "biotype" if sw_annotation == "vep" else "func_ensgene"
    
    # Get the summary count of the mutation by type
    biotype_summary = Counter(model_project.objects.using(project_db).values_list(biotype_col, 
                                                                                  flat=True))

    # Format data for Highcharts --> PIE CHART
    plot_data = list(biotype_summary.items())

    return JsonResponse({'plot_data': plot_data}, status=200)


def get_exonictype_variations(request, project_name):
    # Get the project model
    model_project = apps.get_model(app_label=app_label, model_name=project_name)

    # Get DB INFO
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()

    # Consequence column
    mutation_col = dbinfo.get_mutation_col()

    # Get the summary count of the mutation by type
    mutation_type_summary = Counter(model_project.objects.using(project_db).values_list(mutation_col, 
                                                                                        flat=True))

    # Format data for Highcharts --> PIE CHART
    plot_data = list(mutation_type_summary.items())

    return JsonResponse({'plot_data': plot_data}, status=200)


def get_top_genes(request, project_name):
    # N genes and categories to display
    n_genes = 20
    n_categories = 5

    # Get the project model
    model_project = apps.get_model(app_label=app_label, model_name=project_name)

    # Get DB INFO
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()

    # Get sw annotation
    sw_annotation = dbinfo.sw_annotation

    # Consequence column
    mutation_col = dbinfo.get_mutation_col()

    # Get ENSGENE ID based on annotation sw
    gene_col = "gene" if sw_annotation == "vep" else "gene_ensgene"

    # Get the gene list
    res_genes = Counter(model_project.objects.using(project_db).all().values_list(gene_col, flat=True))

    # Get the first n_genes (most mutated)
    top_genes = [x[0] for x in res_genes.most_common(n_genes)]

    # Get function (catergories) list for the top genes
    search_type = "in"
    filter_string = gene_col + "__" + search_type
    res_functions = Counter(
        model_project.objects.using(project_db).filter(**{filter_string: top_genes}).values_list(mutation_col,
                                                                                                    flat=True))

    # Get the first n_categories (most mutated)
    top_functions = [x[0] for x in res_functions.most_common(n_categories)]

    # Get the plot data
    # The idea is to obtain a list of mutational counts for the top effects of the top genes
    # TODO this could be done in a much simpler and efficient way
    plot_data = defaultdict(list)
    for func in top_functions:
        for gene in top_genes:
            data = model_project.objects.using(project_db).filter(**{gene_col: gene}).filter(
                **{mutation_col: func}).count()
            plot_data[func].append(data)

    return JsonResponse({'top_genes': top_genes,
                         'plot_data': plot_data}, status=200)


def plink_gene(request, project_name, gene_ensgene):
    def get_mutations_plink(model, sw_annotation, ensgene, project_db):
        # return the mutations and default_col of a particular gene based on the sw_annotation
        if sw_annotation == "annovar":
            # exact match
            return model.objects.using(project_db).filter(gene_ensgene__iexact=ensgene)
        return model.objects.using(project_db).filter(gene__iexact=ensgene)

    # get the info of the project
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()
    sw_annotation = dbinfo.sw_annotation
    samples = ast.literal_eval(dbinfo.samples)
    model = apps.get_model(app_label=app_label,
                           model_name=project_name)
    mutations = get_mutations_plink(model, sw_annotation, gene_ensgene, project_db)

    # generate PED/MAP string
    # MAP file
    # The fields in a MAP file are:
    #    Chromosome
    #    Marker ID
    #    Genetic distance
    #    Physical position
    map = ""
    ped = ""
    for m in mutations:
        s_map = ",".join([str(m.chrom),
                          str(m.rs_id),
                          "0",
                          str(m.pos),
                          "\n"])
        map = map + s_map
    for s in samples:
        # Inizialize with sample information
        s_ped = ",".join([project_name, s, "0", "0", "0", "0"])
        # Get genotype
        gt = getattr(m, s.lower(), "notfound")
        for m in mutations:
            if gt == "0":
                s_ped = s_ped + "," + ",".join([m.ref, m.ref])
            elif gt == "1":
                s_ped = s_ped + "," + ",".join([m.ref, m.alt])
            elif gt == "2":
                s_ped = s_ped + "," + ",".join([m.alt, m.alt])
            else:
                s_ped = s_ped + "," + ",".join(["0", "0"])
        s_ped = s_ped + "\n"
        ped = ped + s_ped

    map_filename = "_".join([project_name, gene_ensgene]) + ".map"
    ped_filename = "_".join([project_name, gene_ensgene]) + ".ped"

    context = json.dumps({'map_filename': map_filename,
                          'map': map,
                          'ped_filename': ped_filename,
                          'ped': ped,
                          })
    return HttpResponse(context)


def plink_region(request, project_name, region):
    def get_mutations_plink(model, region, project_db):
        # Split region in CHR, START, END
        r = region.split("-")
        chr = r[0]
        start = r[1]
        end = r[2]
        # return the mutations of a region
        return model.objects.using(project_db).filter(chrom=chr).filter(pos__range=[start, end])

    # get the info of the project
    dbinfo = DbInfo.objects.filter(project_name=project_name).first()
    samples = ast.literal_eval(dbinfo.samples)
    model = apps.get_model(app_label=app_label,
                           model_name=project_name)
    mutations = get_mutations_plink(model, region, project_db)

    # generate PED/MAP string
    # MAP file
    # The fields in a MAP file are:
    #    Chromosome
    #    Marker ID
    #    Genetic distance
    #    Physical position

    map = ""
    ped = ""
    for m in mutations:
        s_map = ",".join([str(m.chrom),
                          str(m.rs_id),
                          "0",
                          str(m.pos),
                          "\n"])
        map = map + s_map
    for s in samples:
        # Inizialize with sample information
        s_ped = ",".join([project_name, s, "0", "0", "0", "0"])
        # Get genotype
        gt = getattr(m, s.lower(), "notfound")
        for m in mutations:
            if gt == "0":
                s_ped = s_ped + "," + ",".join([m.ref, m.ref])
            elif gt == "1":
                s_ped = s_ped + "," + ",".join([m.ref, m.alt])
            elif gt == "2":
                s_ped = s_ped + "," + ",".join([m.alt, m.alt])
            else:
                s_ped = s_ped + "," + ",".join(["0", "0"])
        s_ped = s_ped + "\n"
        ped = ped + s_ped

    map_filename = "_".join([project_name, region]) + ".map"
    ped_filename = "_".join([project_name, region]) + ".ped"

    context = json.dumps({'map_filename': map_filename,
                          'map': map,
                          'ped_filename': ped_filename,
                          'ped': ped,
                          })
    return HttpResponse(context)
