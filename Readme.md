This is a static site generator that generates web versions of CWRU career fair employer guides.


    > python3 careerfair.py --help
    usage: careerfair.py [-h] {spring,fall} year data

    Generate static HTML site for the CWRU career fair employer guide

    positional arguments:
      {spring,fall}
      year
      data           CSV file

    optional arguments:
      -h, --help     show this help message and exit

Output will be in `{season}{year}/`. `index.html` will link to files in that directory.

The CSV columns are defined in `company.py`.
