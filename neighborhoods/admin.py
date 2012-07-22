from django.contrib.gis import admin

from neighborhoods.models import Neighborhood

class NeighborhoodAdmin(admin.options.OSMGeoAdmin):
    list_display = (
            'name',
            'city',
            'county',
            'state',
            'region_id',
            )
    search_fields = (
                'name',
                'city',
                'county',
                'state',
            )

admin.site.register(Neighborhood, NeighborhoodAdmin)
