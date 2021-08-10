from typing_extensions import OrderedDict
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.apps import apps
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.exceptions import BadRequest, RequestAborted

import json
import re
import os
import sys
import time
from collections import defaultdict
from subprocess import check_output, CalledProcessError

import vcf
import sqlite3
from myvcf_browser.base_models import DbInfo, Groups

# name of the app in django 
APP_LABEL = "myvcf_browser"

# DB containing mutations
PROJECT_DB = "projects"


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']
        print("Authenticating {}, {}".format(username, password))
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
            print("Invalid login details: {}, {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    # The request is not a HTTP POST, so display the login form.
    else:
        context = {}
        return render(request, 'login.html', context)


@login_required
def user_logout(request):
    # log out and redirect to home page
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def main_page(request):
    # Fetch the list of projects
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
    # get project name from request
    project_name = request.POST['project_name']
    # __iexact is case-insensitive
    res = DbInfo.objects.filter(project_name__iexact=project_name).exists()
    context = json.dumps({'valid': not res})
    return HttpResponse(context)


def delete_db(request):
    # get project name from request
    project_name = request.POST['project_name']

    # get the model
    model = apps.get_model(app_label=APP_LABEL, model_name=project_name)

    # Delete project from the model
    model.objects.using(PROJECT_DB).all().delete()

    # Delete project from the database
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # TODO the path to the DB should be stored somewhere
    database = os.path.join(base_dir, "data/db/projects_data.sqlite3")
    conn = sqlite3.connect(database)
    try:
        with conn:
            table_name = model._meta.db_table
            sql = "DROP TABLE %s;" % (table_name)
            conn.execute(sql)
            sql = "VACUUM;"
            conn.execute(sql)
    except Exception as e:
        print("Error deleting project {}\n{}".format(project_name, e))
        return HttpResponseBadRequest("The project could not be deleted.")
    finally:
        conn.close()

    # Update model
    db = DbInfo.objects.get(project_name=project_name)
    db.delete()
    _updateModel()

    print("Project {} deleted".format(project_name))
    msg_validate = "Project deleted"
    context = json.dumps({'project_name': project_name,
                          'msg_validate': msg_validate})
    return HttpResponse(context)


def select_vcf(request):
    # path = request.POST['static_path']
    # TODO get path from static_path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vcf_dir = os.path.join(base_dir, "data/VCFs")
    files = os.listdir(vcf_dir)
    context = json.dumps({'vcf_dir': vcf_dir, 'files': files})
    return HttpResponse(context)


def preprocessing_vcf(request):
    # path = request.POST['static_path']
    # TODO get path from STATIC
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vcf_dir = os.path.join(base_dir, "data/VCFs")
    vcf_name = request.POST['vcf_name']
    vcf_file = os.path.join(vcf_dir, vcf_name)
    valid = True
    msg = "OK!"
    annotation = None
    annovar_field = "Gene_ensGene"
    vep_field = "CSQ"
    snpeff_field = "ANN"

    # Check if it is a correct VCF file with the corrent content
    try:
        with open(vcf_file, 'r') as fhandler:
            # Parse file
            vcf_handler = vcf.Reader(fhandler)

            # Get the INFO fields
            vcf_infos = list(vcf_handler.infos.keys())

            # Check if contains INFO fields
            if len(vcf_infos) == 0:
                msg = "The VCF file does not contain INFO fields..."
                valid = False

            # Check if contains at least 1 sample
            if len(vcf_handler.samples) == 0 and valid:
                msg = "The VCF file does not contain ANY sample genotype..."
                valid = False

            # Check if the VCF was annotated with supported software:
            # Annovar = Gene_ensGene field, exonic annotation = ExonicFunc_ensGene
            # VEP = CSQ field
            # snpEff = ANN field
            if valid:
                is_annovar = annovar_field in vcf_infos
                is_vep = vep_field in vcf_infos
                is_snpeff = snpeff_field in vcf_infos
                if is_snpeff:
                    annotation = "snpeff"
                elif is_annovar:
                    annotation = "annovar"
                elif is_vep:
                    annotation = "vep"
                else:
                    msg = "The VCF file was not annotated with a supported " \
                          "software (Annovar, snpEff and VEP)."
                    valid = False
    except:
        msg = "The file does not seem to be a valid VCF file."
        valid = False

    context = json.dumps({'annotation': annotation,
                          'msg_validate': msg,
                          'valid': valid})
    return HttpResponse(context)


def _populateDatabase(vcf_handler, database, project_name, columns_clean):
    """Internal function to populate the database with the content
    of the VCF file. 
    """
    autoincremental_id = 1
    data = []
    start_time = time.time()
    print('Parsing VCF records')
    for record in vcf_handler:
        values_dict = defaultdict(str, dict.fromkeys(columns_clean))

        # Get FILTER status [] = PASS
        if record.FILTER == []:
            filter_string = "PASS"
        else:
            filter_string = ''.join(record.FILTER)

        # Get base information generation (CHR, POS, ALT ...)
        values_dict['ID'] = autoincremental_id
        values_dict['CHROM'] = record.CHROM
        values_dict['POS'] = str(record.POS)
        values_dict['RS_ID'] = str(record.ID)
        values_dict['REF'] = record.REF
        values_dict['ALT'] = str(record.ALT[0])
        values_dict['QUAL'] = str(record.QUAL)
        values_dict['FILTER'] = filter_string

        # INFO generation
        for key, info in record.INFO.items():
            # TODO for now taking only the first record when multiple record in a mutation
            value = info[0] if type(info) == list else info
            value = int(value) if type(value) == bool else value
            if key == "CSQ":
                i = 1
                for x in value.split("|"):
                    values_dict["CSQ{}".format(i)] = x
                    i += 1
            elif key == "ANN":
                i = 1
                for x in value.split("|")[:-1]:
                    values_dict["ANN{}".format(i)] = x
                    i += 1
            else:
                values_dict[key] = value

        # Genotype generation
        for sample in record.samples:
            values_dict[sample.sample] = sample['GT']

        autoincremental_id += 1
        data.append(tuple(values_dict.values()))
    print('VCF file parsed')

    # storing time
    vcf_store_time = time.time() - start_time

    # build query and upload the data to the database
    params = ("?," * len(columns_clean))[:-1]
    query = "INSERT OR IGNORE INTO " + project_name + " VALUES(" + params + ");"
    success = False
    conn = sqlite3.connect(database)
    try:
        with conn:
            conn.execute("PRAGMA synchronous = OFF")
            conn.execute("PRAGMA journal_mode = OFF")
            conn.executemany(query, data)
            success = True
    except Exception as e:
        print("Error uploading VCF data to database {}".format(e))
    finally:
        conn.close()
    loading_time = time.time() - start_time
    return loading_time, vcf_store_time, autoincremental_id, success


@login_required
def submit_vcf(request):
    # Read the input data from request
    sw_annotation = request.POST['sw_annotation']
    annotation_version = request.POST['annotation_version']
    vcf_name = request.POST['vcf_name']
    assembly_version = request.POST['assembly_version']
    project_name = request.POST['project_name']

    # Get necessary fields
    # path = request.POST['static_path']
    # TODO get path from STATIC
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vcf_dir = os.path.join(base_dir, "data/VCFs")
    filename = os.path.join(vcf_dir, vcf_name)
    database = os.path.join(base_dir, "data/db/projects_data.sqlite3")

    # Create DB table and populate it
    # Mandatory fields:
    # Annovar = exonicfunc_ensgene
    # VEP = consequence
    # snpEff = annotation
    if sw_annotation == "annovar":
        default_col = ['chrom', 'pos', 'rs_id', 'ref', 'alt', 
                       'gene_refgene', 'ac', 'af', 'exonicfunc_ensgene']
        mutation_col = 'exonicfunc_ensgene'
    elif sw_annotation == "vep":
        default_col = ['chrom', 'pos', 'rs_id', 'ref', 'alt', 
                       'symbol', 'ac', 'af', 'consequence']
        mutation_col = 'consequence'
    elif sw_annotation == "snpeff":
        default_col = ['chrom', 'pos', 'rs_id', 'ref', 'alt', 
                       'gene_name', 'ac', 'af', 'annotation']
        mutation_col = 'annotation'
    else:
        return HttpResponse("Invalid annotation fields in the VCF file.")

    # Read the VCF
    print('Opening VCF file {}'.format(filename))
    with open(filename, 'r') as fhandler:
        vcf_handler = vcf.Reader(fhandler)

        # Get the sample list 
        samples = vcf_handler.samples

        # get samples number
        samples_len = len(vcf_handler.samples)
        print('Number of samples in VCF file {}'.format(samples_len))

        # Get attribute names to add them as columns in the table
        table_columns = []
        columns_clean = ["ID", "CHROM", "POS", "RS_ID", "REF", "ALT", "QUAL", "FILTER"]
        for key, info in vcf_handler.infos.items():
            # Get the attribute type
            if info.type == "String":
                table_type = "TEXT"
            elif info.type == "Float":
                table_type = "REAL"
            elif info.type == "Integer":
                table_type = "INTEGER"
            elif info.type == "Flag":
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
            elif key == "CSQ":
                start_pos = int(info.desc.index(":")) + 2
                i = 1
                for field in info.desc[start_pos:].split('|'):
                    table_columns.append('"' + field.strip() + '" ' + "TEXT" + ", ")
                    columns_clean.append("CSQ{}".format(i))
                    i += 1
            elif key == "ANN":
                start_pos = int(info.desc.index(":")) + 3
                i = 1
                for field in info.desc[start_pos:].split('|')[:-1]:
                    table_columns.append('"' + field.strip() + '" ' + "TEXT" + ", ")
                    columns_clean.append("ANN{}".format(i))
                    i += 1
            else:
                table_columns.append('"' + key + '" ' + table_type + ", ")
                columns_clean.append(key)

        # Get sample names to add them as columns in the table
        sampleStatement = ""
        for sample in vcf_handler.samples:
            sampleStatement += '"' + sample + '"' + " TEXT, "
            columns_clean.append(sample)

        # Build query
        drop_query = "DROP TABLE IF EXISTS {};".format(project_name)
        defaultStatement = "CREATE TABLE {} " \
                            "(ID INT PRIMARY KEY NOT NULL, CHROM TEXT NOT NULL, POS INT NOT NULL, " \
                            "RS_ID TEXT, REF TEXT NOT NULL, ALT TEXT, QUAL REAL, FILTER TEXT, ".format(project_name)
        query = defaultStatement + ''.join(table_columns) + sampleStatement[:-2] + ");"

        # Create table
        conn = sqlite3.connect(database)
        try:
            with conn:
                conn.execute(drop_query)
                conn.execute(query)
        except Exception as e:
            print("Error creating table from VCF data {}".format(e))
            return HttpResponse("The VCF file seems to be malformed (table could not be created).")
        finally:
            conn.close()

        # Add records to table
        print('Uploading VCF data to database')
        loading_time, vcf_store_time, n_record, success = _populateDatabase(vcf_handler,
                                                                            database,
                                                                            project_name,
                                                                            columns_clean)
    if not success:
        # Remove table if not success
        conn = sqlite3.connect(database)
        with conn:
            conn.execute(drop_query)
            conn.close()
        return HttpResponse("There was as an error uploading the VCF data to the database.")

    n_record_rate = n_record / vcf_store_time

    # Add dataset info to django model--> dbinfo
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
               'record_store_time': 1,
               'n_record_rate': n_record_rate,
               'n_record': n_record
               }

    # Modify model.py
    _updateModel()

    # Redirect to upload summary stats page
    return render(request, 'vcf_submitted.html', context)


def _updateModel():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manage_script = os.path.join(base_dir, "manage.py")
    models = os.path.join(base_dir, APP_LABEL, "models.py")
    python_bin = sys.executable
    command = [python_bin,
               manage_script,
               "inspectdb",
               "--database",
               PROJECT_DB]
    try:
        print("Modyfing model with command {}".format(command))
        m = check_output(command)
        with open(models, "w") as fm:
            fm.write(re.sub('managed = False\n', "", m.decode('utf-8')))
    except CalledProcessError as e:
        print("Error modifying the model after uploading VCF data\n{}".format(e))