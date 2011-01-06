from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from  wbdata.models import *
from django.db import IntegrityError, reset_queries, close_connection
import os
import re
import decimal
from csv import DictReader


wb_data_types = (
    'Data',
    'Country',
    'Series',
)

filename_delim = '_'

filename_parts_list = ['%s%s' % (filename_delim, x) for x in (wb_data_types)]

countries_map = (
    ('Country_Code', 'id'),
    ('Country_Name', 'name'),
    ('Source_note', 'source_note'),
)

series_map = (
    ('Indicator_Code'),
    ('Indicator_Name'),
    ('Level_1'),
    ('Level_2'),
    ('Source_note'),
)

size = 300

def save_object(obj):
    try:
        obj.full_clean()
    except ValidationError, e:
        print "[%s]:\n\t%s" % (obj, ', '.join(e.messages))
    try:
        obj.save()
    except IntegrityError, e:
        print "[%s]:\n\t%s" % (obj, 'columns indicator_id, country_id, year are not unique')
    
class Command(BaseCommand):
    args = 'csvfile [csvfile ...]'
    help = "Imports World Bank development indicators data from the csv file(s) into the database. Currently works only with files with %s in the filename" % filename_parts_list

    def handle(self, *csvfiles, **options):
        for csvfile in csvfiles:
            if os.path.isfile(os.path.abspath(csvfile)):
                basename = os.path.basename(csvfile)
                (root, ext) = os.path.splitext(basename)
                # This approach will break on filenames not being seriestitle_datatype.csv, but we need to assume some uniformity of the csv (and I checked a few myself)
                parts = root.split(filename_delim)
                if parts[-1] in wb_data_types:                    
                    fp = open(csvfile, 'rb')
                    reader = DictReader(fp)
                    rows = [row for row in reader]
                    rowcount = len(rows)
                    for i in range(0, rowcount, size):
                        reset_queries() #In case debug=True, reset db queries on occassion so we don't get memory leaks
                        close_connection()
                        print i
                        for row in rows[i:i+size]:
                            if parts[-1] == 'Country':
                                obj = Country(id=row['Country_Code'].strip(), name=row['Country_Name'].strip().upper(), source_note=row['Source_note'].strip())
                                save_object(obj)
                            elif parts[-1] == 'Series':
                                # print '%s, %s, %s' % (row['Indicator_Code'], row['Indicator_Name'], row['Source_note'])
                                obj = Indicator(id=row['Indicator_Code'].strip().upper(), name=row['Indicator_Name'].strip(), source_note=row['Source_note'].strip())
                                save_object(obj)
                            else:
                                print "Processing '%s' for %s" % (row['Series Code'].strip(), row['Country Code'].strip())
                                # print "Row Country Code : '%s'" % row['Country Code'].strip()
                                indicator = Indicator.objects.get(id=row['Series Code'].strip().upper())
                                country = Country.objects.get(id=row['Country Code'].strip().upper())
                                for key, value in row.items():
                                    if re.match(r'\d{4}', key) and value.strip():
                                        obj = DataPoint(indicator=indicator, country=country, year=key, value=decimal.Decimal(value.strip()))
                                        save_object(obj)
                    fp.close()
                else:
                    print "%s does not have %s in the filename. Skipping..." % (basename, filename_parts_list)
        print "Finished importing World Bank data"