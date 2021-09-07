

# MyVCF2: web-based tool for analysis and visualization of mutations in VCF files

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
a single VCF file. The tool will recognize the different samples and show them as different
columns. 

The following fields are required for each of the annotation tools:

* VEP = CSQ, symbol and consequence 
* Annovar = gene_refgene, gene_ensgene and exonicfunc_ensgene
* snpEff = gene_name, gene_id, ANN and annotation

### Deployment

Instructions on how to deploy the tool with Anaconda:


``` shell
git clone https://github.com/jfnavarro/myVCF.git
cd myVCF
conda env create -f environment.yml
conda activate myvcf
python manage.py runserver
# Open the internet browser and go to http://localhost:8000/
# The user "admin" with password "1234admin" is already registered in the database
# Go to http://localhost:8000/admin to change the password
```

Instructions on how to deploy the tool with Docker:


``` shell
git clone https://github.com/jfnavarro/myVCF.git
cd myVCF
docker-compose build
docker-compose up
# Open the internet browser and go to http://localhost:8000/
# The user "admin" with password "1234admin" is already registered in the database
# Go to http://localhost:8000/admin to change the password
```

To deploy the tool in a production environment the following
steps must be followed:

* Update the secret key in .env  (KEEP THIS SAFE). 
* Copy the mysql3 databases to somewhere local. 
* Update myvcf_main/settings.py to the new location of the databases. 
* Update .env to add your host to ALLOWED_HOSTS
* Create a super user using python manage.py createsuperuser
* Configure access trough a WSGI server or similar and deploy the tool
* Change the password of the admin user

### Configuration

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

### Test datasets
Two test VCF files annodated with Annovar and VEP are located
in /data/VCFs. They can be used to test and develop the tool. 

### Main functionalities

The tool requires login acess. Once the user has logged in, the main page
is shown and here the user can create, delete and open projects (one project per VCF file).
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

