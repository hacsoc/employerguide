import argparse
import csv
import itertools
import os
import re

import jinja2

from company import *


def sanitized(v):
    return re.sub('[^a-zA-Z_]', '', v)


def commajoin(v):
    return ', '.join(v)


def yesorno(v):
    return 'Yes' if v else 'No'


def render(name, out, *args, **kwargs):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
    env.filters['sanitized'] = sanitized
    env.filters['commajoin'] = commajoin
    env.filters['yesorno'] = yesorno
    t = env.get_template(name)
    with open(out, 'w') as f:
        f.write(t.render(*args, **kwargs))


def make_arg_parser():
    parser = argparse.ArgumentParser(description="Generate static HTML site for the CWRU career fair employer guide")
    parser.add_argument('season', choices=('spring', 'fall'))
    parser.add_argument('year', type=int)
    parser.add_argument('data', help="CSV file")
    return parser


def process(args):
    season_name = {'fall': 'Fall', 'spring': 'Spring'}[args.season]

    with open(args.data, 'r') as csv_f:
        reader = csv.reader(csv_f, dialect=csv.excel)
        sorted_companies = sorted((Company(*row) for row in list(reader)[1:]),
                                  key=lambda c: c.name)
        all_companies = {c.name: c for c in sorted_companies}
        majors = set()
        mlists = [set() for i in range(5)]
        for c in all_companies.values():
            majors = majors | set(c.majors)
            for i in range(5):
                mlists[i] = mlists[i] | set(c.mlists[i])

        titles = ('Degrees',
                  'College of Arts and Sciences',
                  'Case School of Engineering',
                  'Weatherhead School of Management',
                  'Professional Schools')
        sections = zip(titles, mlists)

    for company in sorted_companies:
        print(company)

    out_dir = '{args.season}{args.year}'.format(args=args)
    try:
        os.mkdir(out_dir)
    except OSError:
        pass

    title = 'CWRU Career Fair {0} {1} Employer Guide'.format(season_name, args.year)
    companies = sorted_companies
    render('template.html', os.path.join(out_dir, 'index.html'), **locals())

    for major in majors:
        title = 'Companies looking for {0} majors'.format(major)
        companies = [c for c in sorted_companies if major in c.majors]
        render('template.html', os.path.join(out_dir, sanitized(major)), **locals())


if __name__ == '__main__':
    parser = make_arg_parser()
    process(parser.parse_args())
