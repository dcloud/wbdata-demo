Requirements
============
Required libraries, including the correct version of Django, are listed in requirements/apps.txt.

This project was built with Django 1.2.4



Installation
============

*Note*: This is a demo project rather than a packaged application, so this does not install using pip, setuptools, etc., but the requirements for the project do.

1.  Clone this repo if you haven't done so already

    `git clone git://github.com/dcloud/wbdata-demo.git`

2. Install dependencies. You'll probably want to setup a virtualenv and install [pip](http://pip.openplans.org/), then from the project directory run:

    `pip install -r requirements/apps.txt`

That should be it for installing the project and it's dependencies. Next, you will need to modify some settings...

Setup
=====

Relevant settings are in settings.py. You should only need to modify a few of them. This demo hasn't been tested in a production environment, but you are welcome to try it out. See the DEVLOG for further discussion.

Dev/Demo
--------
If you are running this in a dev environment using `python manage.py runserver`, then you should probably make sure `DEBUG=True` is set in settings.py. In DEBUG mode, staticfiles handles the serving of css, js, etc. Otherwise if `DEBUG=False`, you will need to set MEDIA\_ROOT, STATIC\_ROOT, then run `python manage.py build_static`. Note that the application will be noticeably slower when DEBUG is turned on.

For demonstration purposes, I would recommend using the sqlite dev.db included with this repository. See "Populating the tables" below and the DEVLOG for further explanation. This definitely not something you would want to use in a production environment.

Production
----------

If you are going to run the demo on a production environment, you will need to at least
    * change the DATABASES setting to your liking
    * set MEDIA_ROOT to a path where you want to store user-uploaded files
    * set STATIC_ROOT to a path where you want to store static media for the site and apps (site js, css, etc).
    * run `python manage.py syncdb` to create the tables in your database.
    
Populating the tables
---------------------

You can use the `loadwbdata` command to load data from "ADI\_Series.csv" (Indicators) or" ADI\_Country.csv". Currently this command looks at the filename for "\_Country", "\_Series", or "\_Data" to determine what model the csv contains. Populating the tables can take some time. It takes over two hours to import the data from "ADI\_Data.csv" since there are over 70000 rows in the csv which results in over 1.6million **DataPoint** objects once the rows are split by year. If you don't mind trimming the dataset or waiting a few hours, feel free to load from "ADI\_Data.csv".

There are fixtures for the **Country** and **Indicator** models, so you can  
run `python manage.py loaddata` giving `countries.json` and `indicators.json` as arguments.


See Also
========

[django-staticfiles](http://django-staticfiles.readthedocs.org/)


