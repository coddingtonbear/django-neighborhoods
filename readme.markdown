Django-neighborhoods
====================

Almost 80% of Americans live in urban environments; if you do, too, and have coordinates that you might want to gather the neighborhood from, you can use this tool to do so.

This application allows you to import data from shapefiles provided by both [Zillow](http://www.zillow.com/howto/api/neighborhood-boundaries.htm) and the [City of Portland](http://www.civicapps.org/datasets/neighborhood-associations); please give them attribution on pages in which you use this information.

Installation
------------

You can either install from pip:

    pip install django-neighborhoods

*or* checkout and install the source from the [github repository](https://github.com/latestrevision/django-neighborhoods):

    git clone https://github.com/latestrevision/django-neighborhoods.git
    cd django-neighborhoods
    python setup.py install

If you live in Portland, Oregon, I recommend using the shapefiles provided by the City of Portland (note that you can use both the shapefiles provided by the City of Portland as well as those provided by Zillow; each source has an adjustable priority priority, with those provided by the City of Portland having a higher priority than those of Zillow):

    python manage.py import_portland_neighborhoods

But, if you happen to live in, perhaps, Chicago, Illinois and almost never leave the state, you might just run:

    python manage.py import_zillow_neighborhoods IL

Or, if you're developing an application that could utilize data from the entire nation:

    python manage.py import_zillow_neighborhoods all

See the 'Commands' section below for more information.

Use
---

For a point named `point`, you can find which (if any) neighborhood the point is within by finding which Neighborhood object overlaps this point, like:

    from neighborhoods.models import Neighborhood

    try:
        neighborhood = Neighborhood.get_containing(point)
    except Neighborhood.DoesNotExist:
        # You are currently outside of any known neighborhood's boundaries
        neighborhood = None

Commands
--------

`import_zillow_neighborhoods <Two-letter state abbreviation|'all'>`: Download the specified state's shapefile (or 'all' avaliable shapefiles), and import the data into your application.

`import_portland_neighborhoods`: Download neighborhood boundaries produced by the City of Portland, and import them into your application.

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/latestrevision/django-neighborhoods/trend.png)](https://bitdeli.com/free "Bitdeli Badge")
