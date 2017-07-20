from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^titles_by_location$', views.titles_by_location, name="oregon_titles_by_location"),
]
