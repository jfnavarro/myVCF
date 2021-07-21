from typing_extensions import OrderedDict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

import json
import re
import os
import sys

from subprocess import check_output, CalledProcessError

import vcf
import sqlite3
from vcfdb.base_models import DbInfo, Groups

app_label = "vcfdb"

# DB containing mutations
project_db = "projects"


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']
        print("Authenticating {} {}".format(username, password))
        user = authenticate(username=username, password=password)
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    # The request is not a HTTP POST, so display the login form.
    else:
        context = {}
        return render(request, 'login.html', context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def main_page(request):
    db_list = DbInfo.objects.values("project_name",
                                    "gene_annotation",
                                    "sw_annotation",
                                    "assembly_version",
                                    "samples",
                                    "samples_len")
    context = {'db_list': db_list}
    return render(request, 'base_site.html', context)


@login_required
def upload_project(request):
    context = {}
    return render(request, 'upload.html', context)


def check_project_name(request):
    project_name = request.POST['project_name']
    # __iexact is case-insensitive
    res = DbInfo.objects.filter(project_name__iexact=project_name).exists()
    if res:
        context = json.dumps({'valid': False})
    else:
        context = json.dumps({'valid': True})
    return HttpResponse(context)


def delete_db(request):
    # AJAX request
    project_name = request.POST['project_name']

    # get the model
    model = apps.get_model(app_label=app_label,
                           model_name=project_name)

    # Delete data
    model.objects.using(project_db).all().delete()

    # Delete table
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    database = os.path.join(base_dir, "data/db/projects_DB.sqlite3")
    conn = sqlite3.connect(database)
    c = conn.cursor()
    table_name = model._meta.db_table
    sql = "DROP TABLE %s;" % (table_name)
    c.execute(sql)

    # Restore projects_DB.sqlite3 size
    sql = "VACUUM;"
    c.execute(sql)
    conn.close()

    # Delete the link in home page
    db = DbInfo.objects.get(project_name=project_name)
    db.delete()

    msg_validate = "Project deleted"
    context = json.dumps({'project_name': project_name,
                          'msg_validate': msg_validate})
    return HttpResponse(context)


def select_vcf(request):
    # path = request.POST['static_path']
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vcf_dir = os.path.join(base_dir, "data/VCFs")
    files = os.listdir(vcf_dir)
    context = json.dumps({'vcf_dir': vcf_dir,
                          'files': files})
    return HttpResponse(context)


def preprocessing_vcf(request):
    # path = request.POST['static_path']
    # TODO get path from STATIC
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vcf_dir = os.path.join(base_dir, "data/VCFs")
    vcf_name = request.POST['vcf_name']
    vcf_file = os.path.join(vcf_dir, vcf_name)

    def validate_vcf(vcf_file):
        import vcf
        valid = False
        annotation = None
        annovar_field = "Gene_ensGene"
        annovar_exonic_field = "ExonicFunc_ensGene"
        annovar_genesymbol_field = "Gene_refGene"
        vep_field = "CSQ"

        # Check if is a VCF file
        try:
            vcf_handler = vcf.Reader(open(vcf_file, 'r'))
        except:
            msg = "The file does not seem to be a valid VCF file..."
            return valid, msg, annotation

        # Check if contains INFO fields
        if vcf_handler.infos.keys() == []:
            msg = "The VCF file does not contain INFO fields..."
            return valid, msg, annotation

        # Check if contains at least 1 sample
        if len(vcf_handler.samples) == 0:
            msg = "The VCF file does not contain ANY sample genotype..."
            return valid, msg, annotation

        # Check if the VCF was annotated with supported software:
        # Annovar = Gene_ensGene field
        # Annovar exonic annotation = ExonicFunc_ensGene
        # VEP = CSQ field
        if ((annovar_field or annovar_exonic_field or annovar_genesymbol_field) not in vcf_handler.infos.keys()) \
                and (vep_field not in vcf_handler.infos.keys()):
            msg = "This VCF file was not annotated with Annovar nor VEP software<br>" \
                  "Please follow the manual to use a VCF file compatible with myVCF,"
            return valid, msg, annotation
        else:
            if annovar_field in vcf_handler.infos.keys():
                annotation = "annovar"
            elif vep_field in vcf_handler.infos.keys():
                annotation = "vep"

        valid = True
        msg = "OK!"
        return valid, msg, annotation

    valid, msg_validate, annotation = validate_vcf(vcf_file)

    context = json.dumps({'annotation': annotation,
                          'msg_validate': msg_validate,
                          'valid': valid})
    return HttpResponse(context)


def _populateDatabase(vcf_handler, database, project_name, columns_clean):
    import string
    import time
    from numpy import mean
    from collections import OrderedDict

    autoincremental_id = 1
    data = []
    start_time = time.time()
    record_time = []

    print('Parsing VCF records')
    max_columns = -1
    for record in vcf_handler:
        start_record = time.time()
        values_dict = OrderedDict.fromkeys(columns_clean)

        # Get FILTER status [] = PASS
        if record.FILTER == []:
            filter_string = "PASS"
        else:
            filter_string = ''.join(record.FILTER)

        # Get base information generation (CHR, POS, ALT ...) and ID
        values_dict['ID'] = autoincremental_id
        values_dict['CHROM'] = record.CHROM,
        values_dict['POS'] = str(record.POS)
        values_dict['RS_ID'] = str(record.ID)
        values_dict['REF'] = record.REF
        values_dict['ALT'] = str(record.ALT[0])
        values_dict['QUAL'] = str(record.QUAL)
        values_dict['FILTER'] = filter_string

        # INFO generation
        for key, info in record.INFO.items():
            value = info[0] if type(info) == list else info
            if key == "CSQ":
                for x in value.split("|"):
                    values_dict[]
                    info_values.append(str(x))
            elif type(value) == bool:
                info_values.append(str(int(value)))
            else:
                info_values.append(str(value))

        # Genotype generation
        gt_values = []
        for sample in record.samples:
            gt_values.append(sample['GT'])

        autoincremental_id += 1
        item = tuple(coordinates + info_values + gt_values)
        data.append(item)
        max_columns = max(len(item), max_columns)
        end_record = time.time()
        record_time.append(end_record - start_record)
    print('VCF file parsed')

    # storing time
    vcf_store_time = time.time() - start_time
    record_store_time = mean(record_time) * 1000

    params = ("?," * max_columns)[:-1]
    query = "INSERT OR IGNORE INTO " + project_name + " VALUES(" + params + ");"
    conn = sqlite3.connect(database)
    c = conn.cursor()
    try:
        c.execute("PRAGMA synchronous = OFF")
        c.execute("PRAGMA journal_mode = OFF")
        c.executemany(query, data)
    except Exception as e:
        print("Error uploading VCF data to database {}".format(e))
    conn.commit()
    conn.close()
    loading_time = (time.time() - start_time)
    return loading_time, vcf_store_time, record_store_time, autoincremental_id
    
@login_required
def submit_vcf(request):
    import sqlite3

    # Reading the input
    sw_annotation = request.POST['sw_annotation']
    annotation_version = request.POST['annotation_version']
    vcf_name = request.POST['vcf_name']
    assembly_version = request.POST['assembly_version']
    project_name = request.POST['project_name']

    # Preprocessing
    # Get the absolute path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models = os.path.join(base_dir, app_label, "models.py")
    vcf_dir = os.path.join(base_dir, "data/VCFs")
    filename = os.path.join(vcf_dir, vcf_name)
    database = os.path.join(base_dir, "data/db/projects_DB.sqlite3")
    manage_script = os.path.join(base_dir, "manage.py")
    python_bin = sys.executable

    # Create DB and populate it
    # Mandatory fields:
    # Annovar = exonicfunc_ensgene, gene_ensgene, func_ensgene, gene_refgene
    # VEP = consequence
    if sw_annotation == "annovar":
        default_col = ['chrom', 'pos', 'rs_id', 'ref', 'alt', 'gene_refgene', 'ac', 'af', 'exonicfunc_ensgene']
        mutation_col = 'exonicfunc_ensgene'
    elif sw_annotation == "vep":
        default_col = ['chrom', 'pos', 'rs_id', 'ref', 'alt', 'symbol', 'ac', 'af', 'consequence']
        mutation_col = 'consequence'
    else:
        return HttpResponse("Invalid annotation when uploading VCF file.")

    # Read the VCF
    vcf_handler = vcf.Reader(open(filename, 'r'))
    print('Opening VCF file {}'.format(filename))

    # Get the sample list 
    samples = vcf_handler.samples

    # get samples number
    samples_len = len(vcf_handler.samples)
    print('Number of samples {}'.format(samples_len))

    drop_query = "DROP TABLE IF EXISTS {};".format(project_name)
    defaultStatement = "CREATE TABLE {} " \
                        "(ID INT PRIMARY KEY NOT NULL, CHROM TEXT NOT NULL, POS INT NOT NULL, " \
                        "RS_ID TEXT, REF TEXT NOT NULL, ALT TEXT, QUAL REAL, FILTER TEXT, ".format(project_name)

    # Get attribute names to use as columns in the table
    table_columns = []
    columns_clean = []
    for key, info in vcf_handler.infos.items():
        # Get the attribute type
        if info.type == "String":
            table_type = "TEXT"
        elif info.type == "Float":
            table_type = "REAL"
        elif info.type == "Integer":
            table_type = "INTEGER"
        else:
            table_type = "TEXT"
        # Get the attribute name
        if key[0].isdigit():
            table_columns.append('"u' + key + '" ' + table_type + ", ")
            columns_clean.append(key)
        elif key.startswith("GERP"):
            table_columns.append('"GERP_RS"' + table_type + ", ")
            columns_clean.append(key)
        elif key.startswith("CSQ"):
            start_pos = int(info.desc.index(":")) + 2
            for field in info.desc[start_pos:].split('|'):
                table_columns.append('"' + field + '" ' + "TEXT" + ", ")
                columns_clean.append(field)
        else:
            table_columns.append('"' + key + '" ' + table_type + ", ")
            columns_clean.append(key)

    # Get sample to use as columns in the table
    sampleStatement = ""
    for sample in vcf_handler.samples:
        sampleStatement += '"' + sample + '"' + " TEXT, "

    # Build query
    query = defaultStatement + ''.join(table_columns) + sampleStatement[:-2] + ");"

    # Create table
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute(drop_query)
    print("SQL query to generate table for VCF file \n{}".format(query.count(',')))
    c.execute(query)
    conn.commit()
    c.close()

    # Add records to table
    print('Uploading VCF data to database')
    loading_time, vcf_store_time, record_store_time, n_record = _populateDatabase(vcf_handler, 
                                                                                  database,
                                                                                  project_name,
                                                                                  columns_clean)
    n_record_rate = n_record / vcf_store_time

    # Add dataset info to DB in myVCF_DB--> dbinfo
    print('Adding dataset info to the database')
    db = DbInfo.objects.create(project_name=project_name,
                               gene_annotation=annotation_version,
                               sw_annotation=sw_annotation,
                               samples=samples,
                               samples_len=samples_len,
                               default_col=default_col,
                               mutation_col=mutation_col,
                               assembly_version=assembly_version)
    db.save()

    # Output the context
    sanity_check = "OK"
    context = {'sanity_check': sanity_check,
               'vcf_name': vcf_name,
               'annotation_version': annotation_version,
               'assembly_version': assembly_version,
               'sw_annotation': sw_annotation,
               'project_name': project_name,
               'loading_time': loading_time,
               'vcf_store_time': vcf_store_time,
               'record_store_time': record_store_time,
               'n_record_rate': n_record_rate,
               'n_record': n_record
               }

    # Modify model.py
    command = [python_bin,
               manage_script,
               "inspectdb",
               "--database",
               project_db]
    try:
        print("Modyfing model with command {}".format(command))
        m = check_output(command)
    except CalledProcessError as e:
        print("Error modifying whe model when uploading VCF file \n{}".format(e))
    m = re.sub('managed = False\n', "", m)
    fm = open(models, "w")
    fm.write(m)
    fm.close()

    # Redirect to upload summary stats page
    return render(request, 'vcf_submitted.html', context)
