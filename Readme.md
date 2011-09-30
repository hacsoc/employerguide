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

Output will be in `{season}{year}/`. `index.html` in the root directory will link to files in `{season}{year}/` so that Github Pages shows the index as the main page.

Files in `content/` will be copied to the output directory.

The CSV columns are defined in `company.py`.
