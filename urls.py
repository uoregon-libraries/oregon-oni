from django.conf.urls import url, include
import views

urlpatterns = [
  url(r'^cities$', views.cities, name="oregon_cities"),
]
