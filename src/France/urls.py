from django.urls import path, include

from France.views import stats_region, stats_all_regions, request_asJson_France, request_asJson_Region


urlpatterns = [
    path("Dashboard/region/code=<str:codeRegion>", stats_region, name="focusRegion_code"),
    path("Dashboard/", stats_all_regions, name="stats_all_regions"),
    path("tableStat/France/", request_asJson_France, name='request_ajax_url_france'),
    path("tableStatFrance/Region/code=<str:codeRegion>", request_asJson_Region, name='request_ajax_url_region'),
]
