# -*- coding: utf-8 -*-
# http://filer.case.edu/srj15/careerfair2011/

import sys
import csv
import itertools
import codecs

from company import *
from gen import *

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: python2.7 careerfair.py spring/fall <year> <datafile.csv>'
        sys.exit(1)
    
    if sys.argv[1].lower() == 'spring':
        season_name = 'Spring'
        season_abbrev = 'spring'
    elif sys.argv[1].lower() == 'fall':
        season_name = 'Fall'
        season_abbrev = 'fall'
    
    year = sys.argv[2]
    
    with codecs.open(sys.argv[3], mode='rb', encoding='utf-8') as f:
        rows = list(unicode_csv_reader(f))[1:]
        companies = {v[0]: Company(v) for v in rows}
        sorted_companies = [companies[cn] for cn in sorted(companies.keys())]
        majors = set()
        mlists = [set(), set(), set(), set(), set()]
        for c in companies.viewvalues():
            majors = majors | set(c.majors)
            for i in xrange(5):
                mlists[i] = mlists[i] | set(c.mlists[i])
    
    for major in majors:
        gen(major, mlists, sorted_companies, 'careerfair%s%s' % (season_abbrev, year))
    
    gen_index(mlists, sorted_companies, 
              u'careerfair%s%s' % (season_abbrev, year), 
              u'CWRU Career Fair %s %s Employer Guide' % (season_name, year))
