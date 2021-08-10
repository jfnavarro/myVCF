

# MyVCF2: web-based tool for analysis and visualization of mutations stored in VCF files

MyVCF2 is a tool that enables the storage, loading, querying and analysis of mutational
data (SNPs and indels) stored in VCF files. The tool implements a simple django 
interface with a mysql3 database and secure access (login). The VCF files can be 
stored in the database and they can be opened and browsed once the user has logged
in to the application. The tool can be deployed either locally or in a dedicated
server (See deployment).

### Acknowledgement

This tool is a modified version of the code present in [http://github.com/apietrelli/myVCF/](http://github.com/apietrelli/myVCF/)

### Requirements 

The tool requires well formed VCF files that have been annotated with either Annovar,
VEP or snpEff. If multiple samples are available, it is recommended to merge them into
a single VCF file. The tool will recognize the different samples and add them as different
columns. 

The following fields are required for each of the annotation tools:

* VEP = CSQ, symbol and consequence fields. 
* Annovar = gene_refgene, gene_ensgene and exonicfunc_ensgene
* snpEff = gene_name, gene_id, ANN and annotation

### Deployment

We recommend to use Anaconda or similar (Python 3).

Instructions on how to deploy the tool in a local environment:


``` shell
git clone https://github.com/jfnavarro/myVCF.git
cd myVCF
conda create -n myvcf python=3.6
conda activate myvcf
pip install -r requirements.txt
python manage.py runserver
# Open the internet browser and go to http://localhost:8000/
# The user "admin" with password "1234admin" is already registered in the database
```

To deploy the tool in a production environment the following
steps must be followed:

* Update the secret key in myvcf_main/settings.py (KEEP THIS SAFE). 
* Copy the mysql3 databases to somewhere local. 
* Update myvcf_main/settings.py to the new location of the databases. 
* Create a super user using python manage.py createsuperuser
* Deploy the tool (recommend to use a cron job or similar). 
* Configure a gateway with a public IP and ensure secure access (firewall and HTTPS). 

### Configuration

Test datasets annotated with Annovar, VEP and snpEff are present in /data/VCFs. 

The folder /data/annotation contains files with gene names and ensembl ids 
downloaded from different versions of Ensemble. These are then added to the database
in order to be able to fetch gene names from Ensembl ids. 

The tool was configured using the following commands:

``` shell
cd myVCF
python manage.py startproject 
python data/db/popuplate_genes.py 
python manage.py makemigration
python manage.py migrate
python manage.py createsuperuser
# admin 
# 1234admin
``` 

The test VCF files were then loaded and stored so the tool is
ready to be launched and tested with two test datasets. 

### Main functionalities

The tool requires login acess. Once the user has logged in, the main page
is shown and here the users can create, delete and open projects (one project per VCF files).
Once a project has been opened, the user enters the VCF browser mode where different
options are available: 

* See summary statistics of the dataset.
* Open the settings to define groups or which columns are visible.
* Query the dataset using: genes, regions and variants. 
* See the results of the query (genes and regions) in tables with filtering options. 
* See variants where multiple statistics and graphs are displayed. 

Most of the visualizations and tables are interactive. 

In order to upload a file to the database, the VCF file must
be located in the folder /data/VCFs. 

### Contact

* Jose Fernandez Navarro [jc.fernandez.navarro@gmail.com](mailto:jc.fernandez.navarro@gmail.com)

### License 
See LICENSE

