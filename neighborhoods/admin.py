from django.contrib.gis import admin

from neighborhoods.models import Neighborhood, NeighborhoodSource

class NeighborhoodAdmin(admin.options.OSMGeoAdmin):
    list_display = (
            'name',
            'city',
            'state',
            'region_id',
            )
    search_fields = (
                'name',
                'city',
                'state',
            )

admin.site.register(NeighborhoodSource)
admin.site.register(Neighborhood, NeighborhoodAdmin)
