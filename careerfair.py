# -*- coding: utf-8 -*-
# http://filer.case.edu/srj15/careerfair2011/

import sys
import csv
import itertools

from company import *
from gen import *

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
    
    with open(sys.argv[3], 'rb') as f:
        rows = list(csv.reader(f))[1:]
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
              'careerfair%s%s' % (season_abbrev, year), 
              'CWRU Career Fair %s %s Employer Guide' % (season_name, year))
