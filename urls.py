from django.conf.urls import url, include
from onisite.plugins.title_locations import views as tl_views
import views

urlpatterns = [
    url(r'^titles_by_location$', tl_views.titles_by_location, name="oregon_titles_by_location"),
    url(r'^$', views.home),
]
