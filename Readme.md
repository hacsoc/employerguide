This is a static site generator that generates web versions of CWRU career fair employer guides. It takes UTF-8 CSV files with columns in this order:

* Company Name
* Web Address
* Description
* Contact Name
* Contact Title
* Address
* Contact Phone
* Contact Fax
* Contact Email
* Position Types 
* Degrees 
* Academic Programs 
* College of Arts and Sciences 
* Case School of Engineering 
* Weatherhead School of Management 
* Professional Schools 
* F-1
* Location

Usage: `python2.7 careerfair.py spring/fall <year> <datafile.csv>`

The results will be stored in `careerfair<season><year>/`, which should have a `blueprintcss` folder in it. This repository contains an example without the HTML. You can generate the example with `python2.7 careerfair.py spring 2011 employers_spring2011.csv`.
