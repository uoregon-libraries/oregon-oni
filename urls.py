from django.urls import include, re_path
from onisite.plugins.title_locations import views as tl_views
from . import views
from . import api

urlpatterns = [
    # JSON reimplementations
    re_path(r'^batches\.json$', api.batches),
    re_path(r'^batches/(?P<page_number>\d+).json$', api.batches, name="oregon_batches_json_page"),
    re_path(r'^batches/(?P<batch_name>.+)\.json$', api.batch),
    re_path(r'^lccn/(?P<lccn>\w+).json', api.title),
    re_path(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+).json$', api.issue),

    re_path(r'^titles_by_location$', tl_views.titles_by_location, name="oregon_titles_by_location"),
    re_path(r'^$', views.home),
]
