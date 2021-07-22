

# myVCF: web-based tool for the visualization and analysis of VCF files

This tool enables the storage, loading, querying and visulization of 
<<<<<<< HEAD
VCF files. The tool implments a simple Django interface with a mysql3
database and secure access (login). VCF files are loaded into the 
database and they can be openned and browse once the user has logged
in to the application. The tool can be deployed locally and in a dedicated
=======
VCF files. The tool implements a simple django interface with a sqlite3
database and secure access (login). VCF files are loaded into the 
database and they can be opened and browsed once the user has logged
in to the application. The tool can be deployed locally or in a dedicated
>>>>>>> b0784adddae3135e8813b42c5aae2c71a056e34c
server (See deployment). 

### Acknoledgements

<<<<<<< HEAD
This tool is a cutom version of the code present in [http://github.com/apietrelli/myVCF/](http://github.com/apietrelli/myVCF/)
=======
This tool is a custom version of the code present in [http://github.com/apietrelli/myVCF/](http://github.com/apietrelli/myVCF/)
>>>>>>> b0784adddae3135e8813b42c5aae2c71a056e34c

### Deployment

We recommend to use Anaconda or similar (Python 3).

Instructions on how to deploy the tool in a local environment:


``` shell
# Clone the repository
git clone https://github.com/jfnavarro/myVCF.git

# Enter into myVCF directory
cd myVCF

# Install requirements
pip install -r requirements.txt

# Run the server
python manage.py runserver

> Performing system checks...
> System check identified no issues (0 silenced).
> December 05, 2016 - 17:30:09
> Django version 1.8.4, using settings 'myVCF_django.settings'
> Starting development server at http://127.0.0.1:8000/
> Quit the server with CONTROL-C.

Open the internet browser and go to http://localhost:8000/
```

### Documentation

You will find further instructions for installation and setup at [http://myvcf.readthedocs.io/](http://myvcf.readthedocs.io/)

### Contact
<<<<<<< HEAD

* Jose Fernandez Navarro [jc.fernandez.navarro@gmail.com](mailto:jc.fernandez.navarro@gmail.com)

### License 
See LICENSE

=======

* Jose Fernandez Navarro [jc.fernandez.navarro@gmail.com](mailto:jc.fernandez.navarro@gmail.com)

### License 
See LICENSE
>>>>>>> b0784adddae3135e8813b42c5aae2c71a056e34c
