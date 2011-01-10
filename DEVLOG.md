Looking at World Bank site
=======================
* indicators for many parts of the world
* api section for developing RESTful apps off this data
* use iso3 as id but also record iso 2
* Read about data: http://data.worldbank.org/about/data-overview/methodologies

Assignment Parameters
=====================

* The code; ideally in a Git or Subversion repository.  I'd like to see your commit messages and how the code developed over time.
* A README describing how to install your software, including any dependencies, and load the data.
* I want to be able to take the CSV or Excel file (your choice) and load it through a command-line or web-based interface.
* A development log describing your thought process: how you went about defining your solution, the research you did, the tools you used, observations, abandoned efforts, etc.   Some/all of this could be detailed in commit messages.
* A description of how you would expand this if you had more time.


How I would expand this...
==========================
* Better/more visualizations. Comparative charts of indicators between two or more countries. Maps, specifically heatmaps of Africa. Make it easier to see change over time and differences between countries. Allow for multiple indicators.  
* Menus. I did a homepage menu, but not a persistent menu/nav bar. A simple solution would be a form to choose a country and an indicator, but it would be cool to have a menu that could help you build a query that could combine multiple vectors. So you could click a few indicators, a few countries, and maybe a few yers, and click submit and you'd get a page that graphs those values. I would use ajax to build the query (clicking names, years creates a list of vectors), and modify my urls/views to handle multiple items of one type. So a url like http://example.com/wbdata/country/ETH;BDI;ZWE/indicator/DT.ODA.NDAC.KD;GCI.12THPILLAR.XQ/year/1960;1980/ would gather data for Ethiopa, Burundi, and Zimbabwe for the indicators provided for the years provided. The regex for this would be simple to create, but I'm stopping myself from doing any more at this point. Did you notice that my urls are similar to the World Bank API (http://api.worldbank.org/indicators/NY.GDP.MKTP.CD)?
* Intelligent grouping of Indicators by topic. The first part of the indicator code is a general topic. AG is agriculture, for example. However, some indicators could fall into multiple categories, such as 'EN.ATM.METH.AG.ZS' which is in *Environment* but concerns *Agriculture* as well (AG is later in the code). Probably a manual way to group in admin, like a Category model that can have multiple indicator IDs.
* Additional apps that allow reporters to record notes on data, create custom lists or saved searches.
* Robust search, perhaps using django-haystack. **This is a big feature, especially given the number of indicators**
* Data pruning. There is data for all of Africa, which I would take out and have the database calculate. Or perhaps migrate from a "Country" model to a "Location" model if we wanted to be able to go to different levels.
* Consider NULL versus no entry for DataPoints where there was no data provided.
* Separate app from project and test models against other country data. The way I set this up, it looks like I could start importing other datasets.
* Consider the World Bank API. World Bank API allows us to access this information using RESTful requests, so that might provide a means to update and build the database out without importing csv from the command line.


Issues
======

Data formatting
---------------
It wouldn't be programming if there weren't 4 rows where the Series\_Code wasn't capitalized properly. Good thing for `str.upper()`. 

Country code matchup
--------------------
World Bank uses both the 2 letter and 3 letter country codes.
  * 2letter != 3letter[:2]
  * 2letter also not first and last of 3letter

Columns for each year versus row per year+country+indicator
------------------------------------------------------
Database design issue. CSV has a column per year, which might be more efficient representation in the database (fewer rows than one per year+country+indicator). To make this work, I'd have to write a custom model class that automatically adds columns like 'year\_1990' when importing new data. This can be done (see django-modeltranslation), but would require a modified search method for looking at a particular year (search on column title rather than in a row field). This is simply beyond the scope of the demo for this project. Would be interesting to see how large databases represent longitudinal datasets and how to fit this into Django ORM, but not now.

Yearfield does not exist in django. 
-----------------------------------
Custom datefield does not make sense since it is based on date.datetime object, which requires, day, month, and year.

Years in fields
---------------
Data goes back to 1960, but we probably don't want to validate dates to that. Decided against using DateField with a date format of `%s-12-31` though maybe that was the right way to go. I had been thinking about representation in the admin and issues with the DateWidget for the form if we needed to edit. Simpler to use a PositiveIntegerField for now. Could write a custom migration using South if I wanted to go back and use DateField.

Decimal precision in the csv
-------------------------
This was a small, but sticky problem. I thought I had regexed properly to find the largest decimal value in ADI\_Data.csv but when testing ran across an error that made me realize I needed to make the DecimalField's max_digits a bit bigger than I had planned for

Data set is huge, importing can cause memory issues
---------------------------------------------------
import and save can run out of memory. Had to use the technique described at http://www.ofbrooklyn.com/2010/07/18/migrating-django-mysql-postgresql-easy-way/. Basically, chunking out the processing of ADI\_Data.csv so that `loadwbdata` goes over 300 records at a time and runs `db.reset_queries()` and `db.close_connection()` at the beginning of a chunk so we release some of the memory usage. Issue is relevant to environments running `DEBUG=True`. See http://docs.djangoproject.com/en/dev/faq/models/#why-is-django-leaking-memory