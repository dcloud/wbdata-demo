from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from  wbdata.models import *

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

def save_object(obj):
    try:
        obj.full_clean()
    except ValidationError, e:
        print "[%s]: %s" % (obj, ', '.join(e.messages))
    obj.save()
    
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
                    for row in reader:
                        if parts[-1] == 'Country':
                            obj = Country(id=row['Country_Code'].strip(), name=row['Country_Name'].strip(), source_note=row['Source_note'].strip())
                            save_object(obj)
                        elif parts[-1] == 'Series':
                            # print '%s, %s, %s' % (row['Indicator_Code'], row['Indicator_Name'], row['Source_note'])
                            obj = Indicator(id=row['Indicator_Code'].strip(), name=row['Indicator_Name'].strip(), source_note=row['Source_note'].strip())
                            save_object(obj)
                            # print row
                        else:
                            print "Processing '%s' for %s" % (row['Series Code'].strip(), row['Country Code'].strip())
                            # print "Row Country Code : '%s'" % row['Country Code'].strip()
                            indicator = Indicator.objects.get(id=row['Series Code'].strip())
                            country = Country.objects.get(id=row['Country Code'].strip())
                            # for key, value in row.items():
                            #     if re.match(r'\d{4}', key) and value.strip():
                            #         obj = DataPoint(indicator=indicator, country=country, year=key, value=decimal.Decimal(value))
                            #         save_object(obj)
                    fp.close()
                else:
                    print "%s does not have %s in the filename. Skipping..." % (basename, filename_parts_list)
        print "Finished importing World Bank data"