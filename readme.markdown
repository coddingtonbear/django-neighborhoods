Introduction
============

Almost 80% of Americans live in urban environments; if you do, too, and have coordinates that you might want to gather the neighborhood from, you can use this tool to do so.

This application allows you to import data from shapefiles provided by [Zillow](http://www.zillow.com/howto/api/neighborhood-boundaries.htm); please give them attribution on pages in which you use this information.

Installation
------------

You can either install from pip:

    pip install django-neighborhoods

*or* checkout and install the source from the [bitbucket repository](https://bitbucket.org/latestrevision/django-neighborhoods):

    hg clone https://bitbucket.org/latestrevision/django-neighborhoods
    cd django-neighborhoods
    python setup.py install

*or* checkout and install the source from the [github repository](https://github.com/latestrevision/django-neighborhoods):

    git clone https://github.com/latestrevision/django-neighborhoods.git
    cd django-neighborhoods
    python setup.py install

Use
---

For a point named `point`, you can find which (if any) neighborhood the point is within by finding which Neighborhood object overlaps this point, like:

    from neighborhoods.models import Neighborhood

    try:
        city = Neighborhood.get_containing(point)
    except Neighborhood.DoesNotExist:
        # You are currently outside of any known neighborhood's boundaries
        city = None

Commands
--------

`import_neighborhoods <Two-letter state abbreviation>`: Download the specified state's shapefile, and import the data into your application.

Examples
--------

If you, perhaps, live in Portland, Oregon, and are using this application to identify the city name for any points gathered from Google Latitude or another service, you may desire to import data for only Washington and Oregon.  To do that you would run:

    python manage.py import_neighborhoods OR
    python manage.py import_neighborhoods WA
