from django.conf.urls import url, include
from onisite.plugins.title_locations import views as tl_views
from . import views
from . import api

urlpatterns = [
    # JSON reimplementations
    url(r'^batches\.json$', api.batches),
    url(r'^batches/(?P<page_number>\d+).json$', api.batches, name="oregon_batches_json_page"),
    url(r'^batches/(?P<batch_name>.+)\.json$', api.batch),
    url(r'^lccn/(?P<lccn>\w+).json', api.title),
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+).json$', api.issue),

    url(r'^titles_by_location$', tl_views.titles_by_location, name="oregon_titles_by_location"),
    url(r'^$', views.home),
]
